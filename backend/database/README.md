# Database — MedBooking

## 📁 Cấu trúc

database/
├── schema/              ← Tạo bảng (12 file)
├── seed/                ← Data mẫu (4 file)
├── init.sql             ← File tổng
├── seed.sql
└── README.md

## 📊 12 bảng

| # | Tên bảng | File schema |
|---|----------|-------------|
| 1 | nguoi_dung | 01_nguoi_dung.sql |
| 2 | admin | 02_admin.sql |
| 3 | benh_nhan | 03_benh_nhan.sql |
| 4 | bac_si | 04_bac_si.sql |
| 5 | chuyen_khoa | 05_chuyen_khoa.sql |
| 6 | dich_vu | 06_dich_vu.sql |
| 7 | lich_lam_viec | 07_lich_lam_viec.sql |
| 8 | lich_hen | 08_lich_hen.sql |
| 9 | thanh_toan | 09_thanh_toan.sql |
| 10 | log_trang_thai | 10_log_trang_thai.sql |
| 11 | trieu_chung | 11_trieu_chung.sql |
| 12 | trieu_chung_bac_si | 12_trieu_chung_bac_si.sql |

## 🚀 Cách chạy

Docker tự động chạy init.sql + seed.sql:

docker compose up --build

## 📝 Update

docker compose down -v
docker compose up --build