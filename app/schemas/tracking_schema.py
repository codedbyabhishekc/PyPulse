"""
Tracking Schema
---------------
Defines tracking request + status update contract.
"""

from pydantic import BaseModel


class TrackingRequest(BaseModel):
    tracking_id: str


class TrackingStatusUpdate(BaseModel):
    tracking_id: str
    status: str


class TrackingResponse(BaseModel):
    tracking_id: str
    status: str
    sender: str
    receiver: str
