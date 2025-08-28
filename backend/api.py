from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel
from backend.app import WebContentAnalyzer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

analyzer = WebContentAnalyzer()

class URLRequest(BaseModel):
    url: str

@app.post("/analyze")
async def analyze_url(request: URLRequest):
    result = await analyzer.analyze_url(request.url)
    return result

@app.post("/export-pdf")
async def export_pdf(data: dict):
    analysis = data.get('analysis', {})
    pdf_content = f'Simple PDF: {analysis.get("title", "No title")}'
    return Response(content=pdf_content.encode(), media_type='application/pdf')

@app.get("/")
async def root():
    return {"message": "API running"}
