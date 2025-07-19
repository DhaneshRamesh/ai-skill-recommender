import requests

def extract_skills_with_ollama(text: str) -> list:
    """
    Sends resume text (plain or markdown) to Ollama (gemma:2b)
    and returns a list of extracted skills/tools.
    """

    # Step 1: Prompt template
    prompt = (
        "Extract all relevant job-related tools, technologies, platforms, or soft skills mentioned "
        "in the following resume text. List one skill or tool per line. Do not include duplicates or empty lines.\n\n"
        + text
    )

    try:
        # Step 2: Call Ollama
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "gemma:2b",
                "prompt": prompt,
                "stream": False
            }
        )

        response.raise_for_status()  # Raise if response is not 200 OK

        # Step 3: Parse text output
        output = response.json().get("response", "")
        skills = [line.strip("-• ").strip() for line in output.splitlines() if line.strip()]

        # Optional debug print
        # print("🧠 Ollama raw response:\n", output)

        return skills

    except requests.RequestException as e:
        print(f"❌ Ollama API request failed: {e}")
        return []

    except Exception as e:
        print(f"❌ Skill parsing failed: {e}")
        return []
