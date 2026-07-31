from starlette.middleware.base import BaseHTTPMiddleware

from app.config.logging import app_logger


class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        app_logger.info(
            f"{request.method} {request.url.path}"
        )

        response = await call_next(request)

        app_logger.info(
            f"Status Code: {response.status_code}"
        )

        return response