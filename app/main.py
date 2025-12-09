from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from . import crud, schemas
from .database import SessionLocal, init_db

app = FastAPI(title="Appointment Booking")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
def on_startup():
    init_db()


@app.post("/appointments", response_model=schemas.AppointmentRead)
def create_appointment(appointment: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    try:
        created = crud.create_appointment(db, appointment)
        return created
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/appointments", response_model=list[schemas.AppointmentRead])
def list_appointments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.list_appointments(db, skip=skip, limit=limit)


@app.get("/appointments/{appointment_id}", response_model=schemas.AppointmentRead)
def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    a = crud.get_appointment(db, appointment_id)
    if not a:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return a


@app.delete("/appointments/{appointment_id}", status_code=204)
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_appointment(db, appointment_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return
