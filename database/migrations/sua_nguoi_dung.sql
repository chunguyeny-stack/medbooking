USE MedBooking;
GO

-- 3. Trạng thái & khóa tài khoản
IF NOT EXISTS (SELECT * FROM sys.columns WHERE name = 'trang_thai' AND object_id = OBJECT_ID('nguoi_dung'))
ALTER TABLE nguoi_dung ADD
    trang_thai NVARCHAR(20) DEFAULT N'hoat_dong',
    ly_do_khoa NVARCHAR(MAX);
GO

-- 4. Đổi mật khẩu & token
IF NOT EXISTS (SELECT * FROM sys.columns WHERE name = 'bat_buoc_doi_mk' AND object_id = OBJECT_ID('nguoi_dung'))
ALTER TABLE nguoi_dung ADD
    bat_buoc_doi_mk BIT DEFAULT 0,
    reset_token NVARCHAR(255);
GO

-- 5. Xóa mềm + 6. Theo dõi người tạo/sửa
IF NOT EXISTS (SELECT * FROM sys.columns WHERE name = 'xoa_luc' AND object_id = OBJECT_ID('nguoi_dung'))
ALTER TABLE nguoi_dung ADD
    xoa_luc DATETIME,
    xoa_boi VARCHAR(36),
    ly_do_xoa NVARCHAR(MAX),
    created_by VARCHAR(36),
    updated_by VARCHAR(36),
    updated_at DATETIME DEFAULT GETDATE();
GO

PRINT '✅ Cập nhật bảng nguoi_dung';
