import requests

def extract_skills_with_ollama(text: str) -> list:
    """
    Sends resume text to a local Ollama LLM (e.g., gemma:2b or phi),
    and returns a cleaned list of extracted skills/tools.
    """
    model = "gemma:2b"  # or use "phi" if gemma is too weak

    prompt = (
        "You are a resume analysis assistant. Extract all relevant technical skills, tools, technologies, platforms, and soft skills "
        "mentioned in the following resume. Return only a list. Do not include any explanations or extra formatting. "
        "One skill per line. Avoid duplicates.\n\n"
        "Resume text:\n"
        + text
    )

    try:
        print("\n📤 Sending prompt to Ollama model:", model)
        print("📝 Prompt preview:\n", prompt[:500], "\n")

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            }
        )

        response.raise_for_status()
        output = response.json().get("response", "")

        print("🧠 RAW Ollama Response:\n", output, "\n")

        skills = [line.strip("-• ").strip() for line in output.splitlines() if line.strip()]

        print("🧹 Cleaned Extracted Skills:\n", skills, "\n")
        return skills

    except requests.RequestException as e:
        print(f"❌ Ollama API request failed: {e}")
        return []

    except Exception as e:
        print(f"❌ Skill parsing failed: {e}")
        return []
