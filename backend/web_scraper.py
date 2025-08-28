"""
Web scraper module for fetching web content.
Uses requests for HTTP requests and BeautifulSoup for HTML parsing.
"""
import requests
from bs4 import BeautifulSoup
from typing import Dict, Optional
from backend.validators import validate_url
from backend.security import check_url_security

class WebScraper:
    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def fetch_page(self, url: str) -> Optional[Dict]:
        """
        Fetches a webpage and returns its content.
        
        Args:
            url (str): The URL to fetch
            
        Returns:
            Dict containing status, content, and error message if any
        """
        try:
            # Validate URL format and security
            if not validate_url(url):
                return {"status": "error", "error": "Invalid URL format"}
            
            if not check_url_security(url):
                return {"status": "error", "error": "URL failed security check"}

            # Fetch the page
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()

            return {
                "status": "success",
                "content": response.text,
                "status_code": response.status_code,
                "headers": dict(response.headers)
            }

        except requests.Timeout:
            return {"status": "error", "error": "Request timed out"}
        except requests.RequestException as e:
            return {"status": "error", "error": str(e)}
        
    def get_soup(self, html_content: str) -> BeautifulSoup:
        """
        Creates a BeautifulSoup object from HTML content.
        
        Args:
            html_content (str): Raw HTML content
            
        Returns:
            BeautifulSoup object
        """
        return BeautifulSoup(html_content, 'html.parser')

