from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional


class AppointmentBase(BaseModel):
    name: str = Field(..., example="Alice")
    email: EmailStr
    start_time: datetime
    end_time: datetime
    notes: Optional[str] = None


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentRead(AppointmentBase):
    id: int

    class Config:
        orm_mode = True
