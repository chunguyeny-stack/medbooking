from pydantic import BaseModel, EmailStr
from datetime import datetime, date
from typing import Optional

class UserRegister(BaseModel):
    email: EmailStr
    mat_khau: str
    ho_ten: str
    so_dien_thoai: Optional[str] = None
    vai_tro: str = "benh_nhan"
    ngay_sinh: Optional[date] = None
    gioi_tinh: Optional[str] = None
    dia_chi: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class UserResponse(BaseModel):
    id: int
    email: str
    ho_ten: str
    so_dien_thoai: Optional[str] = None
    vai_tro: str
    ngay_tao: datetime

    class Config:
        from_attributes = True