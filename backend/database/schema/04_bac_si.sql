USE PhongKhamDB;
GO

IF OBJECT_ID('dbo.bac_si', 'U') IS NOT NULL DROP TABLE dbo.bac_si;
GO

CREATE TABLE dbo.bac_si (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nguoi_dung_id INT NOT NULL UNIQUE,
    chuyen_khoa_id INT NOT NULL,
    hoc_vi NVARCHAR(50) NULL,
    kinh_nghiem INT DEFAULT 0,
    gia_kham DECIMAL(18,2) NOT NULL DEFAULT 0.00,
    rating FLOAT NOT NULL DEFAULT 0.0,
    so_luong_danh_gia INT NOT NULL DEFAULT 0,
    CONSTRAINT FK_bac_si_nguoi_dung FOREIGN KEY (nguoi_dung_id) REFERENCES dbo.nguoi_dung(id) ON DELETE CASCADE
    -- Khóa ngoại chuyen_khoa_id được add sau khi tạo bảng chuyen_khoa
);
GO