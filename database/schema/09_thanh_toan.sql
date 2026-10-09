USE PhongKhamDB;
GO

IF OBJECT_ID('dbo.thanh_toan', 'U') IS NOT NULL DROP TABLE dbo.thanh_toan;
GO

CREATE TABLE dbo.thanh_toan (
    id INT IDENTITY(1,1) PRIMARY KEY,
    lich_hen_id INT NOT NULL UNIQUE,
    tong_tien DECIMAL(18,2) NOT NULL DEFAULT 0.00,
    phuong_thuc NVARCHAR(50) NULL, -- Tiền mặt, Chuyển khoản, VNPAY
    trang_thai_thanh_toan NVARCHAR(50) NOT NULL DEFAULT N'Chưa thanh toán', -- Chưa thanh toán, Đã thanh toán
    ngay_thanh_toan DATETIME NULL,
    CONSTRAINT FK_thanh_toan_lich_hen FOREIGN KEY (lich_hen_id) REFERENCES dbo.lich_hen(id) ON DELETE CASCADE
);
GO