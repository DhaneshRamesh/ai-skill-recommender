from fastapi import FastAPI
from pydantic import BaseModel
from utils.extract_skills_ollama import extract_skills_with_ollama


# Initialize FastAPI app
app = FastAPI()

# Input model
class TextInput(BaseModel):
    text: str

'''
# API route
@app.post("/extract-skills/")
def extract_skills(data: TextInput):
    skills = extract_skills_logic(data.text) 
    return {"skills": skills}

'''   

@app.post("/extract-skills/")
def extract_skills(data: TextInput):
    text = data.text
    skills = extract_skills_with_ollama(text)
    return {"skills": skills}
