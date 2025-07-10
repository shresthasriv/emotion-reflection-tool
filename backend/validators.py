import re
from exceptions import InvalidInputError


def validate_reflection_text(text: str) -> str:
    if not text:
        raise InvalidInputError("Text input is required", "EMPTY_TEXT")
    
    if not isinstance(text, str):
        raise InvalidInputError("Text must be a string", "INVALID_TYPE")

    cleaned_text = text.strip()
    
    if not cleaned_text:
        raise InvalidInputError("Text cannot be empty or only whitespace", "EMPTY_TEXT")

    if len(cleaned_text) < 3:
        raise InvalidInputError("Text must be at least 3 characters long", "TOO_SHORT")

    if len(cleaned_text) > 2000:
        raise InvalidInputError("Text is too long (maximum 2000 characters)", "TOO_LONG")

    if contains_suspicious_content(cleaned_text):
        raise InvalidInputError("Text contains inappropriate content", "INAPPROPRIATE_CONTENT")

    if is_only_special_characters(cleaned_text):
        raise InvalidInputError("Text cannot contain only special characters", "INVALID_CONTENT")

    if is_mostly_numbers(cleaned_text):
        raise InvalidInputError("Please enter meaningful text, not just numbers", "NUMBERS_ONLY")

    if is_likely_spam(cleaned_text):
        raise InvalidInputError("Text appears to be spam or gibberish", "SPAM_DETECTED")
    
    return cleaned_text


def contains_suspicious_content(text: str) -> bool:
    suspicious_patterns = [
        r'<script.*?>.*?</script>', 
        r'javascript:', 
        r'data:text/html', 
        r'<iframe.*?>.*?</iframe>', 
    ]
    
    text_lower = text.lower()
    for pattern in suspicious_patterns:
        if re.search(pattern, text_lower, re.IGNORECASE | re.DOTALL):
            return True
    return False


def is_only_special_characters(text: str) -> bool:
    alphanumeric_count = sum(1 for c in text if c.isalnum())
    if alphanumeric_count == 0:
        return True
    if len(text) > 0 and alphanumeric_count / len(text) < 0.3:
        return True
    return False


def is_mostly_numbers(text: str) -> bool:
    # Check if text is purely numeric (with optional spaces/punctuation)
    if re.match(r'^[\d\s\.,\-\+\(\)]+$', text):
        return True
    
    # Check if text is mostly numbers
    digit_count = sum(1 for c in text if c.isdigit())
    letter_count = sum(1 for c in text if c.isalpha())
    
    # If there are digits but very few letters, it's probably just numbers
    if digit_count > 0 and letter_count < 3:
        return True
    
    # If more than 70% is digits, reject it
    if len(text) > 0 and digit_count / len(text) > 0.7:
        return True
    
    return False


def is_likely_spam(text: str) -> bool:
    words = text.split()
    if len(words) > 5:
        unique_words = set(words)
        if len(unique_words) / len(words) < 0.3:
            return True

    special_char_count = sum(1 for c in text if not c.isalnum() and not c.isspace())
    if len(text) > 0 and special_char_count / len(text) > 0.5:
        return True
    
    return False


def validate_confidence_score(confidence: float) -> float:
    if not isinstance(confidence, (int, float)):
        raise InvalidInputError("Confidence must be a number", "INVALID_CONFIDENCE_TYPE")
    
    if not 0.0 <= confidence <= 1.0:
        raise InvalidInputError("Confidence must be between 0.0 and 1.0", "INVALID_CONFIDENCE_RANGE")
    
    return float(confidence) 