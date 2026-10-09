from datetime import datetime
from app.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String


class LeTan(Base):
  __tablename__ = "le_tan"

  id = Column(Integer, primary_key=True, index=True)
  user_id = Column(Integer, ForeignKey("nguoi_dung.id"), nullable=False)
  full_name = Column(String, nullable=False)
  phone = Column(String, nullable=True)
  shift = Column(String, nullable=True)  # Ca trực: Sáng, Chiều, Tối
  created_at = Column(DateTime, default=datetime.utcnow)