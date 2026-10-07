from datetime import datetime
from database import Base
from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship


# 1. BẢNG NGƯỜI DÙNG (Quản lý tập trung mọi tài khoản)
class NguoiDung(Base):
  __tablename__ = "nguoi_dung"

  id = Column(Integer, primary_key=True, autoincrement=True, index=True)
  email = Column(String(255), unique=True, nullable=False, index=True)
  mat_khau = Column(String(255), nullable=False)
  ho_ten = Column(String(100), nullable=False)
  so_dien_thoai = Column(String(20), nullable=True)
  vai_tro = Column(
      String(20), nullable=False, default="benh_nhan"
  )  # 'benh_nhan', 'bac_si', 'le_tan', 'admin'
  status = Column(Integer, default=1)  # 1: Hoạt động, 0: Đã khóa/Ẩn
  created_at = Column(DateTime, default=datetime.utcnow)
  updated_at = Column(
      DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
  )

  __table_args__ = (
      CheckConstraint(
          vai_tro.in_(["benh_nhan", "bac_si", "le_tan", "admin"]),
          name="check_user_role",
      ),
  )

  benh_nhan = relationship(
      "BenhNhan",
      back_populates="nguoi_dung",
      uselist=False,
      cascade="all, delete-orphan",
  )
  bac_si = relationship(
      "BacSi",
      back_populates="nguoi_dung",
      uselist=False,
      cascade="all, delete-orphan",
  )


# 2. BẢNG BỆNH NHÂN
class BenhNhan(Base):
  __tablename__ = "benh_nhan"

  id = Column(Integer, primary_key=True, autoincrement=True)
  nguoi_dung_id = Column(
      Integer,
      ForeignKey("nguoi_dung.id", ondelete="CASCADE"),
      unique=True,
      nullable=False,
  )
  ngay_sinh = Column(Date, nullable=True)
  gioi_tinh = Column(String(10), nullable=True)
  dia_chi = Column(String(255), nullable=True)
  tien_su_benh = Column(Text, nullable=True)

  __table_args__ = (
      CheckConstraint(
          gioi_tinh.in_(["Nam", "Nữ", "Khác"]), name="check_gender"
      ),
  )

  nguoi_dung = relationship("NguoiDung", back_populates="benh_nhan")
  lich_hen_list = relationship("LichHen", back_populates="benh_nhan")


# 3. BẢNG CHUYÊN KHOA
class ChuyenKhoa(Base):
  __tablename__ = "chuyen_khoa"

  id = Column(Integer, primary_key=True, autoincrement=True, index=True)
  ten_chuyen_khoa = Column(String(100), unique=True, nullable=False)
  mo_ta = Column(String(255), nullable=True)

  bac_si_list = relationship("BacSi", back_populates="chuyen_khoa")
  dich_vu_list = relationship(
      "DichVu", back_populates="chuyen_khoa", cascade="all, delete-orphan"
  )
  trieu_chung_list = relationship(
      "TrieuChung", back_populates="chuyen_khoa", cascade="all, delete-orphan"
  )


# 4. BẢNG BÁC SĨ (Kèm Soft Delete, Audit Log, Tag Badge)
class BacSi(Base):
  __tablename__ = "bac_si"

  id = Column(Integer, primary_key=True, autoincrement=True, index=True)
  nguoi_dung_id = Column(
      Integer,
      ForeignKey("nguoi_dung.id", ondelete="CASCADE"),
      unique=True,
      nullable=False,
  )
  chuyen_khoa_id = Column(
      Integer, ForeignKey("chuyen_khoa.id"), nullable=False
  )
  hoc_vi = Column(String(50), nullable=True)  # ThS, TS, CK1...
  kinh_nghiem = Column(Integer, default=0)
  gia_kham = Column(Numeric(12, 2), nullable=False, default=0)
  rating = Column(Float, default=5.0)

  # Soft Delete & Tags
  status = Column(
      Integer, default=1
  )  # 1: Hoạt động, 0: Xóa ẩn (Soft Delete dành cho Admin)
  is_hot = Column(Boolean, default=False)
  is_new = Column(Boolean, default=True)

  # Audit Trail
  created_at = Column(DateTime, default=datetime.utcnow)
  created_by = Column(String(100), nullable=True)
  updated_at = Column(
      DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
  )
  updated_by = Column(String(100), nullable=True)

  __table_args__ = (
      CheckConstraint(
          "rating >= 0.0 AND rating <= 5.0", name="check_doctor_rating"
      ),
  )

  nguoi_dung = relationship("NguoiDung", back_populates="bac_si")
  chuyen_khoa = relationship("ChuyenKhoa", back_populates="bac_si_list")
  variants = relationship(
      "BacSiVariant", back_populates="doctor", cascade="all, delete-orphan"
  )
  lich_lam_viec_list = relationship(
      "LichLamViec", back_populates="bac_si", cascade="all, delete-orphan"
  )
  lich_hen_list = relationship("LichHen", back_populates="bac_si")
  trieu_chung_bac_si_list = relationship(
      "TrieuChungBacSi", back_populates="bac_si"
  )


# 5. BẢNG DỊ BẢN BÁC SĨ (Cơ sở / Chuyên khoa / Giờ phụ)
class BacSiVariant(Base):
  __tablename__ = "bac_si_variant"

  id = Column(Integer, primary_key=True, autoincrement=True, index=True)
  doctor_id = Column(
      Integer,
      ForeignKey("bac_si.id", ondelete="CASCADE"),
      nullable=False,
      index=True,
  )
  sub_department = Column(String(100), nullable=False)  # Chuyên khoa phụ thuộc
  working_hours = Column(String(100), nullable=True)  # Khung giờ khám phụ
  branch_location = Column(String(255), nullable=True)  # Cơ sở khám phụ

  doctor = relationship("BacSi", back_populates="variants")


# 6. BẢNG DỊCH VỤ & GIÁ
class DichVu(Base):
  __tablename__ = "dich_vu"

  id = Column(Integer, primary_key=True, autoincrement=True, index=True)
  chuyen_khoa_id = Column(
      Integer, ForeignKey("chuyen_khoa.id", ondelete="CASCADE"), nullable=False
  )
  ten_dich_vu = Column(String(150), nullable=False)
  gia_tien = Column(Numeric(12, 2), nullable=False)
  mo_ta = Column(String(255), nullable=True)

  __table_args__ = (CheckConstraint("gia_tien >= 0", name="check_service_price"),)

  chuyen_khoa = relationship("ChuyenKhoa", back_populates="dich_vu_list")
  lich_hen_list = relationship("LichHen", back_populates="dich_vu")


# 7. BẢNG LỊCH LÀM VIỆC CỦA BÁC SĨ
class LichLamViec(Base):
  __tablename__ = "lich_lam_viec"

  id = Column(Integer, primary_key=True, autoincrement=True)
  bac_si_id = Column(
      Integer, ForeignKey("bac_si.id", ondelete="CASCADE"), nullable=False
  )
  ngay_kham = Column(Date, nullable=False)
  khung_gio = Column(String(50), nullable=False)
  trang_thai_trong = Column(Boolean, default=True)

  __table_args__ = (
      UniqueConstraint(
          "bac_si_id", "ngay_kham", "khung_gio", name="UQ_LichLamViec"
      ),
  )

  bac_si = relationship("BacSi", back_populates="lich_lam_viec_list")


# 8. BẢNG LỊCH HẸN KHÁM
class LichHen(Base):
  __tablename__ = "lich_hen"

  id = Column(Integer, primary_key=True, autoincrement=True, index=True)
  benh_nhan_id = Column(Integer, ForeignKey("benh_nhan.id"), nullable=False)
  bac_si_id = Column(Integer, ForeignKey("bac_si.id"), nullable=False)
  dich_vu_id = Column(Integer, ForeignKey("dich_vu.id"), nullable=False)
  ngay_kham = Column(Date, nullable=False)
  khung_gio = Column(String(50), nullable=False)
  trang_thai = Column(
      String(30), default="cho_xac_nhan"
  )  # cho_xac_nhan, da_xac_nhan, dang_kham, can_tai_kham, hoan_thanh, da_huy
  created_at = Column(DateTime, default=datetime.utcnow)

  __table_args__ = (
      CheckConstraint(
          trang_thai.in_([
              "cho_xac_nhan",
              "da_xac_nhan",
              "dang_kham",
              "can_tai_kham",
              "hoan_thanh",
              "da_huy",
          ]),
          name="check_appointment_status",
      ),
  )

  benh_nhan = relationship("BenhNhan", back_populates="lich_hen_list")
  bac_si = relationship("BacSi", back_populates="lich_hen_list")
  dich_vu = relationship("DichVu", back_populates="lich_hen_list")
  thanh_toan = relationship(
      "ThanhToan",
      back_populates="lich_hen",
      uselist=False,
      cascade="all, delete-orphan",
  )
  log_trang_thai_list = relationship(
      "LogTrangThai", back_populates="lich_hen", cascade="all, delete-orphan"
  )


# 9. BẢNG THANH TOÁN
class ThanhToan(Base):
  __tablename__ = "thanh_toan"

  id = Column(Integer, primary_key=True, autoincrement=True)
  lich_hen_id = Column(
      Integer,
      ForeignKey("lich_hen.id", ondelete="CASCADE"),
      unique=True,
      nullable=False,
  )
  so_tien = Column(Numeric(12, 2), nullable=False)
  phuong_thuc = Column(String(50), default="chuyen_khoan")
  trang_thai = Column(String(30), default="chua_thanh_toan")
  created_at = Column(DateTime, default=datetime.utcnow)

  __table_args__ = (
      CheckConstraint("so_tien >= 0", name="check_payment_amount"),
      CheckConstraint(
          trang_thai.in_(["chua_thanh_toan", "da_thanh_toan", "that_bai"]),
          name="check_payment_status",
      ),
  )

  lich_hen = relationship("LichHen", back_populates="thanh_toan")


# 10. BẢNG LOG TRẠNG THÁI LỊCH HẸN
class LogTrangThai(Base):
  __tablename__ = "log_trang_thai"

  id = Column(Integer, primary_key=True, autoincrement=True)
  lich_hen_id = Column(
      Integer, ForeignKey("lich_hen.id", ondelete="CASCADE"), nullable=False
  )
  trang_thai_cu = Column(String(30), nullable=True)
  trang_thai_moi = Column(String(30), nullable=False)
  thoi_gian = Column(DateTime, default=datetime.utcnow)

  lich_hen = relationship("LichHen", back_populates="log_trang_thai_list")


# 11. BẢNG TRIỆU CHỨNG & MAPPING GỢI Ý BÁC SĨ
class TrieuChung(Base):
  __tablename__ = "trieu_chung"

  id = Column(Integer, primary_key=True, autoincrement=True)
  ten_trieu_chung = Column(String(150), unique=True, nullable=False)
  chuyen_khoa_id = Column(
      Integer, ForeignKey("chuyen_khoa.id", ondelete="CASCADE"), nullable=False
  )

  chuyen_khoa = relationship("ChuyenKhoa", back_populates="trieu_chung_list")
  trieu_chung_bac_si_list = relationship(
      "TrieuChungBacSi",
      back_populates="trieu_chung",
      cascade="all, delete-orphan",
  )


class TrieuChungBacSi(Base):
  __tablename__ = "trieu_chung_bac_si"

  id = Column(Integer, primary_key=True, autoincrement=True)
  trieu_chung_id = Column(
      Integer,
      ForeignKey("trieu_chung.id", ondelete="CASCADE"),
      nullable=False,
  )
  bac_si_id = Column(Integer, ForeignKey("bac_si.id"), nullable=False)

  __table_args__ = (
      UniqueConstraint(
          "trieu_chung_id", "bac_si_id", name="UQ_TrieuChungBacSi"
      ),
  )

  trieu_chung = relationship(
      "TrieuChung", back_populates="trieu_chung_bac_si_list"
  )
  bac_si = relationship("BacSi", back_populates="trieu_chung_bac_si_list")
