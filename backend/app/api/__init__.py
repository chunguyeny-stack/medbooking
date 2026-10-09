from fastapi import APIRouter

# Import các router phân hệ từ thư mục routers/
from routers.auth_router import router as auth_router
from routers.bac_si import router as bac_si_router
from routers.lich_hen import router as lich_hen_router
from routers.le_tan import router as le_tan_router

# Import router admin từ thư mục api/
from api.admin import router as admin_router

# Khởi tạo API Router tổng
api_router = APIRouter()

# Đăng ký từng phân hệ
api_router.include_router(auth_router)
api_router.include_router(bac_si_router)
api_router.include_router(lich_hen_router)
api_router.include_router(le_tan_router)
api_router.include_router(admin_router)

__all__ = ["api_router"]
