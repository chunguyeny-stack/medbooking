USE PhongKhamDB;
GO

IF OBJECT_ID('dbo.nguoi_dung', 'U') IS NOT NULL DROP TABLE dbo.nguoi_dung;
GO

CREATE TABLE dbo.nguoi_dung (
    id INT IDENTITY(1,1) PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    mat_khau VARCHAR(255) NOT NULL,
    ho_ten NVARCHAR(100) NOT NULL,
    so_dien_thoai VARCHAR(20) NULL,
    vai_tro NVARCHAR(20) NOT NULL CHECK (vai_tro IN ('admin', 'le_tan', 'bac_si', 'benh_nhan')),
    trang_thai BIT NOT NULL DEFAULT 1, -- 1: Active, 0: Blocked
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE()
);
GO