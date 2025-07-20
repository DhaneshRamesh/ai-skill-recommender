from typing import Dict, List, Union, Optional
import requests
import json
import re
import logging

logger = logging.getLogger(__name__)

def empty_skills_template() -> Dict[str, Union[Dict[str, List[str]], List[str]]]:
    """Universal skills template for all resume types"""
    return {
        "technical_skills": {
            "programming_languages": [],
            "software_tools": [],
            "engineering_skills": [],
            "data_skills": [],
            "design_skills": [],
            "hardware_skills": [],
            "scientific_methods": [],
            "other_technical": []
        },
        "business_skills": {
            "management": [],
            "financial": [],
            "operational": [],
            "administrative": []
        },
        "soft_skills": [],
        "languages": [],
        "certifications": [],
        "domain_expertise": [],
        "creative_skills": [],
        "manual_skills": []
    }

def extract_all_skills(text: str) -> Dict[str, Union[Dict[str, List[str]], List[str]]]:
    """
    Universal professional skill extractor that:
    1. Acts like an expert in the resume's domain
    2. Extracts ONLY mentioned skills
    3. Never hallucinates
    4. Covers all professional fields
    """
    prompt = f"""
    You are a professional skill extractor capable of analyzing resumes across all domains—technical, business, creative, academic, and manual trades.

    Your task is to return ONLY the skills and tools that are **explicitly mentioned** in the text below. Use the exact words and avoid making assumptions.

    💡 Rules:
    1. **Only include skills/tools mentioned verbatim** in the resume.
    2. **Do not infer** skills from job titles or company names.
    3. Follow the **exact JSON schema** given below without modifications.
    4. Extract skills from all sections: experience, education, projects, awards, skills, etc.
    5. Categorize skills accurately. If unsure where a skill belongs, place it in `"other_technical"` or `"domain_expertise"`.

    Resume Text:
    {text[:20000]}

    Output JSON format:
    {{
        "technical_skills": {{
            "programming_languages": [],
            "software_tools": [],
            "engineering_skills": [],
            "data_skills": [],
            "design_skills": [],
            "hardware_skills": [],
            "scientific_methods": [],
            "other_technical": []
        }},
        "business_skills": {{
            "management": [],
            "financial": [],
            "operational": [],
            "administrative": []
        }},
        "soft_skills": [],
        "languages": [],
        "certifications": [],
        "domain_expertise": [],
        "creative_skills": [],
        "manual_skills": []
    }}

    Examples:
    - "JavaScript" → programming_languages
    - "Docker" → software_tools
    - "UX design" → design_skills
    - "Project Management" → business_skills.management
    - "Spanish" → languages
    - "Certified Scrum Master" → certifications

    REMEMBER: Return only what's visible. Never assume. Never hallucinate.
    """

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "format": "json",
                "stream": False,
                "options": {
                    "temperature": 0.0,  # Zero creativity for strict extraction
                    "num_ctx": 8192
                }
            },
            timeout=60
        )
        response.raise_for_status()
        raw_output = response.json().get("response", "{}")
        
        # Strict validation
        result = json.loads(raw_output)
        validated = validate_extraction(result, text)
        return validated

    except Exception as e:
        logger.error(f"Extraction failed: {e}")
        return empty_skills_template()

def validate_extraction(extracted: dict, original_text: str) -> dict:
    """Brute-force validation against original text"""
    validated = empty_skills_template()
    original_lower = original_text.lower()
    
    # Validate technical skills
    for category, skills in extracted.get("technical_skills", {}).items():
        if category in validated["technical_skills"]:
            validated["technical_skills"][category] = [
                s for s in skills 
                if isinstance(s, str) and s.lower() in original_lower
            ]
    
    # Validate other categories
    for category in ["business_skills", "soft_skills", "languages", 
                    "certifications", "domain_expertise", 
                    "creative_skills", "manual_skills"]:
        if category in extracted:
            validated[category] = [
                s for s in extracted[category]
                if isinstance(s, str) and s.lower() in original_lower
            ]
    
    return validated

def post_process_skills(skills: dict) -> dict:
    """Final cleanup of extracted skills"""
    # Remove empty categories
    return {
        k: v for k, v in skills.items() 
        if v and (isinstance(v, list) and v or isinstance(v, dict))
    }