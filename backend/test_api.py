from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class URLRequest(BaseModel):
    url: str

@app.get("/")
async def root():
    return {"message": "API is running"}

@app.post("/export-pdf")
async def export_pdf(data: dict):
    # Simple PDF response
    content = "PDF Export Test - " + str(data.get('analysis', {}).get('title', 'No Title'))
    return Response(
        content=content.encode(),
        media_type='application/pdf',
        headers={'Content-Disposition': 'attachment; filename=report.pdf'}
    )

@app.post("/analyze")  
async def analyze():
    return {"status": "success", "message": "Analyze endpoint works"}
