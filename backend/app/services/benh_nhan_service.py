from typing import List, Dict, Any, Optional
from sqlalchemy import text
from sqlalchemy.orm import Session
from models.models import BenhNhan, NguoiDung
from models.bac_si import BacSi


class BenhNhanService:

    @staticmethod
    def get_profile(db: Session, patient_id: int) -> Optional[BenhNhan]:
        """
        Tìm hồ sơ bệnh nhân theo id bảng BenhNhan hoặc nguoi_dung_id
        """
        patient = db.query(BenhNhan).filter(BenhNhan.id == patient_id).first()
        if not patient:
            patient = db.query(BenhNhan).filter(BenhNhan.nguoi_dung_id == patient_id).first()
        return patient

    @staticmethod
    def recommend_doctors_by_symptom(db: Session, trieu_chung: str) -> List[Dict[str, Any]]:
        """
        Gợi ý Bác sĩ phù hợp dựa trên từ khóa triệu chứng bệnh
        và sắp xếp theo rating giảm dần
        """
        kw = f"%{trieu_chung.strip().lower()}%"

        # 1. Tra cứu các chuyên khoa liên quan từ bảng trieu_chung qua SQL Raw để tránh phụ thuộc Model
        sql_symptom = text(
            "SELECT chuyen_khoa_id FROM trieu_chung WHERE LOWER(ten_trieu_chung) LIKE :kw"
        )
        symptom_rows = db.execute(sql_symptom, {"kw": kw}).fetchall()
        matched_specialty_ids = {r[0] for r in symptom_rows if r[0] is not None}

        # 2. Khởi tạo truy vấn Bác sĩ
        query = db.query(BacSi)

        # 3. Lọc theo chuyên khoa tìm được nếu có
        if matched_specialty_ids:
            query = query.filter(BacSi.chuyen_khoa_id.in_(matched_specialty_ids))

        # 4. Sắp xếp theo rating giảm dần (nếu có cột rating)
        if hasattr(BacSi, "rating"):
            query = query.order_by(BacSi.rating.desc())
        elif hasattr(BacSi, "id"):
            query = query.order_by(BacSi.id.desc())

        doctors = query.limit(5).all()

        results: List[Dict[str, Any]] = []
        for d in doctors:
            # Lấy họ tên an toàn qua quan hệ user hoặc bảng NguoiDung
            full_name = ""
            if hasattr(d, "user") and d.user:
                full_name = getattr(d.user, "ho_ten", "")
            elif hasattr(d, "nguoi_dung_id"):
                user_obj = db.query(NguoiDung).filter(NguoiDung.id == d.nguoi_dung_id).first()
                if user_obj:
                    full_name = getattr(user_obj, "ho_ten", "")

            # Lấy tên chuyên khoa an toàn
            specialty_name = ""
            if hasattr(d, "chuyen_khoa") and d.chuyen_khoa:
                specialty_name = getattr(d.chuyen_khoa, "ten_chuyen_khoa", "")

            results.append({
                "ma_bac_si": d.id,
                "ho_ten": full_name,
                "chuyen_khoa": specialty_name,
                "hoc_vi": getattr(d, "hoc_vi", "") or "",
                "rating": float(getattr(d, "rating", 0.0) or 0.0),
                "gia_kham": float(getattr(d, "gia_kham", 0.0) or 0.0),
            })
        return results
