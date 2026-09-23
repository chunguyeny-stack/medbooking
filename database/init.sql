-- ============================================================
-- INIT.SQL - SQL Server Database Schema
-- Dự án: Hệ thống Đặt lịch khám trực tuyến MedBooking
-- Đồng bộ 100% với ERD + UML Class Diagram đã sửa
-- ĐÃ BỔ SUNG: Bảng Admin + Trigger + Index
-- ============================================================

USE master;
GO

IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'PhongKhamDB')
BEGIN
    CREATE DATABASE PhongKhamDB;
END
GO

USE PhongKhamDB;
GO

-- ============================================================
-- 2. BẢNG NGUOI_DUNG (dùng chung cho tất cả vai trò)
-- ============================================================
CREATE TABLE nguoi_dung (
    id            INT IDENTITY(1,1) PRIMARY KEY,
    email         VARCHAR(255) UNIQUE NOT NULL,
    mat_khau      VARCHAR(255) NOT NULL,
    ho_ten        NVARCHAR(100) NOT NULL,
    so_dien_thoai VARCHAR(20),
    vai_tro       VARCHAR(20) NOT NULL 
                  CHECK (vai_tro IN ('benh_nhan', 'bac_si', 'le_tan', 'admin')),
    ngay_tao      DATETIME DEFAULT GETDATE()
);
GO

-- ============================================================
-- 3. BẢNG ADMIN (✅ BỔ SUNG - 1-1 với nguoi_dung)
-- Lưu thông tin bổ sung của tài khoản quản trị
-- ============================================================
CREATE TABLE admin (
    id             INT IDENTITY(1,1) PRIMARY KEY,
    nguoi_dung_id  INT UNIQUE NOT NULL,
    phong_ban      NVARCHAR(100),          -- Phòng ban (VD: IT, Quản trị hệ thống)
    cap_do         NVARCHAR(20) DEFAULT N'Cao' 
                   CHECK (cap_do IN (N'Cao', N'Trung', N'Thấp')),
    ghi_chu        NVARCHAR(MAX),
    CONSTRAINT fk_admin_nguoidung FOREIGN KEY (nguoi_dung_id) 
        REFERENCES nguoi_dung(id) ON DELETE CASCADE
);
GO

-- ============================================================
-- 4. BẢNG BENH_NHAN
-- ============================================================
CREATE TABLE benh_nhan (
    id            INT IDENTITY(1,1) PRIMARY KEY,
    nguoi_dung_id INT UNIQUE NOT NULL,
    ngay_sinh     DATE,
    gioi_tinh     NVARCHAR(10) 
                  CHECK (gioi_tinh IN (N'Nam', N'Nữ', N'Khác')),
    dia_chi       NVARCHAR(MAX),
    CONSTRAINT fk_bn_nguoidung FOREIGN KEY (nguoi_dung_id) 
        REFERENCES nguoi_dung(id) ON DELETE CASCADE
);
GO

-- ============================================================
-- 5. BẢNG CHUYEN_KHOA
-- ============================================================
CREATE TABLE chuyen_khoa (
    id              INT IDENTITY(1,1) PRIMARY KEY,
    ten_chuyen_khoa NVARCHAR(100) NOT NULL UNIQUE,
    mo_ta           NVARCHAR(MAX)
);
GO

-- ============================================================
-- 6. BẢNG BAC_SI
-- ============================================================
CREATE TABLE bac_si (
    id                 INT IDENTITY(1,1) PRIMARY KEY,
    nguoi_dung_id      INT UNIQUE NOT NULL,
    chuyen_khoa_id     INT NOT NULL,
    mo_ta              NVARCHAR(MAX),
    rating             NUMERIC(2,1) DEFAULT 5.0 
                       CHECK (rating >= 0.0 AND rating <= 5.0),
    so_luong_danh_gia  INT DEFAULT 0 
                       CHECK (so_luong_danh_gia >= 0),
    CONSTRAINT fk_bs_nguoidung FOREIGN KEY (nguoi_dung_id) 
        REFERENCES nguoi_dung(id) ON DELETE CASCADE,
    CONSTRAINT fk_bs_chuyenkhoa FOREIGN KEY (chuyen_khoa_id) 
        REFERENCES chuyen_khoa(id)
);
GO

-- ============================================================
-- 7. BẢNG DICH_VU
-- ============================================================
CREATE TABLE dich_vu (
    id              INT IDENTITY(1,1) PRIMARY KEY,
    chuyen_khoa_id  INT NOT NULL,
    ten_dich_vu     NVARCHAR(150) NOT NULL,
    gia_tien        NUMERIC(12,2) NOT NULL CHECK (gia_tien >= 0),
    mo_ta           NVARCHAR(MAX),
    dang_hoat_dong  BIT DEFAULT 1,
    CONSTRAINT fk_dv_chuyenkhoa FOREIGN KEY (chuyen_khoa_id) 
        REFERENCES chuyen_khoa(id) ON DELETE CASCADE
);
GO

-- ============================================================
-- 8. BẢNG TRIEU_CHUNG
-- ============================================================
CREATE TABLE trieu_chung (
    id              INT IDENTITY(1,1) PRIMARY KEY,
    ten_trieu_chung NVARCHAR(150) NOT NULL UNIQUE,
    chuyen_khoa_id  INT NOT NULL,
    CONSTRAINT fk_tc_chuyenkhoa FOREIGN KEY (chuyen_khoa_id) 
        REFERENCES chuyen_khoa(id) ON DELETE CASCADE
);
GO

-- ============================================================
-- 9. BẢNG LICH_LAM_VIEC
-- ============================================================
CREATE TABLE lich_lam_viec (
    id         INT IDENTITY(1,1) PRIMARY KEY,
    bac_si_id  INT NOT NULL,
    ngay_kham  DATE NOT NULL,
    khung_gio  NVARCHAR(50) NOT NULL,
    con_trong  BIT DEFAULT 1,
    CONSTRAINT fk_llv_bacsi FOREIGN KEY (bac_si_id) 
        REFERENCES bac_si(id) ON DELETE CASCADE,
    CONSTRAINT uq_lich_lam_viec UNIQUE (bac_si_id, ngay_kham, khung_gio)
);
GO

-- ============================================================
-- 10. BẢNG LICH_HEN
-- ============================================================
CREATE TABLE lich_hen (
    id                INT IDENTITY(1,1) PRIMARY KEY,
    benh_nhan_id      INT NOT NULL,
    bac_si_id         INT NOT NULL,
    dich_vu_id        INT NOT NULL,
    lich_lam_viec_id  INT NOT NULL,
    le_tan_id         INT NULL,
    trang_thai        VARCHAR(30) DEFAULT 'cho_xac_nhan'
                      CHECK (trang_thai IN (
                          'cho_xac_nhan', 'da_xac_nhan', 'dang_kham',
                          'can_tai_kham', 'hoan_thanh', 'da_huy'
                      )),
    ngay_tao          DATETIME DEFAULT GETDATE(),
    CONSTRAINT fk_lh_benhnhan FOREIGN KEY (benh_nhan_id) 
        REFERENCES benh_nhan(id),
    CONSTRAINT fk_lh_bacsi FOREIGN KEY (bac_si_id) 
        REFERENCES bac_si(id),
    CONSTRAINT fk_lh_dichvu FOREIGN KEY (dich_vu_id) 
        REFERENCES dich_vu(id),
    CONSTRAINT fk_lh_llv FOREIGN KEY (lich_lam_viec_id) 
        REFERENCES lich_lam_viec(id),
    CONSTRAINT fk_lh_letan FOREIGN KEY (le_tan_id) 
        REFERENCES nguoi_dung(id) ON DELETE SET NULL
);
GO

-- ============================================================
-- 11. BẢNG THANH_TOAN
-- ============================================================
CREATE TABLE thanh_toan (
    id          INT IDENTITY(1,1) PRIMARY KEY,
    lich_hen_id INT NOT NULL,
    so_tien     NUMERIC(12,2) NOT NULL CHECK (so_tien >= 0),
    phuong_thuc NVARCHAR(50) DEFAULT 'chuyen_khoan'
                CHECK (phuong_thuc IN ('tien_mat', 'chuyen_khoan', 'vi_dien_tu')),
    trang_thai  VARCHAR(30) DEFAULT 'chua_thanh_toan'
                CHECK (trang_thai IN ('chua_thanh_toan', 'da_thanh_toan', 'that_bai')),
    thoi_gian   DATETIME DEFAULT GETDATE(),
    CONSTRAINT fk_tt_lichhen FOREIGN KEY (lich_hen_id) 
        REFERENCES lich_hen(id) ON DELETE CASCADE
);
GO

-- ============================================================
-- 12. BẢNG LOG_TRANG_THAI
-- ============================================================
CREATE TABLE log_trang_thai (
    id                  INT IDENTITY(1,1) PRIMARY KEY,
    lich_hen_id         INT NOT NULL,
    trang_thai_cu       VARCHAR(30) NULL,
    trang_thai_moi      VARCHAR(30) NOT NULL,
    thoi_gian           DATETIME DEFAULT GETDATE(),
    nguoi_thuc_hien_id  INT NULL,
    CONSTRAINT fk_log_lichhen FOREIGN KEY (lich_hen_id) 
        REFERENCES lich_hen(id) ON DELETE CASCADE,
    CONSTRAINT fk_log_nguoidung FOREIGN KEY (nguoi_thuc_hien_id) 
        REFERENCES nguoi_dung(id) ON DELETE SET NULL
);
GO

-- ============================================================
-- 13. BẢNG TRIEU_CHUNG_BAC_SI
-- ============================================================
CREATE TABLE trieu_chung_bac_si (
    id              INT IDENTITY(1,1) PRIMARY KEY,
    trieu_chung_id  INT NOT NULL,
    bac_si_id       INT NOT NULL,
    CONSTRAINT fk_tcbs_trieuchung FOREIGN KEY (trieu_chung_id) 
        REFERENCES trieu_chung(id) ON DELETE CASCADE,
    CONSTRAINT fk_tcbs_bacsi FOREIGN KEY (bac_si_id) 
        REFERENCES bac_si(id) ON DELETE CASCADE,
    CONSTRAINT uq_trieu_chung_bac_si UNIQUE (trieu_chung_id, bac_si_id)
);
GO

-- ============================================================
-- 14. INDEXES
-- ============================================================
CREATE INDEX idx_bac_si_chuyen_khoa        ON bac_si(chuyen_khoa_id);
CREATE INDEX idx_bac_si_rating             ON bac_si(rating DESC);
CREATE INDEX idx_lich_lam_viec_lookup      ON lich_lam_viec(bac_si_id, ngay_kham, con_trong);
CREATE INDEX idx_lich_hen_benh_nhan        ON lich_hen(benh_nhan_id);
CREATE INDEX idx_lich_hen_bac_si           ON lich_hen(bac_si_id);
CREATE INDEX idx_lich_hen_trang_thai       ON lich_hen(trang_thai);
CREATE INDEX idx_lich_hen_ngay_tao         ON lich_hen(ngay_tao DESC);
CREATE INDEX idx_thanh_toan_lich_hen       ON thanh_toan(lich_hen_id);
CREATE INDEX idx_log_trang_thai_lich_hen   ON log_trang_thai(lich_hen_id);
CREATE INDEX idx_trieu_chung_chuyen_khoa   ON trieu_chung(chuyen_khoa_id);
CREATE INDEX idx_trieu_chung_bac_si_bac_si ON trieu_chung_bac_si(bac_si_id);
CREATE INDEX idx_admin_nguoi_dung          ON admin(nguoi_dung_id);  -- ✅ THÊM
GO

-- ============================================================
-- 15. TRIGGER: TỰ ĐỘNG GHI LOG KHI LỊCH HẸN ĐỔI TRẠNG THÁI
-- ============================================================
CREATE TRIGGER trg_log_trang_thai_lich_hen
ON lich_hen
AFTER INSERT, UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    -- Trường hợp INSERT: ghi log với trang_thai_cu = NULL
    IF NOT EXISTS (SELECT 1 FROM deleted)
    BEGIN
        INSERT INTO log_trang_thai (lich_hen_id, trang_thai_cu, trang_thai_moi, nguoi_thuc_hien_id)
        SELECT i.id, NULL, i.trang_thai, i.le_tan_id
        FROM inserted i;
    END
    -- Trường hợp UPDATE: chỉ ghi log nếu trạng thái thay đổi
    ELSE
    BEGIN
        INSERT INTO log_trang_thai (lich_hen_id, trang_thai_cu, trang_thai_moi, nguoi_thuc_hien_id)
        SELECT i.id, d.trang_thai, i.trang_thai, i.le_tan_id
        FROM inserted i
        JOIN deleted d ON i.id = d.id
        WHERE ISNULL(i.trang_thai, '') <> ISNULL(d.trang_thai, '');
    END
END;
GO

PRINT N'✅ Khởi tạo database PhongKhamDB thành công!';
PRINT N'   - 12 bảng chính (bao gồm bảng ADMIN)';
PRINT N'   - 12 indexes';
PRINT N'   - 1 trigger tự động ghi log';
GO
