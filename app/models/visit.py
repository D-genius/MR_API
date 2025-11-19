from sqlalchemy import Column, Integer, String, Text, DateTime, Date, ForeignKey, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Visit(Base):
    __tablename__ = "visits"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    visit_date = Column(Date, nullable=False)
    visit_type = Column(String)  # OPD or IPD
    # symptoms = Column(Text)
    diagnosis = Column(Text)
    # treatment = Column(Text)
    prescription = Column(Text)
    notes = Column(Text)
    # blood_pressure = Column(String)
    # heart_rate = Column(Integer)
    # temperature = Column(Float)
    # weight = Column(Float)
    # height = Column(Float)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    patient = relationship("Patient", back_populates="visits")