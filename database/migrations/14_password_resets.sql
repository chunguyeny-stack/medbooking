USE MedBooking;
GO

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'password_resets')
CREATE TABLE password_resets (
    id INT IDENTITY(1,1) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    token NVARCHAR(255) NOT NULL UNIQUE,
    da_su_dung BIT DEFAULT 0,
    het_han DATETIME NOT NULL,
    -- Xóa mềm
    xoa_luc DATETIME,
    xoa_boi VARCHAR(36),
    ly_do_xoa NVARCHAR(MAX),

    CONSTRAINT fk_resetpass_user 
        FOREIGN KEY (user_id) REFERENCES nguoi_dung(id) ON DELETE CASCADE
);
GO

CREATE UNIQUE INDEX idx_reset_token ON password_resets(token);
GO

PRINT '✅ Tạo bảng password_resets';
