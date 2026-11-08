import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.database import Base
from app.models.models import NguoiDung
from app.auth import get_password_hash, verify_password

# ============ CẤU HÌNH DB TEST ============
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_auth_isolated.db"

if os.path.exists("./test_auth_isolated.db"):
    os.remove("./test_auth_isolated.db")

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

# ============ FIXTURES ============
@pytest.fixture(scope="function")
def db_session():
    """Tạo session DB test, xóa sạch dữ liệu sau khi test xong."""
    db = TestingSessionLocal()
    yield db
    db.close()

@pytest.fixture(scope="function")
def setup_user(db_session):
    """Tạo user mẫu để test logic Đăng nhập."""
    # Xóa sạch bảng
    db_session.query(NguoiDung).delete()
    db_session.commit()
    
    # Tạo user với mật khẩu ĐÃ BĂM (chuẩn bảo mật)
    user = NguoiDung(
        email="test@medbooking.com",
        mat_khau=get_password_hash("TestPassword123"),
        ho_ten="Test User",
        so_dien_thoai="0901234567",
        vai_tro="benh_nhan",
        trang_thai=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

# ============ CÁC BÀI TEST CỐT LÕI ============

def test_register_success(db_session):
    """Test tạo user mới thành công."""
    new_user = NguoiDung(
        email="newuser@test.com",
        mat_khau=get_password_hash("Password123"),
        ho_ten="Nguyễn Văn A",
        vai_tro="benh_nhan",
        trang_thai=True
    )
    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user)
    
    assert new_user.id is not None
    assert new_user.email == "newuser@test.com"

def test_register_duplicate_email(db_session):
    """Test chặn trùng email."""
    # Tạo user đầu tiên
    user1 = NguoiDung(
        email="test@medbooking.com",
        mat_khau=get_password_hash("Password123"),
        ho_ten="Nguyễn Văn B",
        vai_tro="benh_nhan"
    )
    db_session.add(user1)
    db_session.commit()
    
    # Thử tạo user thứ 2 với cùng email
    user2 = NguoiDung(
        email="test@medbooking.com",
        mat_khau=get_password_hash("Password123"),
        ho_ten="Nguyễn Văn C",
        vai_tro="benh_nhan"
    )
    
    # Kỳ vọng: SQLAlchemy sẽ báo lỗi trùng lặp (UNIQUE constraint) hoặc bạn phải tự kiểm tra
    with pytest.raises(Exception):
        db_session.add(user2)
        db_session.commit()

def test_login_success(setup_user):
    """Test so khớp mật khẩu thành công."""
    user = setup_user
    assert verify_password("TestPassword123", user.mat_khau) is True

def test_login_wrong_password(setup_user):
    """Test so khớp mật khẩu sai."""
    user = setup_user
    assert verify_password("WrongPassword", user.mat_khau) is False