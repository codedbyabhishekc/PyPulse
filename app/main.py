"""
PyPulse Application Entry Point
--------------------------------
FastAPI app factory with clean modular routing.
Designed for testability and future scalability.
"""

from fastapi import FastAPI

from app.routes.auth import router as auth_router
from app.routes.pickup import router as pickup_router
from app.routes.tracking import router as tracking_router


def create_app() -> FastAPI:
    """
    Creates and configures FastAPI application instance.

    Returns:
        FastAPI: configured app instance
    """

    app = FastAPI(
        title="PyPulse Courier API",
        version="0.1.0",
        description="Contract-driven courier service system"
    )

    # Register routes
    app.include_router(auth_router, prefix="/auth", tags=["Auth"])
    app.include_router(pickup_router, prefix="/pickup", tags=["Pickup"])
    app.include_router(tracking_router, prefix="/tracking", tags=["Tracking"])

    @app.get("/health")
    def health_check():
        """Service health endpoint"""
        return {"status": "ok"}

    return app


app = create_app()