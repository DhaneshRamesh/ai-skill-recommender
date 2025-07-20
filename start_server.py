import sys
import subprocess
import webbrowser
import time
import logging
from typing import Optional

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
CONFIG = {
    "api_file": "main",
    "host": "127.0.0.1",
    "port": "8001",
    "reload": True,
    "workers": 1,
    "timeout": 30
}

def check_dependencies():
    """Verify required packages are installed"""
    try:
        import uvicorn
        import pymupdf4llm
        import fitz
    except ImportError as e:
        logger.error(f"Missing dependency: {e}")
        raise RuntimeError("Run: pip install uvicorn pymupdf4llm pymupdf")

def start_server():
    """Start the FastAPI server with configured options"""
    check_dependencies()
    
    cmd = [
        sys.executable, "-m", "uvicorn",
        f"{CONFIG['api_file']}:app",
        "--host", CONFIG["host"],
        "--port", CONFIG["port"],
        "--timeout-keep-alive", str(CONFIG["timeout"])
    ]
    
    if CONFIG["reload"]:
        cmd.append("--reload")
    else:
        cmd.extend(["--workers", str(CONFIG["workers"])])
    
    try:
        logger.info("Starting server...")
        proc = subprocess.Popen(cmd)
        
        url = f"http://{CONFIG['host']}:{CONFIG['port']}/docs"
        logger.info(f"Server running at {url}")
        
        # Wait for server to initialize
        time.sleep(2)
        webbrowser.open(url)
        
        return proc
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        raise

if __name__ == "__main__":
    try:
        proc = start_server()
        proc.wait()
    except KeyboardInterrupt:
        logger.info("Shutting down server...")
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except subprocess.TimeoutExpired:
            proc.kill()
        logger.info("Server stopped")
    except Exception as e:
        logger.error(f"Critical error: {e}")
        sys.exit(1)