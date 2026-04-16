"""
Auth Routes
-----------
Handles HTTP layer only. No business logic here.
"""

from fastapi import APIRouter
from app.schemas.user_schema import UserCreate
from app.services.auth_service import register_user

router = APIRouter()


@router.post("/register")
def register(user: UserCreate):
    """
    Registers a new user.

    Delegates logic to service layer.
    """
    return register_user(user)