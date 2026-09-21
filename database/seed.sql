-- 0. TẮT RÀNG BUỘC KHÓA NGOẠI ĐỂ TRUNCATE / DELETE DỮ LIỆU CŨ
EXEC sp_MSforeachtable 'ALTER TABLE ? NOCHECK CONSTRAINT ALL';

-- Xóa dữ liệu các bảng
DELETE FROM trieu_chung_bac_si;
DELETE FROM lich_lam_viec;
DELETE FROM trieu_chung;
DELETE FROM dich_vu;
DELETE FROM bac_si;
DELETE FROM nguoi_dung;
DELETE FROM chuyen_khoa;

-- Bật lại ràng buộc khóa ngoại
EXEC sp_MSforeachtable 'ALTER TABLE ? CHECK CONSTRAINT ALL';

-- BẬT IDENTITY_INSERT ĐỂ CHÈN CÁC CỘT ID THỦ CÔNG
SET IDENTITY_INSERT chuyen_khoa ON;

-- 1. CHUYÊN KHOA (10 Chuyên khoa)
INSERT INTO chuyen_khoa (id, ten_chuyen_khoa, mo_ta) VALUES
(1, N'Thần kinh', N'Chẩn đoán và điều trị bệnh lý về não bộ, thần kinh, mất ngủ, đau đầu'),
(2, N'Tim mạch', N'Tầm soát và điều trị bệnh lý mạch máu, cao huyết áp, rối loạn nhịp tim'),
(3, N'Nhi khoa', N'Chăm sóc sức khỏe toàn diện và điều trị bệnh lý ở trẻ nhỏ'),
(4, N'Tai Mũi Họng', N'Điều trị viêm xoang, viêm họng, các vấn đề thính lực và thanh quản'),
(5, N'Da liễu', N'Tư vấn và điều trị bệnh lý về da, dị ứng, mụn trứng cá, chàm'),
(6, N'Xương khớp', N'Chẩn đoán thoái hóa khớp, thoát vị đĩa đệm, đau cột sống'),
(7, N'Tiêu hóa', N'Điều trị dạ dày, đại tràng, trào ngược thực quản, gan mật'),
(8, N'Mắt (Nhãn khoa)', N'Khám khúc xạ, cận thị, đau mắt đỏ, cườm mắt'),
(9, N'Sản phụ khoa', N'Tư vấn thai kỳ, khám phụ khoa, tầm soát ung thư phụ khoa'),
(10, N'Hô hấp', N'Điều trị viêm phổi, hen suyễn, viêm phế quản và bệnh phổi mãn tính');

SET IDENTITY_INSERT chuyen_khoa OFF;

-- Reset IDENTITY cho chuyen_khoa về 10
DBCC CHECKIDENT ('chuyen_khoa', RESEED, 10);


-- 2. TÀI KHOẢN ADMIN & LỄ TÂN & BÁC SĨ (nguoi_dung)
SET IDENTITY_INSERT nguoi_dung ON;

INSERT INTO nguoi_dung (id, email, mat_khau, ho_ten, so_dien_thoai, vai_tro) VALUES
(1, 'admin@medbooking.com', '$2b$12$eImiTXuWVxfM37uY4JANjOL.8129hb1283h129h38', N'Hệ Thống Admin', '0901000000', 'admin'),

-- Lễ tân
(2, 'letan.mai@medbooking.com', '$2b$12$eImiTXuWVxfM37uY4JANjOL.8129hb1283h129h38', N'Lễ tân Nguyễn Mai Phương', '0901000001', 'le_tan'),
(3, 'letan.hoa@medbooking.com', '$2b$12$eImiTXuWVxfM37uY4JANjOL.8129hb1283h129h38', N'Lễ tân Trần Thị Hoa', '0901000002', 'le_tan'),
(4, 'letan.linh@medbooking.com', '$2b$12$eImiTXuWVxfM37uY4JANjOL.8129hb1283h129h38', N'Lễ tân Bùi Khánh Linh', '0901000003', 'le_tan'),
(5, 'letan.trang@medbooking.com', '$2b$12$eImiTXuWVxfM37uY4JANjOL.8129hb1283h129h38', N'Lễ tân Lê Thu Trang', '0901000004', 'le_tan'),
(6, 'letan.vy@medbooking.com', '$2b$12$eImiTXuWVxfM37uY4JANjOL.8129hb1283h129h38', N'Lễ tân Đỗ Thảo Vy', '0901000005', 'le_tan'),
(7, 'letan.huyen@medbooking.com', '$2b$12$eImiTXuWVxfM37uY4JANjOL.8129hb1283h129h38', N'Lễ tân Phạm Ngọc Huyền', '0901000006', 'le_tan'),
(8, 'letan.an@medbooking.com', '$2b$12$eImiTXuWVxfM37uY4JANjOL.8129hb1283h129h38', N'Lễ tân Vũ Hoài An', '0901000007', 'le_tan'),

-- Bác sĩ (ID 9-58)
-- Khoa 1: Thần kinh
(9, 'bs.hung.tk@medbooking.com', 'pass_hash', N'BS. Nguyễn Văn Hùng', '0902000001', 'bac_si'),
(10, 'bs.lan.tk@medbooking.com', 'pass_hash', N'PGS.TS Trần Thị Lan', '0902000002', 'bac_si'),
(11, 'bs.minh.tk@medbooking.com', 'pass_hash', N'BS. Lê Hoài Minh', '0902000003', 'bac_si'),
(12, 'bs.tuan.tk@medbooking.com', 'pass_hash', N'BS. Phạm Anh Tuấn', '0902000004', 'bac_si'),
(13, 'bs.ha.tk@medbooking.com', 'pass_hash', N'BS. Đỗ Thu Hà', '0902000005', 'bac_si'),
-- Khoa 2: Tim mạch
(14, 'bs.duc.tm@medbooking.com', 'pass_hash', N'BS. Hoàng Minh Đức', '0902000006', 'bac_si'),
(15, 'bs.nam.tm@medbooking.com', 'pass_hash', N'BS. Vũ Hải Nam', '0902000007', 'bac_si'),
(16, 'bs.thao.tm@medbooking.com', 'pass_hash', N'BS. Nguyễn Phương Thảo', '0902000008', 'bac_si'),
(17, 'bs.huong.tm@medbooking.com', 'pass_hash', N'BS. Bùi Thanh Hương', '0902000009', 'bac_si'),
(18, 'bs.khang.tm@medbooking.com', 'pass_hash', N'BS. Ngô Bảo Khang', '0902000010', 'bac_si'),
-- Khoa 3: Nhi khoa
(19, 'bs.an.nk@medbooking.com', 'pass_hash', N'BS. Phạm Quốc An', '0902000011', 'bac_si'),
(20, 'bs.binh.nk@medbooking.com', 'pass_hash', N'BS. Lý Thanh Bình', '0902000012', 'bac_si'),
(21, 'bs.cuong.nk@medbooking.com', 'pass_hash', N'BS. Trịnh Văn Cường', '0902000013', 'bac_si'),
(22, 'bs.dung.nk@medbooking.com', 'pass_hash', N'BS. Hoàng Mỹ Dũng', '0902000014', 'bac_si'),
(23, 'bs.giang.nk@medbooking.com', 'pass_hash', N'BS. Lê Hương Giang', '0902000015', 'bac_si'),
-- Khoa 4: Tai Mũi Họng
(24, 'bs.hai.tmh@medbooking.com', 'pass_hash', N'BS. Nguyễn Quang Hải', '0902000016', 'bac_si'),
(25, 'bs.khanh.tmh@medbooking.com', 'pass_hash', N'BS. Đỗ Vân Khánh', '0902000017', 'bac_si'),
(26, 'bs.long.tmh@medbooking.com', 'pass_hash', N'BS. Vũ Phi Long', '0902000018', 'bac_si'),
(27, 'bs.my.tmh@medbooking.com', 'pass_hash', N'BS. Bùi Huyền Mỹ', '0902000019', 'bac_si'),
(28, 'bs.nghia.tmh@medbooking.com', 'pass_hash', N'BS. Trần Tấn Nghĩa', '0902000020', 'bac_si'),
-- Khoa 5: Da liễu
(29, 'bs.oanh.dl@medbooking.com', 'pass_hash', N'BS. Hoàng Kiều Oanh', '0902000021', 'bac_si'),
(30, 'bs.phong.dl@medbooking.com', 'pass_hash', N'BS. Lê Thanh Phong', '0902000022', 'bac_si'),
(31, 'bs.quyen.dl@medbooking.com', 'pass_hash', N'BS. Đặng Ngọc Quyên', '0902000023', 'bac_si'),
(32, 'bs.son.dl@medbooking.com', 'pass_hash', N'BS. Nguyễn Thái Sơn', '0902000024', 'bac_si'),
(33, 'bs.tam.dl@medbooking.com', 'pass_hash', N'BS. Trịnh Minh Tâm', '0902000025', 'bac_si'),
-- Khoa 6: Xương khớp
(34, 'bs.uy.xk@medbooking.com', 'pass_hash', N'BS. Phan Quốc Uy', '0902000026', 'bac_si'),
(35, 'bs.vinh.xk@medbooking.com', 'pass_hash', N'BS. Vũ Thế Vinh', '0902000027', 'bac_si'),
(36, 'bs.xuan.xk@medbooking.com', 'pass_hash', N'BS. Nguyễn Thanh Xuân', '0902000028', 'bac_si'),
(37, 'bs.yen.xk@medbooking.com', 'pass_hash', N'BS. Bùi Bảo Yến', '0902000029', 'bac_si'),
(38, 'bs.anh.xk@medbooking.com', 'pass_hash', N'BS. Trần Tuấn Anh', '0902000030', 'bac_si'),
-- Khoa 7: Tiêu hóa
(39, 'bs.bao.th@medbooking.com', 'pass_hash', N'BS. Hoàng Gia Bảo', '0902000031', 'bac_si'),
(40, 'bs.chau.th@medbooking.com', 'pass_hash', N'BS. Đỗ Minh Châu', '0902000032', 'bac_si'),
(41, 'bs.dat.th@medbooking.com', 'pass_hash', N'BS. Lê Tiến Đạt', '0902000033', 'bac_si'),
(42, 'bs.giang.th@medbooking.com', 'pass_hash', N'BS. Phạm Đức Giang', '0902000034', 'bac_si'),
(43, 'bs.hang.th@medbooking.com', 'pass_hash', N'BS. Nguyễn Thúy Hằng', '0902000035', 'bac_si'),
-- Khoa 8: Mắt
(44, 'bs.khoi.mat@medbooking.com', 'pass_hash', N'BS. Vũ Đăng Khôi', '0902000036', 'bac_si'),
(45, 'bs.linh.mat@medbooking.com', 'pass_hash', N'BS. Trịnh Khánh Linh', '0902000037', 'bac_si'),
(46, 'bs.manh.mat@medbooking.com', 'pass_hash', N'BS. Phan Đức Mạnh', '0902000038', 'bac_si'),
(47, 'bs.ngan.mat@medbooking.com', 'pass_hash', N'BS. Lê Thu Ngân', '0902000039', 'bac_si'),
(48, 'bs.phuc.mat@medbooking.com', 'pass_hash', N'BS. Hoàng Hồng Phúc', '0902000040', 'bac_si'),
-- Khoa 9: Sản phụ khoa
(49, 'bs.quynh.spk@medbooking.com', 'pass_hash', N'BS. Nguyễn Như Quỳnh', '0902000041', 'bac_si'),
(50, 'bs.sang.spk@medbooking.com', 'pass_hash', N'BS. Đỗ Tấn Sáng', '0902000042', 'bac_si'),
(51, 'bs.trang.spk@medbooking.com', 'pass_hash', N'BS. Bùi Đoan Trang', '0902000043', 'bac_si'),
(52, 'bs.tu.spk@medbooking.com', 'pass_hash', N'BS. Vũ Anh Tú', '0902000044', 'bac_si'),
(53, 'bs.van.spk@medbooking.com', 'pass_hash', N'BS. Phạm Cẩm Vân', '0902000045', 'bac_si'),
-- Khoa 10: Hô hấp
(54, 'bs.viet.hh@medbooking.com', 'pass_hash', N'BS. Hoàng Quốc Việt', '0902000046', 'bac_si'),
(55, 'bs.vinh.hh@medbooking.com', 'pass_hash', N'BS. Nguyễn Quang Vinh', '0902000047', 'bac_si'),
(56, 'bs.y.hh@medbooking.com', 'pass_hash', N'BS. Trịnh Như Ý', '0902000048', 'bac_si'),
(57, 'bs.khai.hh@medbooking.com', 'pass_hash', N'BS. Lê Quang Khải', '0902000049', 'bac_si'),
(58, 'bs.lam.hh@medbooking.com', 'pass_hash', N'BS. Đỗ Tung Lâm', '0902000050', 'bac_si');

SET IDENTITY_INSERT nguoi_dung OFF;
DBCC CHECKIDENT ('nguoi_dung', RESEED, 58);


-- 5. BẢNG BAC_SI
SET IDENTITY_INSERT bac_si ON;

INSERT INTO bac_si (id, nguoi_dung_id, chuyen_khoa_id, mo_ta, rating) VALUES
-- Khoa 1
(1, 9, 1, N'Chuyên gia Thần kinh hơn 15 năm kinh nghiệm', 4.9),
(2, 10, 1, N'PGS.TS Thần kinh học lâm sàng', 4.8),
(3, 11, 1, N'Bác sĩ chuyên khoa chẩn đoán đau đầu mãn tính', 4.7),
(4, 12, 1, N'Bác sĩ điều trị rối loạn giấc ngủ', 4.6),
(5, 13, 1, N'Bác sĩ Thần kinh ngoại biên', 4.8),
-- Khoa 2
(6, 14, 2, N'Chuyên gia Tim mạch can thiệp', 4.9),
(7, 15, 2, N'Bác sĩ điều trị cao huyết áp và xơ vữa', 4.7),
(8, 16, 2, N'Bác sĩ chuyên tầm soát rối loạn nhịp tim', 4.8),
(9, 17, 2, N'Bác sĩ Tim mạch lâm sàng', 4.6),
(10, 18, 2, N'Bác sĩ Tim mạch lão khoa', 4.9),
-- Khoa 3
(11, 19, 3, N'Bác sĩ Nhi khoa tổng quát', 4.8),
(12, 20, 3, N'Chuyên gia Dinh dưỡng & Nhi khoa', 4.9),
(13, 21, 3, N'Bác sĩ Nhi khoa giàu kinh nghiệm', 4.7),
(14, 22, 3, N'Bác sĩ tư vấn sức khỏe trẻ sơ sinh', 4.8),
(15, 23, 3, N'Bác sĩ Nhi hô hấp', 4.6),
-- Khoa 4
(16, 24, 4, N'Bác sĩ Tai Mũi Họng tu nghiệp tại Pháp', 4.9),
(17, 25, 4, N'Bác sĩ phẫu thuật vi phẫu Tai Mũi Họng', 4.8),
(18, 26, 4, N'Chuyên gia điều trị viêm xoang', 4.7),
(19, 27, 4, N'Bác sĩ Tai Mũi Họng Nhi', 4.6),
(20, 28, 4, N'Bác sĩ nội soi Tai Mũi Họng', 4.8),
-- Khoa 5
(21, 29, 5, N'Chuyên gia Da liễu thẩm mỹ & lâm sàng', 4.9),
(22, 30, 5, N'Bác sĩ điều trị mụn trứng cá chuyên sâu', 4.8),
(23, 31, 5, N'Bác sĩ điều trị chàm & vi dị ứng da', 4.7),
(24, 32, 5, N'Bác sĩ Da liễu tổng quát', 4.6),
(25, 33, 5, N'Bác sĩ Da liễu trẻ em', 4.8),
-- Khoa 6
(26, 34, 6, N'Bác sĩ Cơ Xương Khớp & Phục hồi chức năng', 4.9),
(27, 35, 6, N'Chuyên gia chẩn đoán thoát vị đĩa đệm', 4.8),
(28, 36, 6, N'Bác sĩ điều trị thoái hóa khớp', 4.7),
(29, 37, 6, N'Bác sĩ Cột sống & Đau khớp', 4.6),
(30, 38, 6, N'Bác sĩ Xương khớp thể thao', 4.9),
-- Khoa 7
(31, 39, 7, N'Chuyên gia Nội soi Tiêu hóa', 4.9),
(32, 40, 7, N'Bác sĩ điều trị dạ dày & trào ngược', 4.8),
(33, 41, 7, N'Bác sĩ chuyên khoa Gan Mật', 4.7),
(34, 42, 7, N'Bác sĩ Đại trực tràng', 4.6),
(35, 43, 7, N'Bác sĩ Tiêu hóa tổng quát', 4.8),
-- Khoa 8
(36, 44, 8, N'Bác sĩ Nhãn khoa phẫu thuật khúc xạ', 4.9),
(37, 45, 8, N'Bác sĩ Mắt trẻ em & Khúc xạ', 4.8),
(38, 46, 8, N'Bác sĩ chẩn đoán Cườm mắt & Glôcôm', 4.7),
(39, 47, 8, N'Bác sĩ điều trị Viêm kết mạc', 4.6),
(40, 48, 8, N'Bác sĩ Nhãn khoa tổng quát', 4.8),
-- Khoa 9
(41, 49, 9, N'Chuyên gia Sản phụ khoa & Theo dõi thai kỳ', 4.9),
(42, 50, 9, N'Bác sĩ tầm soát ung thư phụ khoa', 4.8),
(43, 51, 9, N'Bác sĩ Phụ khoa lâm sàng', 4.7),
(44, 52, 9, N'Bác sĩ Hỗ trợ sinh sản', 4.9),
(45, 53, 9, N'Bác sĩ Tư vấn sức khỏe sinh sản', 4.6),
-- Khoa 10
(46, 54, 10, N'Chuyên gia Hô hấp & Bệnh phổi mãn tính', 4.9),
(47, 55, 10, N'Bác sĩ điều trị Hen suyễn', 4.8),
(48, 56, 10, N'Bác sĩ Hô hấp lâm sàng', 4.7),
(49, 57, 10, N'Bác sĩ chẩn đoán Viêm phế quản', 4.6),
(50, 58, 10, N'Bác sĩ Hô hấp tổng quát', 4.8);

SET IDENTITY_INSERT bac_si OFF;
DBCC CHECKIDENT ('bac_si', RESEED, 50);


-- 6. DỊCH VỤ KHÁM
SET IDENTITY_INSERT dich_vu ON;

INSERT INTO dich_vu (id, chuyen_khoa_id, ten_dich_vu, gia_tien, mo_ta) VALUES
(1, 1, N'Khám Thần kinh chuyên sâu', 350000.00, N'Tư vấn chứng đau đầu, chóng mặt, mất ngủ'),
(2, 2, N'Khám Tim mạch & Đo ECG', 500000.00, N'Đo điện tâm đồ và tầm soát cao huyết áp'),
(3, 3, N'Khám Nhi tổng quát', 250000.00, N'Khám sức khỏe trẻ em và tư vấn dinh dưỡng'),
(4, 4, N'Nội soi Tai Mũi Họng', 300000.00, N'Nội soi tầm soát viêm xoang, viêm họng'),
(5, 5, N'Khám & Tư vấn Da liễu', 200000.00, N'Điều trị mụn, nấm da, dị ứng'),
(6, 6, N'Khám Xương khớp & Cột sống', 400000.00, N'Chẩn đoán thoát vị đĩa đệm, đau lưng'),
(7, 7, N'Nội soi Dạ dày - Tiêu hóa', 600000.00, N'Nội soi tầm soát viêm loét dạ dày, trào ngược'),
(8, 8, N'Đo khúc xạ & Khám Mắt', 200000.00, N'Khám mắt tổng quát, đo độ cận viễn loạn'),
(9, 9, N'Khám Phụ khoa & Siêu âm', 450000.00, N'Siêu âm thai, tầm soát phụ khoa'),
(10, 10, N'Khám Hô hấp & Đo thông khí', 350000.00, N'Khám hen suyễn, viêm phế quản');

SET IDENTITY_INSERT dich_vu OFF;
DBCC CHECKIDENT ('dich_vu', RESEED, 10);


-- 7. DANH MỤC TRIỆU CHỨNG
SET IDENTITY_INSERT trieu_chung ON;

INSERT INTO trieu_chung (id, ten_trieu_chung, chuyen_khoa_id) VALUES
-- Khoa 1: Thần kinh
(1, N'Đau đầu nửa đầu', 1), (2, N'Mất ngủ kéo dài', 1), (3, N'Chóng mặt hoa mắt', 1), (4, N'Tê bì tay chân', 1), (5, N'Suy giảm trí nhớ', 1),
-- Khoa 2: Tim mạch
(6, N'Đau tức ngực', 2), (7, N'Hồi hộp đánh trống ngực', 2), (8, N'Tăng huyết áp', 2), (9, N'Khó thở khi vận động', 2), (10, N'Sưng phù chân tay', 2),
-- Khoa 3: Nhi khoa
(11, N'Sốt cao ở trẻ em', 3), (12, N'Ho khò khè ở trẻ', 3), (13, N'Biếng ăn chậm lớn', 3), (14, N'Nôn trớ ở trẻ nhỏ', 3), (15, N'Quấy khóc đêm ở trẻ', 3),
-- Khoa 4: Tai Mũi Họng
(16, N'Đau họng khó nuốt', 4), (17, N'Ù tai đau tai', 4), (18, N'Nghẹt mũi chảy nước mũi', 4), (19, N'Khàn tiếng mất tiếng', 4), (20, N'Hắt hơi liên tục', 4),
-- Khoa 5: Da liễu
(21, N'Nổi mẩn đỏ ngứa da', 5), (22, N'Mụn trứng cá nặng', 5), (23, N'Rụng tóc bất thường', 5), (24, N'Vảy nến bong tróc da', 5), (25, N'Dị ứng mề đay', 5),
-- Khoa 6: Xương khớp
(26, N'Đau lưng mỏi cổ', 6), (27, N'Đau khớp gối khi đi lại', 6), (28, N'Cứng khớp buổi sáng', 6), (29, N'Tê sưng các khớp', 6), (30, N'Đau nhức cột sống', 6),
-- Khoa 7: Tiêu hóa
(31, N'Đau thượng vị dạ dày', 7), (32, N'Trào ngược ợ chua', 7), (33, N'Đầy hơi khó tiêu', 7), (34, N'Rối loạn tiêu hóa', 7), (35, N'Táo bón hoặc tiêu chảy', 7),
-- Khoa 8: Mắt (Nhãn khoa)
(36, N'Nhìn mờ mỏi mắt', 8), (37, N'Đau mắt đỏ chảy nước mắt', 8), (38, N'Khô mắt rát mắt', 8), (39, N'Sợ ánh sáng', 8), (40, N'Nhìn thấy đốm đen', 8),
-- Khoa 9: Sản phụ khoa
(41, N'Chậm kinh đau bụng dưới', 9), (42, N'Khám thai định kỳ', 9), (43, N'Rối loạn kinh nguyệt', 9), (44, N'Khí hư bất thường', 9), (45, N'Ngứa rát vùng kín', 9),
-- Khoa 10: Hô hấp
(46, N'Ho kéo dài có đờm', 10), (47, N'Tức ngực thở khò khè', 10), (48, N'Sốt ho tức ngực', 10), (49, N'Khó thở về đêm', 10), (50, N'Thở gấp hụt hơi', 10);

SET IDENTITY_INSERT trieu_chung OFF;
DBCC CHECKIDENT ('trieu_chung', RESEED, 50);


-- 8. MAP TRIỆU CHỨNG - BÁC SĨ
INSERT INTO trieu_chung_bac_si (trieu_chung_id, bac_si_id)
SELECT tc.id, bs.id
FROM trieu_chung tc
JOIN bac_si bs ON tc.chuyen_khoa_id = bs.chuyen_khoa_id;


-- 9. LỊCH LÀM VIỆC MẪU (Tạo lịch ngày mai cho các Bác sĩ)
INSERT INTO lich_lam_viec (bac_si_id, ngay_kham, khung_gio, trang_thai_trong)
SELECT id, DATEADD(day, 1, CAST(GETDATE() AS DATE)), '08:00 - 09:00', 1 FROM bac_si
UNION ALL
SELECT id, DATEADD(day, 1, CAST(GETDATE() AS DATE)), '09:00 - 10:00', 1 FROM bac_si
UNION ALL
SELECT id, DATEADD(day, 1, CAST(GETDATE() AS DATE)), '14:00 - 15:00', 1 FROM bac_si;