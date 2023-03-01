from pydantic import BaseModel, Field


class CodeRequest(BaseModel):
    login: str



class CodeRespond(BaseModel):
    code: str


class SignInRequest(BaseModel):
    username: str = Field(..., min_length=5, max_length=20)
    hash_password: str = Field(..., min_length=8, max_length=90)
