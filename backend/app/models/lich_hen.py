from datetime import datetime
from app.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text


class LichHen(Base):
  __tablename__ = "lich_hen"

  id = Column(Integer, primary_key=True, index=True)
  doctor_id = Column(Integer, ForeignKey("bac_si.id"), nullable=False)
  patient_name = Column(String, nullable=False)
  patient_phone = Column(String, nullable=False)
  appointment_date = Column(DateTime, nullable=False)
  status = Column(
      String, default="pending"
  )  # pending, confirmed, cancelled, completed
  notes = Column(Text, nullable=True)
  created_at = Column(DateTime, default=datetime.utcnow)