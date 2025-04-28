from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    name: str
    surname: str
    email: str
    alias: str
    password: str
    agree: bool
