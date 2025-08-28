"""
Main service for coordinating web scraping operations.
"""
from typing import Dict, Optional
from backend.web_scraper import WebScraper
from backend.content_extractor import ContentExtractor
from backend.validators import validate_url
from backend.security import check_url_security

class ScrapingService:
    def __init__(self):
        self.scraper = WebScraper()
        self.extractor = ContentExtractor()

    def analyze_url(self, url: str) -> Dict:
        """
        Analyzes a URL by scraping and extracting its content.
        
        Args:
            url (str): URL to analyze
            
        Returns:
            Dict containing analysis results and any errors
        """
        try:
            # Initial validation
            if not validate_url(url):
                return {
                    "status": "error",
                    "error": "Invalid URL format",
                    "url": url
                }

            # Security check
            if not check_url_security(url):
                return {
                    "status": "error",
                    "error": "URL failed security check",
                    "url": url
                }

            # Fetch page content
            page_result = self.scraper.fetch_page(url)
            if page_result["status"] == "error":
                return page_result

            # Parse content
            soup = self.scraper.get_soup(page_result["content"])
            
            # Extract content
            content = self.extractor.extract_content(soup)

            return {
                "status": "success",
                "url": url,
                "content": content,
                "metadata": {
                    "status_code": page_result["status_code"],
                    "headers": page_result["headers"]
                }
            }

        except Exception as e:
            return {
                "status": "error",
                "error": f"Unexpected error: {str(e)}",
                "url": url
            }

    def analyze_multiple_urls(self, urls: list[str]) -> list[Dict]:
        """
        Analyzes multiple URLs in sequence.
        
        Args:
            urls (list[str]): List of URLs to analyze
            
        Returns:
            list[Dict]: List of analysis results
        """
        results = []
        for url in urls:
            result = self.analyze_url(url)
            results.append(result)
        return results

