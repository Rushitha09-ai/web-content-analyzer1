"""
Content extractor module for parsing and extracting relevant content from web pages.
"""
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
import re

class ContentExtractor:
    def __init__(self):
        # Common tags that usually contain main content
        self.content_tags = ['article', 'main', 'div', 'section']
        # Tags to exclude from content
        self.exclude_tags = ['nav', 'header', 'footer', 'script', 'style', 'noscript']

    def extract_content(self, soup: BeautifulSoup) -> Dict[str, str]:
        """
        Extracts main content from a BeautifulSoup object.
        
        Args:
            soup (BeautifulSoup): Parsed HTML content
            
        Returns:
            Dict containing extracted content elements
        """
        return {
            "title": self._extract_title(soup),
            "main_content": self._extract_main_content(soup),
            "meta_description": self._extract_meta_description(soup),
            "links": self._extract_links(soup)
        }

    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extracts page title"""
        title = soup.title.string if soup.title else ""
        return self._clean_text(title)

    def _extract_meta_description(self, soup: BeautifulSoup) -> str:
        """Extracts meta description"""
        meta = soup.find('meta', attrs={'name': 'description'})
        return meta.get('content', '') if meta else ''

    def _extract_main_content(self, soup: BeautifulSoup) -> str:
        """Extracts main content from the page"""
        # Remove unwanted elements
        for tag in soup.find_all(self.exclude_tags):
            tag.decompose()

        # Try to find main content container
        main_content = None
        for tag in self.content_tags:
            main_content = soup.find(tag, class_=re.compile(r'(content|article|post|main)'))
            if main_content:
                break

        if not main_content:
            main_content = soup.find('body')

        return self._clean_text(main_content.get_text()) if main_content else ""

    def _extract_links(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """Extracts relevant links from the page"""
        links = []
        for link in soup.find_all('a', href=True):
            text = self._clean_text(link.get_text())
            href = link['href']
            if text and href and not href.startswith('#'):
                links.append({
                    "text": text,
                    "href": href
                })
        return links

    def _clean_text(self, text: Optional[str]) -> str:
        """Cleans extracted text"""
        if not text:
            return ""
        # Remove extra whitespace and newlines
        text = re.sub(r'\s+', ' ', text.strip())
        return text

