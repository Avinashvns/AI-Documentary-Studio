from fastapi import APIRouter
from app.config.settings import settings
from app.core.exceptions import AppException

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

@router.get("/test-error")
async def test_error():

    raise AppException(
        status_code=404,
        code="DOCUMENT_NOT_FOUND",
        message="Requested document does not exist.",
    )