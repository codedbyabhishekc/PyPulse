from pydantic import BaseModel

class PickupCreate(BaseModel):
    sender_id: str   # was int
    receiver: str
    phone: str
    email: str       # ADD NEW FIELD