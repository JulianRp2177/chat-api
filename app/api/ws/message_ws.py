from fastapi import WebSocket, WebSocketDisconnect, APIRouter
from typing import Dict, List
from app.core.logging import get_logging

router = APIRouter()
active_connections: Dict[str, List[WebSocket]] = {}

log = get_logging(__name__)

@router.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await websocket.accept()
    log.info(f"Client connected to session '{session_id}'")

    if session_id not in active_connections:
        active_connections[session_id] = []

    active_connections[session_id].append(websocket)
    log.debug(f"Active connections for session '{session_id}': {len(active_connections[session_id])}")

    try:
        while True:
            message = await websocket.receive_text()
            log.info(f"Message received from WebSocket in session '{session_id}': {message}")
    except WebSocketDisconnect:
        active_connections[session_id].remove(websocket)
        log.warning(f"Client disconnected from session '{session_id}'")

        if not active_connections[session_id]:
            del active_connections[session_id]
            log.info(f"Session '{session_id}' removed (no active connections)")
