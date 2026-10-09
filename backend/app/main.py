from pathlib import Path
from fastapi import FastAPI, Request, Response
from fastapi.responses import FileResponse

# Khởi tạo cơ sở dữ liệu và models
from datadase.database import engine, Base
import models

# Import router xác thực và các phân hệ nghiệp vụ
from routers.auth_router import router as auth_router
from routers.bac_si import router as bac_si_router
from routers.lich_hen import router as lich_hen_router
from routers.le_tan import router as le_tan_router

# Import router admin
from api.admin import router as admin_router

# Đảm bảo nạp models để tự động sinh bảng dữ liệu
_ = models
Base.metadata.create_all(bind=engine)

# Xác định đường dẫn thư mục gốc bằng Path chuẩn
BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="MedBooking API System",
    description="Hệ thống quản lý phòng khám, bác sĩ, lịch hẹn và tiếp đón.",
    version="1.0.0",
)


# Cấu hình CORS bằng HTTP Middleware native của FastAPI (không bị lỗi Type Checker PyCharm)
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


# Đăng ký toàn bộ các router vào tiền tố /api
app.include_router(auth_router, prefix="/api")
app.include_router(bac_si_router, prefix="/api")
app.include_router(lich_hen_router, prefix="/api")
app.include_router(le_tan_router, prefix="/api")
app.include_router(admin_router, prefix="/api")


# Route hiển thị giao diện Frontend Dashboard Admin
@app.get("/admin/dashboard", tags=["Admin Frontend"])
def serve_dashboard():
    file_path = BASE_DIR / "templates" / "dashboard.html"
    return FileResponse(str(file_path))


@app.get("/", tags=["HealthCheck"])
def read_root():
    return {
        "status": "online",
        "service": "MedBooking API",
        "docs": "/docs",
    }
