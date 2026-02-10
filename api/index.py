from fastapi import FastAPI
from mangum import Mangum
import sys
import os

app = FastAPI()

@app.get("/api/health")
def health_check():
    return {
        "status": "ok", 
        "message": "Backend is running on Vercel (Minimal App)",
        "sys_path": sys.path,
        "cwd": os.getcwd(),
        "files": os.listdir(".")
    }

handler = Mangum(app, lifespan="off")
