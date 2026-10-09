from datetime import date, time, datetime, timezone
from typing import List, Dict, Any, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.lich_hen import LichHen, LogTrangThai


class LeTanService:

    @staticmethod
    def _format_appointment(a: LichHen) -> Dict[str, Any]:
        """Hàm dùng chung format dữ liệu hiển thị lịch hẹn"""
        return {
            "ma_lich_hen": a.ma_lich_hen,
            "benh_nhan": a.benh_nhan.user.ho_ten if (a.benh_nhan and a.benh_nhan.user) else "",
            "ma_bhyt": a.ma_bhyt or "",
            "ngay_kham": a.ngay_kham,
            "gio_kham": a.gio_kham,
            "bac_si": a.bac_si.user.ho_ten if (a.bac_si and a.bac_si.user) else "",
            "chuyen_khoa": a.bac_si.chuyen_khoa.ten_chuyen_khoa if (a.bac_si and a.bac_si.chuyen_khoa) else "",
            "trang_thai": a.trang_thai
        }

    @classmethod
    def get_daily_checkin_list(cls, db: Session, ngay: Optional[date] = None) -> List[Dict[str, Any]]:
        search_date = ngay or date.today()
        appointments = db.query(LichHen).filter(
            LichHen.ngay_kham == search_date,
            LichHen.trang_thai.in_(["Pending", "Confirmed"])
        ).order_by(LichHen.gio_kham.asc()).all()

        return [cls._format_appointment(a) for a in appointments]

    @staticmethod
    def confirm_checkin(db: Session, ma_lich_hen: int, receptionist_id: int) -> Dict[str, Any]:
        appt = db.query(LichHen).filter(LichHen.ma_lich_hen == ma_lich_hen).first()
        if not appt:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy lịch hẹn.")

        old_status = str(appt.trang_thai)
        appt.trang_thai = "DaDen"

        log = LogTrangThai(
            ma_lich_hen=appt.ma_lich_hen,
            trang_thai_cu=old_status,
            trang_thai_moi="DaDen",
            thoi_gian=datetime.now(timezone.utc),
            nguoi_thuc_hien_id=receptionist_id,
            ghi_chu="Lễ tân xác nhận bệnh nhân đã đến tiếp đón tại quầy."
        )
        db.add(log)
        db.commit()
        return {"message": "Xác nhận check-in thành công.", "ma_lich_hen": ma_lich_hen, "trang_thai": "DaDen"}

    @staticmethod
    def reschedule_appointment(
        db: Session,
        ma_lich_hen: int,
        ngay_moi: date,
        gio_moi: time,
        receptionist_id: int
    ) -> Dict[str, Any]:
        appt = db.query(LichHen).filter(LichHen.ma_lich_hen == ma_lich_hen).first()
        if not appt:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy lịch hẹn.")

        if appt.trang_thai in ["Completed", "Cancelled"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Không thể đổi lịch hẹn đã kết thúc hoặc đã hủy.")

        conflict = db.query(LichHen).filter(
            LichHen.ma_bac_si == appt.ma_bac_si,
            LichHen.ngay_kham == ngay_moi,
            LichHen.gio_kham == gio_moi,
            LichHen.ma_lich_hen != ma_lich_hen,
            LichHen.trang_thai.notin_(["Cancelled"])
        ).first()
        if conflict:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Khung giờ mới này đã có người khác đặt.")

        appt.ngay_kham = ngay_moi
        appt.gio_kham = gio_moi

        log = LogTrangThai(
            ma_lich_hen=appt.ma_lich_hen,
            trang_thai_cu=str(appt.trang_thai),
            trang_thai_moi=str(appt.trang_thai),
            thoi_gian=datetime.now(timezone.utc),
            nguoi_thuc_hien_id=receptionist_id,
            ghi_chu=f"Lễ tân đổi lịch sang ngày {ngay_moi} lúc {gio_moi}"
        )
        db.add(log)
        db.commit()
        return {"message": "Đã đổi lịch hẹn thành công."}
