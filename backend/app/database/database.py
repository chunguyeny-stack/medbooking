import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. Cấu hình chuỗi kết nối cơ sở dữ liệu (Database URL)
# Bạn có thể dùng SQLite (mặc định cho dev/test) hoặc MySQL / PostgreSQL theo cấu hình dự án
# Ví dụ SQLite:
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./medbooking.db")

# Nếu dùng MySQL:
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:password@localhost:3306/medbooking?charset=utf8mb4"

# Nếu dùng PostgreSQL:
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@localhost:5432/medbooking"

# 2. Khởi tạo Engine
# connect_args={"check_same_thread": False} chỉ cần thiết khi sử dụng SQLite
connect_args = {}
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args=connect_args,
    echo=False  # Đặt True nếu muốn in chi tiết các câu lệnh SQL ra terminal
)

# 3. Khởi tạo SessionFactory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# 4. Khởi tạo Base Model (Tất cả model như bac_si, nguoi_dung... sẽ kế thừa từ Base này)
Base = declarative_base()


# 5. Dependency injection lấy DB session cho các Router trong FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
