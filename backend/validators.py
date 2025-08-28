"""
URL validation module for checking URL format and validity.
"""
import re
from urllib.parse import urlparse
from typing import Optional

def validate_url(url: str) -> bool:
    """
    Validates if the given string is a proper URL.
    
    Args:
        url (str): URL to validate
        
    Returns:
        bool: True if URL is valid, False otherwise
    """
    try:
        # Check if URL is not empty or None
        if not url:
            return False

        # Parse the URL
        result = urlparse(url)
        
        # Check for required components
        if not all([result.scheme, result.netloc]):
            return False
            
        # Check if scheme is http or https
        if result.scheme not in ['http', 'https']:
            return False
            
        # Basic regex pattern for URL validation
        pattern = re.compile(
            r'^(?:http|https)://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
            
        return bool(pattern.match(url))
        
    except Exception:
        return False

def get_domain(url: str) -> Optional[str]:
    """
    Extracts domain from URL.
    
    Args:
        url (str): URL to extract domain from
        
    Returns:
        Optional[str]: Domain name if URL is valid, None otherwise
    """
    try:
        if not validate_url(url):
            return None
            
        parsed = urlparse(url)
        return parsed.netloc
    except Exception:
        return None

