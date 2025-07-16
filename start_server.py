import sys
import subprocess
import webbrowser
import time

# Define port and Swagger URL
port = "8001"
url = f"http://127.0.0.1:{port}/docs#/default/extract_skills_extract_skills__post"

try:
    # Start Uvicorn server using the current Python interpreter
    process = subprocess.Popen([
        sys.executable,
        "-m", "uvicorn",
        "main:app",
        "--reload",
        "--port", port
    ])
    print(f"✅ Started FastAPI server on port {port} using: {sys.executable}")

    # Wait a few seconds to ensure the server starts
    time.sleep(3)

    # Open Swagger UI in browser
    webbrowser.open_new_tab(url)
    print(f"🌐 Swagger UI opened at: {url}")

except Exception as e:
    print("❌ Failed to start server:")
    print(e)
