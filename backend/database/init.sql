-- ============================================================
-- INIT.SQL - Khởi tạo Cơ sở dữ liệu và Nạp dữ liệu ban đầu
-- Dự án: Hệ thống Đặt lịch khám trực tuyến MedBooking
-- Cấu trúc: 12 file Schema + 1 file Seed Data
-- ============================================================

-- 1. Tạo Cơ sở dữ liệu nếu chưa tồn tại
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'PhongKhamDB')
BEGIN
    CREATE DATABASE PhongKhamDB;
END
GO

USE PhongKhamDB;
GO

SET DATEFORMAT ymd;
GO

PRINT N'============================================================';
PRINT N'BẮT ĐẦU DỰNG KHUNG DỮ LIỆU (SCHEMA DEFINITION)...';
PRINT N'============================================================';
GO

-- 2. Thực thi lần lượt 12 file Schema trong thư mục schema/
-- LƯU Ý: Nếu chạy qua SQLCMD (Docker / Command Line), sử dụng cú pháp :r bên dưới:

:r ./schema/01_nguoi_dung.sql
:r ./schema/02_admin.sql
:r ./schema/03_benh_nhan.sql
:r ./schema/04_bac_si.sql
:r ./schema/05_chuyen_khoa.sql
:r ./schema/06_dich_vu.sql
:r ./schema/07_lich_lam_viec.sql
:r ./schema/08_lich_hen.sql
:r ./schema/09_thanh_toan.sql
:r ./schema/10_log_trang_thai.sql
:r ./schema/11_trieu_chung.sql
:r ./schema/12_trieu_chung_bac_si.sql

PRINT N'============================================================';
PRINT N'✅ KHỞI TẠO HOÀN TẤT 12 BẢNG SCHEMA!';
PRINT N'BẮT ĐẦU NẠP DỮ LIỆU MẪU (SEED DATA)...';
PRINT N'============================================================';
GO

-- 3. Thực thi nạp dữ liệu mẫu từ seed.sql
:r ./seed.sql

PRINT N'============================================================';
PRINT N'🎉 HỆ THỐNG MEDBOOKING ĐÃ SẴN SÀNG HOẠT ĐỘNG!';
PRINT N'============================================================';
GO