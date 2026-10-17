import importlib
from datetime import date, datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from datadase.database import get_db
from models.models import NguoiDung
from models.lich_hen import LichHen, LogTrangThai

root_auth = importlib.import_module("auth")

router = APIRouter(prefix="/reception", tags=["Phân hệ Lễ tân"])


class RescheduleRequest(BaseModel):
    ngay_moi: date
    khung_gio_moi: str


@router.get("/checkin-list", summary="Danh sách bệnh nhân chờ check-in trong ngày")
def get_checkin_list(
        ngay: Optional[date] = None,
        db: Session = Depends(get_db),
        current_user: NguoiDung = Depends(root_auth.require_role(["le_tan", "admin"]))
):
    _ = current_user  # Xác nhận quyền lễ tân/admin hợp lệ
    search_date = ngay or date.today()

    # Sửa lại cách gọi order_by trực tiếp trên thuộc tính cột để hết cảnh báo PyCharm
    appointments = db.query(LichHen).filter(
        LichHen.ngay_kham == search_date,
        LichHen.trang_thai.in_(["Chờ xác nhận", "Pending", "Confirmed"])
    ).order_by(LichHen.ngay_kham.desc(), LichHen.khung_gio.asc()).all()

    result = []
    for a in appointments:
        result.append({
            "ma_lich_hen": a.id,
            "benh_nhan": a.benh_nhan.user.ho_ten if a.benh_nhan and a.benh_nhan.user else "",
            "ngay_kham": a.ngay_kham,
            "khung_gio": a.khung_gio,
            "bac_si": a.bac_si.user.ho_ten if a.bac_si and a.bac_si.user else "",
            "chuyen_khoa": a.bac_si.chuyen_khoa.ten_chuyen_khoa if a.bac_si and a.bac_si.chuyen_khoa else "",
            "trang_thai": a.trang_thai
        })
    return result


@router.post("/check-in/{ma_lich_hen}", summary="Xác nhận Check-in bệnh nhân tại quầy")
def confirm_checkin(
        ma_lich_hen: int,
        db: Session = Depends(get_db),
        current_user: NguoiDung = Depends(root_auth.require_role(["le_tan", "admin"]))
):
    appt = db.query(LichHen).filter(LichHen.id == ma_lich_hen).first()
    if not appt:
        raise HTTPException(status_code=404, detail="Không tìm thấy lịch hẹn.")

    old_status = appt.trang_thai
    appt.trang_thai = "DaDen"

    log = LogTrangThai(
        lich_hen_id=appt.id,
        trang_thai_cu=old_status,
        trang_thai_moi="DaDen",
        thoi_gian=datetime.now(timezone.utc),
        nguoi_thuc_hien=current_user.ho_ten
    )
    db.add(log)
    db.commit()
    return {"message": "Bệnh nhân đã check-in thành công.", "trang_thai": "DaDen"}


@router.put("/reschedule/{ma_lich_hen}", summary="Lễ tân đổi lịch hẹn / khung giờ mới")
def reschedule_appointment(
        ma_lich_hen: int,
        payload: RescheduleRequest,
        db: Session = Depends(get_db),
        current_user: NguoiDung = Depends(root_auth.require_role(["le_tan", "admin"]))
):
    appt = db.query(LichHen).filter(LichHen.id == ma_lich_hen).first()
    if not appt:
        raise HTTPException(status_code=404, detail="Không tìm thấy lịch hẹn.")

    if appt.trang_thai in ["Completed", "Cancelled", "Đã hoàn thành", "Đã hủy"]:
        raise HTTPException(status_code=400, detail="Không thể đổi lịch hẹn đã hoàn tất hoặc đã hủy.")

    conflict = db.query(LichHen).filter(
        LichHen.bac_si_id == appt.bac_si_id,
        LichHen.ngay_kham == payload.ngay_moi,
        LichHen.khung_gio == payload.khung_gio_moi,
        LichHen.id != ma_lich_hen,
        LichHen.trang_thai.notin_(["Cancelled", "Đã hủy"])
    ).first()
    if conflict:
        raise HTTPException(status_code=400, detail="Khung giờ mới này bác sĩ đã có lịch hẹn khác.")

    appt.ngay_kham = payload.ngay_moi
    appt.khung_gio = payload.khung_gio_moi

    log = LogTrangThai(
        lich_hen_id=appt.id,
        trang_thai_cu=appt.trang_thai,
        trang_thai_moi=appt.trang_thai,
        thoi_gian=datetime.now(timezone.utc),
        nguoi_thuc_hien=current_user.ho_ten
    )
    db.add(log)
    db.commit()
    return {"message": "Đã đổi lịch hẹn thành công."}