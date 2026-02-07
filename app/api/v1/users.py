from typing import Any, List
from fastapi import APIRouter, Body
from sqlalchemy import select
from app.api.deps import SessionDep, CurrentUser
from app.schemas.user import User as UserSchema
from app.models.user import User

router = APIRouter()

@router.get("/me", response_model=UserSchema)
def read_users_me(current_user: CurrentUser) -> Any:
    """
    Get current user.
    """
    return current_user

@router.post("/batch", response_model=List[UserSchema])
async def read_users_batch(user_ids: List[str] = Body(...), session: SessionDep = None) -> Any:
    """
    Get multiple users by ID.
    """
    stmt = select(User).where(User.id.in_(user_ids))
    result = await session.execute(stmt)
    users = result.scalars().all()
    return users
