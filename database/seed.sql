-- ============================================================
-- SEED.SQL - Khởi tạo dữ liệu mẫu MedBooking
-- Dự án: Hệ thống Đặt lịch khám trực tuyến MedBooking
-- Mật khẩu dạng đơn giản: Ten + NgaySinh
-- ============================================================

USE PhongKhamDB;
GO

SET DATEFORMAT ymd;
GO

-- ============================================================
-- 1. CHUYÊN KHOA [05_chuyen_khoa.sql] - 10 Chuyên khoa
-- ============================================================
SET IDENTITY_INSERT chuyen_khoa ON;
INSERT INTO chuyen_khoa (id, ten_chuyen_khoa, mo_ta) VALUES
(1,  N'Thần kinh',        N'Chẩn đoán và điều trị bệnh lý về nền thần kinh, mất ngủ, đau đầu'),
(2,  N'Tim mạch',         N'Tầm soát và điều trị bệnh lý mạch máu, cao huyết áp, rối loạn nhịp tim'),
(3,  N'Nhi khoa',         N'Chăm sóc sức khỏe toàn diện và điều trị bệnh lý ở trẻ nhỏ'),
(4,  N'Tai Mũi Họng',      N'Điều trị viêm xoang, viêm họng, các vấn đề thính lực và thanh quản'),
(5,  N'Da liễu',          N'Tư vấn và điều trị bệnh lý về da, dị ứng, mụn trứng cá, chàm'),
(6,  N'Xương khớp',        N'Chẩn đoán thoái hóa khớp, thoát vị đĩa đệm, đau cột sống'),
(7,  N'Tiêu hóa',          N'Điều trị dạ dày, đại tràng, trào ngược thực quản, gan mật'),
(8,  N'Mắt (Nhãn khoa)',  N'Khám khúc xạ, cận thị, đau mắt đỏ, cườm mắt'),
(9,  N'Sản phụ khoa',      N'Tư vấn thai kỳ, khám phụ khoa, tầm soát ung thư phụ khoa'),
(10, N'Hô hấp',            N'Điều trị viêm phổi, hen suyễn, viêm phế quản và bệnh phổi mãn tính');
SET IDENTITY_INSERT chuyen_khoa OFF;
DBCC CHECKIDENT ('chuyen_khoa', RESEED, 10);
GO

-- ============================================================
-- 2. NGƯỜI DÙNG [01_nguoi_dung.sql] - Tối giản: 2 Admin, 20 Bác sĩ (Bệnh nhân & Lễ tân để trống cho API tự thêm)
-- ============================================================
SET IDENTITY_INSERT nguoi_dung ON;

-- Admin (ID 1 - 2)
INSERT INTO nguoi_dung (id, email, mat_khau, ho_ten, so_dien_thoai, vai_tro) VALUES
(1, 'admin@medbooking.com',    'Admin01011990',   N'Hệ Thống Admin',      '0901000000', 'admin'),
(2, 'it.admin@medbooking.com', 'ITAdmin01011990', N'Kỹ Thuật Viên Admin', '0901000099', 'admin');

-- Bác sĩ đại diện (2 BS / Chuyên khoa -> ID từ 3 đến 22)
INSERT INTO nguoi_dung (id, email, mat_khau, ho_ten, so_dien_thoai, vai_tro) VALUES
-- Khoa 1: Thần kinh
(3,  'bs.hung.tk@medbooking.com',  'Hung15051980',  N'BS. Nguyễn Văn Hùng',   '0902000001', 'bac_si'),
(4,  'bs.lan.tk@medbooking.com',   'Lan10101975',   N'PGS.TS Trần Thị Lan',   '0902000002', 'bac_si'),
-- Khoa 2: Tim mạch
(5,  'bs.duc.tm@medbooking.com',   'Duc15011980',   N'BS. Hoàng Minh Đức',    '0902000003', 'bac_si'),
(6,  'bs.nam.tm@medbooking.com',   'Nam20021985',   N'BS. Vũ Hải Nam',        '0902000004', 'bac_si'),
-- Khoa 3: Nhi khoa
(7,  'bs.an.nk@medbooking.com',    'An10011983',    N'BS. Phạm Quốc An',      '0902000005', 'bac_si'),
(8,  'bs.binh.nk@medbooking.com',  'Binh15021980',  N'BS. Lý Thanh Bình',     '0902000006', 'bac_si'),
-- Khoa 4: Tai Mũi Họng
(9,  'bs.hai.tmh@medbooking.com',  'Hai12011979',   N'BS. Nguyễn Quang Hải',  '0902000007', 'bac_si'),
(10, 'bs.khanh.tmh@medbooking.com','Khanh05021985', N'BS. Đỗ Vân Khánh',      '0902000008', 'bac_si'),
-- Khoa 5: Da liễu
(11, 'bs.oanh.dl@medbooking.com',  'Oanh05011982',  N'BS. Hoàng Kiều Oanh',   '0902000009', 'bac_si'),
(12, 'bs.phong.dl@medbooking.com', 'Phong12021984', N'BS. Lê Thanh Phong',    '0902000010', 'bac_si'),
-- Khoa 6: Xương khớp
(13, 'bs.uy.xk@medbooking.com',    'Uy10011980',    N'BS. Phan Quốc Uy',      '0902000011', 'bac_si'),
(14, 'bs.vinh.xk@medbooking.com',  'Vinh15021983',  N'BS. Vũ Thế Vinh',       '0902000012', 'bac_si'),
-- Khoa 7: Tiêu hóa
(15, 'bs.bao.th@medbooking.com',  'Bao01011978',   N'BS. Hoàng Gia Bảo',     '0902000013', 'bac_si'),
(16, 'bs.chau.th@medbooking.com', 'Chau08021984',  N'BS. Đỗ Minh Châu',      '0902000014', 'bac_si'),
-- Khoa 8: Mắt
(17, 'bs.khoi.mat@medbooking.com','Khoi02011981',  N'BS. Vũ Đăng Khôi',      '0902000015', 'bac_si'),
(18, 'bs.linh.mat@medbooking.com','Linh09021985',  N'BS. Trịnh Khánh Linh',  '0902000016', 'bac_si'),
-- Khoa 9: Sản phụ khoa
(19, 'bs.quynh.spk@medbooking.com','Quynh01011979',N'BS. Nguyễn Như Quỳnh', '0902000017', 'bac_si'),
(20, 'bs.sang.spk@medbooking.com', 'Sang08021984', N'BS. Đỗ Tấn Sáng',       '0902000018', 'bac_si'),
-- Khoa 10: Hô hấp
(21, 'bs.viet.hh@medbooking.com',  'Viet05011980', N'BS. Hoàng Quốc Việt',   '0902000019', 'bac_si'),
(22, 'bs.vinh.hh@medbooking.com',  'Vinh11021984', N'BS. Nguyễn Quang Vinh', '0902000020', 'bac_si');

SET IDENTITY_INSERT nguoi_dung OFF;
DBCC CHECKIDENT ('nguoi_dung', RESEED, 22);
GO

-- ============================================================
-- 3. ADMIN [02_admin.sql] - 2 Tài khoản Admin
-- ============================================================
SET IDENTITY_INSERT admin ON;
INSERT INTO admin (id, nguoi_dung_id, phong_ban, cap_do, ghi_chu) VALUES
(1, 1, N'Quản trị hệ thống', N'Cao',   N'Quản trị viên cấp cao'),
(2, 2, N'IT - Kỹ thuật',     N'Trung', N'Tài khoản kỹ thuật');
SET IDENTITY_INSERT admin OFF;
DBCC CHECKIDENT ('admin', RESEED, 2);
GO

-- ============================================================
-- 4. BỆNH NHÂN [03_benh_nhan.sql] - Đặt Identity về 0 để tự sinh khi tạo từ API
-- ============================================================
DBCC CHECKIDENT ('benh_nhan', RESEED, 0);
GO

-- ============================================================
-- 5. BÁC SĨ [04_bac_si.sql] - 20 Bác sĩ tương ứng
-- ============================================================
SET IDENTITY_INSERT bac_si ON;
INSERT INTO bac_si (id, nguoi_dung_id, chuyen_khoa_id, hoc_vi, kinh_nghiem, gia_kham, rating, so_luong_danh_gia) VALUES
(1,  3,  1,  N'Bác sĩ CKI',  15, 250000.00, 4.9, 120),
(2,  4,  1,  N'PGS.TS',      20, 350000.00, 4.8, 95),
(3,  5,  2,  N'Bác sĩ CKII', 15, 300000.00, 4.9, 150),
(4,  6,  2,  N'Thạc sĩ',     10, 250000.00, 4.7, 82),
(5,  7,  3,  N'Thạc sĩ',     12, 200000.00, 4.8, 100),
(6,  8,  3,  N'Bác sĩ CKI',  15, 250000.00, 4.9, 140),
(7,  9,  4,  N'Bác sĩ CKII', 16, 300000.00, 4.9, 125),
(8,  10, 4,  N'Thạc sĩ',     10, 250000.00, 4.8, 95),
(9,  11, 5,  N'Bác sĩ CKI',  13, 250000.00, 4.9, 145),
(10, 12, 5,  N'Thạc sĩ',     11, 250000.00, 4.8, 115),
(11, 13, 6,  N'Bác sĩ CKII', 15, 300000.00, 4.9, 135),
(12, 14, 6,  N'Thạc sĩ',     12, 250000.00, 4.8, 105),
(13, 15, 7,  N'Bác sĩ CKII', 17, 350000.00, 4.9, 155),
(14, 16, 7,  N'Thạc sĩ',     11, 250000.00, 4.8, 110),
(15, 17, 8,  N'Bác sĩ CKII', 14, 300000.00, 4.9, 140),
(16, 18, 8,  N'Thạc sĩ',     10, 250000.00, 4.8, 100),
(17, 19, 9,  N'Bác sĩ CKII', 16, 350000.00, 4.9, 160),
(18, 20, 9,  N'Thạc sĩ',     11, 250000.00, 4.8, 105),
(19, 21, 10, N'Bác sĩ CKII', 15, 300000.00, 4.9, 145),
(20, 22, 10, N'Thạc sĩ',     11, 250000.00, 4.8, 105);

SET IDENTITY_INSERT bac_si OFF;
DBCC CHECKIDENT ('bac_si', RESEED, 20);
GO

-- ============================================================
-- 6. DỊCH VỤ KHÁM [06_dich_vu.sql] - 10 Dịch vụ tiêu chuẩn
-- ============================================================
SET IDENTITY_INSERT dich_vu ON;
INSERT INTO dich_vu (id, chuyen_khoa_id, ten_dich_vu, gia_tien, mo_ta, dang_hoat_dong) VALUES
(1,  1,  N'Khám Thần kinh chuyên sâu',       350000.00, N'Tư vấn chứng đau đầu, chóng mặt, mất ngủ', 1),
(2,  2,  N'Khám Tim mạch & Đo ECG',          500000.00, N'Đo điện tâm đồ và tầm soát cao huyết áp',  1),
(3,  3,  N'Khám Nhi tổng quát',              250000.00, N'Khám sức khỏe trẻ em và tư vấn dinh dưỡng',1),
(4,  4,  N'Nội soi Tai Mũi Họng',            300000.00, N'Nội soi tầm soát viêm xoang, viêm họng',   1),
(5,  5,  N'Khám & Tư vấn Da liễu',           200000.00, N'Điều trị mụn, nấm da, dị ứng',             1),
(6,  6,  N'Khám Xương khớp & Cột sống',      400000.00, N'Chẩn đoán thoát vị đĩa đệm, đau lưng',     1),
(7,  7,  N'Nội soi Dạ dày - Tiêu hóa',       600000.00, N'Nội soi tầm soát viêm loét dạ dày, trào ngược', 1),
(8,  8,  N'Đo khúc xạ & Khám Mắt',           200000.00, N'Khám mắt tổng quát, đo độ cận viễn loạn',  1),
(9,  9,  N'Khám Phụ khoa & Siêu âm',        450000.00, N'Siêu âm thai, tầm soát phụ khoa',          1),
(10, 10, N'Khám Hô hấp & Đo thông khí',      350000.00, N'Khám hen suyễn, viêm phế quản',             1);
SET IDENTITY_INSERT dich_vu OFF;
DBCC CHECKIDENT ('dich_vu', RESEED, 10);
GO

-- ============================================================
-- 7. TRIỆU CHỨNG [11_trieu_chung.sql] - 15 triệu chứng / chuyên khoa
-- ============================================================
SET IDENTITY_INSERT trieu_chung ON;
INSERT INTO trieu_chung (id, ten_trieu_chung, chuyen_khoa_id) VALUES
-- Khoa 1: Thần kinh (1-15)
(1,  N'Đau đầu nửa đầu (Migraine)',    1),
(2,  N'Mất ngủ kéo dài',               1),
(3,  N'Chóng mặt hoa mắt rối loạn tiền đình', 1),
(4,  N'Tê bì tay chân kéo dài',        1),
(5,  N'Suy giảm trí nhớ quên ngắt quãng', 1),
(6,  N'Co giật cơ mặt',                1),
(7,  N'Đau dây thần kinh tọa',         1),
(8,  N'Run tay chân khi nghỉ ngơi',   1),
(9,  N'Mất thăng bằng khi đi lại',     1),
(10, N'Rối loạn hành vi cảm xúc',      1),
(11, N'Đau mỏi cổ vai thần kinh',     1),
(12, N'Cảm giác châm chích dưới da',   1),
(13, N'Đau nửa mặt bộc phát',         1),
(14, N'Giảm vị giác thính giác thần kinh', 1),
(15, N'Đau đầu vùng chẩm sau cổ',      1),

-- Khoa 2: Tim mạch (16-30)
(16, N'Đau tức ngực bóp nghẹt',        2),
(17, N'Hồi hộp đánh trống ngực',       2),
(18, N'Tăng huyết áp vô căn',          2),
(19, N'Khó thở khi vận động nhẹ',      2),
(20, N'Sưng phù hai bàn chân',         2),
(21, N'Nhịp tim quá nhanh hoặc quá chậm', 2),
(22, N'Vã mồ hôi lạnh kèm đau ngực',   2),
(23, N'Choáng váng khi thay đổi tư thế', 2),
(24, N'Tím tái môi và đầu ngón tay',   2),
(25, N'Mệt mỏi kiệt sức bất thường',   2),
(26, N'Đau lan ra vai trái hoặc hàm',  2),
(27, N'Khó thở nằm phải kê cao đầu',   2),
(28, N'Hạ huyết áp tư thế',           2),
(29, N'Cảm giác nghẹn thở bàng hoàng', 2),
(30, N'Mạch đập không đều hẫng nhịp', 2),

-- Khoa 3: Nhi khoa (31-45)
(31, N'Sốt cao co giật ở trẻ em',      3),
(32, N'Ho khò khè thở rít ở trẻ',      3),
(33, N'Biếng ăn suy dinh dưỡng',       3),
(34, N'Nôn trớ ọc sữa kéo dài',       3),
(35, N'Quấy khóc đêm không gián đoạn', 3),
(36, N'Tiêu chảy cấp mất nước ở trẻ', 3),
(37, N'Nổi mẩn đỏ sởi phát ban',       3),
(38, N'Chậm phát triển vận động ngôn ngữ', 3),
(39, N'Sổ mũi đặc ngạt mũi kéo dài',   3),
(40, N'Táo bón bón phân cứng ở trẻ',   3),
(41, N'Viêm tai giữa chảy dịch ear',   3),
(42, N'Da mẩn ngứa hăm tã ở trẻ sơ sinh', 3),
(43, N'Sốt kèm mụn nước chân tay miệng', 3),
(44, N'Đau bụng giật cục ở trẻ',      3),
(45, N'Đái dầm không kiểm soát',       3),

-- Khoa 4: Tai Mũi Họng (46-60)
(46, N'Đau họng rát họng khó nuốt',    4),
(47, N'Ù tai giảm thính lực',           4),
(48, N'Nghẹt mũi chảy nước mũi trong/đục', 4),
(49, N'Khàn tiếng mất tiếng kéo dài',  4),
(50, N'Hắt hơi liên tục do dị ứng',   4),
(51, N'Sưng đau vùng xoang trán/má',   4),
(52, N'Chảy máu cam bất thường',       4),
(53, N'Đau nhói trong tai có mủ',     4),
(54, N'Ngủ ngáy kèm ngừng thở ngắn',   4),
(55, N'Hơi thở có mùi hôi mãn tính',   4),
(56, N'Cảm giác vướng víu ở cổ họng',  4),
(57, N'Sưng đau hạnh nhân Amydal',    4),
(58, N'Ho hèm hẹp khạc đờm nhiều',    4),
(59, N'Đau đầu liên quan viêm xoang',  4),
(60, N'Mất cảm giác mùi hương (Khứu giác)', 4),

-- Khoa 5: Da liễu (61-75)
(61, N'Nổi mẩn đỏ ngứa toàn thân',     5),
(62, N'Mụn trứng cá bọc bọc mủ',      5),
(63, N'Rụng tóc từng mảng ngứa da đầu', 5),
(64, N'Vảy nến bong tróc da nhiều khô', 5),
(65, N'Dị ứng nổi mề đay cục bộ',     5),
(66, N'Viêm da cơ địa chàm khô',       5),
(67, N'Nấm da lang ben ngứa rát',      5),
(68, N'Mụn nhọt sưng đau có mủ',       5),
(69, N'Rạn da biến đổi sắc tố da',    5),
(70, N'Thủy đậu nốt phỏng mụn nước',   5),
(71, N'Nổi mẩn đỏ sau khi ăn hải sản', 5),
(72, N'Mẩn ngứa nốt đỏ dai dẳng',      5),
(73, N'Khô nẻ nứt nẻ da nghiêm trọng',  5),
(74, N'Xuất hiện nốt mụn lạ phát triển', 5),
(75, N'Viêm nang lông chân lông',     5),

-- Khoa 6: Xương khớp (76-90)
(76, N'Đau lưng thắt lưng cột sống',   6),
(77, N'Đau khớp gối khi đi lại cầu thang', 6),
(78, N'Cứng khớp buổi sáng khó vận động', 6),
(79, N'Tê sưng nóng đỏ các khớp',      6),
(80, N'Đau mỏi vùng vai gáy',          6),
(81, N'Cảm giác lục khục ở khớp gối',  6),
(82, N'Thoát vị đĩa đệm tê chân',     6),
(83, N'Đau nhức xương khớp khi đổi thời tiết', 6),
(84, N'Hạn chế ngửa gập xoay cổ thắt lưng', 6),
(85, N'Viêm khớp gút sưng ngón chân cái', 6),
(86, N'Đau lan xuống hông đùi',        6),
(87, N'Yếu cơ đùi cánh tay khó nhấc',  6),
(88, N'Đau biến dạng ngón tay ngón chân', 6),
(89, N'Đau xói vùng hông chậu',        6),
(90, N'Co rút cơ chuột rút liên tục', 6),

-- Khoa 7: Tiêu hóa (91-105)
(91, N'Đau thượng vị dạ dày co thắt',  7),
(92, N'Trào ngược dịch vị ợ chua ợ nóng', 7),
(93, N'Đầy hơi chướng bụng ăn không tiêu', 7),
(94, N'Rối loạn tiêu hóa phân sống',   7),
(95, N'Táo bón dai dẳng phân cứng',    7),
(96, N'Tiêu chảy phân lỏng nhiều lần', 7),
(97, N'Đau bụng quanh rốn/mạn sườn',   7),
(98, N'Nôn buồn nôn sau khi ăn',       7),
(99, N'Chán ăn đắng miệng chán mỡ',    7),
(100, N'Vàng da vàng mắt phân bạc màu', 7),
(101, N'Đi ngoài ra máu tươi hoặc đen', 7),
(102, N'Nổi cục sưng đau hậu môn trĩ', 7),
(103, N'Co thắt đại tràng mạn tính',   7),
(104, N'Cảm giác sút cân nhanh chóng',  7),
(105, N'Đau nhói vùng hạ sườn phải',   7),

-- Khoa 8: Mắt (106-120)
(106, N'Nhìn mờ giảm thị lực dần',     8),
(107, N'Đau mắt đỏ chảy nước mắt liên tục', 8),
(108, N'Khô mắt rát mắt cộm mắt',      8),
(109, N'Sợ ánh sáng chói mắt',         8),
(110, N'Nhìn thấy ruồi bay đốm đen',   8),
(111, N'Nhìn đôi một thành hai (Song thị)', 8),
(112, N'Mắt sưng đỏ có mủ gèn',        8),
(113, N'Đau nhói sâu trong hốc mắt',   8),
(114, N'Chảy nước mắt sống khi ra gió', 8),
(115, N'Nhìn hẹp viền xung quanh (Thị trường)', 8),
(116, N'Sụp mi mắt không nâng lên được', 8),
(117, N'Lác mắt lệch nhãn cầu',        8),
(118, N'Nốt lẹo mụn sưng ở mi mắt',    8),
(119, N'Nhìn quầng hào quang quanh đèn', 8),
(120, N'Ngứa ngáy mi mắt bờ mi',       8),

-- Khoa 9: Sản phụ khoa (121-135)
(121, N'Chậm kinh đau bụng dưới râm rỉ', 9),
(122, N'Khám thai định kỳ kiểm tra thai', 9),
(123, N'Rối loạn kinh nguyệt không đều', 9),
(124, N'Khí hư huyết trắng có màu lạ mùi hôi', 9),
(125, N'Ngứa rát đau vùng kín âm đạo',  9),
(126, N'Chảy máu âm đạo bất thường ngoài kỳ', 9),
(127, N'Đau rát khi quan hệ tình dục', 9),
(128, N'Căng tức tuyến vú sờ có cục u', 9),
(129, N'Đau thắt lưng kinh nguyệt nhiều', 9),
(130, N'Nghén nặng nôn mửa liên tục khi mang thai', 9),
(131, N'Cảm giác sa vùng chậu nặng bụng', 9),
(132, N'Mất kinh nguyệt thời gian dài', 9),
(133, N'Bốc hỏa rối loạn tiền mãn kinh', 9),
(134, N'Hiếm muộn chậm có con',        9),
(135, N'Rối loạn tiểu tiện thai kỳ',    9),

-- Khoa 10: Hô hấp (136-150)
(136, N'Ho kéo dài có đờm đặc',        10),
(137, N'Tức ngực thở khò khè rít',     10),
(138, N'Sốt nhẹ ho khan thở hụt hơi',   10),
(139, N'Khó thở về đêm khi nằm',       10),
(140, N'Thở gấp hụt hơi khi leo cầu thang', 10),
(141, N'Ho ra máu lẫn trong đờm',      10),
(142, N'Đau thắt ngực khi hít sâu',    10),
(143, N'Rút lõm lồng ngực khi thở',    10),
(144, N'Thở khè khè như bị nghẹn',     10),
(145, N'Cảm giác thắt nghẹn phế quản', 10),
(146, N'Sốt cao ho đờm xanh đục',      10),
(147, N'Mệt mỏi thở dốc dai dẳng',     10),
(148, N'Khó thở kèm tiếng ngáy ngạt',  10),
(149, N'Ho kịch phát từng cơn dai dẳng', 10),
(150, N'Viêm phế quản tái phát nhiều lần', 10);

SET IDENTITY_INSERT trieu_chung OFF;
DBCC CHECKIDENT ('trieu_chung', RESEED, 150);
GO

-- ============================================================
-- 8. MAP TRIỆU CHỨNG - BÁC SĨ [12_trieu_chung_bac_si.sql] (2 BS / triệu chứng)
-- ============================================================
INSERT INTO trieu_chung_bac_si (trieu_chung_id, bac_si_id)
SELECT id, (chuyen_khoa_id - 1) * 2 + 1 FROM trieu_chung
UNION ALL
SELECT id, (chuyen_khoa_id - 1) * 2 + 2 FROM trieu_chung;
GO

-- ============================================================
-- 9. LỊCH LÀM VIỆC [07_lich_lam_viec.sql]
-- Sáng: 07:30 - 11:30 | Chiều: 13:30 - 18:30 | Tối ngoài giờ (+10%): 18:30 - 22:30
-- ============================================================
INSERT INTO lich_lam_viec (bac_si_id, ngay_kham, khung_gio, con_trong)
-- Ca Sáng (07:30 - 11:30)
SELECT id, CAST(DATEADD(day, 1, GETDATE()) AS DATE), N'07:30 - 09:30', 1 FROM bac_si
UNION ALL
SELECT id, CAST(DATEADD(day, 1, GETDATE()) AS DATE), N'09:30 - 11:30', 1 FROM bac_si

-- Ca Chiều (13:30 - 18:30)
UNION ALL
SELECT id, CAST(DATEADD(day, 1, GETDATE()) AS DATE), N'13:30 - 16:00', 1 FROM bac_si
UNION ALL
SELECT id, CAST(DATEADD(day, 1, GETDATE()) AS DATE), N'16:00 - 18:30', 1 FROM bac_si

-- Ca Tối ngoài giờ (18:30 - 22:30)
UNION ALL
SELECT id, CAST(DATEADD(day, 1, GETDATE()) AS DATE), N'18:30 - 20:30 (Ngoài giờ +10%)', 1 FROM bac_si
UNION ALL
SELECT id, CAST(DATEADD(day, 1, GETDATE()) AS DATE), N'20:30 - 22:30 (Ngoài giờ +10%)', 1 FROM bac_si;
GO

PRINT N'✅ Đã nạp thành công SEED.SQL chuẩn hóa cho hệ thống MedBooking!';
GO