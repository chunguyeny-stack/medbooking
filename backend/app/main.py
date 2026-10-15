from pathlib import Path
from fastapi import FastAPI, Request, Response
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

# 1. Khởi tạo cơ sở dữ liệu và nạp models
from app.database.database import engine, Base
from app import models

# 2. Import TẤT CẢ các router
from app.api.core_auth import router as core_auth_router
from app.api.nghiep_vu import router as nghiep_vu_router
from app.api.admin import router as admin_router
from app.api.goi_y_router import router as goi_y_router

# Đảm bảo nạp models để tự động sinh bảng dữ liệu
_ = models
Base.metadata.create_all(bind=engine)

# Xác định đường dẫn thư mục gốc
BASE_DIR = Path(__file__).resolve().parent

# Khởi tạo ứng dụng FastAPI
app = FastAPI(
    title="MedBooking API System",
    description="Hệ thống quản lý phòng khám: Core Auth, Nghiệp vụ, Admin Dashboard và Gợi ý bác sĩ.",
    version="1.0.0",
)

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Đăng ký TẤT CẢ các router
app.include_router(core_auth_router, prefix="/api")
app.include_router(nghiep_vu_router, prefix="/api")
app.include_router(admin_router, prefix="/api")
app.include_router(goi_y_router, prefix="/api")

# Route hiển thị giao diện Frontend Dashboard Admin
@app.get("/admin/dashboard", tags=["Admin Frontend"])
def serve_dashboard():
    file_path = BASE_DIR / "templates" / "dashboard.html"
    return FileResponse(str(file_path))

# Route kiểm tra tình trạng hoạt động
@app.get("/", tags=["HealthCheck"])
def read_root():
    return {
        "status": "online",
        "service": "MedBooking API",
        "docs": "/docs",
    }