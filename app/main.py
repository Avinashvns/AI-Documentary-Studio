from fastapi import FastAPI

from app.api.routes import router
from app.config.settings import settings
from app.core.lifespan import lifespan
from app.core.exceptions import AppException
from app.core.handlers import app_exception_handler
from app.middleware.logging import LoggingMiddleware
from app.middleware.request_id import RequestIDMiddleware




app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)

app.include_router(router)
app.add_exception_handler(
    AppException,
    app_exception_handler,
)

app.add_middleware(RequestIDMiddleware)
app.add_middleware(LoggingMiddleware)