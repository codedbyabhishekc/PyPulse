from fastapi import APIRouter
from app.schemas.tracking_schema import TrackingRequest, TrackingStatusUpdate
from app.services.tracking_service import get_tracking_info, update_status

router = APIRouter()


@router.post("/")
def track_shipment(payload: TrackingRequest):
    return get_tracking_info(payload.tracking_id)


@router.patch("/status")
def update_shipment_status(payload: TrackingStatusUpdate):
    return update_status(payload.tracking_id, payload.status)