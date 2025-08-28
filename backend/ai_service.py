"""
OpenAI API client for LLM integration.
"""
import openai
import json
from typing import Dict, Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AIService:
    def __init__(self):
        # Get API key from environment variable
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is missing.")

        # Configure OpenAI
        openai.api_key = api_key
        self.model = "gpt-3.5-turbo"  # Using a more widely available model
        
        # Default structure for analysis response
        self.default_analysis = {
            "title": "",
            "summary": "",
            "key_points": [],
            "sentiment": "",
            "topics": [],
            "readability": "",
            "suggestions": []
        }

    async def analyze_text(self, text: str, prompt: Optional[str] = None) -> Dict:
        """
        Sends text to the LLM for analysis and returns structured output.
        """
        system_prompt = '''You are an expert content analyzer. Analyze the given text and provide insights in a structured way.
        Return your analysis in ONLY valid JSON format with the following structure:
        {
            "title": "Brief title or subject of the content",
            "summary": "A concise summary of the main points",
            "key_points": ["Point 1", "Point 2", "etc"],
            "sentiment": "Overall sentiment (positive/negative/neutral)",
            "topics": ["Topic 1", "Topic 2", "etc"],
            "readability": "Assessment of readability (easy/moderate/difficult)",
            "suggestions": ["Suggestion 1", "Suggestion 2", "etc"]
        }
        Important: Return ONLY the JSON object, no other text or explanation.'''

        try:
            # Make the API call
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": text}
                ],
                temperature=0.7,
                max_tokens=1000
            )

            # Get the response content
            analysis_result = response.choices[0].message['content']
            
            try:
                # Try to parse the JSON response
                parsed_analysis = json.loads(analysis_result)
                
                # Ensure all required fields are present
                for key in self.default_analysis.keys():
                    if key not in parsed_analysis:
                        parsed_analysis[key] = self.default_analysis[key]
                
                return parsed_analysis
                
            except json.JSONDecodeError as e:
                print(f"JSON parsing error: {e}")
                print(f"Raw response: {analysis_result}")
                # Return default structure if JSON parsing fails
                return self.default_analysis.copy()
            
        except Exception as e:
            print(f"Error in AI analysis: {str(e)}")
            return self.default_analysis.copy()

