from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Numeric, Float, 
    Boolean, DateTime, ForeignKey, Text
)
from sqlalchemy.orm import relationship

# Import Base và engine (tự động nhận diện dù chạy đơn lẻ hay theo module)
try:
    from app.database.database import Base, engine
except ImportError:
    from database import Base, engine


class NguoiDung(Base):
    __tablename__ = "nguoi_dung"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    mat_khau = Column(String(255), nullable=False)
    ho_ten = Column(String(100), nullable=False)
    so_dien_thoai = Column(String(20), nullable=True)
    vai_tro = Column(String(20), nullable=False, default="benh_nhan")  # 'benh_nhan', 'bac_si', 'le_tan', 'admin'
    trang_thai = Column(Boolean, default=True)  # True: 1 (Hoạt động), False: 0 (Đã ẩn / Soft Deleted)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(Integer, nullable=True)
    updated_by = Column(Integer, nullable=True)

    # Quan hệ 1-1 với BacSi
    bac_si = relationship("BacSi", back_populates="nguoi_dung", uselist=False, cascade="all, delete-orphan")


class ChuyenKhoa(Base):
    __tablename__ = "chuyen_khoa"

    ma_chuyen_khoa = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ten_chuyen_khoa = Column(String(100), nullable=False)
    mo_ta = Column(String(255), nullable=True)

    bac_si_list = relationship("BacSi", back_populates="chuyen_khoa")


class BacSi(Base):
    __tablename__ = "bac_si"

    # MaBacSi là PK kiêm FK tham chiếu trực tiếp đến NguoiDung.user_id
    ma_bac_si = Column(Integer, ForeignKey("nguoi_dung.user_id", ondelete="CASCADE"), primary_key=True)
    ma_chuyen_khoa = Column(Integer, ForeignKey("chuyen_khoa.ma_chuyen_khoa"), nullable=False)
    hoc_vi = Column(String(50), nullable=True)
    kinh_nghiem = Column(Integer, default=0)
    gia_kham = Column(Numeric(18, 2), nullable=False, default=0.0)
    rating = Column(Float, default=5.0)
    so_luot_dat = Column(Integer, default=0)

    # Relationships
    nguoi_dung = relationship("NguoiDung", back_populates="bac_si")
    chuyen_khoa = relationship("ChuyenKhoa", back_populates="bac_si_list")
    di_ban_list = relationship("BacSiDiBan", back_populates="bac_si", cascade="all, delete-orphan")
    lich_hen_list = relationship("LichHen", back_populates="bac_si")


class BacSiDiBan(Base):
    """
    Bảng lưu các dị bản/thuộc tính phụ thuộc của Bác sĩ:
    Chi nhánh làm việc, khung giờ phụ, chuyên khoa phụ (phụ thuộc vào ma_bac_si).
    """
    __tablename__ = "bac_si_di_ban"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ma_bac_si = Column(Integer, ForeignKey("bac_si.ma_bac_si", ondelete="CASCADE"), nullable=False)
    ten_chi_nhanh_co_so = Column(String(255), nullable=False)
    chuyen_khoa_phu = Column(String(100), nullable=True)
    khung_gio_phu = Column(String(100), nullable=True)
    dia_chi = Column(String(255), nullable=True)

    bac_si = relationship("BacSi", back_populates="di_ban_list")


class LichHen(Base):
    __tablename__ = "lich_hen"

    ma_lich_hen = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ma_benh_nhan = Column(Integer, nullable=False)
    ma_bac_si = Column(Integer, ForeignKey("bac_si.ma_bac_si"), nullable=False)
    ngay_kham = Column(String(50), nullable=False)
    gio_kham = Column(String(50), nullable=False)
    trang_thai = Column(String(30), default="Pending")  # Pending, Confirmed, Completed, Cancelled, In Progress, DaDen
    created_at = Column(DateTime, default=datetime.utcnow)

    bac_si = relationship("BacSi", back_populates="lich_hen_list")


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print(">>> [SUCCESS] Đồng bộ toàn bộ các bảng vào Database thành công!")
