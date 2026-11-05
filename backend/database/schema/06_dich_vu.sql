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