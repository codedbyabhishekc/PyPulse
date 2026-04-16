"""
Auth Service Layer
------------------
Business logic for user management.
Independent of FastAPI or HTTP.
"""

from app.schemas.user_schema import UserCreate

# In-memory store (Phase 1 only)
USERS_DB = {}


def register_user(user: UserCreate):
    """
    Registers a new user in the system.

    Args:
        user (UserCreate): validated user input

    Returns:
        dict: API response
    """

    if user.email in USERS_DB:
        return {
            "success": False,
            "message": "User already exists"
        }

    user_record = {
        "name": user.name,
        "email": user.email
    }

    USERS_DB[user.email] = user_record

    return {
        "success": True,
        "user": user_record
    }