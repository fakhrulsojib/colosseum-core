from fastapi import APIRouter

router = APIRouter()

@router.get("/login/google")
async def login_google():
    return {"message": "Redirect to Google Login"}

@router.get("/callback/google")
async def callback_google():
    return {"message": "Google Callback - Exchange code for token"}
