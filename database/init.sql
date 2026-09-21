-- 1. Tạo Database nếu chưa có
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'PhongKhamDB')
BEGIN
    CREATE DATABASE PhongKhamDB;
END
GO

USE PhongKhamDB;
GO

-- 2. Xóa các bảng cũ (theo thứ tự khóa ngoại từ bảng con đến bảng cha)
DROP TABLE IF EXISTS trieu_chung_bac_si;
DROP TABLE IF EXISTS trieu_chung;
DROP TABLE IF EXISTS log_trang_thai;
DROP TABLE IF EXISTS thanh_toan;
DROP TABLE IF EXISTS lich_hen;
DROP TABLE IF EXISTS lich_lam_viec;
DROP TABLE IF EXISTS dich_vu;
DROP TABLE IF EXISTS bac_si;
DROP TABLE IF EXISTS benh_nhan;
DROP TABLE IF EXISTS chuyen_khoa;
DROP TABLE IF EXISTS nguoi_dung;
GO

-- 3. Tạo bảng nguoi_dung
CREATE TABLE nguoi_dung (
    id INT IDENTITY(1,1) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    mat_khau VARCHAR(255) NOT NULL,
    ho_ten NVARCHAR(100) NOT NULL,
    so_dien_thoai VARCHAR(20),
    vai_tro VARCHAR(20) NOT NULL CHECK (vai_tro IN ('benh_nhan', 'bac_si', 'le_tan', 'admin')),
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE()
);
GO

-- 4. Tạo bảng benh_nhan
CREATE TABLE benh_nhan (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nguoi_dung_id INT UNIQUE NOT NULL FOREIGN KEY REFERENCES nguoi_dung(id) ON DELETE CASCADE,
    ngay_sinh DATE,
    gioi_tinh NVARCHAR(10) CHECK (gioi_tinh IN (N'Nam', N'Nữ', N'Khác')),
    dia_chi NVARCHAR(MAX)
);
GO

-- 5. Tạo bảng chuyen_khoa
CREATE TABLE chuyen_khoa (
    id INT IDENTITY(1,1) PRIMARY KEY,
    ten_chuyen_khoa NVARCHAR(100) NOT NULL UNIQUE,
    mo_ta NVARCHAR(MAX)
);
GO

-- 6. Tạo bảng bac_si
CREATE TABLE bac_si (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nguoi_dung_id INT UNIQUE NOT NULL FOREIGN KEY REFERENCES nguoi_dung(id) ON DELETE CASCADE,
    chuyen_khoa_id INT NOT NULL FOREIGN KEY REFERENCES chuyen_khoa(id),
    mo_ta NVARCHAR(MAX),
    rating NUMERIC(2, 1) DEFAULT 5.0 CHECK (rating >= 0.0 AND rating <= 5.0)
);
GO

-- 7. Tạo bảng dich_vu
CREATE TABLE dich_vu (
    id INT IDENTITY(1,1) PRIMARY KEY,
    chuyen_khoa_id INT NOT NULL FOREIGN KEY REFERENCES chuyen_khoa(id) ON DELETE CASCADE,
    ten_dich_vu NVARCHAR(150) NOT NULL,
    gia_tien NUMERIC(12, 2) NOT NULL CHECK (gia_tien >= 0),
    mo_ta NVARCHAR(MAX)
);
GO

-- 8. Tạo bảng lich_lam_viec
CREATE TABLE lich_lam_viec (
    id INT IDENTITY(1,1) PRIMARY KEY,
    bac_si_id INT NOT NULL FOREIGN KEY REFERENCES bac_si(id) ON DELETE CASCADE,
    ngay_kham DATE NOT NULL,
    khung_gio NVARCHAR(50) NOT NULL,
    trang_thai_trong BIT DEFAULT 1, -- 1: TRUE, 0: FALSE
    CONSTRAINT UQ_LichLamViec UNIQUE(bac_si_id, ngay_kham, khung_gio)
);
GO

-- 9. Tạo bảng lich_hen
CREATE TABLE lich_hen (
    id INT IDENTITY(1,1) PRIMARY KEY,
    benh_nhan_id INT NOT NULL FOREIGN KEY REFERENCES benh_nhan(id),
    bac_si_id INT NOT NULL FOREIGN KEY REFERENCES bac_si(id),
    dich_vu_id INT NOT NULL FOREIGN KEY REFERENCES dich_vu(id),
    ngay_kham DATE NOT NULL,
    khung_gio NVARCHAR(50) NOT NULL,
    trang_thai VARCHAR(30) DEFAULT 'cho_xac_nhan' 
        CHECK (trang_thai IN ('cho_xac_nhan', 'da_xac_nhan', 'dang_kham', 'can_tai_kham', 'hoan_thanh', 'da_huy')),
    created_at DATETIME DEFAULT GETDATE()
);
GO

-- 10. Tạo bảng thanh_toan
CREATE TABLE thanh_toan (
    id INT IDENTITY(1,1) PRIMARY KEY,
    lich_hen_id INT UNIQUE NOT NULL FOREIGN KEY REFERENCES lich_hen(id) ON DELETE CASCADE,
    so_tien NUMERIC(12, 2) NOT NULL CHECK (so_tien >= 0),
    phuong_thuc NVARCHAR(50) DEFAULT 'chuyen_khoan',
    trang_thai VARCHAR(30) DEFAULT 'chua_thanh_toan' 
        CHECK (trang_thai IN ('chua_thanh_toan', 'da_thanh_toan', 'that_bai')),
    created_at DATETIME DEFAULT GETDATE()
);
GO

-- 11. Tạo bảng log_trang_thai
CREATE TABLE log_trang_thai (
    id INT IDENTITY(1,1) PRIMARY KEY,
    lich_hen_id INT NOT NULL FOREIGN KEY REFERENCES lich_hen(id) ON DELETE CASCADE,
    trang_thai_cu VARCHAR(30),
    trang_thai_moi VARCHAR(30) NOT NULL,
    thoi_gian DATETIME DEFAULT GETDATE()
);
GO

-- 12. Tạo bảng trieu_chung
CREATE TABLE trieu_chung (
    id INT IDENTITY(1,1) PRIMARY KEY,
    ten_trieu_chung NVARCHAR(150) NOT NULL UNIQUE,
    chuyen_khoa_id INT NOT NULL FOREIGN KEY REFERENCES chuyen_khoa(id) ON DELETE CASCADE
);
GO

-- 13. Tạo bảng trieu_chung_bac_si
CREATE TABLE trieu_chung_bac_si (
    id INT IDENTITY(1,1) PRIMARY KEY,
    trieu_chung_id INT NOT NULL FOREIGN KEY REFERENCES trieu_chung(id) ON DELETE CASCADE,
    bac_si_id INT NOT NULL FOREIGN KEY REFERENCES bac_si(id),
    CONSTRAINT UQ_TrieuChungBacSi UNIQUE(trieu_chung_id, bac_si_id)
);
GO

-- 14. INDEXES
CREATE INDEX idx_bac_si_chuyen_khoa ON bac_si(chuyen_khoa_id);
CREATE INDEX idx_bac_si_rating ON bac_si(rating DESC);
CREATE INDEX idx_lich_lam_viec_lookup ON lich_lam_viec(bac_si_id, ngay_kham, trang_thai_trong);
CREATE INDEX idx_lich_hen_benh_nhan ON lich_hen(benh_nhan_id);
CREATE INDEX idx_lich_hen_bac_si ON lich_hen(bac_si_id);
GO

-- 15. TRIGGER TỰ ĐỘNG GHI LOG TRẠNG THÁI LỊCH HẸN (T-SQL)
CREATE TRIGGER trg_log_trang_thai_lich_hen
ON lich_hen
AFTER INSERT, UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    -- Trường hợp INSERT
    IF NOT EXISTS (SELECT 1 FROM deleted)
    BEGIN
        INSERT INTO log_trang_thai (lich_hen_id, trang_thai_cu, trang_thai_moi)
        SELECT i.id, NULL, i.trang_thai
        FROM inserted i;
    END
    -- Trường hợp UPDATE
    ELSE
    BEGIN
        INSERT INTO log_trang_thai (lich_hen_id, trang_thai_cu, trang_thai_moi)
        SELECT i.id, d.trang_thai, i.trang_thai
        FROM inserted i
        JOIN deleted d ON i.id = d.id
        WHERE ISNULL(i.trang_thai, '') <> ISNULL(d.trang_thai, '');
    END
END;
GO
