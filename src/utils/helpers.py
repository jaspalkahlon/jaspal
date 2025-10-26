"""
Utility Helper Functions
Common utility functions for the Fashion Guru Bot
"""

import re
from typing import List, Dict, Any


def extract_keywords(text: str, min_length: int = 3) -> List[str]:
    """
    Extract keywords from text

    Args:
        text: Input text
        min_length: Minimum keyword length

    Returns:
        List of keywords
    """
    # Simple keyword extraction - can be enhanced with NLP
    words = re.findall(r'\b\w+\b', text.lower())
    keywords = [w for w in words if len(w) >= min_length]
    return keywords


def calculate_similarity(text1: str, text2: str) -> float:
    """
    Calculate simple similarity between two texts

    Args:
        text1: First text
        text2: Second text

    Returns:
        Similarity score (0-1)
    """
    words1 = set(extract_keywords(text1))
    words2 = set(extract_keywords(text2))

    if not words1 or not words2:
        return 0.0

    intersection = words1.intersection(words2)
    union = words1.union(words2)

    return len(intersection) / len(union)


def format_list(items: List[str], style: str = 'bullet') -> str:
    """
    Format a list for display

    Args:
        items: List of items
        style: 'bullet', 'numbered', or 'comma'

    Returns:
        Formatted string
    """
    if style == 'bullet':
        return '\n'.join([f"• {item}" for item in items])
    elif style == 'numbered':
        return '\n'.join([f"{i}. {item}" for i, item in enumerate(items, 1)])
    elif style == 'comma':
        return ', '.join(items)
    else:
        return '\n'.join(items)


def truncate_text(text: str, max_length: int = 100, suffix: str = '...') -> str:
    """
    Truncate text to maximum length

    Args:
        text: Input text
        max_length: Maximum length
        suffix: Suffix to add when truncated

    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text

    return text[:max_length - len(suffix)] + suffix


def safe_get(data: Dict[str, Any], path: str, default: Any = None) -> Any:
    """
    Safely get nested dictionary value

    Args:
        data: Dictionary
        path: Dot-separated path (e.g., 'user.profile.name')
        default: Default value if not found

    Returns:
        Value or default
    """
    keys = path.split('.')
    value = data

    for key in keys:
        if isinstance(value, dict) and key in value:
            value = value[key]
        else:
            return default

    return value
