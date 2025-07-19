from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from utils.extract_skills_ollama import extract_skills_with_ollama
import io
import pymupdf4llm

# Initialize FastAPI app
app = FastAPI(
    title="AI Skill Extractor",
    description="Upload a resume or paste text to extract job-related skills using Ollama + PDF → Markdown.",
    version="1.0"
)

# 1️⃣ Route: Raw text input
class TextInput(BaseModel):
    text: str

@app.post("/extract-skills/text/", summary="Extract skills from plain text")
def extract_skills_from_text(data: TextInput):
    """
    Accepts plain text and returns extracted skills using Ollama.
    """
    skills = extract_skills_with_ollama(data.text)
    return {"skills": skills}


# 2️⃣ Route: Resume PDF upload
@app.post("/extract-skills/", summary="Extract skills from resume (PDF upload)")
async def extract_skills_from_pdf(file: UploadFile = File(...)):
    """
    Accepts a resume PDF, extracts markdown using pymupdf4llm,
    sends it to Ollama, and returns the extracted skills.
    """
    file_bytes = await file.read()

    try:
        # Extract markdown text from the uploaded PDF
        markdown_text = pymupdf4llm.to_markdown(io.BytesIO(file_bytes))
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"PDF parse failed: {str(e)}"})

    try:
        # Send to Ollama and extract skills
        skills = extract_skills_with_ollama(markdown_text)
        return {"skills": skills}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Ollama failed: {str(e)}"})
