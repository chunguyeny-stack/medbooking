from decimal import Decimal
from typing import Dict, Any, List, Optional
from fastapi import HTTPException, status
from sqlalchemy import extract
from sqlalchemy.orm import Session

from models.models import NguoiDung, ChuyenKhoa, DichVu, HoaDon
from models.lich_hen import LichHen, LogTrangThai
from models.bac_si import BacSi


class AdminService:

    # --- Quản trị người dùng & Phân quyền ---
    @staticmethod
    def get_users(db: Session, vai_tro: Optional[str] = None) -> List[NguoiDung]:
        query = db.query(NguoiDung)
        if vai_tro:
            query = query.filter(NguoiDung.vai_tro == vai_tro)
        return query.order_by(NguoiDung.user_id.desc()).all()

    @staticmethod
    def toggle_user_status(db: Session, user_id: int) -> Dict[str, Any]:
        user = db.query(NguoiDung).filter(NguoiDung.user_id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Người dùng không tồn tại.")
        user.trang_thai = 0 if user.trang_thai == 1 else 1
        db.commit()
        return {"message": "Cập nhật trạng thái thành công.", "user_id": user_id, "trang_thai": user.trang_thai}

    # --- Quản trị Chuyên khoa ---
    @staticmethod
    def create_chuyen_khoa(db: Session, ten: str, mo_ta: Optional[str] = None) -> ChuyenKhoa:
        ck = ChuyenKhoa(ten_chuyen_khoa=ten, mo_ta=mo_ta or "")
        db.add(ck)
        db.commit()
        db.refresh(ck)
        return ck

    # --- Quản trị Dịch vụ ---
    @staticmethod
    def create_dich_vu(db: Session, ten: str, gia: Decimal, mo_ta: Optional[str] = None) -> DichVu:
        dv = DichVu(ten_dich_vu=ten, gia_dich_vu=gia, mo_ta=mo_ta or "")
        db.add(dv)
        db.commit()
        db.refresh(dv)
        return dv

    # --- Dashboard Thống kê 4 kỳ trong năm & Báo cáo chi tiết ---
    @staticmethod
    def get_quarterly_dashboard(db: Session, year: int, quarter: Optional[str] = None) -> Dict[str, Any]:
        quarter_months = {
            "Q1": [1, 2, 3],
            "Q2": [4, 5, 6],
            "Q3": [7, 8, 9],
            "Q4": [10, 11, 12]
        }

        query = db.query(LichHen).filter(
            extract('year', LichHen.ngay_kham) == year,
            LichHen.trang_thai == "Completed"
        )

        months_filter = None
        if quarter and quarter.upper() in quarter_months:
            months_filter = quarter_months[quarter.upper()]
            query = query.filter(extract('month', LichHen.ngay_kham).in_(months_filter))

        completed_appointments = query.order_by(LichHen.ngay_kham.desc(), LichHen.gio_kham.desc()).all()

        total_records = len(completed_appointments)
        total_revenue = Decimal("0.0")
        transaction_logs: List[Dict[str, Any]] = []

        chart_labels: List[str] = []
        chart_data_map: Dict[int, float] = {}

        if months_filter:
            for m in months_filter:
                chart_labels.append(f"Tháng {m}")
                chart_data_map[m] = 0.0
        else:
            for m in range(1, 13):
                chart_labels.append(f"T{m}")
                chart_data_map[m] = 0.0

        for appt in completed_appointments:
            bill = db.query(HoaDon).filter(HoaDon.ma_lich_hen == appt.ma_lich_hen).first()
            default_price = appt.bac_si.gia_kham if (appt.bac_si and appt.bac_si.gia_kham) else Decimal("0.0")
            amount = Decimal(str(bill.tong_tien)) if (bill and bill.tong_tien) else default_price
            total_revenue += amount

            month_idx = appt.ngay_kham.month
            if month_idx in chart_data_map:
                chart_data_map[month_idx] += float(amount)

            bac_si_name = appt.bac_si.user.ho_ten if (appt.bac_si and appt.bac_si.user) else "Chưa rõ"

            checkin_log = db.query(LogTrangThai).filter(
                LogTrangThai.ma_lich_hen == appt.ma_lich_hen,
                LogTrangThai.trang_thai_moi.in_(["DaDen", "Confirmed"])
            ).first()

            le_tan_name = "Hệ thống"
            if checkin_log and checkin_log.nguoi_thuc_hien_id:
                receptionist = db.query(NguoiDung).filter(NguoiDung.user_id == checkin_log.nguoi_thuc_hien_id).first()
                if receptionist:
                    le_tan_name = receptionist.ho_ten

            transaction_logs.append({
                "ma_lich_hen": appt.ma_lich_hen,
                "ngay_kham": str(appt.ngay_kham),
                "gio_kham": str(appt.gio_kham),
                "benh_nhan": appt.benh_nhan.user.ho_ten if (appt.benh_nhan and appt.benh_nhan.user) else "Ẩn danh",
                "bac_si": bac_si_name,
                "le_tan_xac_nhan": le_tan_name,
                "so_tien": float(amount),
                "loi_nhuan": float(amount * Decimal("0.35")),
                "trang_thai": "Hoàn thành"
            })

        total_profit = total_revenue * Decimal("0.35")

        top_doctors = db.query(BacSi).join(NguoiDung, BacSi.ma_bac_si == NguoiDung.user_id)\
            .filter(BacSi.status == 1)\
            .order_by(BacSi.rating.desc())\
            .limit(5).all()

        top_doc_list = [
            {"ma_bac_si": d.ma_bac_si, "ho_ten": d.user.ho_ten if d.user else "", "rating": float(d.rating or 0.0)}
            for d in top_doctors
        ]

        return {
            "year": year,
            "quarter": quarter or "ALL",
            "has_data": total_records > 0,
            "total_completed": total_records,
            "total_revenue": float(total_revenue),
            "total_profit": float(total_profit),
            "top_doctors": top_doc_list,
            "chart": {
                "labels": chart_labels,
                "values": list(chart_data_map.values())
            },
            "transactions": transaction_logs
        }
