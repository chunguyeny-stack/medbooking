import importlib
from datetime import date, time, datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from datadase.database import get_db
from models.models import NguoiDung
from models.lich_hen import LichHen, LogTrangThai
from models.bac_si import BacSi

root_auth = importlib.import_module("auth")

router = APIRouter(prefix="/appointments", tags=["Quản lý Lịch hẹn"])


class BookingRequest(BaseModel):
    ma_bac_si: int
    ngay_kham: date
    gio_kham: time
    ghi_chu: Optional[str] = None
    ma_bhyt: Optional[str] = None


class UpdateStatusRequest(BaseModel):
    trang_thai_moi: str  # 'Confirmed', 'In Progress', 'Completed', 'Cancelled', 'DaDen'
    ghi_chu: Optional[str] = None


@router.post("", status_code=status.HTTP_201_CREATED, summary="Bệnh nhân đặt lịch khám mới")
def create_appointment(
    payload: BookingRequest,
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(root_auth.get_current_user)
):
    doctor = db.query(BacSi).filter(BacSi.ma_bac_si == payload.ma_bac_si, BacSi.status == 1).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Bác sĩ không tồn tại hoặc đã bị ẩn.")

    # Kiểm tra ca trùng lịch
    conflict = db.query(LichHen).filter(
        LichHen.ma_bac_si == payload.ma_bac_si,
        LichHen.ngay_kham == payload.ngay_kham,
        LichHen.gio_kham == payload.gio_kham,
        LichHen.trang_thai.notin_(["Cancelled"])
    ).first()
    if conflict:
        raise HTTPException(status_code=400, detail="Khung giờ này đã có bệnh nhân khác đặt.")

    appt = LichHen(
        ma_benh_nhan=current_user.user_id,
        ma_bac_si=payload.ma_bac_si,
        ngay_kham=payload.ngay_kham,
        gio_kham=payload.gio_kham,
        trang_thai="Pending",
        ghi_chu=payload.ghi_chu or "",
        ma_bhyt=payload.ma_bhyt or ""
    )
    db.add(appt)
    db.flush()

    # Truyền chuỗi rỗng thay cho None để thỏa mãn kiểu str
    log = LogTrangThai(
        ma_lich_hen=appt.ma_lich_hen,
        trang_thai_cu="",
        trang_thai_moi="Pending",
        thoi_gian=datetime.now(timezone.utc),
        nguoi_thuc_hien_id=current_user.user_id,
        ghi_chu="Bệnh nhân đặt lịch thành công qua cổng trực tuyến."
    )
    db.add(log)
    db.commit()
    db.refresh(appt)
    return {"message": "Đặt lịch khám thành công.", "ma_lich_hen": appt.ma_lich_hen}


@router.get("", summary="Xem danh sách lịch hẹn")
def get_appointments(
    status_filter: Optional[str] = Query(None, description="Pending, Confirmed, Completed, Cancelled..."),
    ngay: Optional[date] = Query(None, description="Lọc theo ngày khám"),
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(root_auth.get_current_user)
):
    query = db.query(LichHen)

    if current_user.vai_tro == "benh_nhan":
        query = query.filter(LichHen.ma_benh_nhan == current_user.user_id)
    elif current_user.vai_tro == "bac_si":
        query = query.filter(LichHen.ma_bac_si == current_user.user_id)

    if status_filter:
        query = query.filter(LichHen.trang_thai == status_filter)
    if ngay:
        query = query.filter(LichHen.ngay_kham == ngay)

    return query.order_by(LichHen.ngay_kham.desc(), LichHen.gio_kham.asc()).all()


@router.put("/{ma_lich_hen}/status", summary="Cập nhật trạng thái lịch hẹn kèm ghi log hệ thống")
def update_appointment_status(
    ma_lich_hen: int,
    payload: UpdateStatusRequest,
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(root_auth.get_current_user)
):
    appt = db.query(LichHen).filter(LichHen.ma_lich_hen == ma_lich_hen).first()
    if not appt:
        raise HTTPException(status_code=404, detail="Không tìm thấy lịch hẹn tương ứng.")

    old_status = str(appt.trang_thai)
    appt.trang_thai = payload.trang_thai_moi

    log = LogTrangThai(
        ma_lich_hen=appt.ma_lich_hen,
        trang_thai_cu=old_status,
        trang_thai_moi=payload.trang_thai_moi,
        thoi_gian=datetime.now(timezone.utc),
        nguoi_thuc_hien_id=current_user.user_id,
        ghi_chu=payload.ghi_chu or f"Chuyển trạng thái từ {old_status} sang {payload.trang_thai_moi}"
    )
    db.add(log)
    db.commit()
    return {
        "message": "Cập nhật trạng thái thành công.",
        "ma_lich_hen": ma_lich_hen,
        "trang_thai": payload.trang_thai_moi
    }
