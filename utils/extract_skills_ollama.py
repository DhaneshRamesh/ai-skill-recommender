import requests

def extract_skills_with_ollama(text: str) -> list:
    # Step 1: Build the prompt
    prompt = (
        "Generate a list of all tools and skills mentioned in the following text, "
        "formatted as a separate column. Each row should contain only one tool or skill.\n\n"
        + text
    )

    # Step 2: Send prompt to Ollama server
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "gemma:2b",
            "prompt": prompt,
            "stream": False
        }
    )

    # Step 3: Parse the response
    output = response.json().get("response", "")
    skills = [line.strip("-• ").strip() for line in output.splitlines() if line.strip()]
    
    return skills
