from fastapi import APIRouter
from app.api.endpoints import message as message_router
from app.api.ws import message_ws as message_ws_router

api_router = APIRouter()

api_router.include_router(message_router.router, prefix="/messages", tags=["Messages"])
api_router.include_router(message_ws_router.router, prefix="/ws", tags=["Messages"])
