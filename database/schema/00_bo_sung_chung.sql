-- === BẢNG: nguoi_dung ===
ALTER TABLE nguoi_dung
ADD COLUMN IF NOT EXISTS xoa_luc TIMESTAMP,
ADD COLUMN IF NOT EXISTS xoa_boi INT REFERENCES nguoi_dung(id),
ADD COLUMN IF NOT EXISTS ly_do_xoa TEXT,
ADD COLUMN IF NOT EXISTS created_by INT REFERENCES nguoi_dung(id),
ADD COLUMN IF NOT EXISTS updated_by INT REFERENCES nguoi_dung(id);

-- === BẢNG: bac_si ===
ALTER TABLE bac_si
ADD COLUMN IF NOT EXISTS xoa_luc TIMESTAMP,
ADD COLUMN IF NOT EXISTS xoa_boi INT REFERENCES nguoi_dung(id),
ADD COLUMN IF NOT EXISTS ly_do_xoa TEXT,
ADD COLUMN IF NOT EXISTS created_by INT REFERENCES nguoi_dung(id),
ADD COLUMN IF NOT EXISTS updated_by INT REFERENCES nguoi_dung(id);

-- === BẢNG: benh_nhan ===
ALTER TABLE benh_nhan
ADD COLUMN IF NOT EXISTS xoa_luc TIMESTAMP,
ADD COLUMN IF NOT EXISTS xoa_boi INT REFERENCES nguoi_dung(id),
ADD COLUMN IF NOT EXISTS ly_do_xoa TEXT,
ADD COLUMN IF NOT EXISTS created_by INT REFERENCES nguoi_dung(id),
ADD COLUMN IF NOT EXISTS updated_by INT REFERENCES nguoi_dung(id);

-- === BẢNG: lich_hen ===
ALTER TABLE lich_hen
ADD COLUMN IF NOT EXISTS xoa_luc TIMESTAMP,
ADD COLUMN IF NOT EXISTS xoa_boi INT REFERENCES nguoi_dung(id),
ADD COLUMN IF NOT EXISTS ly_do_xoa TEXT,
ADD COLUMN IF NOT EXISTS created_by INT REFERENCES nguoi_dung(id),
ADD COLUMN IF NOT EXISTS updated_by INT REFERENCES nguoi_dung(id);

-- === BẢNG: chuyen_khoa ===
ALTER TABLE chuyen_khoa
ADD COLUMN IF NOT EXISTS xoa_luc TIMESTAMP,
ADD COLUMN IF NOT EXISTS xoa_boi INT REFERENCES nguoi_dung(id),
ADD COLUMN IF NOT EXISTS ly_do_xoa TEXT,
ADD COLUMN IF NOT EXISTS created_by INT REFERENCES nguoi_dung(id),
ADD COLUMN IF NOT EXISTS updated_by INT REFERENCES nguoi_dung(id);

-- === BẢNG: dich_vu ===
ALTER TABLE dich_vu
ADD COLUMN IF NOT EXISTS xoa_luc TIMESTAMP,
ADD COLUMN IF NOT EXISTS xoa_boi INT REFERENCES nguoi_dung(id),
ADD COLUMN IF NOT EXISTS ly_do_xoa TEXT,
ADD COLUMN IF NOT EXISTS created_by INT REFERENCES nguoi_dung(id),
ADD COLUMN IF NOT EXISTS updated_by INT REFERENCES nguoi_dung(id);

-- === BẢNG: phan_hoi ===
ALTER TABLE phan_hoi
ADD COLUMN IF NOT EXISTS xoa_luc TIMESTAMP,
ADD COLUMN IF NOT EXISTS xoa_boi INT REFERENCES nguoi_dung(id),
ADD COLUMN IF NOT EXISTS ly_do_xoa TEXT,
ADD COLUMN IF NOT EXISTS created_by INT REFERENCES nguoi_dung(id),
ADD COLUMN IF NOT EXISTS updated_by INT REFERENCES nguoi_dung(id);

-- === TÌM KIẾM FULLTEXT — Tùy chọn ===
-- Đối với bac_si: tìm theo tên, chuyên môn, mô tả
ALTER TABLE bac_si
ADD COLUMN IF NOT EXISTS fts_vector TSVECTOR;

CREATE INDEX idx_bacsi_fts ON bac_si USING gin(fts_vector);

-- Hàm trigger cập nhật tự động
CREATE OR REPLACE FUNCTION bac_si_fts_update() RETURNS TRIGGER AS $$
BEGIN
    NEW.fts_vector :=
        setweight(to_tsvector('simple', COALESCE(NEW.ten, '')), 'A') ||
        setweight(to_tsvector('simple', COALESCE(NEW.chuyen_mon, '')), 'B') ||
        setweight(to_tsvector('simple', COALESCE(NEW.bio, '')), 'C');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_bacsi_fts ON bac_si;
CREATE TRIGGER trg_bacsi_fts
BEFORE INSERT OR UPDATE ON bac_si
FOR EACH ROW EXECUTE FUNCTION bac_si_fts_update();

-- Tương tự cho benh_nhan
ALTER TABLE benh_nhan
ADD COLUMN IF NOT EXISTS fts_vector TSVECTOR;

CREATE INDEX idx_benhnhan_fts ON benh_nhan USING gin(fts_vector);

CREATE OR REPLACE FUNCTION benh_nhan_fts_update() RETURNS TRIGGER AS $$
BEGIN
    NEW.fts_vector :=
        setweight(to_tsvector('simple', COALESCE(NEW.ten, '')), 'A') ||
        setweight(to_tsvector('simple', COALESCE(NEW.email, '')), 'B') ||
        setweight(to_tsvector('simple', COALESCE(NEW.dien_thoai, '')), 'C');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_benhnhan_fts ON benh_nhan;
CREATE TRIGGER trg_benhnhan_fts
BEFORE INSERT OR UPDATE ON benh_nhan
FOR EACH ROW EXECUTE FUNCTION benh_nhan_fts_update();
