from src.core.celery import celery_app
from src.services.ai import RetrievalAugmentedGeneration
from src.repositories.user_repository import list_users
from src.models.database import SessionLocal


@celery_app.task
def run_rag_pipeline(user_id):
    db = SessionLocal()
    try:
        users = list_users(db)  # this returns all users
        for user in users:
            if user.posts:
                user_id = user.id
                rag = RetrievalAugmentedGeneration(user_id)
                chunks = rag.chunk()
                rag.save_to_faiss(chunks)
                print("RAG processing done for user:", user_id)
    finally:
        db.close()
