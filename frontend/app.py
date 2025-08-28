"""
FastAPI application for the Web Content Analyzer Pro API
"""
from fastapi import FastAPI, Form, Request, Body
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from pathlib import Path

from backend.app import WebContentAnalyzer

app = FastAPI(
    title="Web Content Analyzer Pro API",
    description="Comprehensive website analysis with AI capabilities",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for web interface
static_path = Path("frontend/static")
templates_path = Path("frontend/templates")
app.mount("/static", StaticFiles(directory=str(static_path)), name="static")
templates = Jinja2Templates(directory=str(templates_path))

# Initialize analyzer
analyzer = WebContentAnalyzer()

# Pydantic models for request/response validation
class AnalyzeRequest(BaseModel):
    url: HttpUrl
    custom_prompt: Optional[str] = None

class BatchAnalyzeRequest(BaseModel):
    urls: List[HttpUrl]
    custom_prompt: Optional[str] = None

# Web interface route
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Web interface for the analyzer"""
    return templates.TemplateResponse("index.html", {"request": request})

# API endpoints
@app.post("/analyze", summary="Comprehensive website analysis")
async def analyze(request: AnalyzeRequest):
    """
    Analyze a single website with AI-powered content analysis.
    
    - Extracts main content, metadata, and links
    - Performs AI analysis for insights
    - Validates URL and prevents SSRF attacks
    """
    try:
        result = await analyzer.analyze_url(str(request.url), request.custom_prompt)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "error": str(e)}
        )

@app.post("/batch", summary="Batch website analysis")
async def batch_analyze(request: BatchAnalyzeRequest):
    """
    Analyze multiple websites in batch mode.
    
    - Process multiple URLs simultaneously
    - Same comprehensive analysis as single URL
    - Returns combined results
    """
    try:
        results = await analyzer.batch_analysis(
            [str(url) for url in request.urls],
            request.custom_prompt
        )
        return JSONResponse(content=results)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "error": str(e)}
        )

@app.post("/export-pdf")
async def export_pdf(data: dict = Body(...)):
    """
    Export analysis results to PDF
    """
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    from fastapi.responses import Response
    import io

    # Create PDF buffer
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    # Get data
    analysis = data.get('analysis', {})
    url = data.get('url', 'N/A')
    
    # Draw content
    p.drawString(50, 750, "Web Content Analysis Report")
    p.drawString(50, 720, f"URL: {url}")
    
    # Add analysis details
    y_position = 700
    for key, value in analysis.items():
        if isinstance(value, (str, int, float)):
            p.drawString(50, y_position, f"{key.title()}: {value}")
            y_position -= 20
        elif isinstance(value, list) and key in ['key_points', 'suggestions']:
            p.drawString(50, y_position, f"{key.title()}:")
            y_position -= 20
            for item in value:
                p.drawString(70, y_position, f"• {item}")
                y_position -= 20
    
    p.save()
    buffer.seek(0)
    
    return Response(
        content=buffer.getvalue(),
        media_type='application/pdf',
        headers={'Content-Disposition': 'attachment; filename=analysis_report.pdf'}
    )

@app.get("/health", summary="Health check")
async def health_check():
    """
    Check if the API is operational.
    
    Returns:
        dict: Status information about the API
    """
    return {
        "status": "healthy",
        "version": "1.0.0",
        "services": {
            "web_scraper": "operational",
            "ai_service": "operational",
            "database": "not_configured"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("frontend.app:app", host="127.0.0.1", port=8000, reload=True)
