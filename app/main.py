from fastapi import FastAPI
from app.api import auth

app = FastAPI(title="Colosseum Core", version="0.1.0")

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])

@app.get("/")
async def root():
    return {"message": "Welcome to Colosseum Core Identity Provider"}
