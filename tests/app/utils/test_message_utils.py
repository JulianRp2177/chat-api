import pytest
from datetime import datetime
from app.utils import message_utils
from app.core.constants import FORBIDDEN_WORDS


class TestContainsProhibitedWords:
    def test_returns_true_if_content_has_forbidden_word(self):
        #Given
        forbidden_example = next(iter(FORBIDDEN_WORDS)) 
        content = f"This message contains {forbidden_example} in the text"
        #When and Then
        assert message_utils.contains_prohibited_words(content) is True

    def test_returns_false_if_content_is_clean(self):
        content = "Hello, this is a normal message with nothing unusual"
        
        assert message_utils.contains_prohibited_words(content) is False

    def test_ignores_case_when_checking_words(self):
        forbidden_example = next(iter(FORBIDDEN_WORDS))
        content = f"This message has the word {forbidden_example.upper()}"
        
        assert message_utils.contains_prohibited_words(content) is True


class TestGenerateMetadata:
    def test_returns_correct_word_and_character_count(self):
        content = "hola mundo"
        metadata = message_utils.generate_metadata(content)

        assert metadata["word_count"] == 2
        assert metadata["character_count"] == len(content)

    def test_processed_at_is_datetime_and_utc(self):
        content = "probando metadata"
        metadata = message_utils.generate_metadata(content)

        assert isinstance(metadata["processed_at"], datetime)
        assert metadata["processed_at"].tzinfo is not None

    def test_empty_content_returns_zero_counts(self):
        content = ""
        metadata = message_utils.generate_metadata(content)

        assert metadata["word_count"] == 0
        assert metadata["character_count"] == 0