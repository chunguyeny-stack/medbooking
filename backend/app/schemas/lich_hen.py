from datetime import date, time, datetime
from typing import Optional, List
from pydantic import BaseModel, Field


# --- Lịch làm việc / Ca khám ---
class LichLamViecBase(BaseModel):
    ma_bac_si: int
    ngay_lam: date
    gio_bat_dau: time
    gio_ket_thuc: time
    ca_kham: Optional[str] = None  # Sang / Chieu
    da_dat: int = 0


class LichLamViecCreate(LichLamViecBase):
    pass


class LichLamViecResponse(LichLamViecBase):
    ma_lich_lam: int

    class Config:
        from_attributes = True


# --- Log trạng thái lịch hẹn ---
class LogTrangThaiResponse(BaseModel):
    ma_log: int
    ma_lich_hen: int
    trang_thai_cu: Optional[str] = None
    trang_thai_moi: str
    thoi_gian: datetime
    nguoi_thuc_hien_id: Optional[int] = None
    ghi_chu: Optional[str] = None

    class Config:
        from_attributes = True


# --- Đặt lịch & Cập nhật trạng thái ---
class BookingRequest(BaseModel):
    ma_bac_si: int
    ngay_kham: date
    gio_kham: time
    ghi_chu: Optional[str] = None
    ma_bhyt: Optional[str] = None


class UpdateAppointmentStatusRequest(BaseModel):
    trang_thai_moi: str = Field(..., description="Pending, Confirmed, In Progress, Completed, Cancelled, DaDen")
    ghi_chu: Optional[str] = None


class LichHenResponse(BaseModel):
    ma_lich_hen: int
    ma_benh_nhan: int
    ma_bac_si: int
    ngay_kham: date
    gio_kham: time
    trang_thai: str
    ngay_tao: Optional[datetime] = None
    ghi_chu: Optional[str] = None
    ma_bhyt: Optional[str] = None
    logs: List[LogTrangThaiResponse] = []

    class Config:
        from_attributes = True
