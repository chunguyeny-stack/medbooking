import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.database import Base, get_db
from app.main import app
from app.models.models import NguoiDung, BacSi, ChuyenKhoa, DichVu
from app.auth import get_password_hash

# ============ CẤU HÌNH DB TEST ============

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_integration.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


# ============ FIXTURES ============

@pytest.fixture(scope="function")
def setup_data():
    """Tạo dữ liệu mẫu trước mỗi test."""
    db = TestingSessionLocal()
    
    # Xóa dữ liệu cũ
    db.query(NguoiDung).delete()
    db.query(BacSi).delete()
    db.query(ChuyenKhoa).delete()
    db.query(DichVu).delete()
    db.commit()
    
    # Tạo chuyên khoa
    chuyen_khoa = ChuyenKhoa(
        ten_chuyen_khoa="Thần kinh",
        mo_ta="Khám và điều trị bệnh thần kinh"
    )
    db.add(chuyen_khoa)
    db.commit()
    db.refresh(chuyen_khoa)
    
    # Tạo dịch vụ
    dich_vu = DichVu(
        chuyen_khoa_id=chuyen_khoa.id,
        ten_dich_vu="Khám thần kinh",
        gia_tien=250000,
        mo_ta="Khám chuyên khoa thần kinh",
        dang_hoat_dong=True
    )
    db.add(dich_vu)
    db.commit()
    
    # Tạo bác sĩ
    bac_si_user = NguoiDung(
        email="bs@test.com",
        mat_khau=get_password_hash("Bs123456"),
        ho_ten="BS Test",
        so_dien_thoai="0900000001",
        vai_tro="bac_si",
        trang_thai=True
    )
    db.add(bac_si_user)
    db.commit()
    db.refresh(bac_si_user)
    
    bac_si = BacSi(
        nguoi_dung_id=bac_si_user.id,
        chuyen_khoa_id=chuyen_khoa.id,
        hoc_vi="Bác sĩ CKI",
        kinh_nghiem=10,
        gia_kham=250000,
        rating=4.8
    )
    db.add(bac_si)
    db.commit()
    db.refresh(bac_si)
    
    db.close()
    
    yield {
        "chuyen_khoa_id": chuyen_khoa.id,
        "dich_vu_id": dich_vu.id,
        "bac_si_id": bac_si.id
    }
    
    # Dọn dẹp
    db = TestingSessionLocal()
    db.query(NguoiDung).delete()
    db.query(BacSi).delete()
    db.query(ChuyenKhoa).delete()
    db.query(DichVu).delete()
    db.commit()
    db.close()


# ============ TEST TÍCH HỢP ============

def test_full_booking_flow(setup_data):
    """
    Test tích hợp luồng:
    1. Đăng ký bệnh nhân
    2. Đăng nhập
    3. Đặt lịch khám
    """
    
    # Bước 1: Đăng ký
    register_response = client.post(
        "/api/auth/register",
        json={
            "ho_ten": "Bệnh Nhân Test",
            "email": "benhnhan@test.com",
            "so_dien_thoai": "0987654321",
            "mat_khau": "Patient123"
        }
    )
    assert register_response.status_code == 201
    user_id = register_response.json()["user_id"]
    
    # Bước 2: Đăng nhập
    login_response = client.post(
        "/api/auth/login",
        data={
            "username": "benhnhan@test.com",
            "password": "Patient123"
        }
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Bước 3: Lấy thông tin user
    me_response = client.get("/api/auth/me", headers=headers)
    assert me_response.status_code == 200
    assert me_response.json()["email"] == "benhnhan@test.com"