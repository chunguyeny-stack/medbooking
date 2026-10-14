# MedBooking - Hệ thống Đặt lịch Khám và Quản lý

Hệ thống đặt lịch khám trực tuyến có gợi ý bác sĩ theo triệu chứng, phục vụ 4 phân hệ: Bệnh nhân, Lễ tân, Bác sĩ, Admin.

## 🛠 Công nghệ

- **Backend:** Python 3.11 + FastAPI + SQLAlchemy
- **Frontend:** HTML/CSS/JS + Jinja2 + Bootstrap
- **Database:** SQL Server 2022 (12 bảng)
- **Auth:** JWT + Bcrypt
- **Gợi ý bác sĩ:** Rule-based (Python)
- **Test:** pytest
- **CI/CD:** GitHub Actions
- **Đóng gói:** Docker + Docker Compose
- **Deploy:** Render / Railway

##  Chạy dự án

### Cách 1: Docker (khuyến nghị)

```bash
docker compose up --build
```

- Backend: http://localhost:8000
- Swagger: http://localhost:8000/docs

### Cách 2: Chạy local

```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 🧪 Chạy test

```bash
cd backend
pytest -v
```

## 📚 API Docs

http://localhost:8000/docs

## 📄 License

MIT