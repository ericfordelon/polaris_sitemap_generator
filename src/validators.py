"""
Validation utilities for sitemap generation.
"""

import re
from datetime import datetime
from typing import Optional
from urllib.parse import urlparse

from config import DATE_FORMAT


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


def validate_url(url: str) -> bool:
    """
    Validate that a URL is properly formatted.

    Args:
        url: The URL to validate

    Returns:
        True if valid

    Raises:
        ValidationError: If URL is invalid
    """
    if not url or not isinstance(url, str):
        raise ValidationError(f"URL must be a non-empty string: {url}")

    url = url.strip()

    # Parse URL
    try:
        result = urlparse(url)
    except Exception as e:
        raise ValidationError(f"Invalid URL format '{url}': {e}")

    # Check for scheme and netloc
    if not all([result.scheme, result.netloc]):
        raise ValidationError(f"URL must have scheme and domain: {url}")

    # Check scheme is http or https
    if result.scheme not in ['http', 'https']:
        raise ValidationError(f"URL scheme must be http or https: {url}")

    return True


def validate_date(date_str: Optional[str]) -> Optional[str]:
    """
    Validate and normalize a date string.

    Args:
        date_str: Date string in YYYY-MM-DD format

    Returns:
        Normalized date string or None if input is None/empty

    Raises:
        ValidationError: If date format is invalid
    """
    if not date_str:
        return None

    date_str = str(date_str).strip()

    if not date_str:
        return None

    # Try to parse the date
    try:
        dt = datetime.strptime(date_str, DATE_FORMAT)
        return dt.strftime(DATE_FORMAT)
    except ValueError:
        raise ValidationError(f"Date must be in YYYY-MM-DD format: {date_str}")


def validate_metadata_field(field_name: str, field_value: any) -> str:
    """
    Validate and sanitize a metadata field value.

    Args:
        field_name: Name of the field
        field_value: Value of the field

    Returns:
        Sanitized field value as string
    """
    if field_value is None or str(field_value).strip() == '':
        return ''

    # Convert to string and strip whitespace
    value = str(field_value).strip()

    # Escape XML special characters
    value = escape_xml(value)

    return value


def escape_xml(text: str) -> str:
    """
    Escape special XML characters.

    Args:
        text: Text to escape

    Returns:
        Escaped text
    """
    if not text:
        return text

    replacements = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&apos;',
    }

    for char, escaped in replacements.items():
        text = text.replace(char, escaped)

    return text


def validate_sitemap_size(url_count: int, size_bytes: int) -> None:
    """
    Validate sitemap doesn't exceed size limits.

    Args:
        url_count: Number of URLs in sitemap
        size_bytes: Size of sitemap in bytes

    Raises:
        ValidationError: If limits are exceeded
    """
    from config import MAX_URLS_PER_SITEMAP, MAX_SITEMAP_SIZE_MB

    if url_count > MAX_URLS_PER_SITEMAP:
        raise ValidationError(
            f"Sitemap exceeds maximum URL count: {url_count} > {MAX_URLS_PER_SITEMAP}"
        )

    max_bytes = MAX_SITEMAP_SIZE_MB * 1024 * 1024
    if size_bytes > max_bytes:
        size_mb = size_bytes / (1024 * 1024)
        raise ValidationError(
            f"Sitemap exceeds maximum size: {size_mb:.2f}MB > {MAX_SITEMAP_SIZE_MB}MB"
        )
