from langchain.text_splitter import RecursiveCharacterTextSplitter
from openai import OpenAI
import numpy as np
import faiss
import os
import pickle

from src.models.database import conn

# Set your OpenAI API key
client = OpenAI()


class RetrievalAugmentedGeneration:
    def __init__(self, user_id):
        self.user_id = user_id
        self.index_path = f"./faiss_index_{user_id}.index"
        self.meta_path = f"./metadata_{user_id}.pkl"

        # FAISS index initialization
        self.dimension = (
            1536  # OpenAI's embedding dimension for 'text-embedding-ada-002'
        )
        self.index = faiss.IndexFlatL2(self.dimension)
        self.metadata_store = {}

        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)
            with open(self.meta_path, "rb") as f:
                self.metadata_store = pickle.load(f)

        cursor = conn.cursor()
        cursor.execute(
            f"SELECT id, title, content FROM post WHERE user_id = {user_id};"
        )
        self.rows = cursor.fetchall()
        """
        FAISS (Facebook AI Similarity Search) is a library for efficient 
        similarity search and clustering of dense vectors, often used for tasks
        like nearest neighbor search, document retrieval, or image similarity.
        
        1. Dimension in FAISS
        The dimension refers to the size of the vector that represents each data point in your dataset.

        2. FAISS Index
            An 'index' in FAISS is a data structure that holds the vectors (embeddings) and provides
            an efficient way to search for the closest vector to a given query vector
            (1) Search speed
            (2) Memory usage
            (3) Accuracy of the search
            ** IndexFlatL2
            * This is a brute-force index that calculates the L2 (Euclidean) distance between the query vector and all vectors in the index.
        """

    def chunk(self):
        documents = [{"id": r[0], "title": r[1], "content": r[2]} for r in self.rows]
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = []
        for doc in documents:
            splits = splitter.split_text(doc["content"])
            for i, chunk in enumerate(splits):
                chunks.append(
                    {
                        "id": f"{doc['id']}_{i}",
                        "text": chunk,
                        "metadata": {
                            "title": doc["title"],
                            "doc_id": doc["id"],
                        },
                    }
                )
        return chunks

    def get_embeddings(self, texts):
        response = client.embeddings.create(model="text-embedding-3-small", input=texts)
        return response.data[0].embedding

    def save_to_faiss(self, chunks):
        texts = [chunk["text"] for chunk in chunks]
        embeddings = self.get_embeddings(texts)
        print("embeddings is ->", embeddings)

        # Convert embeddings to a numpy array and add to FAISS index
        embeddings_np = np.array(embeddings).astype("float32")
        if embeddings_np.ndim == 1:
            embeddings_np = embeddings_np.reshape(1, -1)

        self.index.add(embeddings_np)

        # Save the metadata
        for i, chunk in enumerate(chunks):
            self.metadata_store[len(self.metadata_store)] = {
                "metadata": chunk["metadata"],
                "text": chunk["text"],
            }

        # Save to disk
        faiss.write_index(self.index, self.index_path)
        with open(self.meta_path, "wb") as f:
            pickle.dump(self.metadata_store, f)

    def search_faiss(self, query, k=3):
        # Embed the query
        query_embedding = (
            client.embeddings.create(model="text-embedding-3-small", input=[query])
            .data[0]
            .embedding
        )

        # Convert to correct shape
        query_vec = np.array(query_embedding, dtype="float32").reshape(1, -1)

        # Search in FAISS
        distances, indices = self.index.search(query_vec, k)

        # Fetch results
        results = []
        for idx in indices[0]:
            if idx in self.metadata_store:
                results.append(self.metadata_store[idx])
        return results

    def answer_question_with_rag(self, query, k=3):
        # Step 1: Retrieve relevant chunks
        results = self.search_faiss(query, k=k)

        # Step 2: Extract the actual texts
        context_texts = [item["text"] for item in results]
        context = "\n---\n".join(context_texts)

        # Step 3: Construct a prompt
        prompt = f"""You are a helpful assistant. Use the following context to answer the question.

        Context:
        {context}

        Question: {query}

        Answer:"""

        # Step 4: Generate response using OpenAI LLM
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a knowledgeable assistant."},
                {"role": "user", "content": prompt},
            ],
        )

        return response.choices[0].message.content.strip()
