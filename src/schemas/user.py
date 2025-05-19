from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attribute = True


class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str 
    token_type: str