"""
Pickup Schema
-------------
Defines request/response contract for pickup creation.
"""

from pydantic import BaseModel


class PickupCreate(BaseModel):
    sender: str
    receiver: str
    address: str


class PickupResponse(BaseModel):
    success: bool
    tracking_id: str
    sender: str
    receiver: str
    address: str