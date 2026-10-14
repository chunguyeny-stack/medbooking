from pathlib import Path
from fastapi import FastAPI, Request, Response
from fastapi.responses import FileResponse

# 1. Khởi tạo cơ sở dữ liệu và nạp models
from app.database.database import engine, Base
from app import models

# 2. Import trực tiếp các router từ thư mục api/ (tránh lỗi cache package của PyCharm)
from app.api.core_auth import router as core_auth_router
from app.api.nghiep_vu import router as nghiep_vu_router
from app.api.admin import router as admin_router

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


# Cấu hình CORS bằng HTTP Middleware native của FastAPI (sạch hoàn toàn cảnh báo Type Checker)
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


# Route hiển thị giao diện Frontend Dashboard Admin
@app.get("/admin/dashboard", tags=["Admin Frontend"])
def serve_dashboard():
    file_path = BASE_DIR / "templates" / "dashboard.html"
    return FileResponse(str(file_path))


# Route kiểm tra tình trạng hoạt động của hệ thống
@app.get("/", tags=["HealthCheck"])
def read_root():
    return {
        "status": "online",
        "service": "MedBooking API",
        "docs": "/docs",
    }
