USE PhongKhamDB;
GO

IF OBJECT_ID('dbo.benh_nhan', 'U') IS NOT NULL DROP TABLE dbo.benh_nhan;
GO

CREATE TABLE dbo.benh_nhan (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nguoi_dung_id INT NOT NULL UNIQUE,
    ngay_sinh DATE NULL,
    gioitinh NVARCHAR(10) NULL CHECK (gioitinh IN (N'Nam', N'Nữ', N'Khác')),
    dia_chi NVARCHAR(255) NULL,
    tien_su_benh NVARCHAR(MAX) NULL,
    CONSTRAINT FK_benh_nhan_nguoi_dung FOREIGN KEY (nguoi_dung_id) REFERENCES dbo.nguoi_dung(id) ON DELETE CASCADE
);
GO
