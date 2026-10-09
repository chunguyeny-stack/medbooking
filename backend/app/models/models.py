from datetime import datetime
from app.database import Base
from sqlalchemy import Column, DateTime, Integer, String


class NguoiDung(Base):
  __tablename__ = "nguoi_dung"

  id = Column(Integer, primary_key=True, index=True)
  username = Column(String, unique=True, index=True, nullable=False)
  email = Column(String, unique=True, index=True, nullable=False)
  hashed_password = Column(String, nullable=False)
  role = Column(String, nullable=False)  # 'admin', 'bac_si', 'le_tan', 'benh_nhan'
  status = Column(Integer, default=1)  # 1: Hoạt động, 0: Đã khóa/Ẩn
  created_at = Column(DateTime, default=datetime.utcnow)
  updated_at = Column(
      DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
  )