from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class TextInput(BaseModel):
    text: str

@app.post("/extract-skills/")
def extract_skills(data: TextInput):
    text = data.text
    # Call your skill extraction logic here
    return {"skills": ["Python", "FastAPI", "Transformers"]}  # Example
