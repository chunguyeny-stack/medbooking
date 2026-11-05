-- ==========================================================
-- FILE GỘP TỔNG: Khởi tạo & Cập nhật CSDL Phòng Khám
-- Cấu trúc đầy đủ: 12 module đã gộp
-- Lưu ý: Phần 1-2,4,5 = PostgreSQL | Phần 3,6–13 = SQL Server
-- ==========================================================

-- ==========================================================
-- PHẦN 1: BỔ SUNG CHUNG (xóa mềm + Tìm kiếm toàn văn) — PostgreSQL
-- ==========================================================

-- 1. CỘT XÓA MỀM & THEO DÕI
ALTER TABLE nguoi_dung
ADD COLUMN IF NOT EXISTS xoa_luc TIMESTAMP,
ADD COLUMN IF NOT EXISTS xoa_boi INT REFERENCES nguoi_dung(id),
ADD COLUMN IF NOT EXISTS ly_do_xoa TEXT,
ADD COLUMN IF NOT EXISTS created_by INT REFERENCES nguoi_dung(id),
ADD COLUMN IF NOT EXISTS updated_by INT REFERENCES nguoi_dung(id);

ALTER TABLE bac_si
ADD COLUMN IF NOT EXISTS xoa_luc TIMESTAMP,
ADD COLUMN IF NOT EXISTS xoa_boi INT REFERENCES nguoi_dung(id),
ADD COLUMN IF NOT EXISTS ly_do_xoa TEXT,
ADD COLUMN IF NOT EXISTS created_by INT REFERENCES nguoi_dung(id),
ADD COLUMN IF NOT EXISTS updated_by INT REFERENCES nguoi_dung(id);

ALTER TABLE benh_nhan
ADD COLUMN IF NOT EXISTS xoa_luc TIMESTAMP,
ADD COLUMN IF NOT EXISTS xoa_boi INT REFERENCES nguoi_dung(id),
ADD COLUMN IF NOT EXISTS ly_do_xoa TEXT,
ADD COLUMN IF NOT EXISTS created_by INT REFERENCES nguoi_dung(id),
ADD COLUMN IF NOT EXISTS updated_by INT REFERENCES nguoi_dung(id);

ALTER TABLE lich_hen
ADD COLUMN IF NOT EXISTS xoa_luc TIMESTAMP,
ADD COLUMN IF NOT EXISTS xoa_boi INT REFERENCES nguoi_dung(id),
ADD COLUMN IF NOT EXISTS ly_do_xoa TEXT,
ADD COLUMN IF NOT EXISTS created_by INT REFERENCES nguoi_dung(id),
ADD COLUMN IF NOT EXISTS updated_by INT REFERENCES nguoi_dung(id);

ALTER TABLE chuyen_khoa
ADD COLUMN IF NOT EXISTS xoa_luc TIMESTAMP,
ADD COLUMN IF NOT EXISTS xoa_boi INT REFERENCES nguoi_dung(id),
ADD COLUMN IF NOT EXISTS ly_do_xoa TEXT,
ADD COLUMN IF NOT EXISTS created_by INT REFERENCES nguoi_dung(id),
ADD COLUMN IF NOT EXISTS updated_by INT REFERENCES nguoi_dung(id);

ALTER TABLE dich_vu
ADD COLUMN IF NOT EXISTS xoa_luc TIMESTAMP,
ADD COLUMN IF NOT EXISTS xoa_boi INT REFERENCES nguoi_dung(id),
ADD COLUMN IF NOT EXISTS ly_do_xoa TEXT,
ADD COLUMN IF NOT EXISTS created_by INT REFERENCES nguoi_dung(id),
ADD COLUMN IF NOT EXISTS updated_by INT REFERENCES nguoi_dung(id);

ALTER TABLE phan_hoi
ADD COLUMN IF NOT EXISTS xoa_luc TIMESTAMP,
ADD COLUMN IF NOT EXISTS xoa_boi INT REFERENCES nguoi_dung(id),
ADD COLUMN IF NOT EXISTS ly_do_xoa TEXT,
ADD COLUMN IF NOT EXISTS created_by INT REFERENCES nguoi_dung(id),
ADD COLUMN IF NOT EXISTS updated_by INT REFERENCES nguoi_dung(id);

-- 2. TÌM KIẾM TOÀN VĂN
ALTER TABLE bac_si ADD COLUMN IF NOT EXISTS fts_vector TSVECTOR;
CREATE INDEX IF NOT EXISTS idx_bacsi_fts ON bac_si USING gin(fts_vector);

CREATE OR REPLACE FUNCTION bac_si_fts_update() RETURNS TRIGGER AS $$
BEGIN
    NEW.fts_vector :=
        setweight(to_tsvector('simple', COALESCE(NEW.ten, '')), 'A') ||
        setweight(to_tsvector('simple', COALESCE(NEW.chuyen_mon, '')), 'B') ||
        setweight(to_tsvector('simple', COALESCE(NEW.bio, '')), 'C');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_bacsi_fts ON bac_si;
CREATE TRIGGER trg_bacsi_fts
BEFORE INSERT OR UPDATE ON bac_si
FOR EACH ROW EXECUTE FUNCTION bac_si_fts_update();

ALTER TABLE benh_nhan ADD COLUMN IF NOT EXISTS fts_vector TSVECTOR;
CREATE INDEX IF NOT EXISTS idx_benhnhan_fts ON benh_nhan USING gin(fts_vector);

CREATE OR REPLACE FUNCTION benh_nhan_fts_update() RETURNS TRIGGER AS $$
BEGIN
    NEW.fts_vector :=
        setweight(to_tsvector('simple', COALESCE(NEW.ten, '')), 'A') ||
        setweight(to_tsvector('simple', COALESCE(NEW.email, '')), 'B') ||
        setweight(to_tsvector('simple', COALESCE(NEW.dien_thoai, '')), 'C');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_benhnhan_fts ON benh_nhan;
CREATE TRIGGER trg_benhnhan_fts
BEFORE INSERT OR UPDATE ON benh_nhan
FOR EACH ROW EXECUTE FUNCTION benh_nhan_fts_update();

-- ==========================================================
-- PHẦN 2: BỔ SUNG BẢNG nguoi_dung — PostgreSQL
-- ==========================================================
ALTER TABLE nguoi_dung
ADD COLUMN IF NOT EXISTS trang_thai INT DEFAULT 0;

ALTER TABLE nguoi_dung
ADD COLUMN IF NOT EXISTS bat_buoc_doi_mk BOOLEAN DEFAULT FALSE;

ALTER TABLE nguoi_dung
ADD COLUMN IF NOT EXISTS reset_token VARCHAR(255),
ADD COLUMN IF NOT EXISTS reset_token_expires TIMESTAMP;

-- ==========================================================
-- PHẦN 3: TẠO BẢNG admin — SQL Server
-- ==========================================================
USE PhongKhamDB;
GO

IF OBJECT_ID('dbo.admin', 'U') IS NOT NULL DROP TABLE dbo.admin;
GO

CREATE TABLE dbo.admin (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nguoi_dung_id INT NOT NULL UNIQUE,
    phong_ban NVARCHAR(100) NULL,
    cap_do NVARCHAR(50) NULL,
    ghi_chu NVARCHAR(255) NULL,
    CONSTRAINT FK_admin_nguoi_dung FOREIGN KEY (nguoi_dung_id) REFERENCES dbo.nguoi_dung(id) ON DELETE CASCADE
);
GO

-- ==========================================================
-- PHẦN 4: BỔ SUNG BẢNG benh_nhan — PostgreSQL
-- ==========================================================
ALTER TABLE benh_nhan
ADD COLUMN IF NOT EXISTS cccd VARCHAR(20) UNIQUE;

-- ==========================================================
-- PHẦN 5: BỔ SUNG BẢNG bac_si — PostgreSQL
-- ==========================================================
ALTER TABLE bac_si
ADD COLUMN IF NOT EXISTS is_hot BOOLEAN DEFAULT FALSE,
ADD COLUMN IF NOT EXISTS is_new BOOLEAN DEFAULT FALSE,
ADD COLUMN IF NOT EXISTS display_order INT DEFAULT 0,
ADD COLUMN IF NOT EXISTS avatar_url TEXT,
ADD COLUMN IF NOT EXISTS bio TEXT,
ADD COLUMN IF NOT EXISTS training TEXT,
ADD COLUMN IF NOT EXISTS strengths TEXT;

-- ==========================================================
-- PHẦN 6: TẠO BẢNG chuyen_khoa & FK — SQL Server
-- ==========================================================
USE PhongKhamDB;
GO

IF OBJECT_ID('dbo.chuyen_khoa', 'U') IS NOT NULL DROP TABLE dbo.chuyen_khoa;
GO

CREATE TABLE dbo.chuyen_khoa (
    id INT IDENTITY(1,1) PRIMARY KEY,
    ten_chuyen_khoa NVARCHAR(100) NOT NULL UNIQUE,
    mo_ta NVARCHAR(255) NULL
);
GO

IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE name = 'FK_bac_si_chuyen_khoa')
BEGIN
    ALTER TABLE dbo.bac_si 
    ADD CONSTRAINT FK_bac_si_chuyen_khoa 
    FOREIGN KEY (chuyen_khoa_id) REFERENCES dbo.chuyen_khoa(id);
END
GO

-- ==========================================================
-- PHẦN 7: TẠO BẢNG dich_vu — SQL Server
-- ==========================================================
USE PhongKhamDB;
GO

IF OBJECT_ID('dbo.dich_vu', 'U') IS NOT NULL DROP TABLE dbo.dich_vu;
GO

CREATE TABLE dbo.dich_vu (
    id INT IDENTITY(1,1) PRIMARY KEY,
    chuyen_khoa_id INT NOT NULL,
    ten_dich_vu NVARCHAR(100) NOT NULL,
    gia_tien DECIMAL(18,2) NOT NULL DEFAULT 0.00,
    mo_ta NVARCHAR(255) NULL,
    dang_hoat_dong BIT NOT NULL DEFAULT 1,
    CONSTRAINT FK_dich_vu_chuyen_khoa FOREIGN KEY (chuyen_khoa_id) REFERENCES dbo.chuyen_khoa(id)
);
GO

-- ==========================================================
-- PHẦN 8: TẠO BẢNG lich_lam_viec — SQL Server
-- ==========================================================
USE PhongKhamDB;
GO

IF OBJECT_ID('dbo.lich_lam_viec', 'U') IS NOT NULL DROP TABLE dbo.lich_lam_viec;
GO

CREATE TABLE dbo.lich_lam_viec (
    id INT IDENTITY(1,1) PRIMARY KEY,
    bac_si_id INT NOT NULL,
    ngay_kham DATE NOT NULL,
    khung_gio NVARCHAR(100) NOT NULL,
    con_trong BIT NOT NULL DEFAULT 1,
    CONSTRAINT FK_lich_lam_viec_bac_si FOREIGN KEY (bac_si_id) REFERENCES dbo.bac_si(id) ON DELETE CASCADE
);
GO

-- ==========================================================
-- PHẦN 9: TẠO BẢNG lich_hen — SQL Server
-- ==========================================================
USE PhongKhamDB;
GO

IF OBJECT_ID('dbo.lich_hen', 'U') IS NOT NULL DROP TABLE dbo.lich_hen;
GO

CREATE TABLE dbo.lich_hen (
    id INT IDENTITY(1,1) PRIMARY KEY,
    benh_nhan_id INT NOT NULL,
    bac_si_id INT NOT NULL,
    dich_vu_id INT NOT NULL,
    ngay_kham DATE NOT NULL,
    khung_gio NVARCHAR(100) NOT NULL,
    trang_thai NVARCHAR(50) NOT NULL DEFAULT N'Chờ xác nhận',
    ghi_chu NVARCHAR(255) NULL,
    created_at DATETIME DEFAULT GETDATE(),
    CONSTRAINT FK_lich_hen_benh_nhan FOREIGN KEY (benh_nhan_id) REFERENCES dbo.benh_nhan(id),
    CONSTRAINT FK_lich_hen_bac_si FOREIGN KEY (bac_si_id) REFERENCES dbo.bac_si(id),
    CONSTRAINT FK_lich_hen_dich_vu FOREIGN KEY (dich_vu_id) REFERENCES dbo.dich_vu(id)
);
GO

-- ==========================================================
-- PHẦN 10: TẠO BẢNG thanh_toan — SQL Server
-- ==========================================================
USE PhongKhamDB;
GO

IF OBJECT_ID('dbo.thanh_toan', 'U') IS NOT NULL DROP TABLE dbo.thanh_toan;
GO

CREATE TABLE dbo.thanh_toan (
    id INT IDENTITY(1,1) PRIMARY KEY,
    lich_hen_id INT NOT NULL UNIQUE,
    tong_tien DECIMAL(18,2) NOT NULL DEFAULT 0.00,
    phuong_thuc NVARCHAR(50) NULL,
    trang_thai_thanh_toan NVARCHAR(50) NOT NULL DEFAULT N'Chưa thanh toán',
    ngay_thanh_toan DATETIME NULL,
    CONSTRAINT FK_thanh_toan_lich_hen FOREIGN KEY (lich_hen_id) REFERENCES dbo.lich_hen(id) ON DELETE CASCADE
);
GO

-- ==========================================================
-- PHẦN 11: TẠO BẢNG log_trang_thai — SQL Server
-- ==========================================================
USE PhongKhamDB;
GO

IF OBJECT_ID('dbo.log_trang_thai', 'U') IS NOT NULL DROP TABLE dbo.log_trang_thai;
GO

CREATE TABLE dbo.log_trang_thai (
    id INT IDENTITY(1,1) PRIMARY KEY,
    lich_hen_id INT NOT NULL,
    trang_thai_cu NVARCHAR(50) NULL,
    trang_thai_moi NVARCHAR(50) NOT NULL,
    nguoi_thuc_hien NVARCHAR(100) NOT NULL,
    thoi_gian DATETIME DEFAULT GETDATE(),
    CONSTRAINT FK_log_trang_thai_lich_hen FOREIGN KEY (lich_hen_id) REFERENCES dbo.lich_hen(id) ON DELETE CASCADE
);
GO

-- ==========================================================
-- PHẦN 12: TẠO BẢNG trieu_chung — SQL Server
-- ==========================================================
USE PhongKhamDB;
GO

IF OBJECT_ID('dbo.trieu_chung', 'U') IS NOT NULL DROP TABLE dbo.trieu_chung;
GO

CREATE TABLE dbo.trieu_chung (
    id INT IDENTITY(1,1) PRIMARY KEY,
    ten_trieu_chung NVARCHAR(255) NOT NULL,
    chuyen_khoa_id INT NOT NULL,
    CONSTRAINT FK_trieu_chung_chuyen_khoa FOREIGN KEY (chuyen_khoa_id) REFERENCES dbo.chuyen_khoa(id) ON DELETE CASCADE
);
GO

-- ==========================================================
-- PHẦN 13: TẠO BẢNG trieu_chung_bac_si — SQL Server
-- ==========================================================
USE PhongKhamDB;
GO

IF OBJECT_ID('dbo.trieu_chung_bac_si', 'U') IS NOT NULL DROP TABLE dbo.trieu_chung_bac_si;
GO

CREATE TABLE dbo.trieu_chung_bac_si (
    trieu_chung_id INT NOT NULL,
    bac_si_id INT NOT NULL,
    PRIMARY KEY (trieu_chung_id, bac_si_id),
    CONSTRAINT FK_tcbs_trieu_chung FOREIGN KEY (trieu_chung_id) REFERENCES dbo.trieu_chung(id) ON DELETE CASCADE,
    CONSTRAINT FK_tcbs_bac_si FOREIGN KEY (bac_si_id) REFERENCES dbo.bac_si(id) ON DELETE CASCADE
);
GO
