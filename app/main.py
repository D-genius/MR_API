from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List

from app.database import get_db, Base, engine
from app.models import user, patient, visit
from app.schemas import user as user_schema, patient as patient_schema, visit as visit_schema
from app.crud import user as user_crud, patient as patient_crud, visit as visit_crud
from app.auth.jwt import create_access_token, verify_token
# from app.auth.security import verify_password
from app.config import settings

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Meditrak Records API",
    description="Backend API for Medical Records Management System",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_token(token, credentials_exception)
    user = user_crud.get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

# Authentication endpoints
@app.post("/token", response_model=user_schema.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    user = user_crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/register", response_model=user_schema.User)
def register_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_crud.create_user(db=db, user=user)

# User endpoints
@app.get("/users/me", response_model=user_schema.User)
async def read_users_me(current_user: user_schema.User = Depends(get_current_user)):
    return current_user

# Patient endpoints
@app.get("/patients", response_model=List[patient_schema.Patient])
def read_patients(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(get_current_user)
):
    patients = patient_crud.get_patients(db, skip=skip, limit=limit)
    return patients

@app.get("/patients/{patient_id}", response_model=patient_schema.Patient)
def read_patient(
    patient_id: int, 
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(get_current_user)
):
    db_patient = patient_crud.get_patient(db, patient_id=patient_id)
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return db_patient

@app.post("/patients", response_model=patient_schema.Patient)
def create_patient(
    patient: patient_schema.PatientCreate,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(get_current_user)
):
    return patient_crud.create_patient(db=db, patient=patient, user_id=current_user.id)

@app.put("/patients/{patient_id}", response_model=patient_schema.Patient)
def update_patient(
    patient_id: int,
    patient: patient_schema.PatientUpdate,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(get_current_user)
):
    db_patient = patient_crud.update_patient(db, patient_id=patient_id, patient=patient)
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return db_patient

@app.delete("/patients/{patient_id}")
def delete_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(get_current_user)
):
    db_patient = patient_crud.delete_patient(db, patient_id=patient_id)
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {"message": "Patient deleted successfully"}

# Visit endpoints
@app.get("/visits", response_model=List[visit_schema.Visit])
def read_visits(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(get_current_user)
):
    visits = visit_crud.get_visits(db, skip=skip, limit=limit)
    return visits

@app.get("/patients/{patient_id}/visits", response_model=List[visit_schema.Visit])
def read_patient_visits(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(get_current_user)
):
    visits = visit_crud.get_patient_visits(db, patient_id=patient_id)
    return visits

@app.get("/visits/{visit_id}", response_model=visit_schema.Visit)
def read_visit(
    visit_id: int, 
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(get_current_user)
):
    db_visit = visit_crud.get_visit(db, visit_id=visit_id)
    if db_visit is None:
        raise HTTPException(status_code=404, detail="Visit not found")
    return db_visit

@app.post("/visits", response_model=visit_schema.Visit)
def create_visit(
    visit: visit_schema.VisitCreate,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(get_current_user)
):
    return visit_crud.create_visit(db=db, visit=visit, user_id=current_user.id)

@app.put("/visits/{visit_id}", response_model=visit_schema.Visit)
def update_visit(
    visit_id: int,
    visit: visit_schema.VisitUpdate,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(get_current_user)
):
    db_visit = visit_crud.update_visit(db, visit_id=visit_id, visit=visit)
    if db_visit is None:
        raise HTTPException(status_code=404, detail="Visit not found")
    return db_visit

@app.delete("/visits/{visit_id}")
def delete_visit(
    visit_id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(get_current_user)
):
    db_visit = visit_crud.delete_visit(db, visit_id=visit_id)
    if db_visit is None:
        raise HTTPException(status_code=404, detail="Visit not found")
    return {"message": "Visit deleted successfully"}

@app.get("/")
def read_root():
    return {"message": "Meditrak Records API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)