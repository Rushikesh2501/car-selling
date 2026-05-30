import sys
import os

# Add backend directory to system path to ensure app imports resolve perfectly
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

import uvicorn
# Import the app instance from backend/app/main.py
from app.main import app

if __name__ == "__main__":
    # Fallback default port for local testing
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
