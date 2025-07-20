from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, List, Union, Optional
import logging
import tempfile
import os
import pymupdf4llm

from utils.extract_skills_ollama import extract_all_skills
from utils.extract_text import extract_text_from_pdf

logger = logging.getLogger(__name__)
DEBUG = True

app = FastAPI(
    title="AI Skill Extractor Pro",
    description="Extracts job skills from resumes (PDF or plain text) using Ollama",
    version="2.1",
    docs_url="/docs",
    redoc_url=None
)

# --- Response schema ---
class SkillResponse(BaseModel):
    skills: Union[List[str], Dict[str, Union[Dict[str, List[str]], List[str]]]]
    text_length: Optional[int] = None
    warnings: Optional[List[str]] = None

class TextInput(BaseModel):
    text: str

class ErrorResponse(BaseModel):
    error: str
    details: Optional[str] = None
    suggestion: Optional[str] = None

# --- Global exception handler ---
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

# 1️⃣ Extract skills from plain text
@app.post("/extract-skills/text/", response_model=SkillResponse, responses={500: {"model": ErrorResponse}})
async def extract_skills_from_text(data: TextInput):
    try:
        if DEBUG:
            print("📥 Raw input text:", data.text[:500])
        skills = extract_all_skills(data.text)
        return {
            "skills": skills,
            "text_length": len(data.text),
            "warnings": ["Make sure extracted skills are verified."]
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

# 2️⃣ Extract skills from a PDF resume
@app.post("/extract-skills/", response_model=SkillResponse, responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def extract_skills_from_pdf(file: UploadFile = File(...)):
    try:
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Invalid file type",
                    "details": "Only PDF files are supported",
                    "suggestion": "Upload a valid PDF file"
                }
            )

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

        # Save PDF to temp
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            temp_pdf.write(file_bytes)
            temp_pdf.flush()
            temp_path = temp_pdf.name

        if DEBUG:
            print(f"📄 Saved to temp file: {temp_path}")

        # Try extracting text with pymupdf4llm
        full_text = pymupdf4llm.to_text(temp_path)
        if not full_text.strip():
            if DEBUG:
                print("⚠️ Empty from `to_text()`, trying markdown fallback...")
            full_text = pymupdf4llm.to_markdown(temp_path)

        if DEBUG:
            print("📄 Preview extracted text:\n", full_text[:500])

        # Clean up
        os.remove(temp_path)

        if not full_text or len(full_text) < 50:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "Text extraction failed",
                    "details": "Could not extract readable text",
                    "suggestion": "Try a different PDF file"
                }
            )

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
