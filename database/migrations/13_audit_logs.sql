USE MedBooking;
GO

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'audit_logs')
CREATE TABLE audit_logs (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nguoi_thuc_hien VARCHAR(36) NOT NULL,
    hanh_dong NVARCHAR(50) NOT NULL,
    doi_tuong NVARCHAR(50) NOT NULL,
    doi_tuong_id VARCHAR(36),
    noi_dung_thay_doi NVARCHAR(MAX),
    thoi_gian DATETIME DEFAULT GETDATE(),

    CONSTRAINT fk_audit_nguoi_dung 
        FOREIGN KEY (nguoi_thuc_hien) REFERENCES nguoi_dung(id) ON DELETE NO ACTION
);
GO

CREATE INDEX idx_audit_thoi_gian ON audit_logs(thoi_gian DESC);
GO

PRINT '✅ Tạo bảng audit_logs';
