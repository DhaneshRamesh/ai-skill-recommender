from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, List, Union, Optional  # Added Optional here
import logging
from utils.extract_skills_ollama import extract_all_skills
from utils.extract_text import extract_text_from_pdf

logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Skill Extractor Pro",
    description="Extracts skills from resumes with enhanced accuracy",
    version="2.0",
    docs_url="/docs",
    redoc_url=None
)

class SkillResponse(BaseModel):
    skills: Dict[str, Union[Dict[str, List[str]], List[str]]]
    text_length: Optional[int] = None
    warnings: Optional[List[str]] = None

class TextInput(BaseModel):
    text: str

class ErrorResponse(BaseModel):
    error: str
    details: Optional[str] = None
    suggestion: Optional[str] = None

@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    logger.exception("Unhandled exception occurred")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "details": str(exc),
            "suggestion": "Check server logs and try again later"
        }
    )

@app.post("/extract-skills/text/",
         response_model=SkillResponse,
         responses={500: {"model": ErrorResponse}})
async def extract_skills_from_text(data: TextInput):
    """Process full text input"""
    try:
        skills = extract_all_skills(data.text)
        return {
            "skills": skills,
            "text_length": len(data.text)
        }
    except Exception as e:
        logger.error(f"Text processing failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Text processing failed",
                "details": str(e),
                "suggestion": "Check input format and try again"
            }
        )

@app.post("/extract-skills/",
         response_model=SkillResponse,
         responses={
             400: {"model": ErrorResponse},
             500: {"model": ErrorResponse}
         })
async def extract_skills_from_pdf(file: UploadFile = File(...)):
    """Process PDF resume with enhanced extraction"""
    try:
        # Validate input
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Invalid file type",
                    "details": "Only PDF files are supported",
                    "suggestion": "Upload a valid PDF file"
                }
            )

        # Read and validate file
        file_bytes = await file.read()
        if len(file_bytes) < 100:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Invalid PDF",
                    "details": "File is too small",
                    "suggestion": "Upload a valid PDF resume"
                }
            )

        # Extract text
        full_text = extract_text_from_pdf(file_bytes)
        if not full_text or len(full_text) < 50:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "Text extraction failed",
                    "details": "Could not extract readable text",
                    "suggestion": "Try a different PDF file"
                }
            )

        # Extract skills
        skills = extract_all_skills(full_text)
        return {
            "skills": skills,
            "text_length": len(full_text),
            "warnings": ["Always verify extracted skills"] 
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("PDF processing failed")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Processing failed",
                "details": str(e),
                "suggestion": "Check server logs for details"
            }
        )