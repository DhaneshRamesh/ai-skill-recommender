import sys
import subprocess
import webbrowser
import time

# -----------------------------
# CONFIG
# -----------------------------
API_FILE = "main"  # <- This is the file containing your FastAPI app
PORT = "8001"
URL = f"http://127.0.0.1:{PORT}/docs#/default/extract_skills_extract_skills__post"
RELOAD = True  # Set to False in production

# -----------------------------
# Start Uvicorn Server
# -----------------------------
def main():
    try:
        # Build Uvicorn launch command
        uvicorn_cmd = [
            sys.executable, "-m", "uvicorn",
            f"{API_FILE}:app",
            "--port", PORT
        ]
        if RELOAD:
            uvicorn_cmd.append("--reload")

        # Start FastAPI server
        process = subprocess.Popen(uvicorn_cmd)
        print(f"\n✅ FastAPI server launched at: http://127.0.0.1:{PORT}")
        print(f"📄 Running from file: {API_FILE}.py\n")

        # Wait for server to be ready
        time.sleep(3)
        webbrowser.open_new_tab(URL)
        print(f"🌐 Swagger UI opened at: {URL}\n")

        # Wait for manual termination
        process.wait()

    except KeyboardInterrupt:
        print("\n⛔ Shutting down server...")
        process.terminate()
        try:
            process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            process.kill()
        print("✅ Server stopped cleanly.")

    except Exception as e:
        print("❌ Failed to start FastAPI server:")
        print(e)

# -----------------------------
# Entry Point
# -----------------------------
if __name__ == "__main__":
    main()
