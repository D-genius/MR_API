from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.models import User, MedicalRecord
from app.schemas.schemas import UserCreate, MedicalRecordCreate, MedicalRecordUpdate
from app.auth.security import get_password_hash, verify_password

# User CRUD
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# Medical Record CRUD
def get_medical_records(db: Session, skip: int = 0, limit: int = 100, search: str = None):
    query = db.query(MedicalRecord)
    
    if search:
        query = query.filter(
            or_(
                MedicalRecord.patient_name.ilike(f"%{search}%"),
                MedicalRecord.diagnosis.ilike(f"%{search}%"),
                MedicalRecord.symptoms.ilike(f"%{search}%")
            )
        )
    
    return query.offset(skip).limit(limit).all()

def get_medical_record_by_id(db: Session, record_id: int):
    return db.query(MedicalRecord).filter(MedicalRecord.id == record_id).first()

def get_patient_records(db: Session, patient_id: int):
    return db.query(MedicalRecord).filter(MedicalRecord.patient_id == patient_id).all()

def create_medical_record(db: Session, record: MedicalRecordCreate, user_id: int):
    db_record = MedicalRecord(
        **record.dict(),
        created_by=user_id
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

def update_medical_record(db: Session, record_id: int, record_update: MedicalRecordUpdate):
    db_record = db.query(MedicalRecord).filter(MedicalRecord.id == record_id).first()
    
    if not db_record:
        return None
    
    update_data = record_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_record, field, value)
    
    db.commit()
    db.refresh(db_record)
    return db_record

def delete_medical_record(db: Session, record_id: int):
    db_record = db.query(MedicalRecord).filter(MedicalRecord.id == record_id).first()
    
    if not db_record:
        return False
    
    db.delete(db_record)
    db.commit()
    return True