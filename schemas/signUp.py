from pydantic import BaseModel
from fastapi import Form


class SignUpRequest(BaseModel):
    username: str
    password: str


    @classmethod
    def as_form(cls, username: str =  Form(..., min_length=5, max_length=20), password: str = Form(..., min_length=8, max_length=30)):
        return cls(username = username, password = password)
