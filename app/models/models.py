from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False)  # doctor, nurse, patient, admin
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    medical_records = relationship("MedicalRecord", back_populates="patient")
    created_records = relationship("MedicalRecord", foreign_keys="MedicalRecord.created_by", back_populates="creator")

class MedicalRecord(Base):
    __tablename__ = "medical_records"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Patient Information
    patient_name = Column(String(255), nullable=False)
    patient_age = Column(Integer, nullable=False)
    patient_gender = Column(String(10), nullable=False)
    patient_contact = Column(String(20))
    
    # Medical Information
    diagnosis = Column(Text, nullable=False)
    symptoms = Column(Text)
    treatment_plan = Column(Text)
    medications = Column(Text)
    allergies = Column(Text)
    vital_signs = Column(Text)  # JSON string for BP, temperature, etc.
    lab_results = Column(Text)
    notes = Column(Text)
    
    # Record Metadata
    record_date = Column(DateTime(timezone=True), server_default=func.now())
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_confidential = Column(Boolean, default=False)
    
    # Relationships
    patient = relationship("User", foreign_keys=[patient_id], back_populates="medical_records")
    creator = relationship("User", foreign_keys=[created_by], back_populates="created_records")