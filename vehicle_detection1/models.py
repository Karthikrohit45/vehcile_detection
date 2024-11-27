from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from database import Base

class VehicleDetection(Base):
    __tablename__ = "vehicle_detections"
    
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, index=True)
    confidence = Column(Float)
    image_path = Column(String)
    detected_at = Column(DateTime(timezone=True), server_default=func.now())
