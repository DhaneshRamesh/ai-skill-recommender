from fastapi import FastAPI
from pydantic import BaseModel
from utils.extract_skills import extract_skills_logic  # ✅ Import here

# Initialize FastAPI app
app = FastAPI()

# Input model
class TextInput(BaseModel):
    text: str

# API route
@app.post("/extract-skills/")
def extract_skills(data: TextInput):
    skills = extract_skills_logic(data.text)  # ✅ data.text is a string
    return {"skills": skills}
