from datetime import datetime, timezone
from sqlalchemy import (
    Column, Integer, String, Date, Time,
    DateTime, ForeignKey, Text
)
from sqlalchemy.orm import relationship
from datadase.database import Base

def utc_now():
    return datetime.now(timezone.utc)


class LichLamViec(Base):
    """Quản lý ca trực / lịch làm việc của Bác sĩ"""
    __tablename__ = "lich_lam_viec"

    ma_lich_lam = Column(Integer, primary_key=True, autoincrement=True, index=True)
    ma_bac_si = Column(Integer, ForeignKey("bac_si.ma_bac_si", ondelete="CASCADE"), nullable=False)
    ngay_lam = Column(Date, nullable=False)
    gio_bat_dau = Column(Time, nullable=False)
    gio_ket_thuc = Column(Time, nullable=False)
    ca_kham = Column(String(50), nullable=True)  # Sang / Chieu
    da_dat = Column(Integer, default=0)  # 0: Con trong, 1: Da kin / Da lock


class LichHen(Base):
    """Thông tin đặt lịch hẹn khám giữa Bệnh nhân và Bác sĩ"""
    __tablename__ = "lich_hen"

    ma_lich_hen = Column(Integer, primary_key=True, autoincrement=True, index=True)
    ma_benh_nhan = Column(Integer, ForeignKey("benh_nhan.ma_benh_nhan"), nullable=False)
    ma_bac_si = Column(Integer, ForeignKey("bac_si.ma_bac_si"), nullable=False)
    ngay_kham = Column(Date, nullable=False)
    gio_kham = Column(Time, nullable=False)

    # 'Pending', 'Confirmed', 'In Progress', 'Completed', 'Cancelled', 'DaDen'
    trang_thai = Column(String(30), nullable=False, default="Pending", index=True)
    ngay_tao = Column(DateTime(timezone=True), default=utc_now)
    ghi_chu = Column(String(255), nullable=True)
    ma_bhyt = Column(String(50), nullable=True)

    # Relationships
    benh_nhan = relationship("BenhNhan", back_populates="lich_hen_list")
    bac_si = relationship("BacSi", back_populates="lich_hen_list")
    lich_hen_dich_vu_list = relationship("LichHenDichVu", back_populates="lich_hen", cascade="all, delete-orphan")
    hoa_don = relationship("HoaDon", back_populates="lich_hen", uselist=False, cascade="all, delete-orphan")
    logs = relationship("LogTrangThai", back_populates="lich_hen", cascade="all, delete-orphan")


class LogTrangThai(Base):
    """Ghi nhận vết audit log mỗi khi trạng thái lịch hẹn bị thay đổi"""
    __tablename__ = "log_trang_thai"

    ma_log = Column(Integer, primary_key=True, autoincrement=True, index=True)
    ma_lich_hen = Column(Integer, ForeignKey("lich_hen.ma_lich_hen", ondelete="CASCADE"), nullable=False)
    trang_thai_cu = Column(String(30), nullable=True)
    trang_thai_moi = Column(String(30), nullable=False)
    thoi_gian = Column(DateTime(timezone=True), default=utc_now)
    nguoi_thuc_hien_id = Column(Integer, ForeignKey("nguoi_dung.user_id"), nullable=True)
    ghi_chu = Column(Text, nullable=True)

    lich_hen = relationship("LichHen", back_populates="logs")
    nguoi_thuc_hien = relationship("NguoiDung")
