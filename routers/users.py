from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from security.login import getCurrentUser
from models.user import User


router = APIRouter()

@router.get("/user/")
def read_user(current_user: User = Depends(getCurrentUser)):
    return "esto ahora mismo no me sirve"