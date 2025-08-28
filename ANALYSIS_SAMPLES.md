# Analysis Samples

This document showcases sample outputs and screenshots from the Web Content Analyzer.

## Single URL Analysis

### Input
```
URL: https://www.example.com/blog/article
```

### Output
```json
{
  "status": "success",
  "url": "https://www.example.com/blog/article",
  "content": {
    "title": "Sample Article Title",
    "main_content": "Article content here...",
    "metadata": {
      "author": "John Doe",
      "date": "2025-08-27"
    }
  },
  "analysis": {
    "title": "Content Analysis Report",
    "summary": "This article discusses...",
    "sentiment": "positive",
    "key_points": [
      "Main point 1",
      "Main point 2",
      "Main point 3"
    ],
    "suggestions": [
      "Consider adding more examples",
      "Include statistical data"
    ],
    "confidence_score": 0.92
  }
}
```

## PDF Export Sample
![PDF Export Screenshot](assets/pdf_export.png)

## Batch Analysis Sample
![Batch Analysis Screenshot](assets/batch_analysis.png)

## Error Handling Examples

### Invalid URL
```json
{
  "status": "error",
  "error": "Invalid URL format",
  "url": "invalid-url"
}
```

### Rate Limit Example
```json
{
  "status": "error",
  "error": "API rate limit exceeded. Please try again in 60 seconds.",
  "url": "https://example.com"
}
```

## UI Screenshots

### Main Interface
![Main Interface](assets/main_interface.png)

### Results Display
![Results Display](assets/results_display.png)

### Export Options
![Export Options](assets/export_options.png)

Note: Screenshots will be updated with actual application images.
