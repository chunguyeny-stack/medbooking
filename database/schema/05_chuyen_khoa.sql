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

-- Add Foreign Key cho bac_si
IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE name = 'FK_bac_si_chuyen_khoa')
BEGIN
    ALTER TABLE dbo.bac_si 
    ADD CONSTRAINT FK_bac_si_chuyen_khoa 
    FOREIGN KEY (chuyen_khoa_id) REFERENCES dbo.chuyen_khoa(id);
END
GO