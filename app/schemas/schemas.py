from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    role: Optional[str] = None

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Medical Record Schemas
class MedicalRecordBase(BaseModel):
    patient_name: str
    patient_age: int
    patient_gender: str
    patient_contact: Optional[str] = None
    diagnosis: str
    symptoms: Optional[str] = None
    treatment_plan: Optional[str] = None
    medications: Optional[str] = None
    allergies: Optional[str] = None
    vital_signs: Optional[str] = None
    lab_results: Optional[str] = None
    notes: Optional[str] = None
    is_confidential: bool = False

class MedicalRecordCreate(MedicalRecordBase):
    patient_id: int

class MedicalRecordUpdate(BaseModel):
    diagnosis: Optional[str] = None
    symptoms: Optional[str] = None
    treatment_plan: Optional[str] = None
    medications: Optional[str] = None
    allergies: Optional[str] = None
    vital_signs: Optional[str] = None
    lab_results: Optional[str] = None
    notes: Optional[str] = None
    is_confidential: Optional[bool] = None

class MedicalRecord(MedicalRecordBase):
    id: int
    patient_id: int
    created_by: int
    record_date: datetime
    last_updated: datetime
    
    class Config:
        from_attributes = True

# Authentication Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    user_id: Optional[int] = None