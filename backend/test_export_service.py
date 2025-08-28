import pytest
from backend.export_service import ExportService
import json
import csv
import os

@pytest.fixture
def export_service():
    return ExportService()

@pytest.fixture
def sample_data():
    return {
        'url': 'https://example.com',
        'content': {
            'title': 'Test Page',
            'main_content': 'Test content'
        },
        'analysis': {
            'title': 'Analysis of Test Page',
            'summary': 'Test summary',
            'sentiment': 'positive',
            'key_points': ['Point 1', 'Point 2'],
            'suggestions': ['Suggestion 1'],
            'confidence_score': 0.85
        }
    }

def test_export_json(export_service, sample_data, tmp_path):
    # Test JSON export
    json_file = tmp_path / "test_export.json"
    export_service.export_json(sample_data, str(json_file))
    
    # Verify file exists and content is correct
    assert json_file.exists()
    with open(json_file, 'r') as f:
        exported_data = json.load(f)
    assert exported_data == sample_data

def test_export_csv(export_service, sample_data, tmp_path):
    # Test CSV export
    csv_file = tmp_path / "test_export.csv"
    export_service.export_csv(sample_data, str(csv_file))
    
    # Verify file exists and content is correct
    assert csv_file.exists()
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    assert len(rows) == 1
    assert rows[0]['url'] == sample_data['url']

def test_export_pdf(export_service, sample_data, tmp_path):
    # Test PDF export
    pdf_file = tmp_path / "test_export.pdf"
    export_service.export_pdf(sample_data, str(pdf_file))
    
    # Verify file exists and has content
    assert pdf_file.exists()
    assert pdf_file.stat().st_size > 0

def test_error_handling(export_service, sample_data):
    # Test with invalid file paths
    with pytest.raises(Exception):
        export_service.export_json(sample_data, "/invalid/path/file.json")
    
    with pytest.raises(Exception):
        export_service.export_csv(sample_data, "/invalid/path/file.csv")
    
    with pytest.raises(Exception):
        export_service.export_pdf(sample_data, "/invalid/path/file.pdf")
