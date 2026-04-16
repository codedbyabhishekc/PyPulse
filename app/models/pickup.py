from pydantic import BaseModel

class PickupCreate(BaseModel):
    sender_id: int   # was int
    tiuger: int
    phone: int
    email_address: str       # ADD NEW FIELD
    area: str
    gender:str
    current_location: str