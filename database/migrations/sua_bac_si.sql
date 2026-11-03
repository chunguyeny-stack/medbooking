USE MedBooking;
GO

-- 5. Xóa mềm
IF NOT EXISTS (SELECT * FROM sys.columns WHERE name = 'xoa_luc' AND object_id = OBJECT_ID('bac_si'))
ALTER TABLE bac_si ADD
    xoa_luc DATETIME,
    xoa_boi VARCHAR(36),
    ly_do_xoa NVARCHAR(MAX),
    created_by VARCHAR(36),
    updated_by VARCHAR(36);
GO

-- 7. Đánh dấu hiển thị ưu tiên
IF NOT EXISTS (SELECT * FROM sys.columns WHERE name = 'is_hot' AND object_id = OBJECT_ID('bac_si'))
ALTER TABLE bac_si ADD
    is_hot BIT DEFAULT 0,
    is_new BIT DEFAULT 0,
    display_order INT DEFAULT 0;
GO

-- 8. Thông tin chi tiết bác sĩ
IF NOT EXISTS (SELECT * FROM sys.columns WHERE name = 'avatar_url' AND object_id = OBJECT_ID('bac_si'))
ALTER TABLE bac_si ADD
    avatar_url NVARCHAR(500),
    bio NVARCHAR(MAX),
    training NVARCHAR(255),
    strengths NVARCHAR(255);
GO

PRINT '✅ Cập nhật bảng bac_si';
