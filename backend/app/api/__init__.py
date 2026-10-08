from importlib import import_module

from fastapi import APIRouter

api_router = APIRouter(prefix="/api/v1")


def _include_if_available(module_name: str, prefix: str, tags: list[str]):
    try:
        module = import_module(module_name)
    except ModuleNotFoundError:
        return

    router = getattr(module, "router", None)
    if router is not None:
        api_router.include_router(router, prefix=prefix, tags=tags)


# Hỗ trợ nhiều cấu trúc project khác nhau mà không crash khi module chưa tồn tại
_include_if_available("app.routers.auth", "/auth", ["Xác thực & Tài khoản"])
_include_if_available("app.routers.bac_si", "/doctors", ["Quản lý Bác sĩ"])
_include_if_available("app.routers.le_tan", "/receptionist", ["Nghiệp vụ Lễ tân"])
_include_if_available("app.routers.lich_hen", "/appointments", ["Quản lý Lịch hẹn"])

_include_if_available("routers.auth", "/auth", ["Xác thực & Tài khoản"])
_include_if_available("routers.bac_si", "/doctors", ["Quản lý Bác sĩ"])
_include_if_available("routers.le_tan", "/receptionist", ["Nghiệp vụ Lễ tân"])
_include_if_available("routers.lich_hen", "/appointments", ["Quản lý Lịch hẹn"])

_include_if_available("api.routers.auth", "/auth", ["Xác thực & Tài khoản"])
_include_if_available("api.routers.bac_si", "/doctors", ["Quản lý Bác sĩ"])
_include_if_available("api.routers.le_tan", "/receptionist", ["Nghiệp vụ Lễ tân"])
_include_if_available("api.routers.lich_hen", "/appointments", ["Quản lý Lịch hẹn"])

__all__ = ["api_router"]
