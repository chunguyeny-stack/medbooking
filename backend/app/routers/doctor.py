from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.schemas.doctor import DoctorCreate, DoctorUpdate
from app.services.doctor_service import *
from app.utils.auth import get_current_user, require_admin

router = APIRouter(prefix="/doctors", tags=["doctors"])

# Thêm — chỉ Admin
@router.post("/")
def add(data: DoctorCreate, db: Session=Depends(get_db), curr_user=Depends(require_admin)):
    return create_doctor(db, data)

# Danh sách — BN xem ẩn; Admin xem cả đã ẩn
@router.get("/")
def list_docs(page: int=1, page_size: int=10,
              sort_by: str=Query("created_at"), order: str=Query("desc"),
              search: str=None, specialty: str=None,
              min_price: float=None, max_price: float=None,
              view_mode: str=Query("all"),
              db: Session=Depends(get_db), curr_user=Depends(get_current_user)):
    show_del = curr_user.role.role_name == "admin"
    skip = (page-1)*page_size
    return get_doctors_list(db, skip, page_size, sort_by, order,
                            search, specialty, min_price, max_price,
                            view_mode, show_deleted=show_del)

# Chi tiết — BN: xem; Admin: xem + hành động
@router.get("/{doc_id}")
def detail(doc_id: int, db: Session=Depends(get_db), curr_user=Depends(get_current_user)):
    doc = db.query(Doctor).filter(Doctor.id==doc_id).first()
    if not doc or (doc.is_deleted and curr_user.role.role_name!="admin"):
        raise HTTPException(404, "Không tìm thấy")
    return {
        **doc.__dict__,
        "can_edit": curr_user.role.role_name=="admin",
        "can_delete": curr_user.role.role_name=="admin"
    }

# Sửa — Admin
@router.put("/{doc_id}")
def edit(doc_id: int, data: DoctorUpdate, db=Depends(get_db), _=Depends(require_admin)):
    updated = update_doctor(db, doc_id, data)
    if not updated: raise HTTPException(404)
    return updated

# Xóa — có cảnh báo & 2 chế độ
@router.delete("/{doc_id}")
def remove(doc_id: int, hard: bool=False, db=Depends(get_db), curr_user=Depends(require_admin)):
    if hard:
        return hard_delete_doctor(db, doc_id)
    return soft_delete_doctor(db, doc_id, curr_user.id)
  
