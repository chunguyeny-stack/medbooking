import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. Cấu hình chuỗi kết nối Database (ưu tiên đọc từ biến môi trường .env)
# Ví dụ các định dạng chuỗi kết nối:
# - SQLite (chạy dev nội bộ/test nhanh): "sqlite:///./medbooking.db"
# - PostgreSQL: "postgresql://user:password@localhost:5432/medbooking"
# - MySQL: "mysql+pymysql://user:password@localhost:3306/medbooking"
# - SQL Server: "mssql+pyodbc://sa:YourPassword@localhost:1433/medbooking?driver=ODBC+Driver+17+for+SQL+Server"

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./medbooking.db")

# Cấu hình engine: nếu dùng SQLite thì cần check_same_thread=False
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    echo=False  # Đổi thành True nếu bạn muốn in log câu lệnh SQL ra terminal khi dev
)

# 2. Tạo SessionLocal để quản lý phiên làm việc với database
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# 3. Khởi tạo Base class cho tất cả các SQLAlchemy Models kế thừa
Base = declarative_base()

# 4. Dependency cấp Session cho FastAPI Router
def get_db():
    """
    Dependency injection được truyền vào các endpoint trong router.
    Tự động mở session khi có request và đóng session sau khi request kết thúc.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
