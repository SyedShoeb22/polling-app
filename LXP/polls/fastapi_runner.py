import os
import sys
import subprocess

def start_fastapi():
    # Absolute path to the Django project root
    project_root = "/workspaces/polling-app/LXP"
    os.chdir(project_root)  # Ensure we are in Django context

    module_path = "polls.poll_api_service"  # This should match your file structure

    try:
        print(f"🚀 Starting FastAPI from {module_path}:app")

        subprocess.Popen(
            [sys.executable, "-m", "uvicorn", f"{module_path}:app", "--host", "127.0.0.1", "--port", "8080"],
            stdout=None,   # inherit terminal output
            stderr=None
        )

        print("✅ FastAPI service launched at http://127.0.0.1:8080")
    except Exception as e:
        print("❌ Failed to launch FastAPI:", e)

if __name__ == "__main__":
    start_fastapi()
