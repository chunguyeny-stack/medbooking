import os
import sys
# Tự động nạp thư mục chứa file hiện tại vào đường dẫn tìm kiếm của Python
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

import math
from datetime import datetime, timedelta
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc, asc
from passlib.context import CryptContext

from database import get_db
from models import NguoiDung, BacSi, BacSiDiBan, ChuyenKhoa, LichHen
from schemas import (
    DoctorCreateRequest, DoctorUpdateRequest,
    DoctorItemResponse, DoctorListResponse
)
# ... các phần còn lại giữ nguyên

# Import tương thích cả mô hình thư mục ngang cấp và module package
try:
    from app.database.database import get_db
    from app.models.models import NguoiDung, BacSi, BacSiDiBan, ChuyenKhoa, LichHen
    from app.schemas.schemas import (
        DoctorCreateRequest, DoctorUpdateRequest,
        DoctorItemResponse, DoctorListResponse
    )
except ImportError:
    from database import get_db
    from models import NguoiDung, BacSi, BacSiDiBan, ChuyenKhoa, LichHen
    from schemas import (
        DoctorCreateRequest, DoctorUpdateRequest,
        DoctorItemResponse, DoctorListResponse
    )

# Hàm kiểm tra quyền giả lập (mock) nếu chưa cấu hình JWT thực tế
try:
    from app.services.auth import get_current_user
except ImportError:
    try:
        from auth import get_current_user
    except ImportError:
        class MockUser:
            user_id = 1
            vai_tro = "admin"

        def get_current_user():
            return MockUser()

router = APIRouter(prefix="/bac-si", tags=["Nghiệp vụ Bác sĩ"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _format_doctor_dict(bs: BacSi, user_history_ck: Optional[List[int]] = None) -> dict:
    """Đóng gói dữ liệu bác sĩ, tính toán các nhãn thông minh (Badges) cho UI Bệnh nhân"""
    user = bs.nguoi_dung
    badges = []

    # 1. Nhãn 'Hot' nếu đặt nhiều hoặc rating cao
    if bs.rating >= 4.8 or (hasattr(bs, "so_luot_dat") and (bs.so_luot_dat or 0) >= 50):
        badges.append("Hot")

    # 2. Nhãn 'New' cho bác sĩ tạo mới trong 30 ngày
    if user and user.created_at and (datetime.utcnow() - user.created_at <= timedelta(days=30)):
        badges.append("New")

    # 3. Nhãn 'Liên quan' nếu cùng chuyên khoa với tiền sử bệnh nhân
    if user_history_ck and bs.ma_chuyen_khoa in user_history_ck:
        badges.append("Liên quan")

    return {
        "ma_bac_si": bs.ma_bac_si,
        "ho_ten": user.ho_ten if user else "",
        "email": user.email if user else "",
        "so_dien_thoai": user.so_dien_thoai if user else None,
        "ma_chuyen_khoa": bs.ma_chuyen_khoa,
        "ten_chuyen_khoa": bs.chuyen_khoa.ten_chuyen_khoa if bs.chuyen_khoa else None,
        "hoc_vi": bs.hoc_vi,
        "kinh_nghiem": bs.kinh_nghiem,
        "gia_kham": float(bs.gia_kham),
        "rating": bs.rating,
        "trang_thai": user.trang_thai if user else True,
        "status_label": "Hoạt động" if (user and user.trang_thai) else "Đã ẩn/Soft Deleted",
        "badges": badges,
        "di_ban": bs.di_ban_list if hasattr(bs, "di_ban_list") else [],
        "created_at": user.created_at if user else None,
        "updated_at": user.updated_at if user else None,
        "created_by": user.created_by if user else None,
        "updated_by": user.updated_by if user else None
    }


# ==========================================
# 1. THÊM MỚI BÁC SĨ & DỊ BẢN (CHỈ ADMIN)
# ==========================================
@router.post("", response_model=DoctorItemResponse, status_code=status.HTTP_201_CREATED)
def create_doctor(
    request: DoctorCreateRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if current_user.vai_tro != "admin":
        raise HTTPException(status_code=403, detail="Chỉ Quản trị viên (Admin) mới có quyền thêm Bác sĩ")

    # Kiểm tra trùng email
    if db.query(NguoiDung).filter(NguoiDung.email == request.email).first():
        raise HTTPException(status_code=400, detail="Email này đã được sử dụng")

    # Kiểm tra chuyên khoa
    ck = db.query(ChuyenKhoa).filter(ChuyenKhoa.ma_chuyen_khoa == request.ma_chuyen_khoa).first()
    if not ck:
        raise HTTPException(status_code=404, detail="Chuyên khoa không tồn tại")

    # 1. Tạo tài khoản User
    new_user = NguoiDung(
        email=request.email,
        mat_khau=pwd_context.hash(request.mat_khau),
        ho_ten=request.ho_ten,
        so_dien_thoai=request.so_dien_thoai,
        vai_tro="bac_si",
        trang_thai=True,
        created_by=current_user.user_id,
        updated_by=current_user.user_id
    )
    db.add(new_user)
    db.flush()

    # 2. Tạo hồ sơ Bác sĩ (khóa chính lấy từ user_id)
    new_doctor = BacSi(
        ma_bac_si=new_user.user_id,
        ma_chuyen_khoa=request.ma_chuyen_khoa,
        hoc_vi=request.hoc_vi,
        kinh_nghiem=request.kinh_nghiem,
        gia_kham=request.gia_kham,
        rating=5.0,
        so_luot_dat=0
    )
    db.add(new_doctor)
    db.flush()

    # 3. Thêm các thuộc tính phụ thuộc (Dị bản/Cơ sở/Khung giờ phụ)
    if request.di_ban:
        for item in request.di_ban:
            db_diban = BacSiDiBan(
                ma_bac_si=new_doctor.ma_bac_si,
                ten_chi_nhanh_co_so=item.ten_chi_nhanh_co_so,
                chuyen_khoa_phu=item.chuyen_khoa_phu,
                khung_gio_phu=item.khung_gio_phu,
                dia_chi=item.dia_chi
            )
            db.add(db_diban)

    db.commit()
    db.refresh(new_doctor)
    # Trả về đối tượng để FE lập tức Prepend lên đầu trang UI (Top-of-list)
    return _format_doctor_dict(new_doctor)


# ==========================================
# 2. LẤY DANH SÁCH BÁC SĨ (SORT, FILTER, PAGING)
# ==========================================
@router.get("", response_model=DoctorListResponse)
def get_doctors(
    page: int = Query(1, ge=1, description="Trang hiện tại"),
    limit: int = Query(10, ge=1, le=100, description="Số lượng bản ghi/trang"),
    search: Optional[str] = Query(None, description="Tìm theo tên, email, SĐT"),
    status: Optional[int] = Query(None, description="0: Đã ẩn, 1: Hoạt động (chỉ Admin)"),
    ma_chuyen_khoa: Optional[int] = Query(None, description="Lọc theo mã chuyên khoa"),
    min_price: Optional[float] = Query(None, description="Giá khám tối thiểu"),
    max_price: Optional[float] = Query(None, description="Giá khám tối đa"),
    hoc_vi: Optional[str] = Query(None, description="Học hàm, học vị"),
   sort_by: str = Query("created_at", pattern="^(created_at|updated_at|ho_ten|gia_kham|rating)$"),
   order: str = Query("desc", pattern="^(asc|desc)$"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    query = db.query(BacSi).join(NguoiDung, BacSi.ma_bac_si == NguoiDung.user_id)

    # Phân quyền: Bệnh nhân chỉ thấy status = 1 (Active). Admin xem tất cả
    if current_user.vai_tro != "admin":
        query = query.filter(NguoiDung.trang_thai == True)
    else:
        if status is not None:
            query = query.filter(NguoiDung.trang_thai == (status == 1))

    # Bộ lọc tìm kiếm từ khóa
    if search:
        search_kw = f"%{search}%"
        query = query.filter(
            or_(
                NguoiDung.ho_ten.ilike(search_kw),
                NguoiDung.email.ilike(search_kw),
                NguoiDung.so_dien_thoai.ilike(search_kw)
            )
        )

    # Bộ lọc theo thuộc tính
    if ma_chuyen_khoa:
        query = query.filter(BacSi.ma_chuyen_khoa == ma_chuyen_khoa)
    if min_price is not None:
        query = query.filter(BacSi.gia_kham >= min_price)
    if max_price is not None:
        query = query.filter(BacSi.gia_kham <= max_price)
    if hoc_vi:
        query = query.filter(BacSi.hoc_vi.ilike(f"%{hoc_vi}%"))

    # Sắp xếp theo tiêu chí
    col_map = {
        "created_at": NguoiDung.created_at,
        "updated_at": NguoiDung.updated_at,
        "ho_ten": NguoiDung.ho_ten,
        "gia_kham": BacSi.gia_kham,
        "rating": BacSi.rating
    }
    target_col = col_map.get(sort_by, NguoiDung.created_at)
    query = query.order_by(desc(target_col) if order.lower() == "desc" else asc(target_col))

    # Phân trang
    total_records = query.count()
    total_pages = math.ceil(total_records / limit) if total_records > 0 else 1
    offset = (page - 1) * limit
    results = query.offset(offset).limit(limit).all()

    return {
        "data": [_format_doctor_dict(bs) for bs in results],
        "meta": {
            "page": page,
            "limit": limit,
            "total_records": total_records,
            "total_pages": total_pages
        }
    }


# ==========================================
# 3. CHI TIẾT BÁC SĨ THEO ID
# ==========================================
@router.get("/{doctor_id}", response_model=DoctorItemResponse)
def get_doctor_detail(doctor_id: int, db: Session = Depends(get_db)):
    bs = db.query(BacSi).filter(BacSi.ma_bac_si == doctor_id).first()
    if not bs:
        raise HTTPException(status_code=404, detail="Không tìm thấy bác sĩ")
    return _format_doctor_dict(bs)


# ==========================================
# 4. CHỈNH SỬA BÁC SĨ & DỊ BẢN
# ==========================================
@router.put("/{doctor_id}", response_model=DoctorItemResponse)
def update_doctor(
    doctor_id: int,
    request: DoctorUpdateRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if current_user.vai_tro != "admin" and current_user.user_id != doctor_id:
        raise HTTPException(status_code=403, detail="Bạn không có quyền chỉnh sửa hồ sơ này")

    doctor = db.query(BacSi).filter(BacSi.ma_bac_si == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Không tìm thấy bác sĩ")

    user = doctor.nguoi_dung
    if request.ho_ten is not None:
        user.ho_ten = request.ho_ten
    if request.so_dien_thoai is not None:
        user.so_dien_thoai = request.so_dien_thoai
    if request.ma_chuyen_khoa is not None:
        doctor.ma_chuyen_khoa = request.ma_chuyen_khoa
    if request.hoc_vi is not None:
        doctor.hoc_vi = request.hoc_vi
    if request.kinh_nghiem is not None:
        doctor.kinh_nghiem = request.kinh_nghiem
    if request.gia_kham is not None:
        doctor.gia_kham = request.gia_kham

    # Lưu vết chỉnh sửa
    user.updated_at = datetime.utcnow()
    user.updated_by = current_user.user_id

    # Cập nhật danh sách dị bản phụ thuộc: Ghi đè bằng danh sách mới
    if request.di_ban is not None:
        db.query(BacSiDiBan).filter(BacSiDiBan.ma_bac_si == doctor_id).delete()
        for item in request.di_ban:
            db_diban = BacSiDiBan(
                ma_bac_si=doctor_id,
                ten_chi_nhanh_co_so=item.ten_chi_nhanh_co_so,
                chuyen_khoa_phu=item.chuyen_khoa_phu,
                khung_gio_phu=item.khung_gio_phu,
                dia_chi=item.dia_chi
            )
            db.add(db_diban)

    db.commit()
    db.refresh(doctor)
    return _format_doctor_dict(doctor)


# ==========================================
# 5. XÓA BÁC SĨ (SOFT & HARD DELETE - ADMIN)
# ==========================================
@router.delete("/{doctor_id}")
def delete_doctor(
    doctor_id: int,
    type: str = Query("soft", pattern="^(soft|hard)$", description="Loại xóa: soft (ẩn) hoặc hard (vĩnh viễn)"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if current_user.vai_tro != "admin":
        raise HTTPException(status_code=403, detail="Chỉ Quản trị viên (Admin) mới có quyền thực hiện xóa")

    doctor = db.query(BacSi).filter(BacSi.ma_bac_si == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Không tìm thấy bác sĩ")

    if type == "soft":
        # Xóa ẩn: Chỉ chuyển cờ hiển thị sang 0
        doctor.nguoi_dung.trang_thai = False
        doctor.nguoi_dung.updated_at = datetime.utcnow()
        doctor.nguoi_dung.updated_by = current_user.user_id
        db.commit()
        return {"status": "success", "message": "Đã ẩn bác sĩ khỏi danh sách (Soft Delete)"}

    elif type == "hard":
        # Xóa vĩnh viễn: Kiểm tra các lịch hẹn đang xử lý
        active_booking = db.query(LichHen).filter(
            LichHen.ma_bac_si == doctor_id,
            LichHen.trang_thai.in_(["Pending", "Confirmed", "In Progress"])
        ).first()

        if active_booking:
            raise HTTPException(
                status_code=400,
                detail="Cảnh báo: Bác sĩ đang có lịch hẹn đang chờ/đang khám. Không thể xóa vĩnh viễn!"
            )

        db.delete(doctor.nguoi_dung)  # Xóa cascade toàn bộ hồ sơ bác sĩ và các dị bản
        db.commit()
        return {"status": "success", "message": "Đã xóa vĩnh viễn bác sĩ khỏi cơ sở dữ liệu (Hard Delete)"}
