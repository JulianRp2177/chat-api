import pytest
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from tortoise.exceptions import IntegrityError
from starlette.testclient import TestClient

from app.core import error_handlers


@pytest.fixture
def test_app():
    app = FastAPI(debug=False)

    app.add_exception_handler(RequestValidationError,
                              error_handlers.validation_exception_handler)
    app.add_exception_handler(
        IntegrityError, error_handlers.integrity_exception_handler)
    app.add_exception_handler(
        Exception, error_handlers.generic_exception_handler)

    @app.get("/validation-error")
    async def trigger_validation_error(param: int):
        return {"param": param}

    @app.get("/integrity-error")
    async def trigger_integrity_error():
        raise IntegrityError("Duplicate entry", "params", "message_id")

    @app.get("/generic-error")
    async def trigger_generic_error():
        raise Exception("Unexpected")

    return app


def test_validation_exception_handler(test_app):
    client = TestClient(test_app)
    response = client.get("/validation-error", params={"param": "no-es-numero"})

    assert response.status_code == 422
    body = response.json()
    assert body["status"] == "error"
    assert body["error"]["code"] == "INVALID_FORMAT"
    assert isinstance(body["error"]["details"], list)


def test_integrity_exception_handler(test_app):
    client = TestClient(test_app)
    response = client.get("/integrity-error")

    assert response.status_code == 400
    body = response.json()
    assert body["status"] == "error"
    assert body["error"]["code"] == "DUPLICATE_ID"
    assert body["error"]["message"] == "The message_id already exists"


def test_generic_exception_handler(test_app):
    client = TestClient(test_app, raise_server_exceptions=False)
    response = client.get("/generic-error")

    assert response.status_code == 500
    body = response.json()
    assert body["status"] == "error"
    assert body["error"]["code"] == "INTERNAL_ERROR"
    assert body["error"]["message"] == "An unexpected error occurred."
