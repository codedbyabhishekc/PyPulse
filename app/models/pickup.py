from pydantic import BaseModel

class PickupCreate(BaseModel):
    sender_id: int
    receiver: str
    phone: str