from typing import List, Dict, Optional
from backend.scraping_service import ScrapingService       
from backend.ai_analysis_service import AIAnalysisService

class WebContentAnalyzer:
    def __init__(self):
        self.scraping_service = ScrapingService()
        self.ai_service = AIAnalysisService()

    async def analyze_url(self, url: str, custom_prompt: Optional[str] = None) -> Dict:
        try:
            # Use the correct method name: analyze_url
            scraping_result = self.scraping_service.analyze_url(url)
            
            # Check for 'status' field instead of 'success'
            if scraping_result.get('status') != 'success':
                return {
                    'status': 'error',
                    'error': scraping_result.get('error', 'Scraping failed'),
                    'url': url
                }
            
            # Analyze the content
            analysis_result = self.ai_service.analyze_content(scraping_result)
            
            return {
                'status': 'success',
                'url': scraping_result.get('url', url),
                'content': scraping_result.get('content', {}),
                'analysis': analysis_result,
                'metadata': scraping_result.get('metadata', {})
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'url': url
            }

    async def batch_analysis(self, urls: List[str], custom_prompt: Optional[str] = None) -> List[Dict]:
        results = []
        for url in urls:
            result = await self.analyze_url(url, custom_prompt)
            results.append(result)
        return results
