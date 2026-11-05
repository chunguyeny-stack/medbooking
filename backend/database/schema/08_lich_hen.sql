USE PhongKhamDB;
GO

IF OBJECT_ID('dbo.lich_hen', 'U') IS NOT NULL DROP TABLE dbo.lich_hen;
GO

CREATE TABLE dbo.lich_hen (
    id INT IDENTITY(1,1) PRIMARY KEY,
    benh_nhan_id INT NOT NULL,
    bac_si_id INT NOT NULL,
    dich_vu_id INT NOT NULL,
    ngay_kham DATE NOT NULL,
    khung_gio NVARCHAR(100) NOT NULL,
    trang_thai NVARCHAR(50) NOT NULL DEFAULT N'Chờ xác nhận', -- Chờ xác nhận, Đã xác nhận, Đang khám, Hoàn thành, Đã hủy, Đã đến
    ghi_chu NVARCHAR(255) NULL,
    created_at DATETIME DEFAULT GETDATE(),
    CONSTRAINT FK_lich_hen_benh_nhan FOREIGN KEY (benh_nhan_id) REFERENCES dbo.benh_nhan(id),
    CONSTRAINT FK_lich_hen_bac_si FOREIGN KEY (bac_si_id) REFERENCES dbo.bac_si(id),
    CONSTRAINT FK_lich_hen_dich_vu FOREIGN KEY (dich_vu_id) REFERENCES dbo.dich_vu(id)
);
GO