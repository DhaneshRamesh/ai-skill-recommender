from sentence_transformers import SentenceTransformer, util
import json

model = SentenceTransformer('all-MiniLM-L6-v2')

def load_skill_db(path="data/skills_db.json"):
    with open(path) as f:
        return json.load(f)["skills"]

def recommend_skills(cv_skills, user_skills, skill_db):
    combined_input = list(set(cv_skills + user_skills))
    existing_set = set(combined_input)
    candidates = [skill for skill in skill_db if skill not in existing_set]

    input_embeds = model.encode(combined_input, convert_to_tensor=True)
    candidate_embeds = model.encode(candidates, convert_to_tensor=True)

    scores = util.cos_sim(input_embeds, candidate_embeds).mean(dim=0)
    ranked = sorted(zip(candidates, scores), key=lambda x: x[1], reverse=True)[:10]

    recommendations = []
    for skill, score in ranked:
        recommendations.append({
            "skill": skill,
            "score": round(float(score), 3),
            "reason": f"Recommended due to similarity with: {', '.join(cv_skills[:3])}"
        })
    return recommendations
