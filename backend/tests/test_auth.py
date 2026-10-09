
Trò chuyện với Gemini
Setup FastAPI

Cấu hình

SQLAlchemy

Model nguoi_dung,

Model benh_nhan, Model bac_si

Pydantic schema

user/auth

API register, API

login, API me

JWT + phân quyền

Test pytest auth

Review code auth

1 actor (BS)| Thêm - dị bản kèm theo (phụ thuộc) + thêm lên

trên đầu; Xóa: ẩn thông tin của BN - admin nhìn thấy(1-0)+ remove (cảnh

báo)(xóa ẩn và xóa thẳng - admin); Sửa: Xóa + thông tin khác ID; Sắp xếp:Tăng -

giảm + ngày tạo\sửa + bởi ...; Tìm kiếm: Tên/danh mục/giá/...(filter) + Hiển thị:

hot, new, liên quan(BN) + nội dung admin + Hiển thị chi tiết BS (BN: mua sắm;

Admin: xóa, cập nhật, thoát); Phân trang: 1 trang hiển thị ...BS -> DS

trang; Quền năng Admin

Tài liệu phân tích yêu cầu nghiệp vụ (Business Requirements)

và phân định trách nhiệm Frontend - Backend chi tiết cho đối tượng **Bác sĩ

(BS)** và **Admin**. --- ## 1. Chi tiết nghiệp vụ cho Bác sĩ (BS) & Admin

### Thêm mới Bác sĩ * **Thêm dị bản (Variant / Chi nhánh / Chuyên khoa phụ thuộc):**

* Khi tạo BS mới, cho phép thêm các thuộc tính phụ thuộc (ví dụ: các cơ sở làm

việc, khung giờ khám phụ, chuyên khoa phụ). Các dị bản này phụ thuộc trực tiếp

vào ID của BS gốc. * **Quy tắc hiển thị (Thêm lên đầu):** * Khi tạo mới thành

công, bản ghi BS đó phải tự động xuất hiện **ở vị trí đầu tiên** trên danh sách

(Top/Top-of-list) mà không cần load lại toàn bộ trang. ### Xóa bản ghi * **Xóa ẩn

(Soft Delete - Dành cho người dùng / BN & BS):** * Đổi trạng thái hiển thị

của BS (`status` chuyển từ `1` sang `0`). * Bản ghi bị ẩn hoàn toàn đối với Bệnh

nhân (BN) trên giao diện giao dịch / tìm kiếm. * Admin vẫn nhìn thấy bản ghi

này trên hệ thống quản trị (kèm nhãn **Đã ẩn/Soft Deleted**). * **Xóa thẳng /

Xóa vĩnh viễn (Hard Delete - Dành riêng Admin):** * Xóa hoàn toàn dữ liệu BS khỏi

cơ sở dữ liệu (Database). * **Cảnh báo bắt buộc:** Hiển thị popup cảnh báo nguy

hiểm trước khi thực hiện (*"Hành động này sẽ xóa vĩnh viễn dữ liệu BS và

các lịch hẹn liên quan, bạn có chắc chắn không?"*). ### Chỉnh sửa Bác sĩ *

**Cơ chế cập nhật ID:** * Giữ nguyên ID chính (`BS_ID`) của BS. * Khi cập nhật

thông tin/dị bản mới: Thực hiện ghi đè hoặc tạo mới danh sách phụ thuộc kèm `ID

phụ thuộc` riêng (Thông tin mới khác ID phụ thuộc cũ). * Lịch sử sửa đổi lưu vết

lại thời gian và người cập nhật (`updated_at`, `updated_by`). ### Sắp xếp

(Sorting) Hỗ trợ sắp xếp danh sách linh hoạt theo các tiêu chí: * **Chiều:**

Tăng dần (ASC) / Giảm dần (DESC). * **Tiêu chí:** Ngày tạo (`created_at`), Ngày

sửa (`updated_at`), Người thực hiện (`created_by`, `updated_by`), Tên BS, Đánh

giá/Giá dịch vụ. ### Tìm kiếm & Bộ lọc (Search & Filter) * **Tìm kiếm

theo từ khóa (Search):** Tên bác sĩ, Danh mục / Chuyên khoa, Giá khám, Số điện

thoại / Email. * **Bộ lọc thuộc tính (Filter):** Trạng thái (Hoạt động/Đã ẩn),

Khoảng giá, Học hàm/Học vị, Chuyên khoa. ### Hiển thị & Phân quyền nội dung

#### Phía Bệnh nhân (BN) * **Nhãn nổi bật:** `Hot` (Được đặt nhiều), `New` (Bác

sĩ mới), `Liên quan` (Gợi ý theo lịch sử khám/bệnh lý BN). * **Chức năng:** Xem

thông tin, chọn dịch vụ/đặt lịch, mua sắm gói khám. #### Phía Admin

* Xem đầy đủ dữ liệu nội bộ (bao gồm nội dung ẩn `status =

0`, thông tin doanh thu, nhật ký hệ thống). * **Thao tác nhanh trên bản ghi

detail:** * **Xóa:** Xóa ẩn hoặc Xóa thẳng. * **Cập nhật:** Sửa thông tin BS. *

**Thoát / Đóng:** Trở về danh sách quản lý. ### Phân trang (Pagination) * Cho

phép cấu hình số lượng bản ghi hiển thị trên 1 trang (ví dụ: 10, 20, 50

BS/trang). * Trả về danh sách trang (`Page 1, 2, 3...`), tổng số bản ghi

(`total_records`), tổng số trang (`total_pages`). --- ## 2. Phân định nhiệm vụ

Backend vs Frontend | Chức năng | Nhiệm vụ Backend (BE) | Nhiệm vụ Frontend

(FE) | | --- | --- | --- | | **Thêm BS & Dị bản** | • Validate dữ liệu đầu

vào (tên, giá, format email...).<br> <br>• Lưu BS gốc và tạo quan hệ

Foreign Key cho các dị bản/chuyên khoa phụ.<br> <br>• Trả về bản

ghi vừa tạo kèm ID. | • Dựng form thêm mới (dynamic form cho dị bản).<br>

<br>• Gọi API `POST /doctors`.<br> <br>• Prepend (thêm) bản

ghi mới trả về vào đầu danh sách hiển thị trên UI. | | **Xóa (Ẩn & Thẳng)**

| • **Soft Delete:** Update `status = 0` trong DB.<br> <br>• **Hard

Delete:** Kiểm tra ràng buộc dữ liệu (lịch hẹn...) trước khi `DELETE

FROM`.<br> <br>• Check quyền Admin trước khi thực hiện. | • Hiển thị

Nút Xóa.<br> <br>• Bật **Modal Cảnh báo (Confirm Dialog)** xác nhận

xóa thẳng/ẩn.<br> <br>• Gọi API `DELETE

/doctors/{id}?type=soft/hard`.<br> <br>• Cập nhật DOM/State để ẩn/xóa

dòng tương ứng. | | **Chỉnh sửa** | • Nhận `BS_ID` và payload sửa.<br>

<br>• Cập nhật thông tin gốc, quản lý insert/update/delete các `ID phụ

thuộc`.<br> <br>• Tự động lưu `updated_at` và `updated_by` (lấy từ

JWT token). | • Hiển thị form edit điền sẵn data cũ.<br> <br>• Gọi

API `PUT /doctors/{id}`.<br> <br>• Cập nhật giao diện khi sửa thành

công. | | **Sắp xếp & Phân trang** | • Xử lý truy vấn SQL: `ORDER BY

{field} {ASC/DESC} LIMIT {limit} OFFSET {offset}`.<br> <br>• Trả về

danh sách + metadata (`page`, `pageSize`, `total`). | • Bắt sự kiện click cột/dropdown

chọn chiều & tiêu chí xếp.<br> <br>• Dựng UI Phân trang

(Pagination controls).<br> <br>• Truyền query param

`?page=1&limit=10&sort=created_at&order=desc` lên BE. | | **Tìm kiếm

& Bộ lọc** | • Xử lý truy vấn `LIKE` hoặc Full-text search theo tên, chuyên

khoa, lọc theo khoảng giá.<br> <br>• Lọc `status = 1` cho BN và

`status IN (0,1)` cho Admin dựa theo role token. | • Dựng ô input search &

bộ lọc dropdown/range slider.<br> <br>• Debounce ô search (chờ người

dùng gõ xong ~300ms mới gọi API). |

| **Hiển thị chi tiết & Tag** | • Tính toán logic lọc

bác sĩ `Hot`, `New`, `Liên quan` dựa trên thuật toán/lịch sử đặt lịch.<br>

<br>• Cung cấp đầy đủ thông tin admin khi request từ Admin route. | • Hiển

thị badge `Hot`, `New`, `Liên quan` lên avatar/card BS.<br> <br>•

Phân quyền UI:BN thấy nút "Đặt lịch/Mua sắm", Admin thấy thanh công cụ

"Xóa, Cập nhật, Escape". |

 

BS(dị bản:

id,khoa,ngành,...)+tên giá, format, email/////khóa chính:id////thêm BS mới(lên

đầu)

Xóa (ẩn: khách ko

thấy nhưng admin thấy, sạch:admin xóa hết)

sửa( các thuộc

tính không phải khóa chính). khoaas chính ID/// lưu(sửa bởi ai, sửa ngày nào,

giờ nào....... Làm phần backend

Dưới đây là giải pháp backend hoàn chỉnh bằng FastAPI, SQLAlchemy, Pydantic, tích hợp JWT + Phân quyền (RBAC), đầy đủ các nghiệp vụ quản lý Bác sĩ & Dị bản (thêm, xóa ẩn/thẳng, sửa lưu vết, sắp xếp, tìm kiếm, phân trang, gắn thẻ Hot/New), kèm theo Pytest và Code Review.

1. Cấu trúc thư mục dự án
Plaintext
hospital_backend/
│
├── database.py          # Kết nối Database SQLAlchemy
├── models.py            # Định nghĩa các model (NguoiDung, BenhNhan, BacSi, BacSiVariant)
├── schemas.py           # Pydantic schemas validate dữ liệu
├── auth.py              # Xử lý JWT, Password Hashing, Dependencies phân quyền
├── main.py              # Khởi tạo ứng dụng FastAPI & include routers
├── routers/
│   ├── auth.py          # API Register, Login, Me
│   └── doctors.py       # API Quản lý Bác sĩ & Dị bản (CRUD, Search, Sort, Pagination)
└── tests/
    └── test_auth.py     # Unit test pytest cho auth
2. Cấu hình Database & Models (database.py, models.py)
database.py
Python
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./hospital.db"  # Có thể đổi sang PostgreSQL/MySQL

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()
models.py
Python
from datetime import datetime
from database import Base
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class NguoiDung(Base):
  __tablename__ = "nguoi_dung"

  id = Column(Integer, primary_key=True, index=True)
  username = Column(String, unique=True, index=True, nullable=False)
  email = Column(String, unique=True, index=True, nullable=False)
  hashed_password = Column(String, nullable=False)
  role = Column(
      String, nullable=False
  )  # 'admin', 'bac_si', 'benh_nhan'
  status = Column(Integer, default=1)  # 1: Hoạt động, 0: Đã khóa/Ẩn
  created_at = Column(DateTime, default=datetime.utcnow)
  updated_at = Column(
      DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
  )


class BacSi(Base):
  __tablename__ = "bac_si"

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String, index=True, nullable=False)
  specialization = Column(String, index=True, nullable=False)  # Danh mục/Khoa
  price = Column(Float, nullable=False)  # Giá khám
  phone = Column(String, nullable=True)
  email = Column(String, nullable=True)
  status = Column(Integer, default=1)  # 1: Hoạt động, 0: Xóa ẩn (Soft Delete)
  is_hot = Column(Boolean, default=False)
  is_new = Column(Boolean, default=True)

  created_at = Column(DateTime, default=datetime.utcnow)
  created_by = Column(String, nullable=True)
  updated_at = Column(DateTime, nullable=True)
  updated_by = Column(String, nullable=True)

  # Quan hệ 1 - N với dị bản / chuyên khoa phụ thuộc
  variants = relationship(
      "BacSiVariant", back_populates="doctor", cascade="all, delete-orphan"
  )


class BacSiVariant(Base):
  __tablename__ = "bac_si_variant"

  id = Column(Integer, primary_key=True, index=True)
  doctor_id = Column(Integer, ForeignKey("bac_si.id"), nullable=False)
  sub_department = Column(String, nullable=False)  # Chuyên khoa phụ thuộc
  working_hours = Column(String, nullable=True)  # Khung giờ khám phụ
  branch_location = Column(String, nullable=True)  # Cơ sở làm việc phụ

  doctor = relationship("BacSi", back_populates="variants")
3. Pydantic Schemas (schemas.py)
Python
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr


# --- Auth & User ---
class UserCreate(BaseModel):
  username: str
  email: EmailStr
  password: str
  role: str = "benh_nhan"  # admin, bac_si, benh_nhan


class UserLogin(BaseModel):
  username: str
  password: str


class Token(BaseModel):
  access_token: str
  token_type: str


class TokenData(BaseModel):
  username: Optional[str] = None
  role: Optional[str] = None


# --- Doctor Variants ---
class BacSiVariantBase(BaseModel):
  sub_department: str
  working_hours: Optional[str] = None
  branch_location: Optional[str] = None


class BacSiVariantCreate(BacSiVariantBase):
  pass


class BacSiVariantResponse(BacSiVariantBase):
  id: int
  doctor_id: int

  class Config:
    from_attributes = True


# --- Doctor ---
class BacSiCreate(BaseModel):
  name: str
  specialization: str
  price: float
  phone: Optional[str] = None
  email: Optional[EmailStr] = None
  is_hot: Optional[bool] = False
  is_new: Optional[bool] = True
  variants: Optional[List[BacSiVariantCreate]] = []


class BacSiUpdate(BaseModel):
  name: Optional[str] = None
  specialization: Optional[str] = None
  price: Optional[float] = None
  phone: Optional[str] = None
  email: Optional[EmailStr] = None
  is_hot: Optional[bool] = None
  is_new: Optional[bool] = None
  variants: Optional[List[BacSiVariantCreate]] = (
      []
  )  # Ghi đè/cập nhật danh sách dị bản mới


class BacSiResponse(BaseModel):
  id: int
  name: str
  specialization: str
  price: float
  phone: Optional[str]
  email: Optional[str]
  status: int
  is_hot: bool
  is_new: bool
  created_at: datetime
  created_by: Optional[str]
  updated_at: Optional[datetime]
  updated_by: Optional[str]
  variants: List[BacSiVariantResponse] = []

  class Config:
    from_attributes = True


class PaginatedBacSiResponse(BaseModel):
  total_records: int
  total_pages: int
  page: int
  page_size: int
  data: List[BacSiResponse]
4. JWT & Phân quyền (auth.py)
Python
from datetime import datetime, timedelta
from database import get_db
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from models import NguoiDung
from passlib.context import CryptContext
from sqlalchemy.orm import Session

SECRET_KEY = "SUPER_SECRET_KEY_CHANGE_IN_PRODUCTION"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def verify_password(plain_password, hashed_password):
  return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
  return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta = None):
  to_encode = data.copy()
  expire = datetime.utcnow() + (
      expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  )
  to_encode.update({"exp": expire})
  return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
  credentials_exception = HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Could not validate credentials",
      headers={"WWW-Authenticate": "Bearer"},
  )
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get("sub")
    role: str = payload.get("role")
    if username is None:
      raise credentials_exception
  except jwt.PyJWTError:
    raise credentials_exception

  user = db.query(NguoiDung).filter(NguoiDung.username == username).first()
  if user is None:
    raise credentials_exception
  return user


def require_role(allowed_roles: list):
  def role_dependency(current_user: NguoiDung = Depends(get_current_user)):
    if current_user.role not in allowed_roles:
      raise HTTPException(
          status_code=status.HTTP_403_FORBIDDEN,
          detail="You do not have permission to perform this action",
      )
    return current_user

  return role_dependency
5. Routers (routers/auth.py, routers/doctors.py) & main.py
routers/auth.py
Python
from auth import (
    create_access_token,
    get_current_user,
    get_password_hash,
    verify_password,
)
from database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from models import NguoiDung
from schemas import Token, UserCreate, UserLogin
from sqlalchemy.orm import Session

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
  existing_user = (
      db.query(NguoiDung)
      .filter(
          (NguoiDung.username == user_data.username)
          | (NguoiDung.email == user_data.email)
      )
      .first()
  )
  if existing_user:
    raise HTTPException(
        status_code=400, detail="Username or email already registered"
    )

  hashed_pwd = get_password_hash(user_data.password)
  new_user = NguoiDung(
      username=user_data.username,
      email=user_data.email,
      hashed_password=hashed_pwd,
      role=user_data.role,
  )
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return {"message": "User registered successfully", "user_id": new_user.id}


@router.post("/login", response_model=Token)
def login(form_data: UserLogin, db: Session = Depends(get_db)):
  user = (
      db.query(NguoiDung)
      .filter(NguoiDung.username == form_data.username)
      .first()
  )
  if not user or not verify_password(form_data.password, user.hashed_password):
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
    )

  access_token = create_access_token(
      data={"sub": user.username, "role": user.role}
  )
  return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me")
def get_me(current_user: NguoiDung = Depends(get_current_user)):
  return {
      "id": current_user.id,
      "username": current_user.username,
      "email": current_user.email,
      "role": current_user.role,
  }
routers/doctors.py
Python
import math
from auth import get_current_user, require_role
from database import get_db
from fastapi import APIRouter, Depends, HTTPException, Query, status
from models import BacSi, BacSiVariant, NguoiDung
from schemas import BacSiCreate, BacSiResponse, BacSiUpdate, PaginatedBacSiResponse
from sqlalchemy import asc, desc, or_
from sqlalchemy.orm import Session

router = APIRouter(prefix="/doctors", tags=["Doctors & Variants"])


@post("", response_model=BacSiResponse, status_code=status.HTTP_201_CREATED)
def create_doctor(
    payload: BacSiCreate,
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(require_role(["admin", "bac_si"])),
):
  # Tạo bác sĩ mới
  new_doctor = BacSi(
      name=payload.name,
      specialization=payload.specialization,
      price=payload.price,
      phone=payload.phone,
      email=payload.email,
      is_hot=payload.is_hot,
      is_new=payload.is_new,
      created_by=current_user.username,
  )
  db.add(new_doctor)
  db.commit()
  db.refresh(new_doctor)

  # Thêm các dị bản (variants) phụ thuộc
  if payload.variants:
    for var in payload.variants:
      variant_obj = BacSiVariant(
          doctor_id=new_doctor.id,
          sub_department=var.sub_department,
          working_hours=var.working_hours,
          branch_location=var.branch_location,
      )
      db.add(variant_obj)
    db.commit()
    db.refresh(new_doctor)

  return new_doctor


@get("", response_model=PaginatedBacSiResponse)
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

  # Tìm kiếm & Filter
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

  # Sắp xếp
  sort_column = getattr(BacSi, sort_by)
  if order == "desc":
    query = query.order_by(desc(sort_column))
  else:
    query = query.order_by(asc(sort_column))

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


@put("/{doctor_id}", response_model=BacSiResponse)
def update_doctor(
    doctor_id: int,
    payload: BacSiUpdate,
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(require_role(["admin", "bac_si"])),
):
  doctor = db.query(BacSi).filter(BacSi.id == doctor_id).first()
  if not doctor:
    raise HTTPException(status_code=404, detail="Doctor not found")

  # Cập nhật thông tin gốc (Giữ nguyên khóa chính ID)
  update_data = payload.dict(exclude_unset=True)
  variants_data = update_data.pop("variants", None)

  for key, value in update_data.items():
    setattr(doctor, key, value)

  # Lưu vết người sửa, ngày sửa
  doctor.updated_at = datetime.utcnow()
  doctor.updated_by = current_user.username

  # Quản lý dị bản (Xóa cũ, tạo mới các ID phụ thuộc)
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


@delete("/{doctor_id}")
def delete_doctor(
    doctor_id: int,
    delete_type: str = Query(
        "soft", regex="^(soft|hard)$"
    ),  # soft: Xóa ẩn, hard: Xóa vĩnh viễn
    db: Session = Depends(get_db),
    current_user: NguoiDung = Depends(get_current_user),
):
  doctor = db.query(BacSi).filter(BacSi.id == doctor_id).first()
  if not doctor:
    raise HTTPException(status_code=404, detail="Doctor not found")

  if delete_type == "soft":
    # Xóa ẩn: Chuyển status về 0 (Admin và BS thực hiện)
    doctor.status = 0
    db.commit()
    return {"message": "Doctor soft-deleted successfully (status set to 0)"}

  elif delete_type == "hard":
    # Xóa thẳng: Chỉ Admin mới có quyền thực hiện
    if current_user.role != "admin":
      raise HTTPException(
          status_code=403,
          detail="Only Admin can perform hard delete with warning",
      )
    db.delete(doctor)
    db.commit()
    return {"message": "Doctor permanently deleted from database"}
main.py
Python
from database import Base, engine
from fastapi import FastAPI
from routers import auth, doctors

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Hospital Management Backend API",
    version="1.0.0",
    description=(
        "API service for Doctors, Variants, Patients, Authentication and RBAC"
    ),
)

app.include_router(auth.router)
app.include_router(doctors.router)


@app.get("/")
def root():
  return {"message": "Welcome to Hospital Backend API"}
6. Pytest Unit Tests (tests/test_auth.py)
Python
from database import Base, get_db
from fastapi.testclient import TestClient
from main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

Base.metadata.create_all(bind=engine)


def override_get_db():
  db = TestingSessionLocal()
  try:
    yield db
  finally:
    db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_register_and_login():
  # 1. Register User
  response = client.post(
      "/auth/register",
      json={
          "username": "testadmin",
          "email": "admin@hospital.com",
          "password": "securepassword123",
          "role": "admin",
      },
  )
  assert response.status_code == 201
  data = response.json()
  assert "user_id" in data

  # 2. Login User
  response = client.post(
      "/auth/login",
      json={"username": "testadmin", "password": "securepassword123"},
  )
  assert response.status_code == 200
  token_data = response.json()
  assert "access_token" in token_data
  assert token_data["token_type"] == "bearer"

  # 3. Test Get Me
  token = token_data["access_token"]
  response = client.get(
      "/auth/me", headers={"Authorization": f"Bearer {token}"}
  )
  assert response.status_code == 200
  user_info = response.json()
  assert user_info["username"] == "testadmin"
  assert user_info["role"] == "admin"