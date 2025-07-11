from transformers import pipeline

# Load the pipeline once globally
ner_pipeline = pipeline("token-classification", model="dslim/bert-base-NER", aggregation_strategy="simple")

def extract_skills(text: str):
    entities = ner_pipeline(text)
    # Filter for skill-like labels or just return all for now
    extracted = [e['word'] for e in entities if e['entity_group'] in ["ORG", "MISC", "PER"]]
    return list(set(extracted))  # Remove duplicates
