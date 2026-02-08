import requests
from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy import select
from app.api.deps import SessionDep
from app.models.user import User
from app.core import security
from app.core.config import settings

router = APIRouter()

@router.post("/google")
async def verify_google_token(token_data: dict, session: SessionDep):
    token = token_data.get('access_token')
    if not token:
         raise HTTPException(status_code=400, detail="Missing access_token")

    try:
        # Verify access token by fetching user info
        response = requests.get(
             'https://www.googleapis.com/oauth2/v3/userinfo',
             headers={'Authorization': f'Bearer {token}'}
        )
        if response.status_code != 200:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
            
        user_info = response.json()
        email = user_info.get('email')
        
        if not email:
             raise HTTPException(status_code=400, detail="Email not found in token")

        # Upsert user
        result = await session.execute(select(User).where(User.email == email))
        user = result.scalars().first()
        
        if not user:
             user = User(
                 email=email,
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
        return {"access_token": access_token, "token_type": "bearer", "user": {"email": user.email, "name": user.full_name, "picture": user.avatar_url}}
        
    except Exception as e:
        print(f"Auth Error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
