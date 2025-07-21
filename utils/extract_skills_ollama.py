import requests
import json
from typing import Dict, List, Union

def extract_all_skills(markdown_text: str) -> Dict[str, Union[Dict[str, List[str]], List[str]]]:
    """
    Extracts ALL professional skills from resume text with maximum completeness.
    Returns structured JSON with both hard and soft skills.
    """
    prompt = f"""Extract ALL professional skills from this resume with maximum completeness. Return STRICT JSON format:
{{
    "technical_skills": {{
        "programming_languages": [],
        "frameworks": [],
        "databases": [],
        "devops_tools": [],
        "data_science_tools": [],
        "design_tools": []
    }},
    "platforms": [],
    "soft_skills": [],
    "certifications": [],
    "languages": [],
    "domain_skills": []
}}

RULES:
1. Include EVERY mentioned skill/tool (even if mentioned once)
2. Preserve original names/case (e.g., 'React' not 'react')
3. Extract from ALL sections (experience, education, projects, skills)
4. Include proficiency levels if specified (e.g., "Advanced R")
5. For technologies: include versions ONLY if critical (e.g., "Python 2.7")
6. For soft skills: include only professional attributes
7. Categorize properly based on context

SKILL EXAMPLES TO INCLUDE:
- Programming: Python, Java, C++
- Frameworks: React, TensorFlow, Rails
- Tools: Git, Tableau, Docker
- Platforms: AWS, Heroku, GCP
- Data: SQL, Pandas, Spark
- Design: Photoshop, Figma
- Soft: Leadership, Communication
- Domain: Financial Modeling, UX Research

RESUME TEXT:
{markdown_text[:15000]}"""

    try:
        print("[DEBUG] Sending prompt to Ollama API (preview first 1000 chars):")
        print(prompt[:1000])

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2:3b",
                "prompt": prompt,
                "format": "json",
                "stream": False,
                "options": {"temperature": 0.1}
            },
            timeout=1000
        )
        response.raise_for_status()

        print(f"[DEBUG] Raw Ollama API response:\n{response.text}")

        raw_output = response.json().get("response", "{}")
        
        try:
            parsed_skills = json.loads(raw_output)
            print("[DEBUG] Parsed skills JSON successfully")
        except json.JSONDecodeError as json_err:
            print(f"❌ JSON parsing error: {json_err}")
            print(f"[DEBUG] Raw output was:\n{raw_output}")
            return empty_skills_template()

        return validate_skills(parsed_skills)

    except Exception as e:
        print(f"❌ Error processing skills: {e}")
        return empty_skills_template()

def validate_skills(raw_data: dict) -> Dict[str, Union[Dict[str, List[str]], List[str]]]:
    """Ensures output matches our schema with all required categories"""
    template = empty_skills_template()

    if not isinstance(raw_data, dict):
        print("[DEBUG] Raw data not dict, returning empty template")
        return template

    # Validate technical_skills subcategories
    if "technical_skills" in raw_data and isinstance(raw_data["technical_skills"], dict):
        for tech_category in template["technical_skills"]:
            if tech_category in raw_data["technical_skills"]:
                template["technical_skills"][tech_category] = [
                    skill for skill in raw_data["technical_skills"][tech_category]
                    if isinstance(skill, str) and skill.strip()
                ]

    # Validate top-level categories
    for category in ["platforms", "soft_skills", "certifications", "languages", "domain_skills"]:
        if category in raw_data and isinstance(raw_data[category], list):
            template[category] = [
                item for item in raw_data[category]
                if isinstance(item, str) and item.strip()
            ]

    return template

def empty_skills_template() -> Dict[str, Union[Dict[str, List[str]], List[str]]]:
    """Returns a complete empty skills structure"""
    return {
        "technical_skills": {
            "programming_languages": [],
            "frameworks": [],
            "databases": [],
            "devops_tools": [],
            "data_science_tools": [],
            "design_tools": []
        },
        "platforms": [],
        "soft_skills": [],
        "certifications": [],
        "languages": [],
        "domain_skills": []
    }
