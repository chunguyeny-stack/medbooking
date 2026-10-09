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