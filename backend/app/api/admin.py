import importlib
from typing import Optional
from decimal import Decimal
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from datadase.database import get_db
from models.models import NguoiDung
from services.admin import AdminService

root_auth = importlib.import_module("auth")

router = APIRouter(prefix="/admin", tags=["Phân hệ Admin"])


class ChuyenKhoaCreateRequest(BaseModel):
    ten_chuyen_khoa: str
    mo_ta: Optional[str] = None


class DichVuCreateRequest(BaseModel):
    ten_dich_vu: str
    gia_dich_vu: Decimal
    mo_ta: Optional[str] = None


@router.get("/dashboard-stats", summary="Thống kê doanh thu, lợi nhuận theo kỳ và chi tiết giao dịch")
def get_dashboard_quarterly_stats(
    year: int = Query(2026, description="Năm thống kê"),
    quarter: Optional[str] = Query(None, description="Q1, Q2, Q3, Q4 hoặc để trống để xem cả năm"),
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(root_auth.require_role(["admin"]))
):
    _ = current_user
    return AdminService.get_quarterly_dashboard(db=db, year=year, quarter=quarter)


@router.get("/users", summary="Danh sách người dùng theo vai trò")
def list_users(
    role: Optional[str] = Query(None, description="benh_nhan, bac_si, le_tan, admin"),
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(root_auth.require_role(["admin"]))
):
    _ = current_user
    users = AdminService.get_users(db=db, vai_tro=role)
    return [
        {
            "user_id": u.user_id,
            "email": u.email,
            "ho_ten": u.ho_ten,
            "so_dien_thoai": u.so_dien_thoai,
            "vai_tro": u.vai_tro,
            "trang_thai": u.trang_thai
        }
        for u in users
    ]


@router.put("/users/{user_id}/toggle-status", summary="Khóa / Mở khóa tài khoản")
def toggle_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(root_auth.require_role(["admin"]))
):
    _ = current_user
    return AdminService.toggle_user_status(db=db, user_id=user_id)


@router.post("/specialties", summary="Thêm mới chuyên khoa khám")
def add_specialty(
    payload: ChuyenKhoaCreateRequest,
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(root_auth.require_role(["admin"]))
):
    _ = current_user
    ck = AdminService.create_chuyen_khoa(db=db, ten=payload.ten_chuyen_khoa, mo_ta=payload.mo_ta)
    return {"message": "Tạo chuyên khoa thành công.", "ma_chuyen_khoa": ck.ma_chuyen_khoa}


@router.post("/services", summary="Thêm dịch vụ & bảng giá")
def add_service(
    payload: DichVuCreateRequest,
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(root_auth.require_role(["admin"]))
):
    _ = current_user
    dv = AdminService.create_dich_vu(
        db=db,
        ten=payload.ten_dich_vu,
        gia=payload.gia_dich_vu,
        mo_ta=payload.mo_ta
    )
    return {"message": "Tạo dịch vụ thành công.", "ma_dich_vu": dv.ma_dich_vu}
