from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from typing import Optional
from jose import jwt, JWTError
from datetime import datetime
from sqlalchemy import text, func

from app.database.database import get_db
from app.models.models import NguoiDung, BenhNhan, ChuyenKhoa, DichVu, TrieuChung, TrieuChungBacSi
from app.models.bac_si import BacSi
from app.models.lich_hen import LichHen
from app.models.le_tan import LeTan

from app import auth as root_auth

router = APIRouter(prefix="/auth", tags=["Xác thực & Tài khoản"])
tai_khoan_router = APIRouter(tags=["Quản lý Hồ sơ Cá nhân độc lập"])
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, root_auth.SECRET_KEY, algorithms=[root_auth.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token không hợp lệ!")
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Không thể xác thực thông tin đăng nhập hoặc Token đã hết hạn!"
        )

    user = db.query(NguoiDung).filter(NguoiDung.email == email).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Không tìm thấy người dùng từ token!")
    return user

class LoginRequest(BaseModel):
    email: Optional[str] = None
    username: Optional[str] = None
    password: str

class RegisterPatientRequest(BaseModel):
    ho_ten: str
    email: EmailStr
    so_dien_thoai: str
    mat_khau: str

class ChangePasswordRequest(BaseModel):
    mat_khau_cu: str
    mat_khau_moi: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    vai_tro: str
    user_id: int
    ho_ten: str

class PatientUpdateSchema(BaseModel):
    fullname: str
    phone: Optional[str] = None
    address: Optional[str] = None
    gender: Optional[str] = None
    date_of_birth: Optional[str] = None

class LyDoRequest(BaseModel):
    ly_do: Optional[str] = ""
    ly_do_khoa: Optional[str] = ""


@router.post("/register", status_code=status.HTTP_201_CREATED, summary="Đăng ký tài khoản Bệnh nhân")
def register_patient(payload: RegisterPatientRequest, db: Session = Depends(get_db)):
    exist = db.query(NguoiDung).filter(NguoiDung.email == payload.email).first()
    if exist:
        raise HTTPException(status_code=400, detail="Email này đã được sử dụng.")

    user = NguoiDung(
        email=payload.email,
        mat_khau=root_auth.get_password_hash(payload.mat_khau),
        ho_ten=payload.ho_ten,
        so_dien_thoai=payload.so_dien_thoai,
        vai_tro="benh_nhan",
        trang_thai=True
    )
    db.add(user)
    db.flush()

    patient_profile = BenhNhan(nguoi_dung_id=user.id)
    db.add(patient_profile)
    db.commit()
    return {"message": "Đăng ký tài khoản thành công.", "user_id": user.id}


@router.post("/login", response_model=TokenResponse, summary="Đăng nhập & cấp phát Token JWT")
async def login(payload: LoginRequest, db: Session = Depends(get_db)):
    identifier = (payload.email or payload.username or "").strip()
    password = (payload.password or "").strip()

    if not identifier:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vui lòng nhập email hoặc tài khoản đăng nhập!"
        )

    user = db.query(NguoiDung).filter(
        (NguoiDung.email == identifier) | (NguoiDung.so_dien_thoai == identifier)
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tài khoản chưa được đăng ký trong hệ thống!"
        )

    is_password_valid = False
    if user.mat_khau == password:
        is_password_valid = True
    else:
        try:
            if hasattr(root_auth, "verify_password") and root_auth.verify_password(password, user.mat_khau):
                is_password_valid = True
        except Exception:
            pass

    if not is_password_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mật khẩu không chính xác!"
        )

    uid: int = int(user.id)
    token = root_auth.create_access_token(
        data={"id": uid, "role": user.vai_tro, "sub": user.email}
    )

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user_id=uid,
        ho_ten=user.ho_ten or "",
        vai_tro=user.vai_tro
    )


@router.get("/me", summary="Lấy thông tin tài khoản hiện tại")
def get_me(current_user: NguoiDung = Depends(get_current_user)):
    return {
        "user_id": current_user.id,
        "email": current_user.email,
        "ho_ten": current_user.ho_ten,
        "so_dien_thoai": current_user.so_dien_thoai,
        "vai_tro": current_user.vai_tro
    }


@router.post("/change-password", summary="Thay đổi mật khẩu tài khoản hiện tại")
def change_password(
        payload: ChangePasswordRequest,
        current_user: NguoiDung = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    if not root_auth.verify_password(payload.mat_khau_cu, current_user.mat_khau):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mật khẩu cũ không chính xác."
        )

    current_user.mat_khau = root_auth.get_password_hash(payload.mat_khau_moi)
    db.commit()

    return {"message": "Đổi mật khẩu thành công."}


# ==========================================
# CÁC API QUẢN LÝ HỒ SƠ TÀI KHOẢN CÁ NHÂN
# ==========================================

def _xu_ly_lay_ho_so(current_user: NguoiDung):
    return {
        "success": True,
        "data": {
            "id": current_user.id,
            "ho_ten": current_user.ho_ten,
            "email": current_user.email,
            "so_dien_thoai": getattr(current_user, 'so_dien_thoai', '') or '',
            "dia_chi": getattr(current_user, 'dia_chi', '') or ''
        }
    }

async def _xu_ly_cap_nhat_ho_so(request: Request, db: Session, current_user: NguoiDung):
    try:
        body = await request.json()
        if "fullname" in body or "ho_ten" in body:
            current_user.ho_ten = body.get("fullname") or body.get("ho_ten")
        if "phone" in body or "so_dien_thoai" in body:
            if hasattr(current_user, 'so_dien_thoai'):
                current_user.so_dien_thoai = body.get("phone") or body.get("so_dien_thoai")
        if "address" in body or "dia_chi" in body:
            if hasattr(current_user, 'dia_chi'):
                current_user.dia_chi = body.get("address") or body.get("dia_chi")

        db.commit()
        db.refresh(current_user)
        return {
            "success": True,
            "message": "Cập nhật hồ sơ cá nhân thành công!",
            "data": {
                "ho_ten": current_user.ho_ten,
                "email": current_user.email,
                "so_dien_thoai": getattr(current_user, 'so_dien_thoai', ''),
                "dia_chi": getattr(current_user, 'dia_chi', '')
            }
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tai-khoan/ho-so")
@router.get("/ho-so-ca-nhan")
def lay_ho_so_auth(current_user: NguoiDung = Depends(get_current_user)):
    return _xu_ly_lay_ho_so(current_user)

@router.put("/tai-khoan/ho-so")
@router.put("/ho-so-ca-nhan")
async def cap_nhat_ho_so_auth(request: Request, db: Session = Depends(get_db), current_user: NguoiDung = Depends(get_current_user)):
    return await _xu_ly_cap_nhat_ho_so(request, db, current_user)

@tai_khoan_router.get("/tai-khoan/ho-so")
@tai_khoan_router.get("/ho-so-ca-nhan")
def lay_ho_so_tk(current_user: NguoiDung = Depends(get_current_user)):
    return _xu_ly_lay_ho_so(current_user)

@tai_khoan_router.put("/tai-khoan/ho-so")
@tai_khoan_router.put("/ho-so-ca-nhan")
async def cap_nhat_ho_so_tk(request: Request, db: Session = Depends(get_db), current_user: NguoiDung = Depends(get_current_user)):
    return await _xu_ly_cap_nhat_ho_so(request, db, current_user)


@router.get("/ho-so/{email}")
def get_ho_so(email: str, db: Session = Depends(get_db)):
    user = db.query(NguoiDung).filter(NguoiDung.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy thông tin người dùng!")

    patient = db.query(BenhNhan).filter(BenhNhan.nguoi_dung_id == user.id).first()

    return {
        "success": True,
        "data": {
            "user_id": user.id,
            "email": user.email,
            "ho_ten": user.ho_ten,
            "so_dien_thoai": getattr(user, 'so_dien_thoai', ''),
            "tien_su_benh": patient.tien_su_benh if patient else ""
        }
    }


@router.put("/ho-so/{email}")
async def update_ho_so(email: str, request: Request, db: Session = Depends(get_db)):
    user = db.query(NguoiDung).filter(NguoiDung.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy thông tin người dùng!")

    try:
        body = await request.json()
    except Exception:
        body = {}

    if "ho_ten" in body:
        user.ho_ten = body["ho_ten"]
    if "so_dien_thoai" in body and hasattr(user, 'so_dien_thoai'):
        user.so_dien_thoai = body["so_dien_thoai"]

    patient = db.query(BenhNhan).filter(BenhNhan.nguoi_dung_id == user.id).first()
    if not patient:
        patient = BenhNhan(nguoi_dung_id=user.id, tien_su_benh="")
        db.add(patient)

    if "tien_su_benh" in body:
        patient.tien_su_benh = body["tien_su_benh"]

    db.commit()
    db.refresh(user)
    db.refresh(patient)

    return {
        "success": True,
        "message": "Cập nhật hồ sơ thành công!",
        "data": {
            "email": user.email,
            "ho_ten": user.ho_ten,
            "so_dien_thoai": getattr(user, 'so_dien_thoai', ''),
            "tien_su_benh": patient.tien_su_benh
        }
    }


# =================== Admin ==============================

@router.get("/admin/chuyen-khoa", summary="Lấy danh sách chuyên khoa từ SQL Server")
def get_admin_specialties(db: Session = Depends(get_db)):
    specialties = db.query(ChuyenKhoa).all()
    result = []
    for s in specialties:
        doc_count = db.query(func.count(BacSi.id)).filter(BacSi.chuyen_khoa_id == s.id).scalar() or 0
        mo_ta_str = getattr(s, 'mo_ta', None) or getattr(s, 'description', None) or 'Chưa có mô tả chi tiết'
        status_str = str(getattr(s, 'trang_thai', 'active') or 'active').lower().strip()

        result.append({
            "id": str(s.id),
            "name": getattr(s, 'ten_chuyen_khoa', getattr(s, 'name', 'Chuyên khoa')),
            "description": mo_ta_str,
            "doctor_count": doc_count,
            "status": status_str,
            "ly_do_xoa": getattr(s, 'ly_do_xoa', '') or ''
        })
    return result


@router.get("/admin/bac-si")
def get_admin_doctors(db: Session = Depends(get_db)):
    results = db.query(BacSi, ChuyenKhoa, NguoiDung).outerjoin(
        ChuyenKhoa, BacSi.chuyen_khoa_id == ChuyenKhoa.id
    ).outerjoin(
        NguoiDung, BacSi.nguoi_dung_id == NguoiDung.id
    ).all()

    doctors_list = []
    for doctor, chuyen_khoa, nguoi_dung in results:
        doc_name = (
            (nguoi_dung.ho_ten if nguoi_dung else None) or
            getattr(doctor, 'ho_ten', None) or
            getattr(doctor, 'name', None) or
            f"Bác sĩ {doctor.id}"
        )

        doc_email = (nguoi_dung.email if nguoi_dung else '') or getattr(doctor, 'email', '')
        doc_phone = (nguoi_dung.so_dien_thoai if nguoi_dung else '') or getattr(doctor, 'so_dien_thoai', '')

        real_rating = (
            getattr(doctor, 'diem_danh_gia', None) or
            getattr(doctor, 'rating', None) or
            getattr(doctor, 'so_sao', 5.0)
        )

        raw_status = getattr(nguoi_dung, 'trang_thai', 'active') if nguoi_dung else 'active'
        if isinstance(raw_status, bool):
            status_str = "active" if raw_status else "locked"
        else:
            status_str = str(raw_status).lower().strip()
            if "delete" in status_str or "xóa" in status_str:
                status_str = "deleted"
            elif "lock" in status_str or "khóa" in status_str or status_str == "false" or status_str == "0":
                status_str = "locked"
            else:
                status_str = "active"

        real_user_id = doctor.nguoi_dung_id if (doctor and doctor.nguoi_dung_id) else doctor.id

        doctors_list.append({
            "id": f"BS{real_user_id:03d}",
            "name": doc_name,
            "specialtyId": str(doctor.chuyen_khoa_id) if doctor.chuyen_khoa_id else "all",
            "specialtyName": chuyen_khoa.ten_chuyen_khoa if chuyen_khoa and hasattr(chuyen_khoa, 'ten_chuyen_khoa') else "Chưa phân khoa",
            "email": doc_email,
            "phone": doc_phone,
            "status": status_str,
            "ly_do_khoa": getattr(nguoi_dung, 'ly_do_khoa', '') if nguoi_dung else '',
            "ly_do_xoa": getattr(nguoi_dung, 'ly_do_xoa', '') if nguoi_dung else '',
            "rating": float(real_rating)
        })

    return doctors_list


@router.get("/admin/dich-vu", summary="Lấy danh sách dịch vụ từ SQL Server")
def get_admin_services(db: Session = Depends(get_db)):
    results = db.query(DichVu, ChuyenKhoa).outerjoin(
        ChuyenKhoa, DichVu.chuyen_khoa_id == ChuyenKhoa.id
    ).all()

    services_list = []
    for service, chuyen_khoa in results:
        val_price = (
            getattr(service, 'gia_tien', None) or
            getattr(service, 'gia', None) or
            getattr(service, 'gia_niem_yet', None) or
            0.0
        )
        mo_ta_str = getattr(service, 'mo_ta', None) or getattr(service, 'description', None) or 'Chưa có mô tả'
        status_str = str(getattr(service, 'trang_thai', 'active') or 'active').lower().strip()

        services_list.append({
            "id": service.id if hasattr(service, 'id') else 1,
            "name": getattr(service, 'ten_dich_vu', getattr(service, 'name', 'Dịch vụ khám')),
            "specialtyId": str(service.chuyen_khoa_id) if hasattr(service, 'chuyen_khoa_id') and service.chuyen_khoa_id else "all",
            "specialtyName": getattr(chuyen_khoa, 'ten_chuyen_khoa', getattr(chuyen_khoa, 'name', 'Chưa phân khoa')) if chuyen_khoa else "Chưa phân khoa",
            "price": float(val_price),
            "description": mo_ta_str,
            "status": status_str,
            "ly_do_xoa": getattr(service, 'ly_do_xoa', '') or ''
        })

    return services_list


@router.get("/admin/nhat-ky-giao-dich")
def get_nhat_ky_giao_dich(year: str = "2026", month: str = "all", status: str = "all", db: Session = Depends(get_db)):
    try:
        appointments = db.query(LichHen).all()
        results = []

        for idx, appt in enumerate(appointments, start=1):
            patient_name = "Chưa cập nhật"
            doctor_name = "Chưa phân công"
            receptionist_name = "Chưa phân công"
            revenue = 350000.0

            try:
                if hasattr(appt, 'benh_nhan_id') and appt.benh_nhan_id:
                    bn_obj = db.query(BenhNhan).filter(BenhNhan.id == appt.benh_nhan_id).first()
                    user_id_real = getattr(bn_obj, 'nguoi_dung_id', None) if bn_obj else appt.benh_nhan_id
                    if user_id_real:
                        u_bn = db.query(NguoiDung).filter(NguoiDung.id == user_id_real).first()
                        if u_bn and getattr(u_bn, 'ho_ten', None):
                            patient_name = u_bn.ho_ten.strip()
            except Exception:
                pass

            try:
                if hasattr(appt, 'bac_si_id') and appt.bac_si_id:
                    bs = db.query(BacSi).filter(BacSi.id == appt.bac_si_id).first()
                    if bs:
                        ma_nd = getattr(bs, 'nguoi_dung_id', None) or getattr(bs, 'user_id', None)
                        if ma_nd:
                            u_bs = db.query(NguoiDung).filter(NguoiDung.id == ma_nd).first()
                            if u_bs and getattr(u_bs, 'ho_ten', None):
                                doctor_name = u_bs.ho_ten.strip()
                        if doctor_name == "Chưa phân công" and hasattr(bs, 'ho_ten') and bs.ho_ten:
                            doctor_name = bs.ho_ten.strip()
                    if doctor_name == "Chưa phân công":
                        doctor_name = f"BS. Phụ trách #{appt.bac_si_id}"
            except Exception:
                doctor_name = "Bác sĩ chuyên khoa"

            try:
                lt_code = getattr(appt, 'le_tan_ma_le_tan', None)
                if lt_code is not None:
                    lt_obj = db.query(LeTan).filter(
                        (LeTan.id == lt_code) |
                        (LeTan.ma_le_tan == str(lt_code)) |
                        (LeTan.ma_le_tan == lt_code)
                    ).first()

                    if lt_obj:
                        user_id_lt = getattr(lt_obj, 'nguoi_dung_id', None) or getattr(lt_obj, 'user_id', None) or getattr(lt_obj, 'id', None)
                        if user_id_lt:
                            u_lt = db.query(NguoiDung).filter(NguoiDung.id == user_id_lt).first()
                            if u_lt and getattr(u_lt, 'ho_ten', None):
                                receptionist_name = u_lt.ho_ten.strip()

                        if receptionist_name == "Chưa phân công":
                            for name_attr in ['ho_ten', 'ten', 'name', 'full_name']:
                                val = getattr(lt_obj, name_attr, None)
                                if val and isinstance(val, str) and val.strip():
                                    receptionist_name = val.strip()
                                    break

                    if receptionist_name == "Chưa phân công":
                        u_direct = db.query(NguoiDung).filter(NguoiDung.id == lt_code).first()
                        if u_direct and getattr(u_direct, 'ho_ten', None):
                            receptionist_name = u_direct.ho_ten.strip()
            except Exception as e:
                print("Lỗi truy vấn lễ tân từ SQL:", e)

            try:
                if hasattr(appt, 'dich_vu_id') and appt.dich_vu_id:
                    dv = db.query(DichVu).filter(DichVu.id == appt.dich_vu_id).first()
                    if dv:
                        for price_attr in ['gia_tien', 'gia', 'price', 'chi_phi']:
                            if hasattr(dv, price_attr) and getattr(dv, price_attr) is not None:
                                val = float(getattr(dv, price_attr))
                                if val > 0:
                                    revenue = val
                                    break
            except Exception:
                pass

            ngay_kham_str = str(getattr(appt, 'ngay_kham', '2026-11-06'))
            date_only = ngay_kham_str.split()[0] if ngay_kham_str else '2026-11-06'

            results.append({
                "id": f"GD{appt.id:03d}" if hasattr(appt, 'id') else f"GD0{idx}",
                "raw_id": int(appt.id) if hasattr(appt, 'id') else idx,
                "date": date_only,
                "patient": patient_name,
                "revenue": revenue,
                "profit": revenue * 0.75,
                "doctorConfirm": doctor_name,
                "receptionistConfirm": receptionist_name,
                "updatedAt": str(getattr(appt, 'updated_at', date_only)),
                "status": str(getattr(appt, 'trang_thai', 'completed'))
            })

        return results
    except Exception as e:
        print("====== LỖI API NHẬT KÝ GIAO DỊCH ======", str(e))
        return []


@router.get("/admin/notifications")
def get_admin_notifications(db: Session = Depends(get_db)):
    return [
        {
            "id": "N001",
            "title": "Hệ thống hoạt động",
            "message": "Kết nối cơ sở dữ liệu SQL Server thành công.",
            "time": "Vừa xong",
            "read": False
        }
    ]


@router.get("/admin/mapping", summary="Lấy danh sách mapping từ SQL Server")
def get_admin_mappings(db: Session = Depends(get_db)):
    mapping_list = []
    try:
        results = db.query(TrieuChung).all()
        for tc in results:
            ck = None
            if hasattr(tc, 'chuyen_khoa_id') and tc.chuyen_khoa_id:
                ck = db.query(ChuyenKhoa).filter(ChuyenKhoa.id == tc.chuyen_khoa_id).first()

            doc_name = "Không chỉ định"
            doc_id = ""
            link = db.query(TrieuChungBacSi).filter(TrieuChungBacSi.trieu_chung_id == tc.id).first()
            if link and hasattr(link, 'bac_si_id') and link.bac_si_id:
                bs = db.query(BacSi).filter(BacSi.id == link.bac_si_id).first()
                if bs:
                    doc_id = str(bs.id)
                    nd = None
                    if hasattr(bs, 'nguoi_dung_id') and bs.nguoi_dung_id:
                        nd = db.query(NguoiDung).filter(NguoiDung.id == bs.nguoi_dung_id).first()
                    if nd and hasattr(nd, 'ho_ten') and nd.ho_ten:
                        doc_name = nd.ho_ten

            keywords = (
                getattr(tc, 'ten_trieu_chung', None) or
                getattr(tc, 'keywords', None) or
                getattr(tc, 'tu_khoa', None) or
                'Triệu chứng'
            )

            status_str = str(getattr(tc, 'trang_thai', 'active') or 'active').lower().strip()
            if status_str not in ['active', 'deleted', 'đã xóa']:
                status_str = 'active'

            mapping_list.append({
                "id": tc.id,
                "keywords": keywords,
                "tu_khoa": keywords,
                "specialtyId": str(ck.id if ck else 'all'),
                "specialtyName": getattr(ck, 'ten_chuyen_khoa', getattr(ck, 'name', 'Chưa phân khoa')) if ck else "Chưa phân khoa",
                "doctorId": doc_id,
                "doctorName": doc_name,
                "priority": getattr(tc, 'do_uu_tien', getattr(tc, 'priority', 1)),
                "do_uu_tien": getattr(tc, 'do_uu_tien', getattr(tc, 'priority', 1)),
                "status": status_str,
                "trang_thai": status_str,
                "ly_do_xoa": getattr(tc, 'ly_do_xoa', '') or ''
            })
    except Exception as e:
        print("Lỗi API mapping chi tiết:", str(e))
        mapping_list = []

    return mapping_list


@router.get("/admin/dashboard-stats", summary="Lấy thống kê tổng quan doanh thu và lịch hẹn cho Dashboard")
def get_dashboard_stats(year: str = "2026", quarter: str = "all", db: Session = Depends(get_db)):
    total_appts = 0
    canceled_appts = 0
    total_rev = 0.0

    date_filter_sql = ""
    if year and year != "all":
        date_filter_sql += f" AND (YEAR(ngay_thanh_toan) = {year} OR YEAR(created_at) = {year} OR YEAR(ngay_kham) = {year})"

    if quarter and quarter != "all":
        if quarter == "Q1":
            date_filter_sql += " AND (MONTH(ngay_thanh_toan) BETWEEN 1 AND 3 OR MONTH(created_at) BETWEEN 1 AND 3)"
        elif quarter == "Q2":
            date_filter_sql += " AND (MONTH(ngay_thanh_toan) BETWEEN 4 AND 6 OR MONTH(created_at) BETWEEN 4 AND 6)"
        elif quarter == "Q3":
            date_filter_sql += " AND (MONTH(ngay_thanh_toan) BETWEEN 7 AND 9 OR MONTH(created_at) BETWEEN 7 AND 9)"
        elif quarter == "Q4":
            date_filter_sql += " AND (MONTH(ngay_thanh_toan) BETWEEN 10 AND 12 OR MONTH(created_at) BETWEEN 10 AND 12)"

    try:
        res_total = db.execute(text("SELECT COUNT(*) FROM lich_hen WHERE 1=1" + date_filter_sql)).scalar()
        total_appts = int(res_total) if res_total else 0
    except Exception:
        try:
            res_total = db.execute(text("SELECT COUNT(*) FROM lich_hen")).scalar()
            total_appts = int(res_total) if res_total else 0
        except Exception:
            total_appts = 0

    try:
        res_cancel = db.execute(text(
            "SELECT COUNT(*) FROM lich_hen WHERE (trang_thai LIKE N'%huy%' OR trang_thai LIKE N'%cancel%' OR trang_thai = '0')" + date_filter_sql)).scalar()
        canceled_appts = int(res_cancel) if res_cancel else 0
    except Exception:
        canceled_appts = 0

    cancel_rate = round((canceled_appts / total_appts * 100), 1) if total_appts > 0 else 0.0

    try:
        rev_query = f"SELECT SUM(tong_tien) FROM thanh_toan WHERE 1=1"
        if year and year != "all":
            rev_query += f" AND (YEAR(ngay_thanh_toan) = {year})"
        if quarter and quarter != "all":
            if quarter == "Q1":
                rev_query += " AND MONTH(ngay_thanh_toan) BETWEEN 1 AND 3"
            elif quarter == "Q2":
                rev_query += " AND MONTH(ngay_thanh_toan) BETWEEN 4 AND 6"
            elif quarter == "Q3":
                rev_query += " AND MONTH(ngay_thanh_toan) BETWEEN 7 AND 9"
            elif quarter == "Q4":
                rev_query += " AND MONTH(ngay_thanh_toan) BETWEEN 10 AND 12"

        res_rev = db.execute(text(rev_query)).scalar()
        if res_rev is not None:
            total_rev = float(res_rev)
        else:
            res_rev_fallback = db.execute(text("SELECT SUM(tong_tien) FROM thanh_toan")).scalar()
            total_rev = float(res_rev_fallback) if res_rev_fallback else 0.0
    except Exception as e:
        print("Lỗi tính doanh thu thanh_toan:", e)
        total_rev = 0.0

    chart_values = [0, 0, 0, 0, 0, 0, 0]
    prev_values = [0, 0, 0, 0, 0, 0, 0]

    if total_appts > 0:
        try:
            all_appts = db.execute(text("SELECT * FROM lich_hen")).fetchall()
            for appt in all_appts:
                appt_date = None
                for col in ['ngay_kham', 'ngay_khen', 'created_at', 'ngay_dat']:
                    if hasattr(appt, col) and getattr(appt, col):
                        appt_date = getattr(appt, col)
                        break

                if appt_date:
                    try:
                        weekday = datetime.strptime(str(appt_date).split()[0], "%Y-%m-%d").weekday()
                        chart_values[weekday] += 1
                    except Exception:
                        chart_values[0] += 1
                else:
                    idx = total_appts % 7
                    chart_values[idx] += 1
        except Exception:
            for i in range(min(total_appts, 7)):
                chart_values[i] = 1

    total_profit = float(total_rev) * 0.75

    return {
        "totalAppointments": total_appts,
        "cancelRate": cancel_rate,
        "totalRevenue": float(total_rev),
        "totalProfit": float(total_profit),
        "revenueByMonth": [
            {"label": "T2", "value": chart_values[0], "prev": prev_values[0]},
            {"label": "T3", "value": chart_values[1], "prev": prev_values[1]},
            {"label": "T4", "value": chart_values[2], "prev": prev_values[2]},
            {"label": "T5", "value": chart_values[3], "prev": prev_values[3]},
            {"label": "T6", "value": chart_values[4], "prev": prev_values[4]},
            {"label": "T7", "value": chart_values[5], "prev": prev_values[5]},
            {"label": "CN", "value": chart_values[6], "prev": prev_values[6]}
        ]
    }


# =================== THÙNG RÁC HỆ THỐNG ===================

@router.get("/admin/thung-rac", summary="Lấy danh sách các bản ghi đã xóa mềm từ tất cả các bảng")
def get_recycle_bin(db: Session = Depends(get_db)):
    recycle_items = []
    try:
        deleted_users = db.query(NguoiDung).filter(NguoiDung.trang_thai.in_(['deleted', 'Đã xóa'])).all()
        for u in deleted_users:
            reason = getattr(u, 'ly_do_xoa', None) or 'Không có lý do'
            recycle_items.append({
                "id": f"TK-{u.id}",
                "raw_id": u.id,
                "type": "Tài khoản",
                "table": "nguoi_dung",
                "name": getattr(u, 'ho_ten', None) or getattr(u, 'email', 'Tài khoản'),
                "ly_do_xoa": reason
            })

        deleted_ck = db.query(ChuyenKhoa).filter(ChuyenKhoa.trang_thai.in_(['deleted', 'Đã xóa'])).all()
        for ck in deleted_ck:
            reason = getattr(ck, 'ly_do_xoa', None) or 'Không có lý do'
            recycle_items.append({
                "id": f"CK-{ck.id}",
                "raw_id": ck.id,
                "type": "Chuyên khoa",
                "table": "chuyen_khoa",
                "name": getattr(ck, 'ten_chuyen_khoa', getattr(ck, 'name', 'Chuyên khoa')),
                "ly_do_xoa": reason
            })

        deleted_dv = db.query(DichVu).filter(DichVu.trang_thai.in_(['deleted', 'Đã xóa'])).all()
        for dv in deleted_dv:
            reason = getattr(dv, 'ly_do_xoa', None) or 'Không có lý do'
            recycle_items.append({
                "id": f"DV-{dv.id}",
                "raw_id": dv.id,
                "type": "Dịch vụ",
                "table": "dich_vu",
                "name": getattr(dv, 'ten_dich_vu', getattr(dv, 'name', 'Dịch vụ')),
                "ly_do_xoa": reason
            })

        deleted_tc = db.query(TrieuChung).filter(TrieuChung.trang_thai.in_(['deleted', 'Đã xóa'])).all()
        for tc in deleted_tc:
            reason = getattr(tc, 'ly_do_xoa', None) or 'Không có lý do'
            recycle_items.append({
                "id": f"TC-{tc.id}",
                "raw_id": tc.id,
                "type": "Mapping Triệu chứng",
                "table": "trieu_chung",
                "name": getattr(tc, 'ten_trieu_chung', getattr(tc, 'keywords', 'Mapping')),
                "ly_do_xoa": reason
            })
    except Exception as e:
        print("Lỗi lấy danh sách thùng rác:", str(e))

    return recycle_items


@router.post("/admin/thung-rac/khoi-phuc", summary="Khôi phục bản ghi từ thùng rác")
def restore_recycle_item(data: dict, db: Session = Depends(get_db)):
    table_name = data.get("table")
    record_id = data.get("id")

    table_map = {
        "nguoi_dung": NguoiDung,
        "chuyen_khoa": ChuyenKhoa,
        "dich_vu": DichVu,
        "trieu_chung": TrieuChung
    }

    if table_name not in table_map:
        raise HTTPException(status_code=400, detail="Bảng dữ liệu không hợp lệ")

    model_cls = table_map[table_name]
    record = db.query(model_cls).filter(model_cls.id == record_id).first()

    if not record:
        raise HTTPException(status_code=404, detail="Không tìm thấy bản ghi")

    if hasattr(record, 'trang_thai'):
        record.trang_thai = "active"
    if hasattr(record, 'ly_do_xoa'):
        record.ly_do_xoa = None

    db.commit()
    return {"success": True, "message": "Khôi phục thành công!"}


@router.delete("/admin/thung-rac/xoa-vinh-vien", summary="Xóa vĩnh viễn bản ghi khỏi CSDL")
def delete_permanent_item(table: str, id: int, db: Session = Depends(get_db)):
    table_map = {
        "nguoi_dung": NguoiDung,
        "chuyen_khoa": ChuyenKhoa,
        "dich_vu": DichVu,
        "trieu_chung": TrieuChung
    }

    if table not in table_map:
        raise HTTPException(status_code=400, detail="Tên bảng cơ sở dữ liệu không hợp lệ")

    model_cls = table_map[table]
    record = db.query(model_cls).filter(model_cls.id == id).first()

    if not record:
        raise HTTPException(status_code=404, detail="Không tìm thấy bản ghi cần xóa vĩnh viễn")

    db.delete(record)
    db.commit()
    return {"success": True, "message": "Đã xóa vĩnh viễn bản ghi khỏi cơ sở dữ liệu thành công!"}


@router.get("/transactions", summary="Lấy danh sách giao dịch và nhật ký hệ thống")
def get_transactions(
        year: str = None,
        month: str = None,
        status: str = None,
        db: Session = Depends(get_db),
        current_user: NguoiDung = Depends(root_auth.get_current_user)
):
    try:
        query = db.query(LichHen)
        if year:
            query = query.filter(func.year(LichHen.ngay_kham) == int(year))
        if month and month != "all":
            query = query.filter(func.month(LichHen.ngay_kham) == int(month))

        if status and status != "all":
            if status == "completed":
                query = query.filter(LichHen.trang_thai.in_(["Đã hoàn thành", "Hoàn thành", "Đã check-in", "Check-in"]))
            elif status == "cancelled":
                query = query.filter(LichHen.trang_thai.in_(["Đã hủy", "Cancelled", "Hủy"]))
            elif status == "pending":
                query = query.filter(LichHen.trang_thai.in_(["Chờ khám", "Chờ xác nhận", "Đã xác nhận", "confirmed"]))

        lich_hens = query.order_by(LichHen.id.desc()).all()
        results = []
        for l in lich_hens:
            st = str(l.trang_thai or "").strip()
            if st in ["Đã hoàn thành", "Hoàn thành", "Đã check-in", "Check-in"]:
                mapped_status = "completed"
            elif st in ["Đã hủy", "Cancelled", "Hủy"]:
                mapped_status = "cancelled"
            else:
                mapped_status = "pending"

            results.append({
                "id": f"GD{str(l.id).zfill(3)}",
                "date": str(l.ngay_kham) if l.ngay_kham else "",
                "patient": getattr(l, "benh_nhan_name", "Bệnh nhân") or "Bệnh nhân",
                "revenue": 350000,
                "profit": 105000,
                "doctorConfirm": getattr(l.bac_si, "ho_ten", "Bác sĩ") if hasattr(l, "bac_si") and l.bac_si else "Bác sĩ",
                "receptionistConfirm": "Lễ tân hệ thống",
                "updatedAt": str(datetime.now().strftime("%Y-%m-%d %H:%M")),
                "status": mapped_status
            })

        return {"success": True, "data": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi SQL Backend: {str(e)}")


@router.get("/admin/tai-khoan", summary="Lấy danh sách tất cả tài khoản từ SQL Server")
def get_admin_accounts(db: Session = Depends(get_db)):
    try:
        accounts = db.query(NguoiDung).all()
        result = []
        for u in accounts:
            raw_role = str(getattr(u, 'vai_tro', getattr(u, 'role', 'patient'))).lower().strip()
            name_str = str(getattr(u, 'ho_ten', getattr(u, 'name', ''))).lower()
            email_str = str(getattr(u, 'email', '')).lower()

            if "admin" in raw_role or "quản trị" in raw_role or "quan tri" in raw_role or "it.admin" in email_str:
                normalized_role = "admin"
            elif "doctor" in raw_role or "bac_si" in raw_role or "bác sĩ" in raw_role or "bs" in name_str or email_str.startswith("bs."):
                normalized_role = "doctor"
            elif "receptionist" in raw_role or "le_tan" in raw_role or "lễ tân" in raw_role or "letan" in raw_role:
                normalized_role = "receptionist"
            else:
                normalized_role = "patient"

            raw_status = getattr(u, 'trang_thai', None) if hasattr(u, 'trang_thai') else getattr(u, 'status', 'active')
            if isinstance(raw_status, bool):
                status_str = "active" if raw_status else "locked"
            else:
                status_str = str(raw_status).lower().strip()
                if "delete" in status_str or "xóa" in status_str or "daxoa" in status_str:
                    status_str = "deleted"
                elif "lock" in status_str or "khoá" in status_str or "khóa" in status_str or status_str == "false" or status_str == "0":
                    status_str = "locked"
                else:
                    status_str = "active"

            result.append({
                "id": u.id,
                "ho_ten": getattr(u, 'ho_ten', ''),
                "email": getattr(u, 'email', ''),
                "so_dien_thoai": getattr(u, 'so_dien_thoai', ''),
                "vai_tro": normalized_role,
                "trang_thai": status_str,
                "ly_do_khoa": getattr(u, 'ly_do_khoa', '') or '',
                "ly_do_xoa": getattr(u, 'ly_do_xoa', '') or ''
            })

        return {"success": True, "data": result}
    except Exception as e:
        print("Lỗi lấy danh sách tài khoản:", e)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/admin/tai-khoan", summary="Thêm tài khoản mới vào SQL Server")
def create_admin_account(data: dict, db: Session = Depends(get_db)):
    try:
        email = data.get("email")
        exist = db.query(NguoiDung).filter(NguoiDung.email == email).first()
        if exist:
            raise HTTPException(status_code=400, detail="Email này đã được sử dụng.")

        mat_khau_raw = data.get("mat_khau", "123456")
        new_user = NguoiDung(
            ho_ten=data.get("ho_ten"),
            email=email,
            so_dien_thoai=data.get("so_dien_thoai"),
            vai_tro=data.get("vai_tro", "patient"),
            mat_khau=root_auth.get_password_hash(mat_khau_raw),
            trang_thai=True
        )
        db.add(new_user)
        db.commit()
        return {"success": True, "message": "Thêm tài khoản thành công vào CSDL."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/admin/tai-khoan/{account_id}", summary="Cập nhật tài khoản trong SQL Server")
def update_admin_account(account_id: int, data: dict, db: Session = Depends(get_db)):
    try:
        user = db.query(NguoiDung).filter(NguoiDung.id == account_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Không tìm thấy tài khoản.")

        if "ho_ten" in data and data["ho_ten"]:
            user.ho_ten = data["ho_ten"]
        if "email" in data and data["email"]:
            user.email = data["email"]
        if "so_dien_thoai" in data and data["so_dien_thoai"]:
            user.so_dien_thoai = data["so_dien_thoai"]
        if "vai_tro" in data and data["vai_tro"]:
            user.vai_tro = data["vai_tro"]

        db.commit()
        db.refresh(user)
        return {"success": True, "message": "Cập nhật tài khoản thành công."}
    except Exception as e:
        db.rollback()
        print("====== LỖI SQL KHI CẬP NHẬT TÀI KHOẢN ======", str(e))
        raise HTTPException(status_code=500, detail=f"Lỗi SQL: {str(e)}")


@router.post("/admin/tai-khoan/{account_id}/khoa", summary="Khóa tài khoản kèm lý do")
def lock_account(account_id: int, payload: LyDoRequest, db: Session = Depends(get_db)):
    try:
        noi_dung_ly_do = payload.ly_do or payload.ly_do_khoa or "Khóa tài khoản hệ thống"
        user = db.query(NguoiDung).filter(NguoiDung.id == account_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Không tìm thấy tài khoản.")

        user.trang_thai = "locked"
        user.ly_do_khoa = noi_dung_ly_do
        db.execute(
            text("UPDATE nguoi_dung SET trang_thai = :status, ly_do_khoa = :reason WHERE id = :uid"),
            {"status": "locked", "reason": noi_dung_ly_do, "uid": account_id}
        )
        db.commit()
        return {"success": True, "message": "Đã khóa tài khoản và lưu lý do thành công."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/admin/tai-khoan/{account_id}/go-khoa", summary="Gỡ khóa tài khoản kèm lý do")
def unlock_account(account_id: int, payload: LyDoRequest, db: Session = Depends(get_db)):
    try:
        user = db.query(NguoiDung).filter(NguoiDung.id == account_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Không tìm thấy tài khoản.")

        noi_dung_ly_do = payload.ly_do or payload.ly_do_khoa or "Gỡ khóa tài khoản"
        user.trang_thai = "active"
        user.ly_do_go_khoa = noi_dung_ly_do
        db.commit()
        db.refresh(user)
        return {"success": True, "message": "Đã gỡ khóa tài khoản thành công."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/admin/tai-khoan/{account_id}/xoa-tam", summary="Chuyển tài khoản vào thùng rác kèm lý do")
def soft_delete_account(account_id: int, data: dict, db: Session = Depends(get_db)):
    try:
        user = db.query(NguoiDung).filter(NguoiDung.id == account_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Không tìm thấy tài khoản.")

        user.trang_thai = "deleted"
        user.ly_do_xoa = data.get("ly_do")
        db.commit()
        db.refresh(user)
        return {"success": True, "message": "Đã chuyển tài khoản vào thùng rác thành công."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/admin/tai-khoan/{account_id}/khoi-phuc", summary="Khôi phục tài khoản từ thùng rác")
def restore_account(account_id: str, payload: LyDoRequest, db: Session = Depends(get_db)):
    try:
        clean_id = int(str(account_id).replace("TK", "").replace("tk", "").lstrip("0") or "0")
        user = db.query(NguoiDung).filter(NguoiDung.id == clean_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Không tìm thấy tài khoản.")

        user.trang_thai = "active"
        user.ly_do_go_khoa = payload.ly_do or payload.ly_do_khoa or "Khôi phục tài khoản"
        db.commit()
        db.refresh(user)
        return {"success": True, "message": "Đã khôi phục tài khoản thành công."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# ======================== BÁC SĨ ==================================

@router.post("/admin/bac-si", summary="Thêm bác sĩ mới vào SQL Server")
def create_admin_doctor(data: dict, db: Session = Depends(get_db)):
    try:
        email = data.get("email")
        exist_user = db.query(NguoiDung).filter(NguoiDung.email == email).first()
        if exist_user:
            raise HTTPException(status_code=400, detail="Email này đã được sử dụng cho tài khoản khác.")

        new_user = NguoiDung(
            ho_ten=data.get("ho_ten"),
            email=email,
            so_dien_thoai=data.get("so_dien_thoai"),
            vai_tro="Bác sĩ",
            mat_khau=root_auth.get_password_hash("123456"),
            trang_thai=True
        )
        db.add(new_user)
        db.flush()

        new_doctor = BacSi(
            nguoi_dung_id=new_user.id,
            chuyen_khoa_id=data.get("chuyen_khoa_id")
        )
        db.add(new_doctor)
        db.commit()
        return {"success": True, "message": "Thêm bác sĩ mới thành công vào CSDL."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/admin/bac-si/{doctor_id}", summary="Xóa bác sĩ khỏi SQL Server")
def delete_admin_doctor(doctor_id: str, db: Session = Depends(get_db)):
    try:
        clean_id = int(str(doctor_id).replace("BS", "").lstrip("0") or "0")
        doctor = db.query(BacSi).filter(BacSi.id == clean_id).first()
        if not doctor:
            doctor = db.query(BacSi).filter(BacSi.id == doctor_id).first()

        if not doctor:
            raise HTTPException(status_code=404, detail="Không tìm thấy bác sĩ.")

        db.delete(doctor)
        db.commit()
        return {"success": True, "message": "Đã xóa bác sĩ thành công."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/admin/bac-si/{doctor_id}/khoa", summary="Khóa bác sĩ kèm lý do")
def lock_doctor_account(doctor_id: str, payload: LyDoRequest, db: Session = Depends(get_db)):
    try:
        clean_id = int(str(doctor_id).replace("BS", "").replace("bs", "").lstrip("0") or "0")
        doctor = db.query(BacSi).filter(BacSi.nguoi_dung_id == clean_id).first()
        if not doctor:
            doctor = db.query(BacSi).filter(BacSi.id == clean_id).first()

        if not doctor:
            raise HTTPException(status_code=404, detail="Không tìm thấy bác sĩ trong cơ sở dữ liệu.")

        user = db.query(NguoiDung).filter(NguoiDung.id == doctor.nguoi_dung_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Không tìm thấy tài khoản người dùng.")

        noi_dung = payload.ly_do or payload.ly_do_khoa or "Khóa tài khoản bác sĩ"
        user.trang_thai = "locked"
        user.ly_do_khoa = noi_dung
        db.commit()
        return {"success": True, "message": "Đã khóa bác sĩ thành công."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/admin/bac-si/{doctor_id}/go-khoa", summary="Gỡ khóa bác sĩ")
def unlock_doctor_account(doctor_id: str, payload: LyDoRequest, db: Session = Depends(get_db)):
    try:
        clean_id = int(str(doctor_id).replace("BS", "").replace("bs", "").lstrip("0") or "0")
        doctor = db.query(BacSi).filter(BacSi.nguoi_dung_id == clean_id).first()
        if not doctor:
            doctor = db.query(BacSi).filter(BacSi.id == clean_id).first()

        if not doctor:
            raise HTTPException(status_code=404, detail="Không tìm thấy bác sĩ.")

        user = db.query(NguoiDung).filter(NguoiDung.id == doctor.nguoi_dung_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Không tìm thấy tài khoản người dùng.")

        noi_dung = payload.ly_do or payload.ly_do_khoa or "Gỡ khóa tài khoản bác sĩ"
        user.trang_thai = "active"
        user.ly_do_go_khoa = noi_dung
        db.commit()
        return {"success": True, "message": "Đã gỡ khóa bác sĩ thành công."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/admin/bac-si/{doctor_id}/xoa-tam", summary="Chuyển bác sĩ vào thùng rác kèm lý do")
def soft_delete_doctor(doctor_id: str, payload: LyDoRequest, db: Session = Depends(get_db)):
    try:
        clean_id = int(str(doctor_id).replace("BS", "").replace("bs", "").lstrip("0") or "0")
        doctor = db.query(BacSi).filter(BacSi.nguoi_dung_id == clean_id).first()
        if not doctor:
            doctor = db.query(BacSi).filter(BacSi.id == clean_id).first()

        if not doctor:
            raise HTTPException(status_code=404, detail="Không tìm thấy bác sĩ.")

        user = db.query(NguoiDung).filter(NguoiDung.id == doctor.nguoi_dung_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Không tìm thấy tài khoản người dùng.")

        noi_dung = payload.ly_do or payload.ly_do_khoa or "Xóa tài khoản bác sĩ"
        user.trang_thai = "deleted"
        user.ly_do_xoa = noi_dung
        db.commit()
        return {"success": True, "message": "Đã chuyển bác sĩ vào thùng rác thành công."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/admin/bac-si/{doctor_id}/khoi-phuc", summary="Khôi phục bác sĩ từ thùng rác")
def restore_doctor(doctor_id: str, payload: LyDoRequest, db: Session = Depends(get_db)):
    try:
        clean_id = int(str(doctor_id).replace("BS", "").replace("bs", "").lstrip("0") or "0")
        doctor = db.query(BacSi).filter(BacSi.nguoi_dung_id == clean_id).first()
        if not doctor:
            doctor = db.query(BacSi).filter(BacSi.id == clean_id).first()

        if not doctor:
            raise HTTPException(status_code=404, detail="Không tìm thấy bác sĩ trong cơ sở dữ liệu.")

        user = db.query(NguoiDung).filter(NguoiDung.id == doctor.nguoi_dung_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Không tìm thấy tài khoản người dùng.")

        user.trang_thai = "active"
        user.ly_do_go_khoa = payload.ly_do or payload.ly_do_khoa or "Khôi phục tài khoản bác sĩ"
        db.commit()
        return {"success": True, "message": "Đã khôi phục bác sĩ thành công."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# ======================= QUẢN LÝ CHUYÊN KHOA ========================

@router.post("/admin/chuyen-khoa", summary="Thêm chuyên khoa mới vào SQL Server")
def create_admin_chuyen_khoa(data: dict, db: Session = Depends(get_db)):
    try:
        ten_ck = data.get("ten_chuyen_khoa") or data.get("name")
        if not ten_ck:
            raise HTTPException(status_code=400, detail="Tên chuyên khoa không được để trống.")

        exist_spec = db.query(ChuyenKhoa).filter(
            (ChuyenKhoa.ten_chuyen_khoa == ten_ck) | (ChuyenKhoa.name == ten_ck)
        ).first() if hasattr(ChuyenKhoa, 'name') else db.query(ChuyenKhoa).filter(
            ChuyenKhoa.ten_chuyen_khoa == ten_ck).first()

        if exist_spec:
            raise HTTPException(status_code=400, detail="Tên chuyên khoa này đã tồn tại trong hệ thống.")

        new_spec = ChuyenKhoa(
            ten_chuyen_khoa=ten_ck,
            mo_ta=data.get("mo_ta") or data.get("description", ""),
            trang_thai="active"
        )
        if hasattr(new_spec, 'name') and not getattr(new_spec, 'name', None):
            new_spec.name = ten_ck
        if hasattr(new_spec, 'description') and not getattr(new_spec, 'description', None):
            new_spec.description = data.get("mo_ta") or data.get("description", "")

        db.add(new_spec)
        db.commit()
        return {"success": True, "message": "Thêm chuyên khoa mới thành công vào CSDL."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/admin/chuyen-khoa/{spec_id}", summary="Chỉnh sửa thông tin chuyên khoa")
def update_admin_chuyen_khoa(spec_id: int, data: dict, db: Session = Depends(get_db)):
    try:
        spec = db.query(ChuyenKhoa).filter(ChuyenKhoa.id == spec_id).first()
        if not spec:
            raise HTTPException(status_code=404, detail="Không tìm thấy chuyên khoa cần cập nhật.")

        ten_ck = data.get("ten_chuyen_khoa") or data.get("name")
        mo_ta = data.get("mo_ta") or data.get("description", "")

        if ten_ck:
            if hasattr(spec, 'ten_chuyen_khoa'): spec.ten_chuyen_khoa = ten_ck
            if hasattr(spec, 'name'): spec.name = ten_ck
        if mo_ta is not None:
            if hasattr(spec, 'mo_ta'): spec.mo_ta = mo_ta
            if hasattr(spec, 'description'): spec.description = mo_ta

        db.commit()
        return {"success": True, "message": "Cập nhật thông tin chuyên khoa thành công."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/admin/chuyen-khoa/{spec_id}/xoa-tam", summary="Chuyển chuyên khoa vào thùng rác kèm lý do")
def soft_delete_specialty(spec_id: int, payload: LyDoRequest, db: Session = Depends(get_db)):
    try:
        spec = db.query(ChuyenKhoa).filter(ChuyenKhoa.id == spec_id).first()
        if not spec:
            raise HTTPException(status_code=404, detail="Không tìm thấy chuyên khoa.")

        noi_dung = payload.ly_do or payload.ly_do_khoa or "Xóa chuyên khoa hệ thống"
        spec.trang_thai = "deleted"
        spec.ly_do_xoa = noi_dung
        db.commit()
        return {"success": True, "message": "Đã chuyển chuyên khoa vào thùng rác thành công."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/admin/chuyen-khoa/{spec_id}/khoi-phuc", summary="Khôi phục chuyên khoa từ thùng rác")
def restore_specialty(spec_id: int, payload: LyDoRequest, db: Session = Depends(get_db)):
    try:
        spec = db.query(ChuyenKhoa).filter(ChuyenKhoa.id == spec_id).first()
        if not spec:
            raise HTTPException(status_code=404, detail="Không tìm thấy chuyên khoa.")

        spec.trang_thai = "active"
        spec.ly_do_xoa = None
        db.commit()
        return {"success": True, "message": "Đã khôi phục chuyên khoa thành công."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# ========================= QUẢN LÝ DỊCH VỤ =============================

@router.post("/admin/dich-vu", summary="Thêm dịch vụ mới vào SQL Server")
def create_admin_service(data: dict, db: Session = Depends(get_db)):
    try:
        ten_dv = data.get("ten_dich_vu") or data.get("name")
        if not ten_dv:
            raise HTTPException(status_code=400, detail="Tên dịch vụ không được để trống.")

        new_serv = DichVu(
            ten_dich_vu=ten_dv,
            chuyen_khoa_id=data.get("chuyen_khoa_id") or data.get("specialtyId"),
            gia_tien=data.get("gia") or data.get("price") or 0.0,
            mo_ta=data.get("mo_ta") or data.get("description") or "",
            trang_thai="active"
        )
        db.add(new_serv)
        db.commit()
        return {"success": True, "message": "Thêm dịch vụ mới thành công vào CSDL."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/admin/dich-vu/{serv_id}", summary="Chỉnh sửa thông tin dịch vụ")
def update_admin_service(serv_id: int, data: dict, db: Session = Depends(get_db)):
    try:
        serv = db.query(DichVu).filter(DichVu.id == serv_id).first()
        if not serv:
            raise HTTPException(status_code=404, detail="Không tìm thấy dịch vụ cần cập nhật.")

        ten_dv = data.get("ten_dich_vu") or data.get("name")
        gia_val = data.get("gia") if data.get("gia") is not None else data.get("price")
        mo_ta = data.get("mo_ta") if data.get("mo_ta") is not None else data.get("description")
        ck_id = data.get("chuyen_khoa_id") or data.get("specialtyId")

        if ten_dv:
            if hasattr(serv, 'ten_dich_vu'): serv.ten_dich_vu = ten_dv
            if hasattr(serv, 'name'): serv.name = ten_dv
        if gia_val is not None:
            if hasattr(serv, 'gia_tien'): serv.gia_tien = float(gia_val)
            elif hasattr(serv, 'gia'): serv.gia = float(gia_val)
            elif hasattr(serv, 'price'): serv.price = float(gia_val)
        if mo_ta is not None:
            if hasattr(serv, 'mo_ta'): serv.mo_ta = mo_ta
            if hasattr(serv, 'description'): serv.description = mo_ta
        if ck_id:
            serv.chuyen_khoa_id = ck_id

        db.commit()
        return {"success": True, "message": "Cập nhật thông tin dịch vụ thành công."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/admin/dich-vu/{serv_id}/xoa-tam", summary="Chuyển dịch vụ vào thùng rác kèm lý do")
def soft_delete_service(serv_id: int, payload: LyDoRequest, db: Session = Depends(get_db)):
    try:
        serv = db.query(DichVu).filter(DichVu.id == serv_id).first()
        if not serv:
            raise HTTPException(status_code=404, detail="Không tìm thấy dịch vụ.")

        noi_dung = payload.ly_do or payload.ly_do_khoa or "Xóa dịch vụ hệ thống"
        serv.trang_thai = "deleted"
        serv.ly_do_xoa = noi_dung
        db.commit()
        return {"success": True, "message": "Đã chuyển dịch vụ vào thùng rác thành công."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/admin/dich-vu/{serv_id}/khoi-phuc", summary="Khôi phục dịch vụ từ thùng rác")
def restore_service(serv_id: int, payload: LyDoRequest, db: Session = Depends(get_db)):
    try:
        serv = db.query(DichVu).filter(DichVu.id == serv_id).first()
        if not serv:
            raise HTTPException(status_code=404, detail="Không tìm thấy dịch vụ.")

        serv.trang_thai = "active"
        serv.ly_do_xoa = None
        db.commit()
        return {"success": True, "message": "Đã khôi phục dịch vụ thành công."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# ======================= QUẢN LÝ MAPPING =======================

@router.post("/admin/mapping", summary="Thêm quy tắc mapping mới")
def create_admin_mapping(data: dict, db: Session = Depends(get_db)):
    try:
        tu_khoa = data.get("tu_khoa") or data.get("keywords")
        if not tu_khoa:
            raise HTTPException(status_code=400, detail="Từ khóa triệu chứng không được để trống.")

        new_tc = TrieuChung(
            ten_trieu_chung=tu_khoa,
            chuyen_khoa_id=data.get("chuyen_khoa_id") or data.get("specialtyId"),
            do_uu_tien=int(data.get("do_uu_tien") or data.get("priority") or 1),
            trang_thai="active"
        )
        db.add(new_tc)
        db.flush()

        bs_id = data.get("bac_si_id") or data.get("doctorId")
        if bs_id:
            new_link = TrieuChungBacSi(trieu_chung_id=new_tc.id, bac_si_id=int(bs_id))
            db.add(new_link)

        db.commit()
        return {"success": True, "message": "Thêm quy tắc mapping thành công."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/admin/mapping/{map_id}", summary="Chỉnh sửa quy tắc mapping")
def update_admin_mapping(map_id: int, data: dict, db: Session = Depends(get_db)):
    try:
        tc = db.query(TrieuChung).filter(TrieuChung.id == map_id).first()
        if not tc:
            raise HTTPException(status_code=404, detail="Không tìm thấy quy tắc mapping.")

        tu_khoa = data.get("tu_khoa") or data.get("keywords")
        ck_id = data.get("chuyen_khoa_id") or data.get("specialtyId")
        uu_tien = data.get("do_uu_tien") if data.get("do_uu_tien") is not None else data.get("priority")
        bs_id = data.get("bac_si_id") or data.get("doctorId")

        if tu_khoa:
            if hasattr(tc, 'ten_trieu_chung'): tc.ten_trieu_chung = tu_khoa
            if hasattr(tc, 'keywords'): tc.keywords = tu_khoa
        if ck_id:
            tc.chuyen_khoa_id = ck_id
        if uu_tien is not None:
            if hasattr(tc, 'do_uu_tien'): tc.do_uu_tien = int(uu_tien)
            if hasattr(tc, 'priority'): tc.priority = int(uu_tien)
        if bs_id is not None:
            db.query(TrieuChungBacSi).filter(TrieuChungBacSi.trieu_chung_id == map_id).delete()
            if bs_id:
                new_link = TrieuChungBacSi(trieu_chung_id=map_id, bac_si_id=int(bs_id))
                db.add(new_link)

        db.commit()
        return {"success": True, "message": "Cập nhật quy tắc mapping thành công."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/admin/mapping/{map_id}/xoa-tam", summary="Chuyển mapping vào thùng rác kèm lý do")
def soft_delete_mapping(map_id: int, payload: LyDoRequest, db: Session = Depends(get_db)):
    try:
        tc = db.query(TrieuChung).filter(TrieuChung.id == map_id).first()
        if not tc:
            raise HTTPException(status_code=404, detail="Không tìm thấy quy tắc mapping.")

        noi_dung = payload.ly_do or payload.ly_do_khoa or "Xóa quy tắc mapping hệ thống"
        tc.trang_thai = "deleted"
        tc.ly_do_xoa = noi_dung
        db.commit()
        return {"success": True, "message": "Đã chuyển quy tắc mapping vào thùng rác thành công."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/admin/mapping/{map_id}/khoi-phuc", summary="Khôi phục mapping từ thùng rác")
def restore_mapping(map_id: int, payload: LyDoRequest, db: Session = Depends(get_db)):
    try:
        tc = db.query(TrieuChung).filter(TrieuChung.id == map_id).first()
        if not tc:
            raise HTTPException(status_code=404, detail="Không tìm thấy quy tắc mapping.")

        tc.trang_thai = "active"
        tc.ly_do_xoa = None
        db.commit()
        return {"success": True, "message": "Đã khôi phục quy tắc mapping thành công."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))