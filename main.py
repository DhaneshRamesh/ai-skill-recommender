from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from utils.extract_skills_ollama import extract_skills_with_ollama
import io
import tempfile
import pymupdf4llm

# Initialize FastAPI app
app = FastAPI(
    title="AI Skill Extractor",
    description="Extract job skills from PDF resumes or plain text using Ollama + Markdown + FastAPI",
    version="1.0"
)

# 1️⃣ Route: Raw text input (for testing/debugging)
class TextInput(BaseModel):
    text: str

@app.post("/extract-skills/text/", summary="Extract skills from plain text")
def extract_skills_from_text(data: TextInput):
    """
    Accepts raw text and returns extracted skills using Ollama.
    """
    skills = extract_skills_with_ollama(data.text)
    return {"skills": skills}


# 2️⃣ Route: PDF Resume Upload
@app.post("/extract-skills/", summary="Extract skills from resume (PDF upload)")
async def extract_skills_from_pdf(file: UploadFile = File(...)):
    """
    Accepts a PDF file, extracts Markdown using pymupdf4llm,
    feeds it to Ollama (gemma:2b), and returns a list of extracted skills.
    """
    try:
        # Step 1: Read uploaded PDF bytes
        file_bytes = await file.read()

        # Step 2: Save as temp file (required by pymupdf4llm)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            temp_pdf.write(file_bytes)
            temp_pdf.flush()
            temp_path = temp_pdf.name

        # Step 3: Extract Markdown from file
        markdown_text = pymupdf4llm.to_markdown(temp_path)

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"PDF parse failed: {str(e)}"})

    try:
        # Step 4: Extract skills using Ollama
        skills = extract_skills_with_ollama(markdown_text)
        return {"skills": skills}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Ollama failed: {str(e)}"})
