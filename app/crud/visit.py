from sqlalchemy.orm import Session
from app.models.visit import Visit
from app.schemas.visit import VisitCreate, VisitUpdate

def get_visits(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Visit).offset(skip).limit(limit).all()

def get_visit(db: Session, visit_id: int):
    return db.query(Visit).filter(Visit.id == visit_id).first()

def get_patient_visits(db: Session, patient_id: int):
    return db.query(Visit).filter(Visit.patient_id == patient_id).all()

def create_visit(db: Session, visit: VisitCreate, user_id: int):
    db_visit = Visit(**visit.dict(), created_by=user_id)
    db.add(db_visit)
    db.commit()
    db.refresh(db_visit)
    return db_visit

def update_visit(db: Session, visit_id: int, visit: VisitUpdate):
    db_visit = db.query(Visit).filter(Visit.id == visit_id).first()
    if db_visit:
        update_data = visit.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_visit, field, value)
        db.commit()
        db.refresh(db_visit)
    return db_visit

def delete_visit(db: Session, visit_id: int):
    db_visit = db.query(Visit).filter(Visit.id == visit_id).first()
    if db_visit:
        db.delete(db_visit)
        db.commit()
    return db_visit