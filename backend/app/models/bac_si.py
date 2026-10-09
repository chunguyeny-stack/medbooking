from datetime import datetime, timezone
from sqlalchemy import (
    Column, Integer, String, Numeric, Float,
    ForeignKey, DateTime, SmallInteger
)
from sqlalchemy.orm import relationship
from datadase.database import Base


def utc_now():
    """Hàm lấy thời gian UTC chuẩn, tương thích hoàn toàn Python 3.12+"""
    return datetime.now(timezone.utc)


class BacSi(Base):
    __tablename__ = "bac_si"

    # MaBacSi vừa là PK vừa là FK trỏ tới bảng nguoi_dung.user_id
    ma_bac_si = Column(
        Integer,
        ForeignKey("nguoi_dung.user_id", ondelete="CASCADE"),
        primary_key=True
    )
    ma_chuyen_khoa = Column(
        Integer,
        ForeignKey("chuyen_khoa.ma_chuyen_khoa"),
        nullable=False
    )
    hoc_vi = Column(String(50), nullable=True)
    kinh_nghiem = Column(Integer, default=0)
    gia_kham = Column(Numeric(18, 2), nullable=False, default=0.0)
    rating = Column(Float, default=0.0)
    status = Column(SmallInteger, default=1, index=True)  # 1: Hoạt động, 0: Ẩn (Soft-delete)

    # Audit log (Dùng default=utc_now thay cho utcnow cũ để triệt tiêu cảnh báo deprecated)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    created_by = Column(Integer, ForeignKey("nguoi_dung.user_id"), nullable=True)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)
    updated_by = Column(Integer, ForeignKey("nguoi_dung.user_id"), nullable=True)

    # Relationships (Định nghĩa foreign_keys dạng string/sequence đúng type hint của SQLAlchemy)
    user = relationship(
        "NguoiDung",
        foreign_keys="[BacSi.ma_bac_si]",
        back_populates="bac_si_profile"
    )
    creator = relationship(
        "NguoiDung",
        foreign_keys="[BacSi.created_by]"
    )
    updater = relationship(
        "NguoiDung",
        foreign_keys="[BacSi.updated_by]"
    )
    chuyen_khoa = relationship(
        "ChuyenKhoa",
        foreign_keys="[BacSi.ma_chuyen_khoa]",
        back_populates="bac_si_list"
    )

    # Dị bản phụ thuộc: chi nhánh, cơ sở làm việc, chuyên khoa phụ
    variants = relationship(
        "BacSiVariant",
        back_populates="bac_si",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    lich_hen_list = relationship(
        "LichHen",
        back_populates="bac_si"
    )


class BacSiVariant(Base):
    """
    Bảng lưu các dị bản/thuộc tính phụ thuộc vào ID của BS gốc
    """
    __tablename__ = "bac_si_variants"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    ma_bac_si = Column(
        Integer,
        ForeignKey("bac_si.ma_bac_si", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    ten_co_so = Column(String(255), nullable=True)
    dia_chi_co_so = Column(String(255), nullable=True)
    chuyen_khoa_phu = Column(String(150), nullable=True)
    khung_gio_phu = Column(String(100), nullable=True)

    bac_si = relationship(
        "BacSi",
        foreign_keys="[BacSiVariant.ma_bac_si]",
        back_populates="variants"
    )
