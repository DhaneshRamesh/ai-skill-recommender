import webbrowser
import subprocess
import time

# Delay to let server start up
url = "http://127.0.0.1:8000/docs#/default/extract_skills_extract_skills__post"

# Start Uvicorn server as a subprocess
process = subprocess.Popen(["python", "-m", "uvicorn", "main:app", "--reload"])

# Wait a few seconds to ensure the server starts
time.sleep(3)

# Open browser to Swagger docs
webbrowser.open_new_tab(url)
