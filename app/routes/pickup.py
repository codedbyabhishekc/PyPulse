"""
Pickup Routes
-------------
HTTP layer only — no business logic here.
"""

from fastapi import APIRouter
from app.schemas.pickup_schema import PickupCreate
from app.services.pickup_service import create_pickup

router = APIRouter()  # ✅ THIS MUST EXIST


@router.post("/")
def create_pickup_route(payload: PickupCreate):
    """
    Creates a new pickup request.
    """
    return create_pickup(payload)