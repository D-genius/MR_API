from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import timedelta
import os
from dotenv import load_dotenv

from app.models.database import get_db, engine
from app.models.models import Base
from app.schemas.schemas import User, UserCreate, MedicalRecord, MedicalRecordCreate, MedicalRecordUpdate, Token
from app.crud import crud
from app.auth.auth import get_current_active_user, require_role
from app.auth.security import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

load_dotenv()

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Medical Records API",
    description="A secure REST API for managing medical records",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Authentication endpoints
@app.post("/auth/register", response_model=User)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    return crud.create_user(db=db, user=user)

@app.post("/auth/login", response_model=Token)
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id}, 
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

# Medical Records endpoints
@app.get("/records/", response_model=list[MedicalRecord])
def read_records(
    skip: int = 0,
    limit: int = 100,
    search: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    records = crud.get_medical_records(db, skip=skip, limit=limit, search=search)
    return records

@app.get("/records/{record_id}", response_model=MedicalRecord)
def read_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    record = crud.get_medical_record_by_id(db, record_id=record_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return record

@app.post("/records/", response_model=MedicalRecord)
def create_record(
    record: MedicalRecordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("doctor"))
):
    return crud.create_medical_record(db=db, record=record, user_id=current_user.id)

@app.put("/records/{record_id}", response_model=MedicalRecord)
def update_record(
    record_id: int,
    record_update: MedicalRecordUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("doctor"))
):
    record = crud.update_medical_record(db, record_id=record_id, record_update=record_update)
    if record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return record

@app.delete("/records/{record_id}")
def delete_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    success = crud.delete_medical_record(db, record_id=record_id)
    if not success:
        raise HTTPException(status_code=404, detail="Record not found")
    return {"message": "Record deleted successfully"}

# Patient-specific endpoints
@app.get("/patients/{patient_id}/records", response_model=list[MedicalRecord])
def read_patient_records(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Patients can only see their own records, staff can see all
    if current_user.role == "patient" and current_user.id != patient_id:
        raise HTTPException(status_code=403, detail="Not authorized to view these records")
    
    records = crud.get_patient_records(db, patient_id=patient_id)
    return records

# User management
@app.get("/users/me", response_model=User)
def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@app.get("/")
def read_root():
    return {"message": "Medical Records API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)