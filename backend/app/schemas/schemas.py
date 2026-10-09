from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


# ==================== NGƯỜI DÙNG (USER) ====================
class NguoiDungBase(BaseModel):
    email: EmailStr
    ho_ten: str = Field(..., min_length=2, max_length=100)
    so_dien_thoai: Optional[str] = Field(None, max_length=20)
    vai_tro: str = Field(default="benh_nhan")
    trang_thai: int = Field(default=1)


class NguoiDungCreate(NguoiDungBase):
    mat_khau: str = Field(..., min_length=8)


class NguoiDungUpdate(BaseModel):
    ho_ten: Optional[str] = Field(None, min_length=2, max_length=100)
    so_dien_thoai: Optional[str] = None
    trang_thai: Optional[int] = None


class NguoiDungResponse(NguoiDungBase):
    user_id: int

    class Config:
        from_attributes = True


# ==================== BỆNH NHÂN ====================
class BenhNhanBase(BaseModel):
    ngay_sinh: Optional[date] = None
    gioi_tinh: Optional[str] = None
    dia_chi: Optional[str] = None
    tien_su_benh: Optional[str] = None


class BenhNhanCreate(BenhNhanBase):
    ma_benh_nhan: int


class BenhNhanUpdate(BenhNhanBase):
    pass


class BenhNhanResponse(BenhNhanBase):
    ma_benh_nhan: int
    user: Optional[NguoiDungResponse] = None

    class Config:
        from_attributes = True


# ==================== CHUYÊN KHOA ====================
class ChuyenKhoaBase(BaseModel):
    ten_chuyen_khoa: str = Field(..., min_length=2, max_length=100)
    mo_ta: Optional[str] = None


class ChuyenKhoaCreate(ChuyenKhoaBase):
    pass


class ChuyenKhoaUpdate(BaseModel):
    ten_chuyen_khoa: Optional[str] = None
    mo_ta: Optional[str] = None


class ChuyenKhoaResponse(ChuyenKhoaBase):
    ma_chuyen_khoa: int

    class Config:
        from_attributes = True


# ==================== DỊCH VỤ ====================
class DichVuBase(BaseModel):
    ten_dich_vu: str = Field(..., min_length=2, max_length=100)
    gia_dich_vu: Decimal = Field(..., ge=0)
    mo_ta: Optional[str] = None


class DichVuCreate(DichVuBase):
    pass


class DichVuUpdate(BaseModel):
    ten_dich_vu: Optional[str] = None
    gia_dich_vu: Optional[Decimal] = Field(None, ge=0)
    mo_ta: Optional[str] = None


class DichVuResponse(DichVuBase):
    ma_dich_vu: int

    class Config:
        from_attributes = True


# ==================== HÓA ĐƠN ====================
class HoaDonBase(BaseModel):
    ma_lich_hen: int
    tong_tien: Decimal = Field(..., ge=0)
    phuong_thuc: Optional[str] = None
    trang_thai: str = "Chua Thanh Toan"


class HoaDonCreate(HoaDonBase):
    pass


class HoaDonResponse(HoaDonBase):
    ma_hoa_don: int
    ngay_thanh_toan: Optional[datetime] = None

    class Config:
        from_attributes = True
