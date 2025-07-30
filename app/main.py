from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from fastapi.exceptions import RequestValidationError
from tortoise.exceptions import IntegrityError

from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from app.core.limiter import limiter

from app.core.config import settings
from app.core.logging import get_logging
from app.db.database import init_db
from app.core.error_handlers import (
    validation_exception_handler,
    integrity_exception_handler,
    generic_exception_handler,
)
from app.api.router import api_router
from .debugger import initialize_fastapi_server_debugger_if_needed

log = get_logging(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("Starting app...")
    await init_db(app)
    yield
    log.info("Shutting down...")


def create_application() -> FastAPI:
    initialize_fastapi_server_debugger_if_needed()

    app = FastAPI(
        title=settings.WEB_APP_TITLE,
        description=settings.WEB_APP_DESCRIPTION,
        version=settings.WEB_APP_VERSION,
        lifespan=lifespan,
    )

    app.include_router(api_router, prefix="/api")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_exception_handler(RequestValidationError,
                              validation_exception_handler)
    app.add_exception_handler(IntegrityError, integrity_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)

    return app


def rate_limit_exceeded_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded"},
    )


app = create_application()


app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)


@app.get("/")
async def root():
    return {"message": "API de procesamiento de mensajes activa"}
