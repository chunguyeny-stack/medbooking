from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class LichHenCreate(BaseModel):
  doctor_id: int
  patient_name: str
  patient_phone: str
  appointment_date: datetime
  notes: Optional[str] = None


class LichHenUpdate(BaseModel):
  appointment_date: Optional[datetime] = None
  status: Optional[str] = None  # pending, confirmed, cancelled, completed
  notes: Optional[str] = None


class LichHenResponse(BaseModel):
  id: int
  doctor_id: int
  patient_name: str
  patient_phone: str
  appointment_date: datetime
  status: str
  notes: Optional[str]
  created_at: datetime

  class Config:
    from_attributes = True