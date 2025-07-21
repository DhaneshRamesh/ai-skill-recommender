from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
from utils.extract_skills_ollama import extract_all_skills
import pymupdf4llm
import tempfile
import os

# Enable debug logs
DEBUG = True

# Initialize FastAPI app
app = FastAPI(
    title="AI Skill Extractor",
    description="Extract job skills from PDF resumes or plain text using Ollama + FastAPI",
    version="1.1"
)

# Models for detailed skills structure
class TechnicalSkills(BaseModel):
    programming_languages: List[str]
    frameworks: List[str]
    databases: List[str]
    devops_tools: List[str]
    data_science_tools: List[str]
    design_tools: List[str]

class SkillsResponse(BaseModel):
    technical_skills: TechnicalSkills
    platforms: List[str]
    soft_skills: List[str]
    certifications: List[str]
    languages: List[str]
    domain_skills: List[str]

# Input model for plain text extraction
class TextInput(BaseModel):
    text: str

# Extract skills from raw plain text
@app.post("/extract-skills/text/", response_model=SkillsResponse, summary="Extract skills from plain text")
async def extract_skills_from_text(data: TextInput):
    """
    Accepts raw text and returns extracted skills using Ollama.
    """
    try:
        skills = extract_all_skills(data.text)
        if DEBUG:
            print(f"[DEBUG] Skills extracted successfully: {skills}")
        return skills
    except Exception as e:
        if DEBUG:
            print(f"[ERROR] /extract-skills/text/ failed: {e}")
        return JSONResponse(status_code=500, content={"error": f"Ollama failed on text input: {str(e)}"})

# Extract skills from a PDF resume
@app.post("/extract-skills/pdf/", response_model=SkillsResponse, summary="Extract skills from resume (PDF upload)")
async def extract_skills_from_pdf(file: UploadFile = File(...)):
    """
    Accepts a PDF file, extracts text using pymupdf4llm, feeds it to Ollama, and returns extracted skills.
    """
    if not file.filename.endswith(".pdf"):
        return JSONResponse(status_code=400, content={"error": "Only PDF files are supported."})

    try:
        if DEBUG:
            print(f"\n[DEBUG] File received: {file.filename}")

        # Step 1: Read file bytes
        file_bytes = await file.read()

        # Step 2: Save to temp file for pymupdf4llm
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            temp_pdf.write(file_bytes)
            temp_pdf.flush()
            temp_path = temp_pdf.name

        if DEBUG:
            print(f"[DEBUG] Temp file saved at: {temp_path}")

        # Step 3: Extract plain text from PDF
        plain_text = pymupdf4llm.to_markdown(temp_path)

        if not plain_text.strip():
            if DEBUG:
                print("[DEBUG] No text found using to_markdown(); trying fallback...")
            plain_text = pymupdf4llm.to_markdown(temp_path)

        if DEBUG:
            print(f"\n[DEBUG] Extracted Text Preview:\n{plain_text[:500]}\n")

        # Step 4: Extract skills with Ollama
        skills = extract_all_skills(plain_text)

        # Step 5: Clean up temp file
        os.remove(temp_path)
        if DEBUG:
            print("[DEBUG] Temp file deleted.")

        if DEBUG:
            print(f"[DEBUG] Skills extracted successfully: {skills}")
        return skills

    except Exception as e:
        if DEBUG:
            print(f"[ERROR] /extract-skills/pdf/ failed: {e}")
        return JSONResponse(status_code=500, content={"error": f"PDF processing failed: {str(e)}"})
