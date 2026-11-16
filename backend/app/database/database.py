import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# ============================================================
# 1. Cấu hình chuỗi kết nối cơ sở dữ liệu (Database URL)
# ============================================================
# Dự án MedBooking sử dụng SQL Server (qua pymssql).
# Biến DATABASE_URL được cấu hình trong docker-compose.yml hoặc file .env.
#
# Ví dụ:
#   - Docker:     mssql+pymssql://sa:MedPassword123!@db:1433/PhongKhamDB
#   - Local:      mssql+pymssql://sa:MedPassword123!@localhost:1433/PhongKhamDB
#   - Railway:    mssql+pymssql://sa:<password>@<host>:<port>/PhongKhamDB

SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mssql+pymssql://sa:MedPassword123!@localhost:1433/PhongKhamDB"
)

# ============================================================
# 2. Khởi tạo Engine
# ============================================================
# connect_args={"check_same_thread": False} chỉ cần thiết khi sử dụng SQLite.
# Với SQL Server (pymssql), không cần connect_args.
connect_args = {}
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args=connect_args,
    echo=False,  # Đặt True nếu muốn in chi tiết các câu lệnh SQL ra terminal
    pool_pre_ping=True,  # Kiểm tra kết nối trước khi dùng (tránh lỗi "connection closed")
)

# ============================================================
# 3. Khởi tạo SessionFactory
# ============================================================
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ============================================================
# 4. Khởi tạo Base Model
# ============================================================
Base = declarative_base()


# ============================================================
# 5. Dependency injection lấy DB session cho các Router FastAPI
# ============================================================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()