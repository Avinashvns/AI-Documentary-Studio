from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config.logging import app_logger


@asynccontextmanager
async def lifespan(app: FastAPI):

    app_logger.info("===================================")
    app_logger.info("AI Documentary Studio Started")
    app_logger.info("===================================")

    yield

    app_logger.info("===================================")
    app_logger.info("AI Documentary Studio Stopped")
    app_logger.info("===================================")