USE MedBooking;
GO

-- 5. Xóa mềm
IF NOT EXISTS (SELECT * FROM sys.columns WHERE name = 'xoa_luc' AND object_id = OBJECT_ID('benh_nhan'))
ALTER TABLE benh_nhan ADD
    xoa_luc DATETIME,
    xoa_boi VARCHAR(36),
    ly_do_xoa NVARCHAR(MAX),
    created_by VARCHAR(36),
    updated_by VARCHAR(36);
GO

-- 9. Căn cước công dân
IF NOT EXISTS (SELECT * FROM sys.columns WHERE name = 'cccd' AND object_id = OBJECT_ID('benh_nhan'))
ALTER TABLE benh_nhan ADD cccd NVARCHAR(20) UNIQUE;
GO

PRINT '✅ Cập nhật bảng benh_nhan';
