from pydantic import BaseModel


class ChatBase(BaseModel):
    user_id: int
    question: str


class ChatResponse(BaseModel):
    answer: str
