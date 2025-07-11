from fastapi import FastAPI, File, UploadFile
from utils.extract_text import extract_text_from_pdf, extract_text_from_docx
from utils.extract_skills import extract_skills
from utils.match_skills import recommend_skills, load_skill_db

app = FastAPI()

@app.post("/recommend")
async def recommend(file: UploadFile = File(...), user_skills: list[str] = []):
    if file.filename.endswith(".pdf"):
        content = extract_text_from_pdf(file.file)
    elif file.filename.endswith(".docx"):
        content = extract_text_from_docx(file.file)
    else:
        return {"error": "Unsupported file type"}

    cv_skills = extract_skills(content)
    skill_db = load_skill_db()
    recommendations = recommend_skills(cv_skills, user_skills, skill_db)
    return {
        "cv_skills": cv_skills,
        "recommendations": recommendations
    }
