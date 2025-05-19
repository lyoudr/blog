from fastapi import (
    APIRouter, 
    status, 
    Depends, 
    UploadFile, 
    File, 
    Form
)

from src.schemas.chatbot import ChatBase, ChatResponse
from src.services.ai import (
    RetrievalAugmentedGeneration,
    ImageAnalysis
)
from src.models.user import User
from src.utils.auth import get_current_user

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
def ask_question(
    payload: ChatBase,
    user: User = Depends(get_current_user) 
):
    rag = RetrievalAugmentedGeneration(payload.user_id)
    answer = rag.answer_question_with_rag(payload.question)
    return ChatResponse(answer=answer)


@router.post(
    "/image",
    summary="Ask question about image",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
)
def ask_question_image(
    image: UploadFile = File(...),
    question: str = Form(...),
    user: User = Depends(get_current_user)
):
    analyzer = ImageAnalysis()
    base64_image = analyzer.encode_image(image)
    answer = analyzer.analyze_image(base64_image, question)
    return ChatResponse(answer=answer)
