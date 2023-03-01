from pydantic import BaseModel
from fastapi import Depends
from typing import Union

class User(BaseModel):
    id: int
    username:str
    password:str

class UserInDB(User):
    hashed_password:str
    