from fastapi import FastAPI
from pydantic import BaseModel
from utils.extract_skills import extract_skills as extract_skills_from_utils

app = FastAPI()

class TextInput(BaseModel):
    text: str

@app.get("/docs")  
def index():
    return {"message": "Welcome to the AI Skill Recommender API"}

@app.post("/extract-skills/")
def extract_skills(data: TextInput):
    text = data.text
    skills = extract_skills_from_utils(text)
    return {"skills": skills}
   
