from fastapi import APIRouter

from app.config.settings import settings
from app.core.response import success_response

router = APIRouter()


@router.get("/")
async def root():
    return success_response(
        message="Welcome to AI Documentary Studio",
        data={
            "application": settings.app_name,
            "version": settings.app_version,
        },
    )


@router.get("/health")
async def health():
    return success_response(
        message="Health check successful",
        data={
            "status": "healthy",
        },
    )


@router.get("/version")
async def version():
    return success_response(
        data={
            "version": settings.app_version,
        }
    )