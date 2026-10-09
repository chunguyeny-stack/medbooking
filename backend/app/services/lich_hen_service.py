from datetime import datetime, timezone
from typing import Optional
from decimal import Decimal
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.lich_hen import LichHen, LogTrangThai
from models.bac_si import BacSi
from models.models import HoaDon
from schemas.lich_hen import BookingRequest


class LichHenService:

    @staticmethod
    def create_appointment(db: Session, data: BookingRequest, patient_id: int) -> LichHen:
        doctor = db.query(BacSi).filter(BacSi.ma_bac_si == data.ma_bac_si, BacSi.status == 1).first()
        if not doctor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bác sĩ không tồn tại hoặc đã bị ẩn.")

        conflict = db.query(LichHen).filter(
            LichHen.ma_bac_si == data.ma_bac_si,
            LichHen.ngay_kham == data.ngay_kham,
            LichHen.gio_kham == data.gio_kham,
            LichHen.trang_thai.notin_(["Cancelled"])
        ).first()
        if conflict:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Khung giờ khám này đã có bệnh nhân khác đặt."
            )

        appt = LichHen(
            ma_benh_nhan=patient_id,
            ma_bac_si=data.ma_bac_si,
            ngay_kham=data.ngay_kham,
            gio_kham=data.gio_kham,
            trang_thai="Pending",
            ghi_chu=data.ghi_chu or "",
            ma_bhyt=data.ma_bhyt or ""
        )
        db.add(appt)
        db.flush()

        hoa_don = HoaDon(
            ma_lich_hen=appt.ma_lich_hen,
            tong_tien=doctor.gia_kham or Decimal("0.0"),
            trang_thai="Chua Thanh Toan"
        )
        db.add(hoa_don)

        log = LogTrangThai(
            ma_lich_hen=appt.ma_lich_hen,
            trang_thai_cu="",
            trang_thai_moi="Pending",
            thoi_gian=datetime.now(timezone.utc),
            nguoi_thuc_hien_id=patient_id,
            ghi_chu="Bệnh nhân tạo lịch hẹn trực tuyến."
        )
        db.add(log)
        db.commit()
        db.refresh(appt)
        return appt

    @staticmethod
    def update_status(
        db: Session,
        ma_lich_hen: int,
        trang_thai_moi: str,
        user_id: int,
        ghi_chu: Optional[str] = None
    ) -> LichHen:
        appt = db.query(LichHen).filter(LichHen.ma_lich_hen == ma_lich_hen).first()
        if not appt:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy lịch hẹn.")

        old_status = str(appt.trang_thai)
        appt.trang_thai = trang_thai_moi

        log = LogTrangThai(
            ma_lich_hen=appt.ma_lich_hen,
            trang_thai_cu=old_status,
            trang_thai_moi=trang_thai_moi,
            thoi_gian=datetime.now(timezone.utc),
            nguoi_thuc_hien_id=user_id,
            ghi_chu=ghi_chu or f"Cập nhật từ {old_status} sang {trang_thai_moi}"
        )
        db.add(log)
        db.commit()
        db.refresh(appt)
        return appt
