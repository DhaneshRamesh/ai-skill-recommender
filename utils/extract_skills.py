from transformers import pipeline

ner_pipeline = pipeline("token-classification", model="dslim/bert-base-NER", aggregation_strategy="simple")

def extract_skills(text: str):
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
