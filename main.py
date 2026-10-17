from pathlib import Path
from fastapi import FastAPI, Request, Response, Depends, Form, status
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware

# 1. Khởi tạo cơ sở dữ liệu và nạp models
from datadase.database import engine, Base, get_db
import models
from models.models import NguoiDung, BenhNhan

# 2. Import trực tiếp các router từ thư mục api/
from api.core_auth import router as core_auth_router
from api.nghiep_vu import router as nghiep_vu_router
from api.admin import router as admin_router

# Đảm bảo nạp models để tự động sinh bảng dữ liệu
_ = models
Base.metadata.create_all(bind=engine)

# Xác định đường dẫn thư mục gốc bằng Path chuẩn
BASE_DIR = Path(__file__).resolve().parent

# Khởi tạo ứng dụng FastAPI
app = FastAPI(
    title="MedBooking API System",
    description="Hệ thống quản lý phòng khám: Core Auth, Nghiệp vụ và Admin Dashboard.",
    version="1.0.0",
)

# KÍCH HOẠT PHỤC VỤ FILE TĨNH (CSS, JS) TỪ THƯ MỤC /static
app.mount("/static", StaticFiles(directory="static"), name="static")

# Cấu hình SessionMiddleware (Dùng để lưu phiên đăng nhập của người dùng)
app.add_middleware(SessionMiddleware, secret_key="medbooking_secret_key_very_secure_2026")

# Cấu hình Jinja2Templates trỏ đến thư mục chứa các file html
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


# Cấu hình CORS bằng HTTP Middleware native của FastAPI
@app.middleware("http")
async def custom_cors_middleware(request: Request, call_next):
    if request.method == "OPTIONS":
        response = Response(status_code=204)
    else:
        response = await call_next(request)

    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response


# Đăng ký toàn bộ các phân hệ API vào tiền tố /api
app.include_router(core_auth_router, prefix="/api")
app.include_router(nghiep_vu_router, prefix="/api")
app.include_router(admin_router, prefix="/api")


# ==========================================
# CÁC ROUTE GIAO DIỆN HTML (ĐIỀU HƯỚNG MỚI)
# ==========================================

# 1. Mặc định khi truy cập vào trang web ("/") sẽ hiển thị TRANG CHỦ (home.html) đầu tiên
@app.get("/", response_class=HTMLResponse, tags=["Frontend UI"])
def serve_home_default(request: Request):
    user_name = request.session.get("user_name")
    return templates.TemplateResponse(request, "dk_dn/home.html", {
        "user_name": user_name
    })


# Trang chủ chung (/home)
@app.get("/home", response_class=HTMLResponse, tags=["Frontend UI"])
def serve_home(request: Request):
    user_name = request.session.get("user_name")
    return templates.TemplateResponse(request, "dk_dn/home.html", {
        "user_name": user_name
    })


# 2. Trang dành riêng cho bệnh nhân sau khi đăng nhập thành công (/home_bn)
@app.get("/home_bn", response_class=HTMLResponse, tags=["Frontend UI"])
def serve_home_bn(request: Request):
    user_name = request.session.get("user_name")
    user_email = request.session.get("user_email")

    # Bảo mật: Nếu chưa đăng nhập mà cố tình truy cập sẽ bị đá về trang đăng nhập
    if not user_email:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

    return templates.TemplateResponse(request, "benh_nhan/home_bn.html", {
        "user_name": user_name,
        "user_email": user_email
    })


# 3. Giao diện ĐĂNG NHẬP (GET /login)
@app.get("/login", response_class=HTMLResponse, tags=["Frontend UI"])
def serve_login(request: Request):
    return templates.TemplateResponse(request, "dk_dn/dn.html", {"error": None})


# 4. Xử lý logic ĐĂNG NHẬP (POST /login)
@app.post("/login", tags=["Frontend UI"])
def handle_login(
        request: Request,
        email: str = Form(...),
        password: str = Form(...),
        db: Session = Depends(get_db)
):
    user = db.query(NguoiDung).filter(NguoiDung.email == email).first()

    if not user:
        return templates.TemplateResponse(
            request,
            "dk_dn/dn.html",
            {"error": "Tài khoản email này không tồn tại! Vui lòng đăng ký tài khoản mới trước khi đăng nhập."}
        )

    if user.mat_khau != password:
        return templates.TemplateResponse(
            request,
            "dk_dn/dn.html",
            {"error": "Mật khẩu không chính xác!"}
        )

    # ĐĂNG NHẬP THÀNH CÔNG -> Lưu thông tin vào Session
    request.session["user_email"] = user.email
    request.session["user_name"] = user.ho_ten

    return RedirectResponse(url="/home_bn", status_code=status.HTTP_303_SEE_OTHER)


# 5. Giao diện ĐĂNG KÝ (GET /register)
@app.get("/register", response_class=HTMLResponse, tags=["Frontend UI"])
def serve_register(request: Request):
    return templates.TemplateResponse(request, "dk_dn/dk.html", {"error": None})


# 6. Xử lý logic ĐĂNG KÝ (POST /register)
@app.post("/register", tags=["Frontend UI"])
def handle_register(
        request: Request,
        hoten: str = Form(...),
        email: str = Form(...),
        password: str = Form(...),
        db: Session = Depends(get_db)
):
    existing_user = db.query(NguoiDung).filter(NguoiDung.email == email).first()
    if existing_user:
        return templates.TemplateResponse(
            request,
            "dk_dn/dk.html",
            {"error": "Email này đã được đăng ký trên hệ thống. Vui lòng chọn email khác hoặc đăng nhập!"}
        )

    new_user = NguoiDung(
        email=email,
        mat_khau=password,
        ho_ten=hoten
    )
    db.add(new_user)
    db.commit()

    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)


# 7. Đăng xuất: Xóa Session và quay về trang chủ
@app.get("/logout", tags=["Frontend UI"])
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


# ==========================================
# CÁC TAB VÀ CHỨC NĂNG DÀNH CHO BỆNH NHÂN
# ==========================================

# 8. Trang Hồ sơ cá nhân của bệnh nhân (GET /ho_so_ca_nhan)
@app.get("/ho_so_ca_nhan", response_class=HTMLResponse, tags=["Frontend UI"])
def serve_ho_so_ca_nhan(request: Request, db: Session = Depends(get_db)):
    user_email = request.session.get("user_email")
    if not user_email:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

    user = db.query(NguoiDung).filter(NguoiDung.email == user_email).first()
    if not user:
        request.session.clear()
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

    return templates.TemplateResponse(request, "benh_nhan/ho_so_ca_nhan.html", {
        "user": user
    })


# 9. Xử lý cập nhật Hồ sơ cá nhân (POST /update_profile)
@app.post("/update_profile", tags=["Frontend UI"])
def handle_update_profile(
        request: Request,
        name: str = Form(...),
        phone: str = Form(None),
        dob: str = Form(None),
        gender: str = Form(None),
        address: str = Form(None),
        db: Session = Depends(get_db)
):
    user_email = request.session.get("user_email")
    if not user_email:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

    user = db.query(NguoiDung).filter(NguoiDung.email == user_email).first()
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

    # Cập nhật thông tin cơ bản bảng NguoiDung
    user.ho_ten = name
    user.so_dien_thoai = phone

    # Cập nhật thông tin chi tiết bảng BenhNhan (1-1)
    patient = user.benh_nhan_profile
    if not patient:
        from datetime import datetime
        dob_date = datetime.strptime(dob, "%Y-%m-%d").date() if dob else None
        patient = BenhNhan(
            nguoi_dung_id=user.id,
            ngay_sinh=dob_date,
            gioitinh=gender,
            dia_chi=address
        )
        db.add(patient)
    else:
        patient.gioitinh = gender
        patient.dia_chi = address
        if dob:
            from datetime import datetime
            patient.ngay_sinh = datetime.strptime(dob, "%Y-%m-%d").date()
        else:
            patient.ngay_sinh = None

    db.commit()

    # Cập nhật lại tên hiển thị trong session
    request.session["user_name"] = user.ho_ten

    return RedirectResponse(url="/ho_so_ca_nhan", status_code=status.HTTP_303_SEE_OTHER)


# 10. Xử lý ĐỔI MẬT KHẨU (POST /change_password)
@app.post("/change_password", tags=["Frontend UI"])
def handle_change_password(
        request: Request,
        current_password: str = Form(...),
        new_password: str = Form(...),
        confirm_password: str = Form(...),
        db: Session = Depends(get_db)
):
    user_email = request.session.get("user_email")
    if not user_email:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

    user = db.query(NguoiDung).filter(NguoiDung.email == user_email).first()
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

    # Kiểm tra mật khẩu hiện tại có đúng không
    if user.mat_khau != current_password:
        return RedirectResponse(url="/ho_so_ca_nhan", status_code=status.HTTP_303_SEE_OTHER)

    # Kiểm tra mật khẩu mới và xác nhận mật khẩu có khớp nhau không
    if new_password != confirm_password:
        return RedirectResponse(url="/ho_so_ca_nhan", status_code=status.HTTP_303_SEE_OTHER)

    # Cập nhật mật khẩu mới
    user.mat_khau = new_password
    db.commit()

    return RedirectResponse(url="/ho_so_ca_nhan", status_code=status.HTTP_303_SEE_OTHER)


# 11. Tab Tìm kiếm Bác sĩ
@app.get("/danh_sach_bac_si", response_class=HTMLResponse, tags=["Frontend UI"])
def serve_danh_sach_bac_si(request: Request):
    user_email = request.session.get("user_email")
    if not user_email:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    
    return templates.TemplateResponse(request, "benh_nhan/home_bn.html", {
        "user_name": request.session.get("user_name"),
        "user_email": user_email
    })


# 12. Tab Đặt lịch khám
@app.get("/dat_lich", response_class=HTMLResponse, tags=["Frontend UI"])
def serve_dat_lich(request: Request):
    user_email = request.session.get("user_email")
    if not user_email:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    
    return templates.TemplateResponse(request, "benh_nhan/dat_lich.html", {
        "user_name": request.session.get("user_name"),
        "user_email": user_email
    })


# 13. Tab Lịch hẹn của tôi
@app.get("/danh_sach_lich_hen", response_class=HTMLResponse, tags=["Frontend UI"])
def serve_danh_sach_lich_hen(request: Request):
    user_email = request.session.get("user_email")
    if not user_email:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    
    return templates.TemplateResponse(request, "benh_nhan/home_bn.html", {
        "user_name": request.session.get("user_name"),
        "user_email": user_email
    })


# ==========================================
# ADMIN & SYSTEM HEALTHCHECK
# ==========================================

# Route hiển thị giao diện Frontend Dashboard Admin
@app.get("/admin/dashboard", tags=["Admin Frontend"])
def serve_dashboard():
    file_path = BASE_DIR / "templates" / "dashboard.html"
    return FileResponse(str(file_path))


# Route kiểm tra tình trạng hoạt động của hệ thống (HealthCheck)
@app.get("/health", tags=["HealthCheck"])
def read_root():
    return {
        "status": "online",
        "service": "MedBooking API",
        "docs": "/docs",
    }