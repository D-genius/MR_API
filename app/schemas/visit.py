from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class VisitBase(BaseModel):
    patient_id: int
    visit_date: date
    visit_type: Optional[str] = None
    # symptoms: Optional[str] = None
    diagnosis: Optional[str] = None
    # treatment: Optional[str] = None
    prescription: Optional[str] = None
    notes: Optional[str] = None
    # blood_pressure: Optional[str] = None
    # heart_rate: Optional[int] = None
    # temperature: Optional[float] = None
    # weight: Optional[float] = None
    # height: Optional[float] = None

class VisitCreate(VisitBase):
    pass

class VisitUpdate(BaseModel):
    visit_date: Optional[date] = None
    visit_type: Optional[str] = None
    # symptoms: Optional[str] = None
    diagnosis: Optional[str] = None
    # treatment: Optional[str] = None
    prescription: Optional[str] = None
    notes: Optional[str] = None
    # blood_pressure: Optional[str] = None
    # heart_rate: Optional[int] = None
    # temperature: Optional[float] = None
    # weight: Optional[float] = None
    # height: Optional[float] = None

class Visit(VisitBase):
    id: int
    created_by: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True