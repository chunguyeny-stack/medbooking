-- ==========================================
-- File gốc: database/schema/12_trieu_chung_bac_si.sql
-- Mô tả: Bảng nối Triệu chứng ↔ Bác sĩ (quan hệ nhiều-nhiều)
-- CSDL: PhongKhamDB / MedBooking
-- ==========================================

USE PhongKhamDB;
GO

-- Xóa bảng nếu đã tồn tại
IF OBJECT_ID('dbo.trieu_chung_bac_si', 'U') IS NOT NULL 
DROP TABLE dbo.trieu_chung_bac_si;
GO

-- Tạo bảng ánh xạ
CREATE TABLE dbo.trieu_chung_bac_si (
    trieu_chung_id INT NOT NULL,
    bac_si_id INT NOT NULL,

    -- Khóa chính ghép
    PRIMARY KEY (trieu_chung_id, bac_si),

    -- Khóa ngoại
    CONSTRAINT FK_tcbs_trieu_chung 
        FOREIGN KEY (trieu_chung_id) 
        REFERENCES dbo.trieu_chung(id) 
        ON DELETE CASCADE,

    CONSTRAINT FK_tcbs_bac_si 
        FOREIGN KEY (bac_si_id) 
        REFERENCES dbo.bac_si(id) 
        ON DELETE CASCADE
);
GO

PRINT '✅ Tạo bảng trieu_chung_bac_si thành công';
