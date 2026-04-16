from pydantic import BaseModel

class PickupCreate(BaseModel):
    sender_id: int   # changed from int → string
    receiver: str
    phone: str       # new field