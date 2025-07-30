from datetime import datetime, timezone
from app.core.constants import FORBIDDEN_WORDS

def contains_prohibited_words(content: str) -> bool:
    """
    Checks if a message contains any forbidden words.

    Args:
        content (str): The message to validate

    Returns:
        bool: True if a forbidden word is found, otherwise False
    """
    words = content.lower().split()
    return any(word in FORBIDDEN_WORDS for word in words)

def generate_metadata(content: str) -> dict:
    """
    Generates metadata from the message content.

    Args:
        content (str): The original message

    Returns:
        dict: Metadata including word count, character count, and timestamp
    """
    return {
        "word_count": len(content.split()),
        "character_count": len(content),
        "processed_at": datetime.now(timezone.utc),
    }
