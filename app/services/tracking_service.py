"""
Tracking Service Layer
---------------------
Handles shipment lookup and status updates.
"""

from app.db.database import DATABASE

VALID_STATES = ["CREATED", "IN_TRANSIT", "DELIVERED"]


def get_tracking_info(tracking_id: str):
    """
    Fetch shipment details by tracking ID.
    """

    pickup = DATABASE["pickups"].get(tracking_id)

    if not pickup:
        return {"success": False, "message": "Tracking ID not found"}

    return {
        "tracking_id": pickup.tracking_id,
        "status": getattr(pickup, "status", "CREATED"),
        "sender": pickup.sender,
        "receiver": pickup.receiver,
        "address": pickup.address
    }


def update_status(tracking_id: str, status: str):
    """
    Updates shipment status safely.
    """

    pickup = DATABASE["pickups"].get(tracking_id)

    if not pickup:
        return {"success": False, "message": "Tracking ID not found"}

    if status not in VALID_STATES:
        return {"success": False, "message": f"Invalid status: {status}"}

    pickup.status = status

    return {
        "success": True,
        "tracking_id": tracking_id,
        "status": pickup.status
    }