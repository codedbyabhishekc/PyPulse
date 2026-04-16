from pydantic import BaseModel

class PickupCreate(BaseModel):
    sender_id: str   # was int
    receiver_name: str
    phone: int
    email_address: str       # ADD NEW FIELD
    area: str