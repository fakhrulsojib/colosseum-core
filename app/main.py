from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from app.core.config import settings
from app.api.v1 import auth, users

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])

@app.get("/")
def root():
    return {"message": "Welcome to Colosseum Core"}
