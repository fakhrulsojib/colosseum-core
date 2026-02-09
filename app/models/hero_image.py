from sqlalchemy import Column, Integer, String, Text, Boolean
from app.db.base_class import Base

class HeroImage(Base):
    id = Column(Integer, primary_key=True, index=True)
    url = Column(Text, nullable=False)  # Text to support Base64 strings
    alt = Column(String, nullable=True)
    title = Column(String, nullable=True)
    subtitle = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
