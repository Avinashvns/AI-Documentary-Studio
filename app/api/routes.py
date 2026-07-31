from fastapi import APIRouter
from app.config.settings import settings

router = APIRouter()


@router.get("/", tags=["Root"])
async def root():
    return {
        "message": f"Welcome to {settings.app_name}"
    }


@router.get("/health", tags=["Health"])
async def health():
    return {
        "status": "healthy"
    }


@router.get("/version", tags=["System"])
async def version():
    return {
        "version": settings.app_version
    }