from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from tortoise.exceptions import IntegrityError

from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_500_INTERNAL_SERVER_ERROR
)


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "status": "error",
            "error": {
                "code": "INVALID_FORMAT",
                "message": "Invalid message format",
                "details": exc.errors()
            },
        },
    )


async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status": "error",
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred.",
            },
        },
    )


async def integrity_exception_handler(request: Request, exc: IntegrityError):
    return JSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content={
            "status": "error",
            "error": {
                "code": "DUPLICATE_ID",
                "message": "The message_id already exists",
            },
        },
    )
