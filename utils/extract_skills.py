from transformers import pipeline

# Load the NER model (only once, globally)
ner = pipeline("ner", model="dslim/bert-base-NER", aggregation_strategy="simple")

def extract_skills(text):
    entities = ner(text)
    return list(set([
        ent['word']
        for ent in entities
        if ent['entity_group'] in ['ORG', 'MISC']
    ]))
