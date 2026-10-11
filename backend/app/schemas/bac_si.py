from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field


# --- Dị bản (Variants / Chi nhánh / Chuyên khoa phụ) ---
class BacSiVariantBase(BaseModel):
    ten_co_so: Optional[str] = None
    dia_chi_co_so: Optional[str] = None
    chuyen_khoa_phu: Optional[str] = None
    khung_gio_phu: Optional[str] = None


class BacSiVariantCreate(BacSiVariantBase):
    pass


class BacSiVariantResponse(BacSiVariantBase):
    id: int
    ma_bac_si: int

    class Config:
        from_attributes = True


# --- Tạo mới / Cập nhật Bác sĩ ---
class BacSiCreate(BaseModel):
    ho_ten: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    so_dien_thoai: Optional[str] = Field(None, max_length=20)
    mat_khau: str = Field(..., min_length=8)
    ma_chuyen_khoa: int
    hoc_vi: Optional[str] = Field(None, max_length=50)
    kinh_nghiem: int = Field(0, ge=0)
    gia_kham: Decimal = Field(..., ge=0)
    variants: Optional[List[BacSiVariantCreate]] = []


class BacSiUpdate(BaseModel):
    ho_ten: Optional[str] = Field(None, min_length=2, max_length=100)
    so_dien_thoai: Optional[str] = None
    ma_chuyen_khoa: Optional[int] = None
    hoc_vi: Optional[str] = None
    kinh_nghiem: Optional[int] = Field(None, ge=0)
    gia_kham: Optional[Decimal] = Field(None, ge=0)
    status: Optional[int] = Field(None, description="1: Active, 0: Soft-deleted/Ẩn")
    variants: Optional[List[BacSiVariantCreate]] = None


# --- Output trả về client ---
class BacSiResponse(BaseModel):
    ma_bac_si: int
    ho_ten: str
    email: str
    so_dien_thoai: Optional[str] = None
    ma_chuyen_khoa: int
    ten_chuyen_khoa: Optional[str] = None
    hoc_vi: Optional[str] = None
    kinh_nghiem: int
    gia_kham: Decimal
    rating: float
    status: int
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

    # Badges nhận diện
    is_hot: bool = False
    is_new: bool = False
    is_related: bool = False

    variants: List[BacSiVariantResponse] = []

    class Config:
        from_attributes = True


class BacSiPaginationResponse(BaseModel):
    items: List[BacSiResponse]
    page: int
    page_size: int
    total_records: int
    total_pages: int
