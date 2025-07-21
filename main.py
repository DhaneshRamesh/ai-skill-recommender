from fastapi import FastAPI, UploadFile, File
from typing import List
from pydantic import BaseModel
from fastapi.responses import JSONResponse
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

# Response schema for Swagger UI
class SkillResponse(BaseModel):
    skills: List[str]

# Input model for plain text extraction
class TextInput(BaseModel):
    text: str

# Extract skills from raw plain text
@app.post("/extract-skills/text/", response_model=SkillResponse, summary="Extract skills from plain text")
async def extract_skills_from_text(data: TextInput):
    """
    Accepts raw text and returns extracted skills using Ollama.
    """
    try:
        skills = extract_all_skills(data.text)
        if DEBUG:
            print(f"✅ Extracted skills: {skills}")
        return {"skills": skills or []}
    except Exception as e:
        if DEBUG:
            print(f"❌ Error in /extract-skills/text/: {e}")
        return JSONResponse(status_code=500, content={"error": f"Ollama failed on text input: {str(e)}"})

# Extract skills from a PDF resume
@app.post("/extract-skills/pdf/", response_model=SkillResponse, summary="Extract skills from resume (PDF upload)")
async def extract_skills_from_pdf(file: UploadFile = File(...)):
    """
    Accepts a PDF file, extracts text using pymupdf4llm, feeds it to Ollama, and returns extracted skills.
    """
    if not file.filename.endswith(".pdf"):
        return JSONResponse(status_code=400, content={"error": "Only PDF files are supported."})

    try:
        if DEBUG:
            print(f"\n📂 File received: {file.filename}")

        # Step 1: Read file
        file_bytes = await file.read()

        # Step 2: Save to temp file for pymupdf4llm
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            temp_pdf.write(file_bytes)
            temp_pdf.flush()
            temp_path = temp_pdf.name

        if DEBUG:
            print(f"📄 Temp file saved at: {temp_path}")

        # Step 3: Extract plain text from PDF
        plain_text = pymupdf4llm.to_text(temp_path)

        if not plain_text.strip():
            if DEBUG:
                print("⚠️ No text found using to_text(); trying markdown fallback...")
            plain_text = pymupdf4llm.to_markdown(temp_path)

        if DEBUG:
            print("\n📄 Extracted Text Sent to Ollama (preview):")
            print(plain_text[:500], "\n")

        # Step 4: Send text to Ollama
        skills = extract_all_skills(plain_text)

        # Step 5: Clean up
        os.remove(temp_path)
        if DEBUG:
            print("🧹 Temp file deleted.")

        if DEBUG:
            print("✅ Final response going to Swagger:", {"skills": skills or []})
        return {"skills": skills or []}

    except Exception as e:
        if DEBUG:
            print(f"❌ Error in /extract-skills/pdf/: {e}")
        return JSONResponse(status_code=500, content={"error": f"PDF processing failed: {str(e)}"})
