from fastapi import FastAPI
from app.routers.auth import router as auth_router

app = FastAPI(title="MedBooking API")


@app.get("/")
def root():
    return {"message": "Chào mừng đến với hệ thống MedBooking API!"}


app.include_router(auth_router)