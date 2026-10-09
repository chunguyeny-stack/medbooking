import importlib
import math
from datetime import datetime, timedelta, timezone
from typing import Optional, List, Dict, Any
from fastapi import HTTPException, status
from sqlalchemy import or_, func
from sqlalchemy.orm import Session

from models.models import NguoiDung, ChuyenKhoa
from models.lich_hen import LichHen
from models.bac_si import BacSi, BacSiVariant
from schemas.bac_si import BacSiCreate, BacSiUpdate

# Nạp an toàn module auth từ thư mục gốc
root_auth = importlib.import_module("auth")


class BacSiService:

    @staticmethod
    def create_doctor(db: Session, data: BacSiCreate, current_user: NguoiDung) -> BacSi:
        # 1. Kiểm tra email người dùng đã tồn tại chưa
        existing_user = db.query(NguoiDung).filter(NguoiDung.email == data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email này đã được sử dụng trên hệ thống."
            )

        # 2. Kiểm tra Chuyên khoa có tồn tại không
        chk_ck = db.query(ChuyenKhoa).filter(ChuyenKhoa.ma_chuyen_khoa == data.ma_chuyen_khoa).first()
        if not chk_ck:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Chuyên khoa với ID {data.ma_chuyen_khoa} không tồn tại."
            )

        # 3. Tạo tài khoản Người dùng (NguoiDung) với vai trò 'bac_si'
        hashed_password = str(root_auth.get_password_hash(data.mat_khau))
        phone_val: str = str(data.so_dien_thoai) if data.so_dien_thoai is not None else ""

        new_user = NguoiDung(
            email=data.email,
            mat_khau=hashed_password,
            ho_ten=data.ho_ten,
            so_dien_thoai=phone_val,
            vai_tro="bac_si",
            trang_thai=1
        )
        db.add(new_user)
        db.flush()

        # 4. Tạo hồ sơ Bác sĩ gốc
        now_time = datetime.now(timezone.utc)
        doctor = BacSi(
            ma_bac_si=new_user.user_id,
            ma_chuyen_khoa=data.ma_chuyen_khoa,
            hoc_vi=data.hoc_vi or "",
            kinh_nghiem=data.kinh_nghiem,
            gia_kham=data.gia_kham,
            rating=0.0,
            status=1,
            created_at=now_time,
            updated_at=now_time,
            created_by=current_user.user_id,
            updated_by=current_user.user_id
        )
        db.add(doctor)
        db.flush()

        # 5. Lưu các dị bản phụ thuộc vào ID của BS gốc
        if data.variants:
            for v in data.variants:
                variant_record = BacSiVariant(
                    ma_bac_si=doctor.ma_bac_si,
                    ten_co_so=v.ten_co_so or "",
                    dia_chi_co_so=v.dia_chi_co_so or "",
                    chuyen_khoa_phu=v.chuyen_khoa_phu or "",
                    khung_gio_phu=v.khung_gio_phu or ""
                )
                db.add(variant_record)

        db.commit()
        db.refresh(doctor)
        return doctor

    @staticmethod
    def get_doctor_by_id(db: Session, doctor_id: int, is_admin: bool = False) -> BacSi:
        query = db.query(BacSi).filter(BacSi.ma_bac_si == doctor_id)
        if not is_admin:
            query = query.filter(BacSi.status == 1)

        doctor = query.first()
        if not doctor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bác sĩ không tồn tại hoặc đã bị ẩn."
            )
        return doctor

    @staticmethod
    def get_paginated_doctors(
        db: Session,
        page: int = 1,
        page_size: int = 10,
        keyword: Optional[str] = None,
        chuyen_khoa_id: Optional[int] = None,
        hoc_vi: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        doctor_status: Optional[int] = None,
        sort_by: str = "created_at",
        sort_order: str = "desc",
        is_admin: bool = False,
        patient_history_specialty_ids: Optional[List[int]] = None
    ) -> Dict[str, Any]:
        query = db.query(BacSi).join(NguoiDung, BacSi.ma_bac_si == NguoiDung.user_id)

        # 1. Phân quyền hiển thị theo status
        if not is_admin:
            query = query.filter(BacSi.status == 1)
        else:
            if doctor_status is not None:
                query = query.filter(BacSi.status == doctor_status)

        # 2. Tìm kiếm theo từ khóa
        if keyword:
            kw = f"%{keyword.strip()}%"
            query = query.filter(
                or_(
                    NguoiDung.ho_ten.ilike(kw),
                    NguoiDung.email.ilike(kw),
                    NguoiDung.so_dien_thoai.ilike(kw)
                )
            )

        # 3. Bộ lọc thuộc tính
        if chuyen_khoa_id:
            query = query.filter(BacSi.ma_chuyen_khoa == chuyen_khoa_id)
        if hoc_vi:
            query = query.filter(BacSi.hoc_vi.ilike(f"%{hoc_vi.strip()}%"))
        if min_price is not None:
            query = query.filter(BacSi.gia_kham >= min_price)
        if max_price is not None:
            query = query.filter(BacSi.gia_kham <= max_price)

        # 4. Sắp xếp động linh hoạt (Gọi trực tiếp .desc() / .asc() tránh lỗi order_fn not callable)
        sort_column_map = {
            "created_at": BacSi.created_at,
            "updated_at": BacSi.updated_at,
            "ten": NguoiDung.ho_ten,
            "rating": BacSi.rating,
            "gia_kham": BacSi.gia_kham
        }
        target_col = sort_column_map.get(sort_by, BacSi.created_at)
        if sort_order.lower() == "desc":
            query = query.order_by(target_col.desc())
        else:
            query = query.order_by(target_col.asc())

        total_records = query.count()
        total_pages = math.ceil(total_records / page_size) if total_records > 0 else 1
        offset = (page - 1) * page_size
        raw_doctors = query.offset(offset).limit(page_size).all()

        # 5. Gắn nhãn badge
        items: List[Dict[str, Any]] = []
        now = datetime.now(timezone.utc)
        for doc in raw_doctors:
            created_at_val = doc.created_at
            if created_at_val and created_at_val.tzinfo is None:
                created_at_val = created_at_val.replace(tzinfo=timezone.utc)
            is_new = (now - created_at_val) <= timedelta(days=30) if created_at_val else False

            completed_appts = db.query(func.count(LichHen.ma_lich_hen))\
                .filter(LichHen.ma_bac_si == doc.ma_bac_si, LichHen.trang_thai == "Completed")\
                .scalar() or 0
            is_hot = completed_appts >= 20 or (doc.rating is not None and doc.rating >= 4.8)

            is_related = False
            if patient_history_specialty_ids and doc.ma_chuyen_khoa in patient_history_specialty_ids:
                is_related = True

            doc_dict = {
                "ma_bac_si": doc.ma_bac_si,
                "ho_ten": doc.user.ho_ten if doc.user else "",
                "email": doc.user.email if doc.user else "",
                "so_dien_thoai": doc.user.so_dien_thoai if doc.user else None,
                "ma_chuyen_khoa": doc.ma_chuyen_khoa,
                "ten_chuyen_khoa": doc.chuyen_khoa.ten_chuyen_khoa if doc.chuyen_khoa else None,
                "hoc_vi": doc.hoc_vi,
                "kinh_nghiem": doc.kinh_nghiem,
                "gia_kham": doc.gia_kham,
                "rating": doc.rating,
                "status": doc.status,
                "created_at": doc.created_at,
                "updated_at": doc.updated_at,
                "created_by": doc.created_by,
                "updated_by": doc.updated_by,
                "is_hot": is_hot,
                "is_new": is_new,
                "is_related": is_related,
                "variants": doc.variants
            }
            items.append(doc_dict)

        return {
            "items": items,
            "page": page,
            "page_size": page_size,
            "total_records": total_records,
            "total_pages": total_pages
        }

    @staticmethod
    def update_doctor(db: Session, doctor_id: int, data: BacSiUpdate, current_user: NguoiDung) -> BacSi:
        doctor = db.query(BacSi).filter(BacSi.ma_bac_si == doctor_id).first()
        if not doctor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Không tìm thấy bác sĩ cần chỉnh sửa."
            )

        # 1. Cập nhật thông tin User gốc
        if doctor.user:
            if data.ho_ten is not None:
                doctor.user.ho_ten = data.ho_ten
            if data.so_dien_thoai is not None:
                doctor.user.so_dien_thoai = data.so_dien_thoai

        # 2. Cập nhật thông tin Bác sĩ gốc
        if data.ma_chuyen_khoa is not None:
            doctor.ma_chuyen_khoa = data.ma_chuyen_khoa
        if data.hoc_vi is not None:
            doctor.hoc_vi = data.hoc_vi
        if data.kinh_nghiem is not None:
            doctor.kinh_nghiem = data.kinh_nghiem
        if data.gia_kham is not None:
            doctor.gia_kham = data.gia_kham
        if data.status is not None:
            doctor.status = data.status

        doctor.updated_at = datetime.now(timezone.utc)
        doctor.updated_by = current_user.user_id

        # 3. Quản lý dị bản phụ thuộc (Ghi đè)
        if data.variants is not None:
            db.query(BacSiVariant).filter(BacSiVariant.ma_bac_si == doctor_id).delete()
            for v in data.variants:
                new_var = BacSiVariant(
                    ma_bac_si=doctor_id,
                    ten_co_so=v.ten_co_so or "",
                    dia_chi_co_so=v.dia_chi_co_so or "",
                    chuyen_khoa_phu=v.chuyen_khoa_phu or "",
                    khung_gio_phu=v.khung_gio_phu or ""
                )
                db.add(new_var)

        db.commit()
        db.refresh(doctor)
        return doctor

    @staticmethod
    def delete_doctor(db: Session, doctor_id: int, delete_type: str, current_user: NguoiDung) -> Dict[str, Any]:
        doctor = db.query(BacSi).filter(BacSi.ma_bac_si == doctor_id).first()
        if not doctor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bác sĩ cần xóa không tồn tại."
            )

        if delete_type.lower() == "soft":
            doctor.status = 0
            doctor.updated_at = datetime.now(timezone.utc)
            doctor.updated_by = current_user.user_id
            db.commit()
            return {"message": "Đã ẩn bác sĩ thành công (Soft Delete).", "doctor_id": doctor_id, "status": 0}

        elif delete_type.lower() == "hard":
            active_appointments = db.query(LichHen).filter(
                LichHen.ma_bac_si == doctor_id,
                LichHen.trang_thai.in_(["Pending", "Confirmed", "In Progress"])
            ).count()

            if active_appointments > 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Không thể xóa vĩnh viễn: Bác sĩ đang có {active_appointments} lịch hẹn đang xử lý."
                )

            user = db.query(NguoiDung).filter(NguoiDung.user_id == doctor_id).first()
            if user:
                db.delete(user)
            else:
                db.delete(doctor)

            db.commit()
            return {"message": "Đã xóa vĩnh viễn bác sĩ khỏi cơ sở dữ liệu (Hard Delete).", "doctor_id": doctor_id}

        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Kiểu xóa không hợp lệ. Vui lòng chọn 'soft' hoặc 'hard'."
            )
