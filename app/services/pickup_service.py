from app.models.pickup import Pickup, generate_tracking_id
from app.db.database import DATABASE


def create_pickup(payload):
    tracking_id = generate_tracking_id()

    pickup = Pickup(
        sender=payload.sender,
        receiver=payload.receiver,
        address=payload.address,
        tracking_id=tracking_id
    )

    DATABASE["pickups"][tracking_id] = pickup  # always full object

    return {
        "success": True,
        "tracking_id": tracking_id,
        "sender": pickup.sender,
        "receiver": pickup.receiver,
        "address": pickup.address
    }