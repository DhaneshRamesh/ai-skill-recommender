import requests
import json 
from typing import Dict, List, Union

def extract_all_skills(markdown_text: str) -> Dict[str, Union[Dict[str, List[str]], List[str]]]:
    """
    Extracts ALL explicitly mentioned skills, tools, and proficiencies from resume text.
    Returns flat skill list JSON with uncertainty log.
    """
    prompt = f"""You are an expert in resume parsing and in the specific domain that this resume text relates to (e.g., computer science, engineering, finance, healthcare, etc.).

Your task is to extract **only the skills, tools, softwares and proficiencies explicitly mentioned** in the following resume text, considering the context and domain to accurately identify relevant professional capabilities.

Extract ALL explicitly mentioned skills, tools, technologies, methodologies, platforms, and proficiencies that are clearly presented as part of the candidate’s professional experience or expertise in their domains under the skills/highlights or any other relevant sections regardless of if it is legacy or latest.

Include soft skills and domain-specific competencies only if they are explicitly described and clearly relevant to the candidate’s professional abilities (such as leadership, communication, project management, design, etc.).

Exclude any terms that appear only casually, unrelated to the candidate’s skills, or without clear evidence of proficiency or experience.

The output must be a **flat list of skills** — do **not categorize** them into groups such as "Programming Languages" or "Frameworks".

Preserve original spelling and capitalization.
Your memory resets with each new input. Do not accumulate knowledge across runs.

When unsure about a particular skill or tool, or why it was excluded, explain clearly using the following format:

```json
{{
  "Skills": [],
  "Uncertain": [
    {{ "term": "raw text snippet", "reason": "why it was excluded" }}
  ]
}}
Output ONLY valid JSON in the structure above. Do not include any additional text or explanation outside the JSON.

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
            return {"Skills": [], "Uncertain": []}

        return parsed_skills if isinstance(parsed_skills, dict) else {"Skills": [], "Uncertain": []}

    except Exception as e:
        print(f"❌ Error processing skills: {e}")
        return {"Skills": [], "Uncertain": []}
