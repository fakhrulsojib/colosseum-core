from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()

class HeroImage(BaseModel):
    id: int
    url: str
    alt: str
    title: str
    subtitle: str

# Mock data for now - in a real app this might come from DB
hero_images_data = [
    {
        "id": 1,
        "url": 'https://images.unsplash.com/photo-1574629810360-7efbbe195018?w=1200&h=600&fit=crop',
        "alt": 'Soccer Match',
        "title": 'FIFA World League',
        "subtitle": 'Experience the thrill of virtual football'
    },
    {
        "id": 2,
        "url": 'https://images.unsplash.com/photo-1624526267942-ab0ff8a3e972?w=1200&h=600&fit=crop',
        "alt": 'Cricket Match',
        "title": 'Cricket T20 Series',
        "subtitle": 'Big hits and massive sixes'
    }
]

@router.get("/", response_model=List[HeroImage])
def get_hero_images():
    """
    Get list of hero images for the main landing page.
    """
    return hero_images_data
