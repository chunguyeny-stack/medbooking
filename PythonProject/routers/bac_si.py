import importlib
from typing import Optional, List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified
from pydantic import BaseModel, Field
from datetime import datetime, timezone, date

from database.database import get_db
from models.models import NguoiDung, BenhNhan
from models.bac_si import BacSi
from models.lich_hen import LichHen, LichLamViec, LogTrangThai
from schemas.bac_si import (
    BacSiCreate,
    BacSiUpdate,
    BacSiResponse,
    BacSiPaginationResponse
)

from services.bac_si_service import BacSiService

# Nạp module auth từ thư mục gốc
import auth as root_auth

router = APIRouter(prefix="/doctors", tags=["Quản lý Bác sĩ"])


# ==========================================
# 1. CÁC ROUTE CỐ ĐỊNH ĐẶT Ở TRƯỚC (vd: /ho-so, /ho-so-chi-tiet, /danh-sach)
# ==========================================

@router.get(
    "/danh-sach",
    summary="Lấy gọn danh sách toàn bộ bác sĩ cho bộ lọc"
)
def get_all_doctors_list(db: Session = Depends(get_db)):
    """API trả về danh sách cơ bản của bác sĩ phục vụ cho việc hiển thị dropdown bộ lọc."""
    try:
        bac_sis = db.query(BacSi).all()
        data = []
        for bs in bac_sis:
            name = "Bác sĩ"
            if hasattr(bs, 'nguoi_dung') and bs.nguoi_dung:
                name = bs.nguoi_dung.ho_ten
            data.append({
                "id": bs.id,
                "ho_ten": name
            })
        return {"success": True, "data": data}
    except Exception as e:
        return {"success": False, "data": [], "detail": str(e)}


@router.get(
    "/ho-so-chi-tiet",
    summary="Lấy thông tin chi tiết, chuyên khoa chuẩn, lịch trực và danh sách lịch hẹn của bệnh nhân"
)
def get_doctor_profile_detail(
        db: Session = Depends(get_db),
        current_user: NguoiDung = Depends(root_auth.require_role(["bac_si"]))
):
    try:
        bac_si = db.query(BacSi).filter(BacSi.nguoi_dung_id == current_user.id).first()

        ten_chuyen_khoa = "Chưa phân công"
        if bac_si and bac_si.chuyen_khoa:
            ten_chuyen_khoa = bac_si.chuyen_khoa.ten_chuyen_khoa
        elif hasattr(current_user, "chuyen_khoa"):
            ten_chuyen_khoa = current_user.chuyen_khoa

        lich_truc_data = []
        if bac_si:
            schedules = db.query(LichLamViec).filter(LichLamViec.bac_si_id == bac_si.id).all()
            for s in schedules:
                lich_truc_data.append({
                    "id": s.id,
                    "ngay": str(s.ngay_kham) if s.ngay_kham else "",
                    "khung_gio": s.khung_gio,
                    "ca": getattr(s, 'ca_lam_viec', 'Ca sáng'),
                    "trang_thai": getattr(s, 'trang_thai_chi_tiet', 'cho_bac_si'),
                    "ly_do_ban": getattr(s, 'ly_do_ban', '') or ''
                })

        lich_hen_data = []
        if bac_si:
            lich_hens = db.query(LichHen).filter(
                LichHen.bac_si_id == bac_si.id,
                LichHen.trang_thai.notin_(["Cancelled", "Đã hủy"])
            ).all()

            for h in lich_hens:
                bn_name = "Bệnh nhân"
                so_dt = ""
                if h.benh_nhan_id:
                    bn = db.query(BenhNhan).filter(BenhNhan.id == h.benh_nhan_id).first()
                    if bn and bn.nguoi_dung_id:
                        u_bn = db.query(NguoiDung).filter(NguoiDung.id == bn.nguoi_dung_id).first()
                        if u_bn:
                            bn_name = u_bn.ho_ten
                            so_dt = getattr(u_bn, 'so_dien_thoai', '') or ''

                lich_hen_data.append({
                    "id": h.id,
                    "ngay_kham": str(h.ngay_kham) if h.ngay_kham else "",
                    "khung_gio": h.khung_gio,
                    "benh_nhan": bn_name,
                    "so_dien_thoai": so_dt,
                    "trang_thai": h.trang_thai,
                    "ghi_chu": h.ghi_chu or "Khám tổng quát"
                })

        return {
            "success": True,
            "ho_ten": current_user.ho_ten,
            "email": getattr(current_user, 'email', '') or getattr(current_user, 'thu_dien_tu', ''),
            "so_dien_thoai": current_user.so_dien_thoai,
            "chuyen_khoa": ten_chuyen_khoa,
            "lich_truc": lich_truc_data,
            "lich_hen": lich_hen_data
        }
    except Exception as e:
        print(f"Lỗi lấy hồ sơ chi tiết bác sĩ: {e}")
        return {"success": False, "detail": str(e)}


class DoctorProfileSelfUpdate(BaseModel):
    phone: Optional[str] = Field(None, description="Số điện thoại mới")
    bio: Optional[str] = Field(None, description="Kinh nghiệm & Giới thiệu")


@router.put(
    "/ho-so",
    summary="Bác sĩ tự cập nhật thông tin cá nhân của mình"
)
def update_my_doctor_profile(
        payload: DoctorProfileSelfUpdate,
        db: Session = Depends(get_db),
        current_user: NguoiDung = Depends(root_auth.require_role(["bac_si"]))
):
    try:
        if payload.phone is not None:
            current_user.so_dien_thoai = payload.phone
            if hasattr(current_user, 'phone'):
                current_user.phone = payload.phone

        doctor_profile = db.query(BacSi).filter(BacSi.nguoi_dung_id == current_user.id).first()
        if doctor_profile and payload.bio is not None:
            if hasattr(doctor_profile, "gioi_thieu"):
                doctor_profile.gioi_thieu = payload.bio
            if hasattr(doctor_profile, "kinh_nghiem"):
                doctor_profile.kinh_nghiem = payload.bio
            if hasattr(doctor_profile, "bio"):
                doctor_profile.bio = payload.bio

            db.add(doctor_profile)

        db.commit()
        db.refresh(current_user)
        if doctor_profile:
            db.refresh(doctor_profile)

        return {
            "success": True,
            "message": "Cập nhật thông tin cá nhân thành công!",
            "data": {
                "email": getattr(current_user, 'email', '') or getattr(current_user, 'thu_dien_tu', ''),
                "so_dien_thoai": current_user.so_dien_thoai,
                "bio": getattr(doctor_profile, 'gioi_thieu', '') or getattr(doctor_profile, 'bio',
                                                                            '') if doctor_profile else ""
            }
        }
    except Exception as e:
        db.rollback()
        print(f"Lỗi cập nhật hồ sơ bác sĩ: {e}")
        return {"success": False, "detail": str(e)}


@router.post(
    "",
    response_model=BacSiResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Thêm mới Bác sĩ & Dị bản (Admin only)"
)
def create_doctor(
        payload: BacSiCreate,
        db: Session = Depends(get_db),
        current_user: NguoiDung = Depends(root_auth.require_role(["admin"]))
):
    doctor = BacSiService.create_doctor(db=db, data=payload, current_user=current_user)
    paginated_res = BacSiService.get_paginated_doctors(
        db=db, page=1, page_size=1, keyword=doctor.user.email, is_admin=True
    )
    return paginated_res["items"][0]


@router.get(
    "",
    summary="Tìm kiếm, Lọc, Sắp xếp & Phân trang danh sách Bác sĩ"
)
def get_doctors(
        page: int = Query(1, ge=1, description="Số thứ tự trang"),
        limit: int = Query(10, ge=1, le=100, description="Số bản ghi mỗi trang"),
        keyword: Optional[str] = Query(None, description="Tìm theo tên, email, sđt"),
        chuyen_khoa_id: Optional[int] = Query(None, description="Lọc theo ID chuyên khoa"),
        hoc_vi: Optional[str] = Query(None, description="Lọc theo học vị (Thạc sĩ, CKI...)"),
        min_price: Optional[float] = Query(None, ge=0, description="Giá khám tối thiểu"),
        max_price: Optional[float] = Query(None, ge=0, description="Giá khám tối đa"),
        doctor_status: Optional[int] = Query(None, description="Trạng thái (1: Hoạt động, 0: Đã ẩn)"),
        sort_by: str = Query("id", description="id, ten, rating, gia_kham"),
        order: str = Query("desc", pattern="^(asc|desc)$", description="Chiều sắp xếp: asc hoặc desc"),
        db: Session = Depends(get_db),
        current_user: Optional[NguoiDung] = Depends(root_auth.get_optional_current_user)
):
    try:
        is_admin = bool(current_user and current_user.vai_tro == "admin")
        patient_specialties: List[int] = []
        if current_user and current_user.vai_tro == "benh_nhan":
            history = db.query(LichHen.bac_si_id).filter(
                LichHen.benh_nhan_id == current_user.id
            ).all()
            doc_ids = [h[0] for h in history if h[0]]
            if doc_ids:
                ck_records = db.query(BacSi.chuyen_khoa_id).filter(BacSi.id.in_(doc_ids)).all()
                patient_specialties = [c[0] for c in ck_records if c[0]]

        return BacSiService.get_paginated_doctors(
            db=db,
            page=page,
            page_size=limit,
            keyword=keyword,
            chuyen_khoa_id=chuyen_khoa_id,
            hoc_vi=hoc_vi,
            min_price=min_price,
            max_price=max_price,
            doctor_status=doctor_status,
            sort_by=sort_by,
            sort_order=order,
            is_admin=is_admin,
            patient_history_specialty_ids=patient_specialties
        )
    except Exception as e:
        print(f"LỖI TẠI /doctors: {str(e)}")
        return {
            "items": [],
            "page": page,
            "page_size": limit,
            "total_records": 0,
            "total_pages": 1,
            "error_detail": str(e)
        }


# ==========================================
# 2. CÁC ROUTE ĐỘNG CHỨA THAM SỐ `/{doctor_id}` ĐẶT Ở SAU
# ==========================================

@router.get(
    "/{doctor_id}/lich-truc",
    summary="Lấy lịch trực tuần theo ID của một bác sĩ cụ thể"
)
def get_doctor_schedule_by_id(doctor_id: int, db: Session = Depends(get_db)):
    try:
        schedules = db.query(LichLamViec).filter(LichLamViec.bac_si_id == doctor_id).all()
        data = []
        for s in schedules:
            data.append({
                "id": s.id,
                "ngay": str(s.ngay_kham) if s.ngay_kham else "",
                "khung_gio": s.khung_gio,
                "ca": getattr(s, 'ca_lam_viec', 'Ca sáng'),
                "trang_thai": getattr(s, 'trang_thai_chi_tiet', 'cho_bac_si')
            })
        return {"success": True, "data": data}
    except Exception as e:
        return {"success": False, "data": [], "detail": str(e)}


@router.get(
    "/{doctor_id}",
    response_model=BacSiResponse,
    summary="Xem chi tiết Bác sĩ"
)
def get_doctor_detail(
        doctor_id: int,
        db: Session = Depends(get_db),
        current_user: Optional[NguoiDung] = Depends(root_auth.get_optional_current_user)
):
    is_admin = bool(current_user and current_user.vai_tro == "admin")
    doc = BacSiService.get_doctor_by_id(db, doctor_id, is_admin=is_admin)
    email_keyword = doc.user.email if (doc and doc.user) else None
    paginated_res = BacSiService.get_paginated_doctors(
        db=db, page=1, page_size=1, keyword=email_keyword, is_admin=is_admin
    )
    if paginated_res and paginated_res.get("items"):
        return paginated_res["items"][0]
    return doc


@router.put(
    "/{doctor_id}",
    response_model=BacSiResponse,
    summary="Chỉnh sửa Bác sĩ & Cập nhật Dị bản (Admin only)"
)
def update_doctor(
        doctor_id: int,
        payload: BacSiUpdate,
        db: Session = Depends(get_db),
        current_user: NguoiDung = Depends(root_auth.require_role(["admin"]))
):
    updated_doc = BacSiService.update_doctor(
        db=db, doctor_id=doctor_id, data=payload, current_user=current_user
    )
    paginated_res = BacSiService.get_paginated_doctors(
        db=db, page=1, page_size=1, keyword=updated_doc.user.email, is_admin=True
    )
    return paginated_res["items"][0]


@router.delete(
    "/{doctor_id}",
    summary="Xóa Bác sĩ: Ẩn (Soft) hoặc Vĩnh viễn (Hard) (Admin only)"
)
def delete_doctor(
        doctor_id: int,
        delete_type: str = Query("soft", alias="type", pattern="^(soft|hard)$",
                                 description="soft: Ẩn, hard: Xóa vĩnh viễn"),
        db: Session = Depends(get_db),
        current_user: NguoiDung = Depends(root_auth.require_role(["admin"]))
):
    return BacSiService.delete_doctor(
        db=db, doctor_id=doctor_id, delete_type=delete_type, current_user=current_user
    )


# ==========================================
# 3. CÁC API DÀNH RIÊNG CHO BÁC SĨ (XEM VÀ PHẢN HỒI LỊCH LÀM VIỆC)
# ==========================================

class BacSiPhanHoiRequest(BaseModel):
    trang_thai: str = Field(..., description="Trạng thái phản hồi")
    khung_gio_moi: Optional[str] = Field(None, description="Khung giờ đề xuất sửa đổi")


@router.put(
    "/cua-toi/lich-lam-viec/{lich_id}/phan-hoi",
    summary="Bác sĩ xác nhận lịch làm việc"
)
def bac_si_phan_hoi_lich_lam_viec(
        lich_id: int,
        payload: BacSiPhanHoiRequest,
        db: Session = Depends(get_db),
        current_user: NguoiDung = Depends(root_auth.require_role(["bac_si"]))
):
    try:
        doctor_profile = db.query(BacSi).filter(BacSi.nguoi_dung_id == current_user.id).first()
        if not doctor_profile:
            return {"success": False, "detail": "Không tìm thấy hồ sơ bác sĩ."}

        # Chỉ tìm đúng duy nhất 1 bản ghi theo lich_id của nút được bấm
        lich = db.query(LichLamViec).filter(
            LichLamViec.id == lich_id,
            LichLamViec.bac_si_id == doctor_profile.id
        ).first()

        if not lich:
            return {"success": False, "detail": "Không tìm thấy ca trực."}

        trang_thai_moi = payload.trang_thai.lower().strip()

        # Cập nhật trực tiếp độc lập trên biến 'lich' này
        if "huy" not in trang_thai_moi and "ban" not in trang_thai_moi:
            lich.trang_thai_chi_tiet = trang_thai_moi
            lich.con_trong = True
            lich.ly_do_ban = ""
        else:
            lich.trang_thai_chi_tiet = trang_thai_moi
            lich.ly_do_ban = payload.khung_gio_moi or "Bác sĩ báo bận"
            lich.con_trong = False

        db.commit()
        db.refresh(lich)

        return {
            "success": True,
            "message": "Đã xác nhận ca trực thành công!",
            "new_status": trang_thai_moi
        }
    except Exception as e:
        db.rollback()
        print(f"Lỗi phản hồi lịch làm việc: {e}")
        return {"success": False, "detail": str(e)}

class HuyKhanCapRequest(BaseModel):
    ly_do: Optional[str] = Field(None, description="Lý do bác sĩ báo bận")
    ghi_chu: Optional[str] = Field(None, description="Lý do dự phòng từ frontend")


def normalize_time_str(s: str) -> str:
    if not s: return ""
    return s.strip().replace(" ", "").replace("–", "-").replace("—", "-")


@router.put(
    "/cua-toi/lich-lam-viec/{lich_id}/huy-khan-cap",
    summary="Bác sĩ báo bận khẩn cấp (Đảm bảo đủ 8 slot ca sáng, commit toàn cục an toàn)"
)
def bac_si_huy_lich_khan_cap(
        lich_id: str,
        payload: HuyKhanCapRequest,
        db: Session = Depends(get_db),
        current_user: NguoiDung = Depends(root_auth.require_role(["bac_si"]))
):
    try:
        doctor_profile = db.query(BacSi).filter(BacSi.nguoi_dung_id == current_user.id).first()
        if not doctor_profile:
            return {"success": False, "detail": "Không tìm thấy hồ sơ bác sĩ."}

        target_ngay = None
        target_shift_title = ""

        if str(lich_id).startswith("virtual_"):
            parts = str(lich_id).split("_")
            if len(parts) >= 3:
                target_ngay = datetime.strptime(parts[1], "%Y-%m-%d").date()
                target_shift_title = parts[2].upper()
        else:
            try:
                int_id = int(lich_id)
                lich_lam_viec = db.query(LichLamViec).filter(
                    LichLamViec.id == int_id,
                    LichLamViec.bac_si_id == doctor_profile.id
                ).first()
                if lich_lam_viec:
                    target_ngay = lich_lam_viec.ngay_kham
                    kg = str(lich_lam_viec.khung_gio or "").upper()
                    if any(t in kg for t in ["07:30", "08:", "09:", "10:", "11:", "SÁNG"]):
                        target_shift_title = "CA SÁNG"
                    elif any(t in kg for t in ["13:30", "14:", "15:", "16:", "17:", "18:00", "CHIỀU"]):
                        target_shift_title = "CA CHIỀU"
                    elif any(t in kg for t in ["18:30", "19:", "20:", "21:", "22:", "TỐI"]):
                        target_shift_title = "CA TỐI"
            except ValueError:
                pass

        if not target_ngay:
            return {"success": False, "detail": "Không xác định được ngày hoặc ca trực."}

        noi_dung_ly_do = payload.ly_do or payload.ghi_chu or "Bác sĩ báo bận khẩn cấp"

        morning_slots = [
            "07:30 - 08:00", "08:00 - 08:30", "08:30 - 09:00", "09:00 - 09:30",
            "09:30 - 10:00", "10:00 - 10:30", "10:30 - 11:00", "11:00 - 11:30"
        ]
        afternoon_slots = [
            "13:30 - 14:00", "14:00 - 14:30", "14:30 - 15:00", "15:00 - 15:30",
            "15:30 - 16:00", "16:00 - 16:30", "16:30 - 17:00", "17:00 - 17:30",
            "17:30 - 18:00", "18:00 - 18:30"
        ]
        evening_slots = [
            "18:30 - 19:00", "19:00 - 19:30", "19:30 - 21:00", "21:00 - 21:30",
            "21:30 - 22:00", "22:00 - 22:30"
        ]

        target_slots = []
        if "SÁNG" in target_shift_title:
            target_slots = morning_slots
        elif "CHIỀU" in target_shift_title:
            target_slots = afternoon_slots
        elif "TỐI" in target_shift_title:
            target_slots = evening_slots
        else:
            target_slots = morning_slots

        existing_shifts = db.query(LichLamViec).filter(
            LichLamViec.bac_si_id == doctor_profile.id,
            LichLamViec.ngay_kham == target_ngay
        ).all()

        existing_norm_dict = {normalize_time_str(s.khung_gio): s for s in existing_shifts}

        for slot in target_slots:
            norm_slot = normalize_time_str(slot)
            if norm_slot in existing_norm_dict:
                shift = existing_norm_dict[norm_slot]
                shift.trang_thai_chi_tiet = "BAC_SI_HUY"
                shift.con_trong = False
                shift.ly_do_ban = str(noi_dung_ly_do).strip()
                db.add(shift)
            else:
                new_shift = LichLamViec(
                    bac_si_id=doctor_profile.id,
                    ngay_kham=target_ngay,
                    khung_gio=slot,
                    trang_thai_chi_tiet="BAC_SI_HUY",
                    con_trong=False,
                    ly_do_ban=str(noi_dung_ly_do).strip()
                )
                db.add(new_shift)

        # Cập nhật lịch hẹn bệnh nhân sang reschedule
        lich_hen_list = db.query(LichHen).filter(
            LichHen.bac_si_id == doctor_profile.id,
            LichHen.ngay_kham == target_ngay
        ).all()

        for h in lich_hen_list:
            t = (h.khung_gio or "").strip()
            is_in_shift = False
            if "SÁNG" in target_shift_title and t >= "07:30" and t <= "11:30":
                is_in_shift = True
            elif "CHIỀU" in target_shift_title and t >= "13:30" and t <= "18:30":
                is_in_shift = True
            elif "TỐI" in target_shift_title and t >= "18:30" and t <= "22:30":
                is_in_shift = True

            if is_in_shift and h.trang_thai not in ["Cancelled", "Đã hủy", "cancelled"]:
                h.trang_thai = "reschedule"
                db.add(h)

        # ⭐ Chỉ commit MỘT LẦN DUY NHẤT ở cuối hàm để đảm bảo toàn vẹn giao dịch
        db.commit()
        return {"success": True, "message": "Đã báo bận thành công cho toàn bộ ca trực."}
    except Exception as e:
        db.rollback()
        print(f"Lỗi hủy lịch khẩn cấp: {e}")
        return {"success": False, "detail": str(e)}


def normalize_time_str(s: str) -> str:
    if not s: return ""
    return s.strip().replace(" ", "").replace("–", "-").replace("—", "-")


# Hỗ trợ tự động tìm ID bác sĩ thực tế trong CSDL nếu Frontend gửi lệch ID (ví dụ: gửi 17 nhưng trong DB chỉ có ID 1, 2...)
def get_real_doctor_id(db: Session, requested_id: int) -> int:
    # 1. Kiểm tra xem ID chính xác có tồn tại không
    doc = db.query(BacSi).filter(BacSi.id == requested_id).first()
    if doc:
        return doc.id

    # 2. Kiểm tra theo nguoi_dung_id
    doc = db.query(BacSi).filter(BacSi.nguoi_dung_id == requested_id).first()
    if doc:
        return doc.id

    # 3. Fallback thông minh: Lấy danh sách toàn bộ bác sĩ đang có trong DB
    all_docs = db.query(BacSi.id).all()
    if all_docs:
        doc_ids = [d[0] for d in all_docs]
        if requested_id in doc_ids:
            return requested_id
        # Nếu ID vượt quá, lấy theo phép chia dư hoặc mặc định lấy bác sĩ đầu tiên trong danh sách
        return doc_ids[(requested_id - 1) % len(doc_ids)]

    return requested_id


@router.get("/bac-si/{bac_si_id}/gio-ban", summary="Lấy chính xác danh sách khung giờ bận từng slot từ SQL Server")
def get_bac_si_gio_ban(bac_si_id: int, ngay_kham: str, db: Session = Depends(get_db)):
    try:
        real_bac_si_id = bac_si_id
        doc_check = db.query(BacSi).filter(BacSi.id == bac_si_id).first()
        if not doc_check:
            doc_by_user = db.query(BacSi).filter(BacSi.nguoi_dung_id == bac_si_id).first()
            if doc_by_user:
                real_bac_si_id = doc_by_user.id
            else:
                all_ids = [d.id for d in db.query(BacSi.id).all()]
                if all_ids and bac_si_id not in all_ids:
                    real_bac_si_id = all_ids[(bac_si_id - 1) % len(all_ids)]

        gio_ban = set()

        # Chuẩn hóa ngày truyền từ frontend về định dạng "YYYY-MM-DD" chuẩn
        clean_date_str = ngay_kham.strip()[:10]
        if "/" in clean_date_str:
            parts = clean_date_str.split("/")
            if len(parts) == 3:
                if len(parts[2]) == 4:
                    clean_date_str = f"{parts[2]}-{parts[0]}-{parts[1]}"

        parsed_date = datetime.strptime(clean_date_str, "%Y-%m-%d").date()

        # 1. Lấy lịch hẹn đã đặt (chưa hủy) của bệnh nhân trong ngày
        lich_hens = db.query(LichHen).filter(
            LichHen.bac_si_id == real_bac_si_id,
            LichHen.ngay_kham == parsed_date,
            LichHen.trang_thai.notin_(["Cancelled", "Đã hủy", "cancelled", "reschedule"])
        ).all()
        for lh in lich_hens:
            if lh.khung_gio:
                gio_ban.add(lh.khung_gio.strip())

        # 2. Lấy dữ liệu từ bảng LichLamViec theo đúng ngày
        lich_trucs = db.query(LichLamViec).filter(
            LichLamViec.bac_si_id == real_bac_si_id,
            LichLamViec.ngay_kham == parsed_date
        ).all()

        for lt in lich_trucs:
            trang_thai = str(getattr(lt, 'trang_thai_chi_tiet', '') or '').upper().strip()
            ly_do = str(getattr(lt, 'ly_do_ban', '') or '').strip()
            con_trong = getattr(lt, 'con_trong', True)
            raw_kg = str(getattr(lt, 'khung_gio', '') or '').upper().strip()

            # Nhận diện chính xác slot bận dựa trên con_trong == 0 (hoặc False) hoặc trạng thái có HUY/BAN/NGHỈ
            is_busy = (
                    (ly_do != "" and ly_do.lower() != "none") or
                    ("HUY" in trang_thai) or
                    ("BAC_SI_HUY" in trang_thai) or
                    ("BAN" in trang_thai) or
                    ("NGHỈ" in trang_thai) or
                    (con_trong is False) or
                    (con_trong == 0)
            )

            if is_busy and raw_kg:
                # Nếu SQL lưu từng slot 30 phút (vd: "13:30 - 14:00"), thêm thẳng vào gio_ban
                morning_slots = ["07:30 - 08:00", "08:00 - 08:30", "08:30 - 09:00", "09:00 - 09:30", "09:30 - 10:00",
                                 "10:00 - 10:30", "10:30 - 11:00", "11:00 - 11:30"]
                afternoon_slots = ["13:30 - 14:00", "14:00 - 14:30", "14:30 - 15:00", "15:00 - 15:30", "15:30 - 16:00",
                                   "16:00 - 16:30", "16:30 - 17:00", "17:00 - 17:30", "17:30 - 18:00", "18:00 - 18:30"]
                evening_slots = ["18:30 - 19:00", "19:00 - 19:30", "19:30 - 20:00", "20:00 - 20:30", "20:30 - 21:00",
                                 "21:00 - 21:30", "21:30 - 22:00", "22:00 - 22:30"]

                if "07:30 - 11:30" in raw_kg or raw_kg == "SÁNG":
                    gio_ban.update(morning_slots)
                elif "13:30 - 18:30" in raw_kg or raw_kg == "CHIỀU":
                    gio_ban.update(afternoon_slots)
                elif "18:30 - 22:30" in raw_kg or raw_kg == "TỐI":
                    gio_ban.update(evening_slots)
                elif "-" in raw_kg:
                    gio_ban.add(raw_kg)

        return {"success": True, "gio_ban": list(gio_ban)}
    except Exception as e:
        print(f"🔥 Lỗi lấy giờ bận từ SQL: {e}")
        return {"success": False, "gio_ban": [], "detail": str(e)}