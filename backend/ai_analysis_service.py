from typing import Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

class AIAnalysisService:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        
    def analyze_content(self, content_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # Extract content from scraping result
            content = content_data.get('content', {})
            title = content.get('title', 'No title')
            main_content = content.get('main_content', '')
            
            # Simple analysis without AI for now
            word_count = len(main_content.split()) if main_content else 0
            char_count = len(main_content) if main_content else 0
            
            return {
                'title': title,
                'summary': f'Analyzed {title}. Found {word_count} words and {char_count} characters of content.',
                'sentiment': 'neutral',
                'key_points': [
                    f'Page title: {title}',
                    f'Content length: {word_count} words',
                    'Successfully extracted content'
                ],
                'suggestions': [
                    'Content was successfully analyzed',
                    'Consider adding more metadata analysis'
                ],
                'confidence_score': 0.8
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': f'Analysis failed: {str(e)}',
                'title': 'Error',
                'summary': 'Analysis could not be completed'
            }
