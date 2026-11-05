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