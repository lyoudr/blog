from fastapi import APIRouter, status

from src.schemas.chatbot import ChatBase, ChatResponse
from src.services.ai import RetrievalAugmentedGeneration

router = APIRouter(
    tags=["chat"],
    prefix="/chat",
)


@router.post(
    "/",
    summary="Ask question about user condition",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
)
def ask_question(payload: ChatBase):
    rag = RetrievalAugmentedGeneration(payload.user_id)
    answer = rag.answer_question_with_rag(payload.question)
    return ChatResponse(answer=answer)
