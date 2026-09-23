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

class NguoiDung(Base):
    __tablename__ = 'nguoi_dung'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    mat_khau = Column(String(255), nullable=False)
    ho_ten = Column(String(100), nullable=False)
    so_dien_thoai = Column(String(20))
    vai_tro = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    __table_args__ = (
        CheckConstraint(vai_tro.in_(['benh_nhan', 'bac_si', 'le_tan', 'admin'])),
    )
    benh_nhan = relationship("BenhNhan", back_populates="nguoi_dung", uselist=False, cascade="all, delete")
    bac_si = relationship("BacSi", back_populates="nguoi_dung", uselist=False, cascade="all, delete")

class BenhNhan(Base):
    __tablename__ = 'benh_nhan'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nguoi_dung_id = Column(Integer, ForeignKey('nguoi_dung.id', ondelete='CASCADE'), unique=True, nullable=False)
    ngay_sinh = Column(Date)
    gioi_tinh = Column(String(10))
    dia_chi = Column(String)

    __table_args__ = (
        CheckConstraint(gioi_tinh.in_(['Nam', 'Nữ', 'Khác'])),
    )
    nguoi_dung = relationship("NguoiDung", back_populates="benh_nhan")
    lich_hen_list = relationship("LichHen", back_populates="benh_nhan")

class ChuyenKhoa(Base):
    __tablename__ = 'chuyen_khoa'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ten_chuyen_khoa = Column(String(100), unique=True, nullable=False)
    mo_ta = Column(String)
    bac_si_list = relationship("BacSi", back_populates="chuyen_khoa")
    dich_vu_list = relationship("DichVu", back_populates="chuyen_khoa", cascade="all, delete")
    trieu_chung_list = relationship("TrieuChung", back_populates="chuyen_khoa", cascade="all, delete")

class BacSi(Base):
    __tablename__ = 'bac_si'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nguoi_dung_id = Column(Integer, ForeignKey('nguoi_dung.id', ondelete='CASCADE'), unique=True, nullable=False)
    chuyen_khoa_id = Column(Integer, ForeignKey('chuyen_khoa.id'), nullable=False)
    mo_ta = Column(String)
    rating = Column(Numeric(2, 1), default=5.0)

    __table_args__ = (
        CheckConstraint('rating >= 0.0 AND rating <= 5.0'),
    )
    nguoi_dung = relationship("NguoiDung", back_populates="bac_si")
    chuyen_khoa = relationship("ChuyenKhoa", back_populates="bac_si_list")
    lich_lam_viec_list = relationship("LichLamViec", back_populates="bac_si", cascade="all, delete")
    lich_hen_list = relationship("LichHen", back_populates="bac_si")
    trieu_chung_bac_si_list = relationship("TrieuChungBacSi", back_populates="bac_si")

class DichVu(Base):
    __tablename__ = 'dich_vu'

    id = Column(Integer, primary_key=True, autoincrement=True)
    chuyen_khoa_id = Column(Integer, ForeignKey('chuyen_khoa.id', ondelete='CASCADE'), nullable=False)
    ten_dich_vu = Column(String(150), nullable=False)
    gia_tien = Column(Numeric(12, 2), nullable=False)
    mo_ta = Column(String)

    __table_args__ = (
        CheckConstraint('gia_tien >= 0'),
    )
    chuyen_khoa = relationship("ChuyenKhoa", back_populates="dich_vu_list")
    lich_hen_list = relationship("LichHen", back_populates="dich_vu")

class LichLamViec(Base):
    __tablename__ = 'lich_lam_viec'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    bac_si_id = Column(Integer, ForeignKey('bac_si.id', ondelete='CASCADE'), nullable=False)
    ngay_kham = Column(Date, nullable=False)
    khung_gio = Column(String(50), nullable=False)
    trang_thai_trong = Column(Boolean, default=True)

    __table_args__ = (
        UniqueConstraint('bac_si_id', 'ngay_kham', 'khung_gio', name='UQ_LichLamViec'),
    )
    bac_si = relationship("BacSi", back_populates="lich_lam_viec_list")

class LichHen(Base):
    __tablename__ = 'lich_hen'

    id = Column(Integer, primary_key=True, autoincrement=True)
    benh_nhan_id = Column(Integer, ForeignKey('benh_nhan.id'), nullable=False)
    bac_si_id = Column(Integer, ForeignKey('bac_si.id'), nullable=False)
    dich_vu_id = Column(Integer, ForeignKey('dich_vu.id'), nullable=False)
    ngay_kham = Column(Date, nullable=False)
    khung_gio = Column(String(50), nullable=False)
    trang_thai = Column(String(30), default='cho_xac_nhan')
    created_at = Column(DateTime, default=datetime.now)
    
    __table_args__ = (
        CheckConstraint(trang_thai.in_([
            'cho_xac_nhan', 'da_xac_nhan', 'dang_kham',
            'can_tai_kham', 'hoan_thanh', 'da_huy'
        ])),
    )
    benh_nhan = relationship("BenhNhan", back_populates="lich_hen_list")
    bac_si = relationship("BacSi", back_populates="lich_hen_list")
    dich_vu = relationship("DichVu", back_populates="lich_hen_list")
    thanh_toan = relationship("ThanhToan", back_populates="lich_hen", uselist=False, cascade="all, delete")
    log_trang_thai_list = relationship("LogTrangThai", back_populates="lich_hen", cascade="all, delete")
    
class ThanhToan(Base):
    __tablename__ = 'thanh_toan'
    id = Column(Integer, primary_key=True, autoincrement=True)
    lich_hen_id = Column(Integer, ForeignKey('lich_hen.id', ondelete='CASCADE'), unique=True, nullable=False)
    so_tien = Column(Numeric(12, 2), nullable=False)
    phuong_thuc = Column(String(50), default='chuyen_khoan')
    trang_thai = Column(String(30), default='chua_thanh_toan')
    created_at = Column(DateTime, default=datetime.now)
    __table_args__ = (
        CheckConstraint('so_tien >= 0'),
        CheckConstraint(trang_thai.in_(['chua_thanh_toan', 'da_thanh_toan', 'that_bai'])),
    )
    lich_hen = relationship("LichHen", back_populates="thanh_toan")
    
class LogTrangThai(Base):
    __tablename__ = 'log_trang_thai'
    id = Column(Integer, primary_key=True, autoincrement=True)
    lich_hen_id = Column(Integer, ForeignKey('lich_hen.id', ondelete='CASCADE'), nullable=False)
    trang_thai_cu = Column(String(30))
    trang_thai_moi = Column(String(30), nullable=False)
    thoi_gian = Column(DateTime, default=datetime.now)

    lich_hen = relationship("LichHen", back_populates="log_trang_thai_list")

class TrieuChung(Base):
    __tablename__ = 'trieu_chung'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ten_trieu_chung = Column(String(150), unique=True, nullable=False)
    chuyen_khoa_id = Column(Integer, ForeignKey('chuyen_khoa.id', ondelete='CASCADE'), nullable=False)
    chuyen_khoa = relationship("ChuyenKhoa", back_populates="trieu_chung_list")
    trieu_chung_bac_si_list = relationship("TrieuChungBacSi", back_populates="trieu_chung", cascade="all, delete")

class TrieuChungBacSi(Base):
    __tablename__ = 'trieu_chung_bac_si'
    id = Column(Integer, primary_key=True, autoincrement=True)
    trieu_chung_id = Column(Integer, ForeignKey('trieu_chung.id', ondelete='CASCADE'), nullable=False)
    bac_si_id = Column(Integer, ForeignKey('bac_si.id'), nullable=False)
    __table_args__ = (
        UniqueConstraint('trieu_chung_id', 'bac_si_id', name='UQ_TrieuChungBacSi'),
    )
    trieu_chung = relationship("TrieuChung", back_populates="trieu_chung_bac_si_list")
    bac_si = relationship("BacSi", back_populates="trieu_chung_bac_si_list")
    
