from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr


class BacSiVariantBase(BaseModel):
  sub_department: str
  working_hours: Optional[str] = None
  branch_location: Optional[str] = None


class BacSiVariantResponse(BacSiVariantBase):
  id: int
  doctor_id: int

  class Config:
    from_attributes = True


class BacSiCreate(BaseModel):
  name: str
  specialization: str
  price: float
  phone: Optional[str] = None
  email: Optional[EmailStr] = None
  is_hot: Optional[bool] = False
  is_new: Optional[bool] = True
  variants: Optional[List[BacSiVariantBase]] = []


class BacSiUpdate(BaseModel):
  name: Optional[str] = None
  specialization: Optional[str] = None
  price: Optional[float] = None
  phone: Optional[str] = None
  email: Optional[EmailStr] = None
  is_hot: Optional[bool] = None
  is_new: Optional[bool] = None
  variants: Optional[List[BacSiVariantBase]] = []


class BacSiResponse(BaseModel):
  id: int
  name: str
  specialization: str
  price: float
  phone: Optional[str]
  email: Optional[str]
  status: int
  is_hot: bool
  is_new: bool
  created_at: datetime
  created_by: Optional[str]
  updated_at: Optional[datetime]
  updated_by: Optional[str]
  variants: List[BacSiVariantResponse] = []

  class Config:
    from_attributes = True


class PaginatedBacSiResponse(BaseModel):
  total_records: int
  total_pages: int
  page: int
  page_size: int
  data: List[BacSiResponse]