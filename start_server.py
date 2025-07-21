import sys
import subprocess
import webbrowser
import time

API_FILE = "main"
PORT = "8001"
URL = f"http://127.0.0.1:{PORT}/docs#/default/extract_skills_extract_skills__post"
RELOAD = True

def main():
    try:
        uvicorn_cmd = [
            sys.executable, "-m", "uvicorn",
            f"{API_FILE}:app",
            "--port", PORT
        ]
        if RELOAD:
            uvicorn_cmd.append("--reload")

        print(f"[DEBUG] Launching FastAPI server with command: {' '.join(uvicorn_cmd)}")

        process = subprocess.Popen(uvicorn_cmd)
        print(f"\n✅ FastAPI server launched at: http://127.0.0.1:{PORT}")
        print(f"📄 Running from file: {API_FILE}.py\n")

        time.sleep(3)
        webbrowser.open_new_tab(URL)
        print(f"🌐 Swagger UI opened at: {URL}\n")

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
        print(f"❌ Failed to start FastAPI server: {e}")

if __name__ == "__main__":
    main()
