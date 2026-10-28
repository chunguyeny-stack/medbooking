-- Bảng lịch hẹn đặt khám
CREATE TABLE IF NOT EXISTS lich_hen (
    id SERIAL PRIMARY KEY,
    nguoi_dung_id INT REFERENCES nguoi_dung(id) ON DELETE CASCADE NOT NULL,
    bac_si_id INT REFERENCES bac_si(id) ON DELETE CASCADE NOT NULL,
    ngay_hen DATE NOT NULL,
    gio_hen TIME NOT NULL,
    trieu_chung TEXT,
    ghi_chu TEXT,
    trang_thai VARCHAR(30) DEFAULT "cho_xac_nhan",
    -- Trạng thái: cho_xac_nhan | da_xac_nhan | da_huy | da_hoan_thanh | da_qua_han
    ly_do_huy TEXT,
    hien_thi BOOLEAN DEFAULT TRUE, -- Ẩn khi cần
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Chỉ mục tối ưu truy vấn
CREATE INDEX IF NOT EXISTS idx_lichhen_nguoidung ON lich_hen(nguoi_dung_id);
CREATE INDEX IF NOT EXISTS idx_lichhen_bacsi ON lich_hen(bac_si_id);
CREATE INDEX IF NOT EXISTS idx_lichhen_ngay ON lich_hen(ngay_hen DESC);
CREATE INDEX IF NOT EXISTS idx_lichhen_trangthai ON lich_hen(trang_thai);
