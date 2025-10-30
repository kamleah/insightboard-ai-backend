import uvicorn
import os
from datetime import datetime
import google.generativeai as genai

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv


from routers import level1 as v1
from routers import level2 as v2

load_dotenv()

app = FastAPI(title="InsightBoard AI API (Gemini)", version="1.0.0")

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Gemini client
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model_name = os.getenv("LLM_MODEL", "gemini-2.5-flash")
app.state.gemini_model = genai.GenerativeModel(model_name)

# ✅ Include Routers
app.include_router(v1.router)
app.include_router(v2.router)

@app.get("/")
async def root():
    return {"message": "InsightBoard AI API is running", "available_versions": ["v1", "v2"]}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)