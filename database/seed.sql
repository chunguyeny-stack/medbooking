-- Cập nhật tự động mã lễ tân theo khung giờ cho bảng lịch hẹn

UPDATE lh
SET lh.le_tan_ma_le_tan = lt.ma_le_tan
FROM [PhongKhamDB].[dbo].[lich_hen] lh
CROSS APPLY (
    SELECT TOP 1 ma_le_tan FROM [PhongKhamDB].[dbo].[le_tan] 
    WHERE 
        -- Nếu giờ bắt đầu < 12 thì gán lễ tân ca sáng
        (CAST(SUBSTRING(lh.khung_gio, 1, 2) AS INT) < 12 AND ca_truc LIKE N'%sáng%')
        -- Nếu giờ từ 12 đến 17 thì gán lễ tân ca chiều
        OR (CAST(SUBSTRING(lh.khung_gio, 1, 2) AS INT) >= 12 AND CAST(SUBSTRING(lh.khung_gio, 1, 2) AS INT) <= 17 AND ca_truc LIKE N'%chiều%')
        -- Các giờ còn lại gán ca tối
        OR (CAST(SUBSTRING(lh.khung_gio, 1, 2) AS INT) > 17 AND ca_truc LIKE N'%tối%')
) lt;

 -- 1. Chuyển đổi kiểu dữ liệu các cột sang NVARCHAR để lưu tiếng Việt có dấu hoàn hảo
ALTER TABLE [PhongKhamDB].[dbo].[le_tan] ALTER COLUMN [quay_lam_viec] NVARCHAR(100);
ALTER TABLE [PhongKhamDB].[dbo].[le_tan] ALTER COLUMN [ca_truc] NVARCHAR(50);

ALTER TABLE [PhongKhamDB].[dbo].[nguoi_dung] ALTER COLUMN [ho_ten] NVARCHAR(255);

-- 2. Xóa và nạp lại dữ liệu chuẩn có tiền tố N phía trước
DELETE FROM [PhongKhamDB].[dbo].[le_tan];

INSERT INTO [PhongKhamDB].[dbo].[le_tan] ([ma_le_tan], [quay_lam_viec], [ca_truc], [ngay_vao_lam]) VALUES
(101, N'Quầy số 1', N'Ca sáng', '2026-01-10'),
(102, N'Quầy số 2', N'Ca chiều', '2026-01-15'),
(103, N'Quầy số 3', N'Ca sáng', '2026-02-01'),
(104, N'Quầy số 4', N'Ca chiều', '2026-02-10'),
(105, N'Quầy số 5', N'Ca tối', '2026-03-01');

-- 2. Ghép nối chính xác từng triệu chứng với các bác sĩ thuộc đúng chuyên khoa tương ứng
INSERT INTO trieu_chung_bac_si (trieu_chung_id, bac_si_id)
SELECT tc.id, bs.id
FROM trieu_chung tc
JOIN bac_si bs ON tc.chuyen_khoa_id = bs.chuyen_khoa_id;
GO

-- 3. Kiểm tra lại kết quả dữ liệu đã được nạp thành công
SELECT TOP 150 * FROM trieu_chung_bac_si;
GO


