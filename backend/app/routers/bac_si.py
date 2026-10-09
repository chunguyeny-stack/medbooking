import math
from datetime import datetime
from typing import Optional
from app.auth import get_current_user, require_role
from app.database import get_db
from fastapi import APIRouter, Depends, HTTPException, Query, status
from app.models import BacSi, BacSiVariant, NguoiDung
from app.schemas import BacSiCreate, BacSiResponse, BacSiUpdate, PaginatedBacSiResponse
from sqlalchemy import asc, desc, or_
from sqlalchemy.orm import Session

router = APIRouter(prefix="/doctors", tags=["Doctors & Variants"])


@router.post(
    "", response_model=BacSiResponse, status_code=status.HTTP_201_CREATED
)
def create_doctor(
    payload: BacSiCreate,
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(require_role(["admin", "bac_si"])),
):
  # Thêm bác sĩ mới (mặc định created_at mới nhất để đẩy lên đầu danh sách theo chiều DESC)
  new_doc = BacSi(
      name=payload.name,
      specialization=payload.specialization,
      price=payload.price,
      phone=payload.phone,
      email=payload.email,
      is_hot=payload.is_hot,
      is_new=payload.is_new,
      created_by=current_user.username,
  )
  db.add(new_doc)
  db.commit()
  db.refresh(new_doc)

  # Thêm dị bản phụ thuộc kèm theo
  if payload.variants:
    for var in payload.variants:
      sub_var = BacSiVariant(
          doctor_id=new_doc.id,
          sub_department=var.sub_department,
          working_hours=var.working_hours,
          branch_location=var.branch_location,
      )
      db.add(sub_var)
    db.commit()
    db.refresh(new_doc)

  return new_doc


@router.get("", response_model=PaginatedBacSiResponse)
def get_doctors(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    search: Optional[str] = None,
    specialization: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    sort_by: str = Query(
        "created_at",
        regex="^(created_at|updated_at|name|price|created_by|updated_by)$",
    ),
    order: str = Query("desc", regex="^(asc|desc)$"),
    db: Session = Depends(get_db),
    current_user: Optional[NguoiDung] = Depends(get_current_user),
):
  query = db.query(BacSi)

  # Phân quyền hiển thị Status: Bệnh nhân chỉ thấy status = 1, Admin thấy cả 0 và 1
  if not current_user or current_user.role == "benh_nhan":
    query = query.filter(BacSi.status == 1)

  # Tìm kiếm & Bộ lọc
  if search:
    query = query.filter(
        or_(
            BacSi.name.ilike(f"%{search}%"),
            BacSi.specialization.ilike(f"%{search}%"),
            BacSi.phone.ilike(f"%{search}%"),
            BacSi.email.ilike(f"%{search}%"),
        )
    )
  if specialization:
    query = query.filter(BacSi.specialization == specialization)
  if min_price is not None:
    query = query.filter(BacSi.price >= min_price)
  if max_price is not None:
    query = query.filter(BacSi.price <= max_price)

  # Sắp xếp (Tăng/Giảm theo tiêu chí)
  sort_column = getattr(BacSi, sort_by)
  query = (
      query.order_by(desc(sort_column))
      if order == "desc"
      else query.order_by(asc(sort_column))
  )

  # Phân trang
  total_records = query.count()
  total_pages = math.ceil(total_records / page_size) if total_records > 0 else 1
  offset = (page - 1) * page_size
  doctors = query.offset(offset).limit(page_size).all()

  return {
      "total_records": total_records,
      "total_pages": total_pages,
      "page": page,
      "page_size": page_size,
      "data": doctors,
  }


@router.put("/{doctor_id}", response_model=BacSiResponse)
def update_doctor(
    doctor_id: int,
    payload: BacSiUpdate,
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(require_role(["admin", "bac_si"])),
):
  doctor = db.query(BacSi).filter(BacSi.id == doctor_id).first()
  if not doctor:
    raise HTTPException(status_code=404, detail="Không tìm thấy bác sĩ")

  update_data = payload.dict(exclude_unset=True)
  variants_data = update_data.pop("variants", None)

  # Cập nhật thông tin gốc (Giữ nguyên ID chính)
  for key, value in update_data.items():
    setattr(doctor, key, value)

  # Lưu vết người sửa và thời gian sửa
  doctor.updated_at = datetime.utcnow()
  doctor.updated_by = current_user.username

  # Xử lý cập nhật dị bản (Xóa cũ, tạo mới ID phụ thuộc)
  if variants_data is not None:
    db.query(BacSiVariant).filter(
        BacSiVariant.doctor_id == doctor_id
    ).delete()
    for var in variants_data:
      new_var = BacSiVariant(
          doctor_id=doctor_id,
          sub_department=var["sub_department"],
          working_hours=var.get("working_hours"),
          branch_location=var.get("branch_location"),
      )
      db.add(new_var)

  db.commit()
  db.refresh(doctor)
  return doctor


@router.delete("/{doctor_id}")
def delete_doctor(
    doctor_id: int,
    delete_type: str = Query("soft", regex="^(soft|hard)$"),
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(get_current_user),
):
  doctor = db.query(BacSi).filter(BacSi.id == doctor_id).first()
  if not doctor:
    raise HTTPException(status_code=404, detail="Không tìm thấy bác sĩ")

  if delete_type == "soft":
    # Xóa ẩn: Chuyển status về 0 (Bệnh nhân không thấy, Admin thấy kèm nhãn)
    doctor.status = 0
    db.commit()
    return {"message": "Đã ẩn bác sĩ thành công (Soft Delete)"}

  elif delete_type == "hard":
    # Xóa vĩnh viễn: Chỉ Admin mới có quyền
    if current_user.role != "admin":
      raise HTTPException(
          status_code=403,
          detail="Chỉ Admin mới có quyền xóa vĩnh viễn dữ liệu",
      )
    db.delete(doctor)
    db.commit()
    return {"message": "Đã xóa vĩnh viễn bác sĩ khỏi cơ sở dữ liệu"}