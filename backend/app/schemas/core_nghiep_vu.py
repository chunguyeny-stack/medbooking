from datetime import date, time
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


# --- Core Schemas ---
class UserRegisterRequest(BaseModel):
    email: EmailStr
    mat_khau: str = Field(min_length=6, description="Mật khẩu ít nhất 6 ký tự")
    ho_ten: str
    so_dien_thoai: Optional[str] = None
    vai_tro: str = Field(default="benh_nhan", description="benh_nhan, bac_si, le_tan, admin")


class UserLoginRequest(BaseModel):
    email: EmailStr
    mat_khau: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    ho_ten: str
    vai_tro: str


# --- Nghiệp vụ Schemas ---
class BookingCreateRequest(BaseModel):
    ma_bac_si: int
    ngay_kham: date
    gio_kham: time
    ghi_chu: Optional[str] = None


class UpdateTrangThaiRequest(BaseModel):
    trang_thai_moi: str = Field(description="Pending, Confirmed, DaDen, In Progress, Completed, Cancelled")
    ghi_chu: Optional[str] = None


class ThanhToanRequest(BaseModel):
    phuong_thuc: str = Field(default="TienMat", description="TienMat, ChuyenKhoan, The")
    ghi_chu: Optional[str] = None
