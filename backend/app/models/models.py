from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database.database import Base

class NguoiDung(Base):
    __tablename__ = "nguoi_dung"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True, index=True, nullable=False)
    mat_khau = Column(String, nullable=False)
    ho_ten = Column(String, nullable=False)
    so_dien_thoai = Column(String, nullable=True)
    vai_tro = Column(String, default="benh_nhan", nullable=False)
    ngay_tao = Column(DateTime, default=datetime.utcnow, nullable=False)

    benh_nhan = relationship("BenhNhan", back_populates="nguoi_dung", uselist=False)
    bac_si = relationship("BacSi", back_populates="nguoi_dung", uselist=False)

class BenhNhan(Base):
    __tablename__ = "benh_nhan"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nguoi_dung_id = Column(Integer, ForeignKey("nguoi_dung.id"), unique=True, nullable=False)
    ngay_sinh = Column(Date, nullable=True)
    gioi_tinh = Column(String, nullable=True)
    dia_chi = Column(String, nullable=True)

    nguoi_dung = relationship("NguoiDung", back_populates="benh_nhan")

class BacSi(Base):
    __tablename__ = "bac_si"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nguoi_dung_id = Column(Integer, ForeignKey("nguoi_dung.id"), unique=True, nullable=False)
    chuyen_khoa_id = Column(Integer, nullable=True)
    mo_ta = Column(String, nullable=True)
    rating = Column(Float, default=0.0)
    so_luong_danh_gia = Column(Integer, default=0)

    nguoi_dung = relationship("NguoiDung", back_populates="bac_si")