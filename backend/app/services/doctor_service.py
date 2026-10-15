from sqlalchemy.orm import Session
from datetime import datetime
from app.models.doctor import Doctor
from app.schemas.doctor import DoctorCreate, DoctorUpdate

# === THÊM bác sĩ ===
def create_doctor(db: Session, data: DoctorCreate):
    new_doc = Doctor(**data.dict())
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)
    return new_doc

# === XÓA 2 chế độ ===
def soft_delete_doctor(db: Session, doc_id: int, admin_id: int):
    doc = db.query(Doctor).filter(Doctor.id == doc_id, Doctor.is_deleted == False).first()
    if not doc: return None
    doc.is_deleted = True
    doc.deleted_at = datetime.utcnow()
    doc.deleted_by = admin_id
    db.commit()
    return {"message": "Đã ẩn bác sĩ (xóa mềm)", "id": doc_id}

def hard_delete_doctor(db: Session, doc_id: int):
    doc = db.query(Doctor).filter(Doctor.id == doc_id).first()
    if not doc: return None
    db.delete(doc)
    db.commit()
    return {"message": "Đã xóa hoàn toàn", "id": doc_id}

# === SỬA ===
def update_doctor(db: Session, doc_id: int, data: DoctorUpdate):
    doc = db.query(Doctor).filter(Doctor.id == doc_id, Doctor.is_deleted == False).first()
    if not doc: return None
    for field, val in data.dict(exclude_unset=True).items():
        setattr(doc, field, val)
    doc.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(doc)
    return doc

# === SẮP XẾP + TÌM KIẾM + PHÂN TRANG ===
def get_doctors_list(db: Session, skip: int=0, limit: int=10,
                     sort_by: str="created_at", order: str="desc",
                     search: str=None, specialty: str=None,
                     min_price: float=None, max_price: float=None,
                     view_mode: str="all", show_deleted: bool=False):
    q = db.query(Doctor)
    
    # Bộ lọc xóa
    if not show_deleted:
        q = q.filter(Doctor.is_deleted == False)

    # Tìm kiếm
    if search:
        q = q.filter(Doctor.full_name.ilike(f"%{search}%"))
    if specialty:
        q = q.filter(Doctor.specialty.ilike(f"%{specialty}%"))
    if min_price:
        q = q.filter(Doctor.price >= min_price)
    if max_price:
        q = q.filter(Doctor.price <= max_price)

    # Hiển thị hot/new/liên quan
    if view_mode == "hot":
        q = q.filter(Doctor.is_hot == True)
    elif view_mode == "new":
        q = q.order_by(Doctor.created_at.desc())

    # Sắp xếp
    sort_map = {
        "rating": Doctor.rating_avg,
        "created_at": Doctor.created_at,
        "updated_at": Doctor.updated_at,
        "price": Doctor.price
    }
    sort_col = sort_map.get(sort_by, Doctor.created_at)
    if order == "asc":
        q = q.order_by(sort_col.asc())
    else:
        q = q.order_by(sort_col.desc())

    total = q.count()
    items = q.offset(skip).limit(limit).all()
    return {"total": total, "page": skip//limit+1, "page_size": limit, "items": items}
