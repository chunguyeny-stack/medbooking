# MedBooking - Hệ thống Đặt lịch khám trực tuyến

Hệ thống đặt lịch khám có gợi ý bác sĩ theo triệu chứng.

## 🛠 Công nghệ

- **Backend:** Python 3.11 + FastAPI + SQLAlchemy
- **Frontend:** HTML/CSS/JS + Jinja2 + Bootstrap
- **Database:** PostgreSQL 15 (OLTP, 11 bảng)
- **Auth:** JWT
- **Gợi ý bác sĩ:** Rule-based (Python)
- **Test:** pytest
- **CI/CD:** GitHub Actions
- **Đóng gói:** Docker + Docker Compose
- **Deploy:** Render/Railway + Vercel

## 🚀 Chạy dự án

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

## 👥 Phân công nhóm

| Thành viên | Vai trò |
|-----------|---------|
| TV1 - Trà | Trưởng nhóm, DB, ERD, tích hợp |
| TV2 | Auth, user, phân quyền |
| TV3 | Nghiệp vụ (bác sĩ, lịch hẹn, thanh toán) |
| TV4 | Frontend |
| TV5 | DevOps, Test, Docs |

## 📄 License

MIT