import sys
import os

# Add the parent directory to the path so we can import from backend
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from mangum import Mangum
from backend.main import app

@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "Backend is running on Vercel"}

# Mangum handler for Vercel serverless functions
handler = Mangum(app, lifespan="off")
