from pydantic import BaseModel

class PickupCreate(BaseModel):
    sender_id: int   # was int
    receiver_name: str
    reciever: int
    email_address: str       # ADD NEW FIELD
    area: int
    current_location: str