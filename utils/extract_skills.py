from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

# Initialize FastAPI app
app = FastAPI()

# Load the BERT NER pipeline once globally
ner_pipeline = pipeline("token-classification", model="dslim/bert-base-NER", aggregation_strategy="simple")

# Pydantic input model
class TextInput(BaseModel):
    text: str

# Skill extraction logic
def extract_skills_logic(text: str):
    entities = ner_pipeline(text)

    # Step 1: Filter labels
    relevant = [e for e in entities if e['entity_group'] in ["ORG", "MISC", "PER"]]

    # Step 2: Clean weird tokens (like ##ing or GitH)
    cleaned = []
    for ent in relevant:
        word = ent['word']
        if word.startswith("##"):
            continue
        if len(word) <= 1:  # Ignore single letters like "A", "C", etc.
            continue
        cleaned.append(word)

    # Step 3: Return unique results
    return list(set(cleaned))

# API route
@app.post("/extract-skills/")
def extract_skills(data: TextInput):
    skills = extract_skills_logic(data.text)
    return {"skills": skills}
