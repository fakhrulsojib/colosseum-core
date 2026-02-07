from fastapi import APIRouter, Request, Depends
from starlette.responses import RedirectResponse
from sqlalchemy import select

from app.services.google import oauth
from app.api.deps import SessionDep
from app.models.user import User
from app.core import security
from app.core.config import settings

router = APIRouter()

@router.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for('auth_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/callback", name='auth_callback')
async def callback(request: Request, session: SessionDep):
    token = await oauth.google.authorize_access_token(request)
    user_info = token.get('userinfo')
    if user_info:
        # Upsert user
        result = await session.execute(select(User).where(User.email == user_info['email']))
        user = result.scalars().first()
        
        if not user:
             user = User(
                 email=user_info['email'],
                 full_name=user_info.get('name'),
                 avatar_url=user_info.get('picture'),
                 google_sub=user_info.get('sub')
             )
             session.add(user)
        else:
             user.full_name = user_info.get('name')
             user.avatar_url = user_info.get('picture')
             
        await session.commit()
        await session.refresh(user)
        
        access_token = security.create_access_token(user.id)
        return RedirectResponse(url=f"http://localhost:3000/auth/success?token={access_token}")
        
    return {"error": "Authentication failed"}
