"""
User Schema
-----------
Defines API contract for user-related operations.
"""

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    name: str
    email: str