from pydantic import BaseModel

class VehicleDetectionCreate(BaseModel):
    type: str
    confidence: float
    image_path: str

class VehicleDetection(VehicleDetectionCreate):
    id: int
    detected_at: str

    class Config:
        orm_mode = True
