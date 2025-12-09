from sqlalchemy.orm import Session
from sqlalchemy import and_
from . import models, schemas


def list_appointments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Appointment).order_by(models.Appointment.start_time).offset(skip).limit(limit).all()


def get_appointment(db: Session, appointment_id: int):
    return db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()


def has_overlap(db: Session, start_time, end_time) -> bool:
    # overlap if existing.start < new_end and existing.end > new_start
    q = db.query(models.Appointment).filter(
        and_(models.Appointment.start_time < end_time, models.Appointment.end_time > start_time)
    )
    return db.query(q.exists()).scalar()


def create_appointment(db: Session, appointment: schemas.AppointmentCreate):
    if appointment.start_time >= appointment.end_time:
        raise ValueError("start_time must be before end_time")

    if has_overlap(db, appointment.start_time, appointment.end_time):
        raise ValueError("Requested time overlaps with an existing appointment")

    db_obj = models.Appointment(
        name=appointment.name,
        email=appointment.email,
        start_time=appointment.start_time,
        end_time=appointment.end_time,
        notes=appointment.notes,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_appointment(db: Session, appointment_id: int):
    obj = get_appointment(db, appointment_id)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True
