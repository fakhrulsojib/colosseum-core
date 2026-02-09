from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from typing import List, Optional
from pydantic import BaseModel

from app.db.session import get_db
from app.models.hero_image import HeroImage

router = APIRouter()

# Pydantic models
class HeroImageBase(BaseModel):
    url: str
    alt: Optional[str] = None
    title: Optional[str] = None
    subtitle: Optional[str] = None
    is_active: bool = True

class HeroImageCreate(HeroImageBase):
    pass

class HeroImageUpdate(BaseModel):
    url: Optional[str] = None
    alt: Optional[str] = None
    title: Optional[str] = None
    subtitle: Optional[str] = None
    is_active: Optional[bool] = None

class HeroImageResponse(HeroImageBase):
    id: int

    class Config:
        orm_mode = True

@router.get("/", response_model=List[HeroImageResponse])
async def get_active_hero_images(db: Session = Depends(get_db)):
    """
    Get list of active hero images for the main landing page.
    """
    result = await db.execute(select(HeroImage).filter(HeroImage.is_active == True))
    return result.scalars().all()

@router.get("/all", response_model=List[HeroImageResponse])
async def get_all_hero_images(db: Session = Depends(get_db)):
    """
    Get all hero images (active and inactive).
    """
    result = await db.execute(select(HeroImage))
    return result.scalars().all()

@router.post("/", response_model=HeroImageResponse)
async def create_hero_image(image: HeroImageCreate, db: Session = Depends(get_db)):
    """
    Create a new hero image.
    """
    db_image = HeroImage(**image.dict())
    db.add(db_image)
    await db.commit()
    await db.refresh(db_image)
    return db_image

@router.patch("/{image_id}", response_model=HeroImageResponse)
async def update_hero_image(image_id: int, image_update: HeroImageUpdate, db: Session = Depends(get_db)):
    """
    Update a hero image.
    """
    result = await db.execute(select(HeroImage).filter(HeroImage.id == image_id))
    db_image = result.scalars().first()
    
    if not db_image:
        raise HTTPException(status_code=404, detail="Hero image not found")
    
    update_data = image_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_image, key, value)
    
    await db.commit()
    await db.refresh(db_image)
    return db_image

@router.delete("/{image_id}")
async def delete_hero_image(image_id: int, db: Session = Depends(get_db)):
    """
    Delete a hero image.
    """
    result = await db.execute(select(HeroImage).filter(HeroImage.id == image_id))
    db_image = result.scalars().first()
    
    if not db_image:
        raise HTTPException(status_code=404, detail="Hero image not found")
    
    await db.delete(db_image)
    await db.commit()
    return {"ok": True}
