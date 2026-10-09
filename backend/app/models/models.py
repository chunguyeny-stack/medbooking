from datetime import datetime, timezone
from sqlalchemy import (
    Column, Integer, String, Numeric,
    Date, DateTime, SmallInteger, ForeignKey
)
from sqlalchemy.orm import relationship
from datadase.database import Base


def utc_now():
    """Hàm lấy mốc thời gian UTC chuẩn cho Python 3.12+"""
    return datetime.now(timezone.utc)


class NguoiDung(Base):
    __tablename__ = "nguoi_dung"

    user_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    mat_khau = Column(String(255), nullable=False)
    ho_ten = Column(String(100), nullable=False)
    so_dien_thoai = Column(String(20), nullable=True)
    vai_tro = Column(String(20), nullable=False, default="benh_nhan")
    trang_thai = Column(SmallInteger, default=1)

    # Relationships
    benh_nhan_profile = relationship(
        "BenhNhan",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )
    bac_si_profile = relationship(
        "BacSi",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )


class BenhNhan(Base):
    __tablename__ = "benh_nhan"

    ma_benh_nhan = Column(
        Integer,
        ForeignKey("nguoi_dung.user_id", ondelete="CASCADE"),
        primary_key=True
    )
    ngay_sinh = Column(Date, nullable=True)
    gioi_tinh = Column(String(10), nullable=True)
    dia_chi = Column(String(255), nullable=True)
    tien_su_benh = Column(String(500), nullable=True)

    # Relationships
    user = relationship(
        "NguoiDung",
        foreign_keys="[BenhNhan.ma_benh_nhan]",
        back_populates="benh_nhan_profile"
    )
    lich_hen_list = relationship(
        "LichHen",
        back_populates="benh_nhan",
        cascade="all, delete-orphan"
    )


class ChuyenKhoa(Base):
    __tablename__ = "chuyen_khoa"

    ma_chuyen_khoa = Column(Integer, primary_key=True, autoincrement=True, index=True)
    ten_chuyen_khoa = Column(String(100), nullable=False)
    mo_ta = Column(String(255), nullable=True)

    # Relationships
    bac_si_list = relationship(
        "BacSi",
        back_populates="chuyen_khoa"
    )
    mappings = relationship(
        "MappingTrieuChung",
        back_populates="chuyen_khoa"
    )


class DichVu(Base):
    __tablename__ = "dich_vu"

    ma_dich_vu = Column(Integer, primary_key=True, autoincrement=True, index=True)
    ten_dich_vu = Column(String(100), nullable=False)
    gia_dich_vu = Column(Numeric(18, 2), nullable=False, default=0.0)
    mo_ta = Column(String(255), nullable=True)

    # Relationships
    bac_si_dich_vu_list = relationship(
        "BacSiDichVu",
        back_populates="dich_vu",
        cascade="all, delete-orphan"
    )
    lich_hen_dich_vu_list = relationship(
        "LichHenDichVu",
        back_populates="dich_vu",
        cascade="all, delete-orphan"
    )


class BacSiDichVu(Base):
    """Bảng trung gian N-N giữa Bác sĩ và Dịch vụ"""
    __tablename__ = "bac_si_dich_vu"

    ma_bac_si = Column(
        Integer,
        ForeignKey("bac_si.ma_bac_si", ondelete="CASCADE"),
        primary_key=True
    )
    ma_dich_vu = Column(
        Integer,
        ForeignKey("dich_vu.ma_dich_vu", ondelete="CASCADE"),
        primary_key=True
    )
    ghi_chu = Column(String(255), nullable=True)

    # Relationships
    bac_si = relationship(
        "BacSi",
        foreign_keys="[BacSiDichVu.ma_bac_si]",
        back_populates="bac_si_dich_vu_list"
    )
    dich_vu = relationship(
        "DichVu",
        foreign_keys="[BacSiDichVu.ma_dich_vu]",
        back_populates="bac_si_dich_vu_list"
    )


class LichHenDichVu(Base):
    """Bảng trung gian N-N lưu dịch vụ sử dụng trong từng ca khám"""
    __tablename__ = "lich_hen_dich_vu"

    ma_lich_hen = Column(
        Integer,
        ForeignKey("lich_hen.ma_lich_hen", ondelete="CASCADE"),
        primary_key=True
    )
    ma_dich_vu = Column(
        Integer,
        ForeignKey("dich_vu.ma_dich_vu", ondelete="CASCADE"),
        primary_key=True
    )
    so_luong = Column(Integer, default=1, nullable=False)
    thanh_tien = Column(Numeric(18, 2), nullable=False, default=0.0)

    # Relationships
    lich_hen = relationship(
        "LichHen",
        foreign_keys="[LichHenDichVu.ma_lich_hen]",
        back_populates="lich_hen_dich_vu_list"
    )
    dich_vu = relationship(
        "DichVu",
        foreign_keys="[LichHenDichVu.ma_dich_vu]",
        back_populates="lich_hen_dich_vu_list"
    )


class HoaDon(Base):
    """Bảng hóa đơn (quan hệ 1-1 với LichHen)"""
    __tablename__ = "hoa_don"

    ma_hoa_don = Column(Integer, primary_key=True, autoincrement=True, index=True)
    ma_lich_hen = Column(
        Integer,
        ForeignKey("lich_hen.ma_lich_hen", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )
    tong_tien = Column(Numeric(18, 2), nullable=False, default=0.0)
    ngay_thanh_toan = Column(DateTime(timezone=True), nullable=True)
    phuong_thuc = Column(String(50), nullable=True)
    trang_thai = Column(String(20), default="Chua Thanh Toan")

    # Relationships
    lich_hen = relationship(
        "LichHen",
        foreign_keys="[HoaDon.ma_lich_hen]",
        back_populates="hoa_don"
    )


class MappingTrieuChung(Base):
    """Ánh xạ gợi ý Bác sĩ / Chuyên khoa từ triệu chứng"""
    __tablename__ = "mapping_trieu_chung"

    ma_mapping = Column(Integer, primary_key=True, autoincrement=True, index=True)
    trieu_chung = Column(String(255), nullable=False, index=True)
    ma_bac_si = Column(
        Integer,
        ForeignKey("bac_si.ma_bac_si", ondelete="SET NULL"),
        nullable=True
    )
    ma_chuyen_khoa = Column(
        Integer,
        ForeignKey("chuyen_khoa.ma_chuyen_khoa", ondelete="SET NULL"),
        nullable=True
    )

    # Relationships
    bac_si = relationship(
        "BacSi",
        foreign_keys="[MappingTrieuChung.ma_bac_si]",
        back_populates="mapping_trieu_chung_list"
    )
    chuyen_khoa = relationship(
        "ChuyenKhoa",
        foreign_keys="[MappingTrieuChung.ma_chuyen_khoa]",
        back_populates="mappings"
    )
