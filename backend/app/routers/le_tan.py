import importlib
from datetime import time, date, datetime, timezone
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
    gio_moi: time


@router.get("/checkin-list", summary="Danh sách bệnh nhân chờ check-in trong ngày")
def get_checkin_list(
    ngay: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(root_auth.require_role(["le_tan", "admin"]))
):
    _ = current_user  # Xác nhận quyền lễ tân/admin hợp lệ
    search_date = ngay or date.today()
    appointments = db.query(LichHen).filter(
        LichHen.ngay_kham == search_date,
        LichHen.trang_thai.in_(["Pending", "Confirmed"])
    ).order_by(LichHen.gio_kham.asc()).all()

    result = []
    for a in appointments:
        result.append({
            "ma_lich_hen": a.ma_lich_hen,
            "benh_nhan": a.benh_nhan.user.ho_ten if a.benh_nhan and a.benh_nhan.user else "",
            "ma_bhyt": a.ma_bhyt,
            "ngay_kham": a.ngay_kham,
            "gio_kham": a.gio_kham,
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
    appt = db.query(LichHen).filter(LichHen.ma_lich_hen == ma_lich_hen).first()
    if not appt:
        raise HTTPException(status_code=404, detail="Không tìm thấy lịch hẹn.")

    old_status = appt.trang_thai
    appt.trang_thai = "DaDen"

    log = LogTrangThai(
        ma_lich_hen=appt.ma_lich_hen,
        trang_thai_cu=old_status,
        trang_thai_moi="DaDen",
        thoi_gian=datetime.now(timezone.utc),
        nguoi_thuc_hien_id=current_user.user_id,
        ghi_chu="Lễ tân xác nhận tiếp đón và check-in bệnh nhân tại quầy."
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
    appt = db.query(LichHen).filter(LichHen.ma_lich_hen == ma_lich_hen).first()
    if not appt:
        raise HTTPException(status_code=404, detail="Không tìm thấy lịch hẹn.")

    if appt.trang_thai in ["Completed", "Cancelled"]:
        raise HTTPException(status_code=400, detail="Không thể đổi lịch hẹn đã hoàn tất hoặc đã hủy.")

    conflict = db.query(LichHen).filter(
        LichHen.ma_bac_si == appt.ma_bac_si,
        LichHen.ngay_kham == payload.ngay_moi,
        LichHen.gio_kham == payload.gio_moi,
        LichHen.ma_lich_hen != ma_lich_hen,
        LichHen.trang_thai.notin_(["Cancelled"])
    ).first()
    if conflict:
        raise HTTPException(status_code=400, detail="Khung giờ mới này đã có người đặt trước.")

    appt.ngay_kham = payload.ngay_moi
    appt.gio_kham = payload.gio_moi

    log = LogTrangThai(
        ma_lich_hen=appt.ma_lich_hen,
        trang_thai_cu=appt.trang_thai,
        trang_thai_moi=appt.trang_thai,
        thoi_gian=datetime.now(timezone.utc),
        nguoi_thuc_hien_id=current_user.user_id,
        ghi_chu=f"Lễ tân đổi lịch hẹn sang: Ngày {payload.ngay_moi} lúc {payload.gio_moi}"
    )
    db.add(log)
    db.commit()
    return {"message": "Đã đổi lịch hẹn thành công."}
