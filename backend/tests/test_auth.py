import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.database import Base, get_db
from app.main import app
from app.models.models import NguoiDung
from app.auth import get_password_hash

# ============ CẤU HÌNH DB TEST ============

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_auth.db"
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
def setup_user():
    """Tạo user mẫu trước mỗi test."""
    db = TestingSessionLocal()
    db.query(NguoiDung).delete()
    db.commit()
    
    user = NguoiDung(
        email="test@medbooking.com",
        mat_khau=get_password_hash("TestPassword123"),
        ho_ten="Test User",
        so_dien_thoai="0901234567",
        vai_tro="benh_nhan",
        trang_thai=True
    )
    db.add(user)
    db.commit()
    db.close()
    
    yield
    
    db = TestingSessionLocal()
    db.query(NguoiDung).delete()
    db.commit()
    db.close()


# ============ TEST 1: ROOT ============

def test_root():
    """Test API GET / — HealthCheck."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert data["service"] == "MedBooking API"
    assert data["docs"] == "/docs"


# ============ TEST 2: ĐĂNG KÝ ============

def test_register_success(setup_user):
    """Test đăng ký thành công."""
    response = client.post(
        "/api/auth/register",
        json={
            "ho_ten": "Nguyễn Văn A",
            "email": "newuser@test.com",
            "so_dien_thoai": "0987654321",
            "mat_khau": "Password123"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert "message" in data
    assert "user_id" in data
    assert data["message"] == "Đăng ký tài khoản thành công."


def test_register_duplicate_email(setup_user):
    """Test đăng ký với email đã tồn tại."""
    response = client.post(
        "/api/auth/register",
        json={
            "ho_ten": "Nguyễn Văn B",
            "email": "test@medbooking.com",  # Email đã tồn tại
            "so_dien_thoai": "0987654322",
            "mat_khau": "Password123"
        }
    )
    assert response.status_code == 400
    assert "đã được sử dụng" in response.json()["detail"]


def test_register_invalid_email(setup_user):
    """Test đăng ký với email không hợp lệ."""
    response = client.post(
        "/api/auth/register",
        json={
            "ho_ten": "Nguyễn Văn C",
            "email": "invalid_email",
            "so_dien_thoai": "0987654323",
            "mat_khau": "Password123"
        }
    )
    assert response.status_code == 422


def test_register_missing_fields(setup_user):
    """Test đăng ký thiếu trường bắt buộc."""
    response = client.post(
        "/api/auth/register",
        json={
            "ho_ten": "Nguyễn Văn D"
            # Thiếu email, password, phone
        }
    )
    assert response.status_code == 422


# ============ TEST 3: ĐĂNG NHẬP ============

def test_login_success(setup_user):
    """Test đăng nhập thành công."""
    response = client.post(
        "/api/auth/login",
        data={
            "username": "test@medbooking.com",
            "password": "TestPassword123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["vai_tro"] == "benh_nhan"
    assert data["ho_ten"] == "Test User"
    assert "user_id" in data


def test_login_wrong_password(setup_user):
    """Test đăng nhập sai mật khẩu."""
    response = client.post(
        "/api/auth/login",
        data={
            "username": "test@medbooking.com",
            "password": "WrongPassword"
        }
    )
    assert response.status_code == 401
    assert "không chính xác" in response.json()["detail"]


def test_login_nonexistent_user(setup_user):
    """Test đăng nhập với user không tồn tại."""
    response = client.post(
        "/api/auth/login",
        data={
            "username": "nonexistent@test.com",
            "password": "Password123"
        }
    )
    assert response.status_code == 401


# ============ TEST 4: GET /ME ============

def test_get_me_success(setup_user):
    """Test lấy thông tin user hiện tại."""
    # Đăng nhập trước
    login_response = client.post(
        "/api/auth/login",
        data={
            "username": "test@medbooking.com",
            "password": "TestPassword123"
        }
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Lấy thông tin
    response = client.get("/api/auth/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@medbooking.com"
    assert data["ho_ten"] == "Test User"
    assert data["vai_tro"] == "benh_nhan"


def test_get_me_no_token(setup_user):
    """Test lấy thông tin user không có token."""
    response = client.get("/api/auth/me")
    assert response.status_code == 401


# ============ TEST 5: ĐỔI MẬT KHẨU ============

def test_change_password_success(setup_user):
    """Test đổi mật khẩu thành công."""
    # Đăng nhập
    login_response = client.post(
        "/api/auth/login",
        data={
            "username": "test@medbooking.com",
            "password": "TestPassword123"
        }
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Đổi mật khẩu
    response = client.post(
        "/api/auth/change-password",
        headers=headers,
        json={
            "mat_khau_cu": "TestPassword123",
            "mat_khau_moi": "NewPassword456"
        }
    )
    assert response.status_code == 200
    assert "thành công" in response.json()["message"]


def test_change_password_wrong_old(setup_user):
    """Test đổi mật khẩu với mật khẩu cũ sai."""
    login_response = client.post(
        "/api/auth/login",
        data={
            "username": "test@medbooking.com",
            "password": "TestPassword123"
        }
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.post(
        "/api/auth/change-password",
        headers=headers,
        json={
            "mat_khau_cu": "WrongOldPassword",
            "mat_khau_moi": "NewPassword456"
        }
    )
    assert response.status_code == 400