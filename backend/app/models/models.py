from datetime import datetime

from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import relationship

from database import Base


class NguoiDung(Base):
    __tablename__ = "nguoi_dung"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    mat_khau = Column(String(255), nullable=False)
    ho_ten = Column(String(100), nullable=False)
    so_dien_thoai = Column(String(20), nullable=True)
    vai_tro = Column(String(20), nullable=False)  # 'benh_nhan', 'bac_si', 'le_tan', 'admin'
    trang_thai = Column(Boolean, default=True)  # True: Active, False: Blocked
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(Integer, nullable=True)
    updated_by = Column(Integer, nullable=True)

    bac_si = relationship("BacSi", uselist=False, back_populates="nguoi_dung")
    benh_nhan = relationship("BenhNhan", uselist=False, back_populates="nguoi_dung")


class BenhNhan(Base):
    __tablename__ = "benh_nhan"

    ma_benh_nhan = Column(Integer, ForeignKey("nguoi_dung.user_id"), primary_key=True)
    ngay_sinh = Column(Date, nullable=True)
    gioi_tinh = Column(String(10), nullable=True)
    dia_chi = Column(String(255), nullable=True)
    tien_su_benh = Column(Text, nullable=True)

    nguoi_dung = relationship("NguoiDung", back_populates="benh_nhan")
    lich_hen_list = relationship("LichHen", back_populates="benh_nhan")


class ChuyenKhoa(Base):
    __tablename__ = "chuyen_khoa"

    ma_chuyen_khoa = Column(Integer, primary_key=True, autoincrement=True)
    ten_chuyen_khoa = Column(String(100), nullable=False)
    mo_ta = Column(String(255), nullable=True)

    bac_si_list = relationship("BacSi", back_populates="chuyen_khoa")


class BacSi(Base):
    __tablename__ = "bac_si"

    ma_bac_si = Column(Integer, ForeignKey("nguoi_dung.user_id"), primary_key=True)
    ma_chuyen_khoa = Column(Integer, ForeignKey("chuyen_khoa.ma_chuyen_khoa"), nullable=False)
    hoc_vi = Column(String(100), nullable=True, default="Bác sĩ Chuyên khoa")
    kinh_nghiem = Column(Integer, nullable=False, default=0)
    gia_kham = Column(Numeric(18, 2), nullable=False, default=0)
    rating = Column(Numeric(3, 2), nullable=False, default=5.0)
    so_luot_dat = Column(Integer, nullable=False, default=0)

    nguoi_dung = relationship("NguoiDung", back_populates="bac_si")
    chuyen_khoa = relationship("ChuyenKhoa", back_populates="bac_si_list")
    di_ban_list = relationship("BacSiDiBan", back_populates="bac_si", cascade="all, delete-orphan")
    lich_hen_list = relationship("LichHen", back_populates="bac_si")


class BacSiDiBan(Base):
    __tablename__ = "bac_si_di_ban"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ma_bac_si = Column(Integer, ForeignKey("bac_si.ma_bac_si"), nullable=False)
    ten_chi_nhanh_co_so = Column(String(255), nullable=False)
    chuyen_khoa_phu = Column(String(100), nullable=True)
    khung_gio_phu = Column(String(100), nullable=True)
    dia_chi = Column(String(255), nullable=True)

    bac_si = relationship("BacSi", back_populates="di_ban_list")


class LichHen(Base):
    __tablename__ = "lich_hen"

    ma_lich_hen = Column(Integer, primary_key=True, autoincrement=True)
    ma_benh_nhan = Column(Integer, ForeignKey("benh_nhan.ma_benh_nhan"), nullable=False)
    ma_bac_si = Column(Integer, ForeignKey("bac_si.ma_bac_si"), nullable=False)
    ngay_kham = Column(Date, nullable=False)
    gio_kham = Column(String(20), nullable=True)
    trang_thai = Column(String(50), default="Pending")
    ghi_chu = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    benh_nhan = relationship("BenhNhan", back_populates="lich_hen_list")
    bac_si = relationship("BacSi", back_populates="lich_hen_list")


class DichVu(Base):
    __tablename__ = "dich_vu"

    ma_dich_vu = Column(Integer, primary_key=True, autoincrement=True)
    ten_dich_vu = Column(String(100), nullable=False)
    gia_dich_vu = Column(Numeric(18, 2), nullable=False)
    mo_ta = Column(String(255), nullable=True)


class HoaDon(Base):
    __tablename__ = "hoa_don"

    ma_hoa_don = Column(Integer, primary_key=True, autoincrement=True)
    ma_lich_hen = Column(Integer, ForeignKey("lich_hen.ma_lich_hen"), unique=True, nullable=False)
    tong_tien = Column(Numeric(18, 2), nullable=False)
    ngay_thanh_toan = Column(DateTime, nullable=True)
    phuong_thuc = Column(String(50), nullable=True)
    trang_thai = Column(String(20), default="Chua Thanh Toan")
