
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
import crud, models, schemas, database, vehicle_detection
import shutil
import os

app = FastAPI()

# Database dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
@app.get("/")
async def read_root():
    return {"message": "Welcome to the vehicle detection API!"}
# File upload and processing
@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    image_path = f"uploads/{file.filename}"
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    detections = vehicle_detection.detect_vehicles(image_path)
    for detection in detections:
        crud.create_vehicle_detection(db, detection)
    return {"detections": detections}

# CRUD endpoints for vehicle detections
@app.get("/detections/", response_model=list[schemas.VehicleDetection])
def read_detections(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_vehicle_detections(db, skip=skip, limit=limit)

@app.delete("/detections/{vehicle_id}")
def delete_detection(vehicle_id: int, db: Session = Depends(get_db)):
    crud.delete_vehicle_detection(db, vehicle_id)
    return {"message": "Vehicle detection deleted"}


from fastapi import WebSocket

@app.websocket("/ws/vehicle-detection")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        frame = await websocket.receive_bytes()  # Assuming frames are sent as byte arrays
        detections = vehicle_detection.detect_vehicles_from_frame(frame)  # Implement frame-based detection
        await websocket.send_json({"detections": detections})
