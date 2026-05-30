import sys
import os

# Insert the backend directory into the search path so that the app's internal imports resolve perfectly
backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
sys.path.insert(0, backend_path)

# Import the FastAPI app instance from backend/app/main.py
from app.main import app
