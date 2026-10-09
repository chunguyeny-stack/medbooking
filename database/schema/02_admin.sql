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