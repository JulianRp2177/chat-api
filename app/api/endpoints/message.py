from fastapi import APIRouter, HTTPException, Query, Depends, Request
from app.schemas.message import MessageIn, MessageResponse, MessageListResponse
from app.services.message import message_repository
from app.core.security import api_key_auth
from app.core.limiter import limiter

router = APIRouter()


@router.post("", response_model=MessageResponse, status_code=201)
@limiter.limit("5/minute")
async def receive_message(
    request: Request,
    payload: MessageIn,
    current_user: str = Depends(api_key_auth),
):
    """
    Creates and stores a new message.

    - **Input**: MessageIn (content, sender, session_id, timestamp)
    - **Output**: MessageOut with metadata
    - **Status Code**: 201 Created
    - **Errors**:
        - 422: validation error
        - 403: if the message contains forbidden content
    """
    try:
        result = await message_repository.process_and_store_message(payload)
        return {"status": "success", "data": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(
            status_code=500, detail="Error interno del servidor")


@router.get("/search", response_model=MessageListResponse)
async def search_messages(
    query: str,
    limit: int = 10,
    current_user: str = Depends(api_key_auth),
):
    """
    Searches messages containing a specific keyword in their content.

    - **Query Parameters**:
        - query: The keyword or phrase to search for

    - **Response**: List of matching messages

    - **Status Code**: 200 OK

    - **Errors**:
        - 422: if the query parameter is missing or invalid
    """
    try:
        result = await message_repository.search_messages(query=query, limit=limit)
        return {"status": "success", "data": result}
    except Exception:
        raise HTTPException(
            status_code=500, detail="Error when searching for messages")


@router.get("/session/{session_id}", response_model=MessageListResponse)
async def get_messages(
    session_id: str,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    sender: str = Query(None, pattern="^(user|system)?$"),
    current_user: str = Depends(api_key_auth),
):
    """
    Retrieves a list of messages associated with a given session.

    - **Query Parameters**:
        - session_id: Required session identifier to filter messages
        - limit: Max number of results to return (default: 10)
        - offset: Number of records to skip (default: 0)
        - sender: Optional filter by sender type ("user" or "system")

    - **Response**: List of messages with metadata

    - **Status Code**: 200 OK

    - **Errors**:
        - 422: if query parameters are invalid
    """
    try:
        result = await message_repository.get_messages(session_id, limit, offset, sender)
        return {"status": "success", "data": result}
    except Exception:
        raise HTTPException(
            status_code=500, detail="Error when searching for messages")
