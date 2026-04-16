from pydantic import BaseModel

class PickupCreate(BaseModel):
    sender_id: int   # was int
    receiver_name: int
    phone: int
    email_address: str       # ADD NEW FIELD
    area: str
    counry:str