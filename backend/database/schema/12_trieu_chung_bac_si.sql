USE PhongKhamDB;
GO

IF OBJECT_ID('dbo.trieu_chung_bac_si', 'U') IS NOT NULL DROP TABLE dbo.trieu_chung_bac_si;
GO

CREATE TABLE dbo.trieu_chung_bac_si (
    trieu_chung_id INT NOT NULL,
    bac_si_id INT NOT NULL,
    PRIMARY KEY (trieu_chung_id, bac_si_id),
    CONSTRAINT FK_tcbs_trieu_chung FOREIGN KEY (trieu_chung_id) REFERENCES dbo.trieu_chung(id) ON DELETE CASCADE,
    CONSTRAINT FK_tcbs_bac_si FOREIGN KEY (bac_si_id) REFERENCES dbo.bac_si(id) ON DELETE CASCADE
);
GO