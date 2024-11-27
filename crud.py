from sqlalchemy.orm import Session
import models, schemas

def create_vehicle_detection(db: Session, vehicle: schemas.VehicleDetectionCreate):
    db_vehicle = models.VehicleDetection(**vehicle.dict())
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

def get_vehicle_detections(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.VehicleDetection).offset(skip).limit(limit).all()

def delete_vehicle_detection(db: Session, vehicle_id: int):
    db.query(models.VehicleDetection).filter(models.VehicleDetection.id == vehicle_id).delete()
    db.commit()
