USE MedBooking;
GO

-- Tìm triệu chứng
IF NOT EXISTS (SELECT * FROM sys.fulltext_catalogs WHERE name = 'ft_search')
CREATE FULLTEXT CATALOG ft_search AS DEFAULT;
GO

CREATE FULLTEXT INDEX ON trieu_chung(ten_trieu_chung)
KEY INDEX PK_trieu_chung;
GO

-- Tìm bác sĩ
CREATE FULLTEXT INDEX ON bac_si(ho_ten, chuyen_mon, bio)
KEY INDEX PK_bac_si;
GO

PRINT '✅ Tạo Full-Text Index';
