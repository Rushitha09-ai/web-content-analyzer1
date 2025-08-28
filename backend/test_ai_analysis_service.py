import pytest
from backend.ai_analysis_service import AIAnalysisService

@pytest.fixture
def ai_service():
    return AIAnalysisService()

def test_analyze_content_structure(ai_service):
    test_content = {
        'title': 'Test Page',
        'main_content': 'This is a test content for analysis.',
        'url': 'https://example.com'
    }
    
    result = ai_service.analyze_content(test_content)
    
    # Check required fields
    assert 'title' in result
    assert 'summary' in result
    assert 'sentiment' in result
    assert 'key_points' in result
    assert 'suggestions' in result
    assert 'confidence_score' in result

def test_analyze_content_empty(ai_service):
    test_content = {}
    
    result = ai_service.analyze_content(test_content)
    
    # Should handle empty content gracefully
    assert result is not None
    assert isinstance(result, dict)

def test_analyze_content_large(ai_service):
    # Test with content larger than typical token limits
    large_content = {
        'title': 'Large Test',
        'main_content': 'Test content ' * 1000,  # Create large content
        'url': 'https://example.com'
    }
    
    result = ai_service.analyze_content(large_content)
    
    # Should handle large content properly
    assert result is not None
    assert isinstance(result, dict)

def test_error_handling(ai_service):
    # Test with invalid content type
    with pytest.raises(Exception):
        ai_service.analyze_content(None)
    
    with pytest.raises(Exception):
        ai_service.analyze_content(42)
