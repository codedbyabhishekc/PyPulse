from pydantic import BaseModel

class PickupCreate(BaseModel):
    sender_id: str   # changed from int → string
    receiver: str
    phone: str       # new field