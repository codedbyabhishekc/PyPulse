from pydantic import BaseModel

class PickupCreate(BaseModel):
    sender_id: str        # ← Changed from int to str
    receiver_name: int
    phone: int
    email_address: str
    area: str
    notes: str = ""       # ← Added new field