USE PhongKhamDB;
GO

IF OBJECT_ID('dbo.lich_lam_viec', 'U') IS NOT NULL DROP TABLE dbo.lich_lam_viec;
GO

CREATE TABLE dbo.lich_lam_viec (
    id INT IDENTITY(1,1) PRIMARY KEY,
    bac_si_id INT NOT NULL,
    ngay_kham DATE NOT NULL,
    khung_gio NVARCHAR(100) NOT NULL, -- VD: '07:30 - 09:30', '18:30 - 20:30 (Ngoài giờ +10%)'
    con_trong BIT NOT NULL DEFAULT 1,
    CONSTRAINT FK_lich_lam_viec_bac_si FOREIGN KEY (bac_si_id) REFERENCES dbo.bac_si(id) ON DELETE CASCADE
);
GO