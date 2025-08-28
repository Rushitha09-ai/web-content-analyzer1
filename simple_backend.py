from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Backend API running"}

@app.post("/export-pdf")  
def export_pdf(data: dict):
    # Create proper PDF
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    # Get data
    analysis = data.get('analysis', {})
    url = data.get('url', 'N/A')
    title = analysis.get('title', 'No Title')
    summary = analysis.get('summary', 'No Summary')
    
    # Draw content
    p.drawString(50, 750, "Web Content Analysis Report")
    p.drawString(50, 720, f"URL: {url}")
    p.drawString(50, 700, f"Title: {title}")
    p.drawString(50, 680, f"Summary: {summary}")
    p.drawString(50, 660, f"Sentiment: {analysis.get('sentiment', 'N/A')}")
    p.drawString(50, 640, f"Confidence: {analysis.get('confidence_score', 'N/A')}")
    
    p.save()
    buffer.seek(0)
    
    return Response(
        content=buffer.getvalue(),
        media_type='application/pdf',
        headers={'Content-Disposition': 'attachment; filename=analysis_report.pdf'}
    )

@app.post("/analyze")
async def analyze_url(data: dict):
    url = data.get('url', 'No URL')
    return {
        "status": "success",
        "url": url,
        "content": {
            "title": f"Analysis of {url}",
            "main_content": "Sample content extracted"
        },
        "analysis": {
            "title": f"Analysis of {url}",
            "summary": f"Analyzed {url} successfully",
            "sentiment": "neutral",
            "key_points": ["Sample analysis point"],
            "suggestions": ["Sample suggestion"],
            "confidence_score": 0.8
        }
    }
