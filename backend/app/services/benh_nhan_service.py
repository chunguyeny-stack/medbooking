from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from models.models import BenhNhan, MappingTrieuChung, NguoiDung
from models.bac_si import BacSi


class BenhNhanService:

    @staticmethod
    def get_profile(db: Session, patient_id: int) -> Optional[BenhNhan]:
        return db.query(BenhNhan).filter(BenhNhan.ma_benh_nhan == patient_id).first()

    @staticmethod
    def recommend_doctors_by_symptom(db: Session, trieu_chung: str) -> List[Dict[str, Any]]:
        """
        Gợi ý Bác sĩ phù hợp dựa trên từ khóa triệu chứng bệnh
        và sắp xếp theo rating giảm dần
        """
        kw = f"%{trieu_chung.strip().lower()}%"
        mappings = db.query(MappingTrieuChung).filter(
            MappingTrieuChung.trieu_chung.ilike(kw)
        ).all()

        matched_doc_ids = set()
        matched_specialty_ids = set()

        for m in mappings:
            if m.ma_bac_si:
                matched_doc_ids.add(m.ma_bac_si)
            if m.ma_chuyen_khoa:
                matched_specialty_ids.add(m.ma_chuyen_khoa)

        # Query bác sĩ theo ID trực tiếp hoặc theo chuyên khoa ánh xạ
        query = db.query(BacSi).join(NguoiDung, BacSi.ma_bac_si == NguoiDung.user_id)\
            .filter(BacSi.status == 1)

        if matched_doc_ids or matched_specialty_ids:
            query = query.filter(
                (BacSi.ma_bac_si.in_(matched_doc_ids)) |
                (BacSi.ma_chuyen_khoa.in_(matched_specialty_ids))
            )

        doctors = query.order_by(BacSi.rating.desc()).limit(5).all()

        results: List[Dict[str, Any]] = []
        for d in doctors:
            results.append({
                "ma_bac_si": d.ma_bac_si,
                "ho_ten": d.user.ho_ten if d.user else "",
                "chuyen_khoa": d.chuyen_khoa.ten_chuyen_khoa if d.chuyen_khoa else "",
                "hoc_vi": d.hoc_vi or "",
                "rating": float(d.rating or 0.0),
                "gia_kham": float(d.gia_kham or 0.0)
            })
        return results
