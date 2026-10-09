from datetime import datetime
from app.database import Base
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class BacSi(Base):
  __tablename__ = "bac_si"

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String, index=True, nullable=False)
  specialization = Column(String, index=True, nullable=False)
  price = Column(Float, nullable=False)
  phone = Column(String, nullable=True)
  email = Column(String, nullable=True)
  status = Column(Integer, default=1)  # 1: Hoạt động, 0: Xóa ẩn (Soft Delete)
  is_hot = Column(Boolean, default=False)
  is_new = Column(Boolean, default=True)

  created_at = Column(DateTime, default=datetime.utcnow)
  created_by = Column(String, nullable=True)
  updated_at = Column(DateTime, nullable=True)
  updated_by = Column(String, nullable=True)

  # Quan hệ 1 - N với các dị bản/chuyên khoa phụ thuộc
  variants = relationship(
      "BacSiVariant", back_populates="doctor", cascade="all, delete-orphan"
  )


class BacSiVariant(Base):
  __tablename__ = "bac_si_variant"

  id = Column(Integer, primary_key=True, index=True)
  doctor_id = Column(Integer, ForeignKey("bac_si.id"), nullable=False)
  sub_department = Column(String, nullable=False)
  working_hours = Column(String, nullable=True)
  branch_location = Column(String, nullable=True)

  doctor = relationship("BacSi", back_populates="variants")