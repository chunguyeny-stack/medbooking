from fastapi import FastAPI
from .api.goi_y_router import router as goi_y_router

app = FastAPI(title="MedBooking — Gợi ý Bác sĩ", version="1.0.0")

# Đăng ký router
app.include_router(goi_y_router)

@app.get("/")
def root():
    return {
        "service": "MedBooking API",
        "endpoints": {
            "Gợi ý theo chuyên khoa": "/api/goi-y/bac-si?chuyen_khoa_id=X",
            "Gợi ý theo triệu chứng": "/api/goi-y/bac-si?trieu_chung_id=X",
            "Có lịch trống sớm": "/api/goi-y/bac-si-lich-trong"
        }
    }