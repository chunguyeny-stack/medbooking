from app.database import Base, engine
from fastapi import FastAPI
from app.routers import auth, doctors

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Medbooking Backend API",
    version="1.0.0",
    description="Hệ thống Backend quản lý Bác sĩ, Dị bản, Phân quyền và Lịch hẹn",
)

app.include_router(auth.router)
app.include_router(doctors.router)


@app.get("/")
def root():
  return {"message": "Hệ thống Medbooking Backend đang chạy ổn định!"}