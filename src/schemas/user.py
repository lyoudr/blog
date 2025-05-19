from pydantic import BaseModel, EmailStr


class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attribute = True

class RegisterResponse(BaseModel):
    status: str

class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str 
    token_type: str