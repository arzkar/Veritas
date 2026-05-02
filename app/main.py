import uvicorn
import os
import sys

# Add root to sys.path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.append(root_dir)

print("\n[VERITAS] Initializing investigative intelligence terminal...")
print("[VERITAS] Loading multi-agent orchestration and local reasoning models...")

from app.api.routes import app

if __name__ == "__main__":
    # Point uvicorn to the routes file app instance
    uvicorn.run("app.api.routes:app", host="0.0.0.0", port=8000, reload=True, log_level="info")
