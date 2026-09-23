-- ============================================================
-- SEED.SQL - SQL Server Seed Data
-- Dự án: Hệ thống Đặt lịch khám trực tuyến MedBooking
-- Bao gồm: 2 Admin, 7 Lễ tân, 10 chuyên khoa, 50 bác sĩ, 50 triệu chứng, 3 bệnh nhân
-- ============================================================

USE PhongKhamDB;
GO

SET DATEFORMAT ymd;
GO


-- ============================================================
-- 1. CHUYÊN KHOA (10 chuyên khoa)
-- ============================================================
SET IDENTITY_INSERT chuyen_khoa ON;
INSERT INTO chuyen_khoa (id, ten_chuyen_khoa, mo_ta) VALUES
(1,  N'Thần kinh',        N'Chẩn đoán và điều trị bệnh lý về não bộ, thần kinh, mất ngủ, đau đầu'),
(2,  N'Tim mạch',          N'Tầm soát và điều trị bệnh lý mạch máu, cao huyết áp, rối loạn nhịp tim'),
(3,  N'Nhi khoa',          N'Chăm sóc sức khỏe toàn diện và điều trị bệnh lý ở trẻ nhỏ'),
(4,  N'Tai Mũi Họng',      N'Điều trị viêm xoang, viêm họng, các vấn đề thính lực và thanh quản'),
(5,  N'Da liễu',           N'Tư vấn và điều trị bệnh lý về da, dị ứng, mụn trứng cá, chàm'),
(6,  N'Xương khớp',        N'Chẩn đoán thoái hóa khớp, thoát vị đĩa đệm, đau cột sống'),
(7,  N'Tiêu hóa',          N'Điều trị dạ dày, đại tràng, trào ngược thực quản, gan mật'),
(8,  N'Mắt (Nhãn khoa)',  N'Khám khúc xạ, cận thị, đau mắt đỏ, cườm mắt'),
(9,  N'Sản phụ khoa',      N'Tư vấn thai kỳ, khám phụ khoa, tầm soát ung thư phụ khoa'),
(10, N'Hô hấp',            N'Điều trị viêm phổi, hen suyễn, viêm phế quản và bệnh phổi mãn tính');
SET IDENTITY_INSERT chuyen_khoa OFF;
DBCC CHECKIDENT ('chuyen_khoa', RESEED, 10);
GO

-- ============================================================
-- 2. NGƯỜI DÙNG
-- 2 admin + 7 lễ tân + 50 bác sĩ + 3 bệnh nhân = 62 người dùng
-- Mật khẩu mẫu: "password123" (hash bcrypt thật)
-- ============================================================
SET IDENTITY_INSERT nguoi_dung ON;

-- Admin (ID 1, 62)
INSERT INTO nguoi_dung (id, email, mat_khau, ho_ten, so_dien_thoai, vai_tro) VALUES
(1,  'admin@medbooking.com',    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewUvE.eLpO5wE7km', N'Hệ Thống Admin',      '0901000000', 'admin'),
(62, 'it.admin@medbooking.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewUvE.eLpO5wE7km', N'Kỹ Thuật Viên Admin', '0901000099', 'admin');

-- Lễ tân (ID 2-8)
INSERT INTO nguoi_dung (id, email, mat_khau, ho_ten, so_dien_thoai, vai_tro) VALUES
(2, 'letan.mai@medbooking.com',   '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewUvE.eLpO5wE7km', N'Lễ tân Nguyễn Mai Phương', '0901000001', 'le_tan'),
(3, 'letan.hoa@medbooking.com',   '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewUvE.eLpO5wE7km', N'Lễ tân Trần Thị Hoa',      '0901000002', 'le_tan'),
(4, 'letan.linh@medbooking.com',  '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewUvE.eLpO5wE7km', N'Lễ tân Bùi Khánh Linh',    '0901000003', 'le_tan'),
(5, 'letan.trang@medbooking.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewUvE.eLpO5wE7km', N'Lễ tân Lê Thu Trang',      '0901000004', 'le_tan'),
(6, 'letan.vy@medbooking.com',    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewUvE.eLpO5wE7km', N'Lễ tân Đỗ Thảo Vy',        '0901000005', 'le_tan'),
(7, 'letan.huyen@medbooking.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewUvE.eLpO5wE7km', N'Lễ tân Phạm Ngọc Huyền',   '0901000006', 'le_tan'),
(8, 'letan.an@medbooking.com',    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewUvE.eLpO5wE7km', N'Lễ tân Vũ Hoài An',        '0901000007', 'le_tan');

-- Bác sĩ khoa 1: Thần kinh (ID 9-13)
INSERT INTO nguoi_dung (id, email, mat_khau, ho_ten, so_dien_thoai, vai_tro) VALUES
(9,  'bs.hung.tk@medbooking.com',  '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewUvE.eLpO5wE7km', N'BS. Nguyễn Văn Hùng',   '0902000001', 'bac_si'),
(10, 'bs.lan.tk@medbooking.com',   '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewUvE.eLpO5wE7km', N'PGS.TS Trần Thị Lan',   '0902000002', 'bac_si'),
(11, 'bs.minh.tk@medbooking.com',  '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewUvE.eLpO5wE7km', N'BS. Lê Hoài Minh',      '0902000003', 'bac_si'),
(12, 'bs.tuan.tk@medbooking.com',  '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewUvE.eLpO5wE7km', N'BS. Phạm Anh Tuấn',     '0902000004', 'bac_si'),
(13, 'bs.ha.tk@medbooking.com',    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewUvE.eLpO5wE7km', N'BS. Đỗ Thu Hà',         '0902000005', 'bac_si');

-- Bác sĩ khoa 2: Tim mạch (ID 14-18)
INSERT INTO nguoi_dung (id, email, mat_khau, ho_ten, so_dien_thoai, vai_tro) VALUES
(14, 'bs.duc.tm@medbooking.com',   '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewUvE.eLpO5wE7km', N'BS. Hoàng Minh Đức',    '0902000006', 'bac_si'),
(15, 'bs.nam.tm@medbooking.com',   '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewUvE.eLpO5wE7km', N'BS. Vũ Hải Nam',        '0902000007', 'bac_si'),
(16, 'bs.thao.tm@medbooking.com',  '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewUvE.eLpO5wE7km', N'BS. Nguyễn Phương Thảo','0902000008', 'bac_si'),
(17, 'bs.huong.tm@medbooking.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewUvE.eLpO5wE7km', N'BS. Bùi Thanh Hương',   '0902000009', 'bac_si'),
(18, 'bs.khang.tm@medbooking.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewUvE.eLpO5wE7km', N'BS. Ngô Bảo Khang',     '0902000010', 'bac_si');

-- Bác sĩ khoa 3: Nhi khoa (ID 19-23)
INSERT INTO nguoi_dung (id, email, mat_khau, ho_ten, so_dien_thoai, vai_tro) VALUES
(19, 'bs.an.nk@medbooking.com',    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewUvE.eLpO5wE7km', N'BS. Phạm Quốc An',      '0902000011', 'bac_si'),
(20, 'bs.binh.nk@medbooking.com',  '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewUvE.eLpO5wE7km', N'BS. Lý Thanh Bình',     '0902000012', 'bac_si'),
(21, 'bs.cuong.nk@medbooking.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewUvE.eLpO5wE7km', N'BS. Trịnh Văn Cường',   '0902000013', 'bac_si'),
(22, 'bs.dung.nk@medbooking.com',  '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewUvE.eLpO5wE7km', N'BS. Hoàng Mỹ Dung',     '0902000014', 'bac_si'),
(23, 'bs.giang.nk@medbooking.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewUvE.eLpO5wE7km', N'BS. Lê Hương Giang',    '0902000015', 'bac_si');

-- Bác sĩ khoa 4: Tai Mũi Họng (ID 24-28)
INSERT INTO nguoi_dung (id, email, mat_khau, ho_ten, so_dien_thoai, vai_tro) VALUES
(24, 'bs.hai.tmh@medbooking.com',  '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewUvE.eLpO5wE7km', N'BS. Nguyễn Quang Hải',  '0902000016', 'bac_si'),
(25, 'bs.khanh.tmh@medbooking.com','$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewUvE.eLpO5wE7km', N'BS. Đỗ Vân Khánh',      '0902000017', 'bac_si'),
(26, 'bs.long.tmh@medbooking.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewUvE.eLpO5wE7km', N'BS. Vũ Phi Long',       '0902000018', 'bac_si'),
(27, 'bs.my.tmh@medbooking.com',   '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewUvE.eLpO5wE7km', N'BS. Bùi Huyền Mỹ',      '0902000019', 'bac_si'),
(28, 'bs.nghia.tmh@medbooking.com','$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewUvE.eLpO5wE7km', N'BS. Trần Tấn Nghĩa',    '0902000020', 'bac_si');

-- Bác sĩ khoa 5: Da liễu (ID 29-33)
INSERT INTO nguoi_dung (id, email, mat_khau, ho_ten, so_dien_thoai, vai_tro) VALUES
(29, 'bs.oanh.dl@medbooking.com',  '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewUvE.eLpO5wE7km', N'BS. Hoàng Kiều Oanh',   '0902000021', 'bac_si'),
(30, 'bs.phong.dl@medbooking.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewUvE.eLpO5wE7km', N'BS. Lê Thanh Phong',    '0902000022', 'bac_si'),
(31, 'bs.quyen.dl@medbooking.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewUvE.eLpO5wE7km', N'BS. Đặng Ngọc Quyên',   '0902000023', 'bac_si'),
(32, 'bs.son.dl@medbooking.com',   '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewUvE.eLpO5wE7km', N'BS. Nguyễn Thái Sơn',   '0902000024', 'bac_si'),
(33, 'bs.tam.dl@medbooking.com',   '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewUvE.eLpO5wE7km', N'BS. Trịnh Minh Tâm',    '0902000025', 'bac_si');

-- Bác sĩ khoa 6: Xương khớp (ID 34-38)
INSERT INTO nguoi_dung (id, email, mat_khau, ho_ten, so_dien_thoai, vai_tro) VALUES
(34, 'bs.uy.xk@medbooking.com',    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewUvE.eLpO5wE7km', N'BS. Phan Quốc Uy',      '0902000026', 'bac_si'),
(35, 'bs.vinh.xk@medbooking.com',  '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewUvE.eLpO5wE7km', N'BS. Vũ Thế Vinh',       '0902000027', 'bac_si'),
(36, 'bs.xuan.xk@medbooking.com',  '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewUvE.eLpO5wE7km', N'BS. Nguyễn Thanh Xuân', '0902000028', 'bac_si'),
(37, 'bs.yen.xk@medbooking.com',   '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewUvE.eLpO5wE7km', N'BS. Bùi Bảo Yến',       '0902000029', 'bac_si'),
(38, 'bs.anh.xk@medbooking.com',   '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewUvE.eLpO5wE7km', N'BS. Trần Tuấn Anh',     '0902000030', 'bac_si');

-- Bác sĩ khoa 7: Tiêu hóa (ID 39-43)
INSERT INTO nguoi_dung (id, email, mat_khau, ho_ten, so_dien_thoai, vai_tro) VALUES
(39, 'bs.bao.th@medbooking.com',   '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewUvE.eLpO5wE7km', N'BS. Hoàng Gia Bảo',     '0902000031', 'bac_si'),
(40, 'bs.chau.th@medbooking.com',  '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewUvE.eLpO5wE7km', N'BS. Đỗ Minh Châu',      '0902000032', 'bac_si'),
(41, 'bs.dat.th@medbooking.com',   '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewUvE.eLpO5wE7km', N'BS. Lê Tiến Đạt',       '0902000033', 'bac_si'),
(42, 'bs.giang.th@medbooking.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewUvE.eLpO5wE7km', N'BS. Phạm Đức Giang',    '0902000034', 'bac_si'),
(43, 'bs.hang.th@medbooking.com',  '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewUvE.eLpO5wE7km', N'BS. Nguyễn Thúy Hằng',  '0902000035', 'bac_si');

-- Bác sĩ khoa 8: Mắt (ID 44-48)
INSERT INTO nguoi_dung (id, email, mat_khau, ho_ten, so_dien_thoai, vai_tro) VALUES
(44, 'bs.khoi.mat@medbooking.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewUvE.eLpO5wE7km', N'BS. Vũ Đăng Khôi',      '0902000036', 'bac_si'),
(45, 'bs.linh.mat@medbooking.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewUvE.eLpO5wE7km', N'BS. Trịnh Khánh Linh',  '0902000037', 'bac_si'),
(46, 'bs.manh.mat@medbooking.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewUvE.eLpO5wE7km', N'BS. Phan Đức Mạnh',     '0902000038', 'bac_si'),
(47, 'bs.ngan.mat@medbooking.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewUvE.eLpO5wE7km', N'BS. Lê Thu Ngân',       '0902000039', 'bac_si'),
(48, 'bs.phuc.mat@medbooking.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewUvE.eLpO5wE7km', N'BS. Hoàng Hồng Phúc',   '0902000040', 'bac_si');

-- Bác sĩ khoa 9: Sản phụ khoa (ID 49-53)
INSERT INTO nguoi_dung (id, email, mat_khau, ho_ten, so_dien_thoai, vai_tro) VALUES
(49, 'bs.quynh.spk@medbooking.com','$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewUvE.eLpO5wE7km', N'BS. Nguyễn Như Quỳnh',  '0902000041', 'bac_si'),
(50, 'bs.sang.spk@medbooking.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewUvE.eLpO5wE7km', N'BS. Đỗ Tấn Sáng',       '0902000042', 'bac_si'),
(51, 'bs.trang.spk@medbooking.com','$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewUvE.eLpO5wE7km', N'BS. Bùi Đoan Trang',    '0902000043', 'bac_si'),
(52, 'bs.tu.spk@medbooking.com',   '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewUvE.eLpO5wE7km', N'BS. Vũ Anh Tú',         '0902000044', 'bac_si'),
(53, 'bs.van.spk@medbooking.com',  '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewUvE.eLpO5wE7km', N'BS. Phạm Cẩm Vân',      '0902000045', 'bac_si');

-- Bác sĩ khoa 10: Hô hấp (ID 54-58)
INSERT INTO nguoi_dung (id, email, mat_khau, ho_ten, so_dien_thoai, vai_tro) VALUES
(54, 'bs.viet.hh@medbooking.com',  '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewUvE.eLpO5wE7km', N'BS. Hoàng Quốc Việt',   '0902000046', 'bac_si'),
(55, 'bs.vinh.hh@medbooking.com',  '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewUvE.eLpO5wE7km', N'BS. Nguyễn Quang Vinh', '0902000047', 'bac_si'),
(56, 'bs.y.hh@medbooking.com',     '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewUvE.eLpO5wE7km', N'BS. Trịnh Như Ý',       '0902000048', 'bac_si'),
(57, 'bs.khai.hh@medbooking.com',  '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewUvE.eLpO5wE7km', N'BS. Lê Quang Khải',     '0902000049', 'bac_si'),
(58, 'bs.lam.hh@medbooking.com',   '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewUvE.eLpO5wE7km', N'BS. Đỗ Tung Lâm',       '0902000050', 'bac_si');

-- Bệnh nhân mẫu (ID 59-61)
INSERT INTO nguoi_dung (id, email, mat_khau, ho_ten, so_dien_thoai, vai_tro) VALUES
(59, 'bn.an@gmail.com',    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewUvE.eLpO5wE7km', N'Nguyễn Văn An',  '0912345678', 'benh_nhan'),
(60, 'bn.binh@gmail.com',  '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewUvE.eLpO5wE7km', N'Trần Thị Bình',  '0912345679', 'benh_nhan'),
(61, 'bn.cuong@gmail.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewUvE.eLpO5wE7km', N'Lê Văn Cường',   '0912345680', 'benh_nhan');

SET IDENTITY_INSERT nguoi_dung OFF;
DBCC CHECKIDENT ('nguoi_dung', RESEED, 62);
GO

-- ============================================================
-- 3. ADMIN (Thông tin quản trị)
-- ============================================================
SET IDENTITY_INSERT admin ON;
INSERT INTO admin (id, nguoi_dung_id, phong_ban, cap_do, ghi_chu) VALUES
(1, 1,  N'Quản trị hệ thống', N'Cao',   N'Quản trị viên cấp cao, toàn quyền hệ thống'),
(2, 62, N'IT - Kỹ thuật',     N'Trung', N'Tài khoản dự phòng cho kỹ thuật viên');
SET IDENTITY_INSERT admin OFF;
DBCC CHECKIDENT ('admin', RESEED, 2);
GO

-- ============================================================
-- 4. BỆNH NHÂN (3 người)
-- ============================================================
SET IDENTITY_INSERT benh_nhan ON;
INSERT INTO benh_nhan (id, nguoi_dung_id, ngay_sinh, gioi_tinh, dia_chi) VALUES
(1, 59, '1990-05-15', N'Nam', N'123 Lê Lợi, Quận 1, TP.HCM'),
(2, 60, '1995-08-20', N'Nữ',  N'456 Nguyễn Huệ, Quận 1, TP.HCM'),
(3, 61, '1988-12-01', N'Nam', N'789 Trần Hưng Đạo, Quận 5, TP.HCM');
SET IDENTITY_INSERT benh_nhan OFF;
DBCC CHECKIDENT ('benh_nhan', RESEED, 3);
GO

-- ============================================================
-- 5. BÁC SĨ (50 bác sĩ)
-- ============================================================
SET IDENTITY_INSERT bac_si ON;
INSERT INTO bac_si (id, nguoi_dung_id, chuyen_khoa_id, mo_ta, rating, so_luong_danh_gia) VALUES
-- Khoa 1: Thần kinh
(1,  9,  1, N'Chuyên gia Thần kinh hơn 15 năm kinh nghiệm', 4.9, 120),
(2,  10, 1, N'PGS.TS Thần kinh học lâm sàng',                4.8, 95),
(3,  11, 1, N'Bác sĩ chuyên khoa chẩn đoán đau đầu mãn tính',4.7, 78),
(4,  12, 1, N'Bác sĩ điều trị rối loạn giấc ngủ',           4.6, 65),
(5,  13, 1, N'Bác sĩ Thần kinh ngoại biên',                  4.8, 88),
-- Khoa 2: Tim mạch
(6,  14, 2, N'Chuyên gia Tim mạch can thiệp',                4.9, 150),
(7,  15, 2, N'Bác sĩ điều trị cao huyết áp và xơ vữa',      4.7, 82),
(8,  16, 2, N'Bác sĩ chuyên tầm soát rối loạn nhịp tim',    4.8, 110),
(9,  17, 2, N'Bác sĩ Tim mạch lâm sàng',                     4.6, 70),
(10, 18, 2, N'Bác sĩ Tim mạch lão khoa',                    4.9, 130),
-- Khoa 3: Nhi khoa
(11, 19, 3, N'Bác sĩ Nhi khoa tổng quát',                    4.8, 100),
(12, 20, 3, N'Chuyên gia Dinh dưỡng & Nhi khoa',            4.9, 140),
(13, 21, 3, N'Bác sĩ Nhi khoa giàu kinh nghiệm',            4.7, 90),
(14, 22, 3, N'Bác sĩ tư vấn sức khỏe trẻ sơ sinh',          4.8, 105),
(15, 23, 3, N'Bác sĩ Nhi hô hấp',                            4.6, 60),
-- Khoa 4: Tai Mũi Họng
(16, 24, 4, N'Bác sĩ Tai Mũi Họng tu nghiệp tại Pháp',      4.9, 125),
(17, 25, 4, N'Bác sĩ phẫu thuật vi phẫu Tai Mũi Họng',      4.8, 95),
(18, 26, 4, N'Chuyên gia điều trị viêm xoang',              4.7, 80),
(19, 27, 4, N'Bác sĩ Tai Mũi Họng Nhi',                     4.6, 55),
(20, 28, 4, N'Bác sĩ nội soi Tai Mũi Họng',                  4.8, 100),
-- Khoa 5: Da liễu
(21, 29, 5, N'Chuyên gia Da liễu thẩm mỹ & lâm sàng',       4.9, 145),
(22, 30, 5, N'Bác sĩ điều trị mụn trứng cá chuyên sâu',     4.8, 115),
(23, 31, 5, N'Bác sĩ điều trị chàm & vi dị ứng da',         4.7, 85),
(24, 32, 5, N'Bác sĩ Da liễu tổng quát',                    4.6, 65),
(25, 33, 5, N'Bác sĩ Da liễu trẻ em',                        4.8, 90),
-- Khoa 6: Xương khớp
(26, 34, 6, N'Bác sĩ Cơ Xương Khớp & Phục hồi chức năng',   4.9, 135),
(27, 35, 6, N'Chuyên gia chẩn đoán thoát vị đĩa đệm',       4.8, 105),
(28, 36, 6, N'Bác sĩ điều trị thoái hóa khớp',              4.7, 75),
(29, 37, 6, N'Bác sĩ Cột sống & Đau khớp',                  4.6, 60),
(30, 38, 6, N'Bác sĩ Xương khớp thể thao',                  4.9, 120),
-- Khoa 7: Tiêu hóa
(31, 39, 7, N'Chuyên gia Nội soi Tiêu hóa',                 4.9, 155),
(32, 40, 7, N'Bác sĩ điều trị dạ dày & trào ngược',         4.8, 110),
(33, 41, 7, N'Bác sĩ chuyên khoa Gan Mật',                  4.7, 85),
(34, 42, 7, N'Bác sĩ Đại trực tràng',                        4.6, 65),
(35, 43, 7, N'Bác sĩ Tiêu hóa tổng quát',                    4.8, 95),
-- Khoa 8: Mắt
(36, 44, 8, N'Bác sĩ Nhãn khoa phẫu thuật khúc xạ',         4.9, 140),
(37, 45, 8, N'Bác sĩ Mắt trẻ em & Khúc xạ',                 4.8, 100),
(38, 46, 8, N'Bác sĩ chẩn đoán Cườm mắt & Glôcôm',          4.7, 80),
(39, 47, 8, N'Bác sĩ điều trị Viêm kết mạc',                4.6, 55),
(40, 48, 8, N'Bác sĩ Nhãn khoa tổng quát',                  4.8, 90),
-- Khoa 9: Sản phụ khoa
(41, 49, 9, N'Chuyên gia Sản phụ khoa & Theo dõi thai kỳ',  4.9, 160),
(42, 50, 9, N'Bác sĩ tầm soát ung thư phụ khoa',            4.8, 105),
(43, 51, 9, N'Bác sĩ Phụ khoa lâm sàng',                    4.7, 80),
(44, 52, 9, N'Bác sĩ Hỗ trợ sinh sản',                      4.9, 125),
(45, 53, 9, N'Bác sĩ Tư vấn sức khỏe sinh sản',             4.6, 60),
-- Khoa 10: Hô hấp
(46, 54, 10, N'Chuyên gia Hô hấp & Bệnh phổi mãn tính',     4.9, 145),
(47, 55, 10, N'Bác sĩ điều trị Hen suyễn',                  4.8, 105),
(48, 56, 10, N'Bác sĩ Hô hấp lâm sàng',                     4.7, 75),
(49, 57, 10, N'Bác sĩ chẩn đoán Viêm phế quản',             4.6, 60),
(50, 58, 10, N'Bác sĩ Hô hấp tổng quát',                    4.8, 90);
SET IDENTITY_INSERT bac_si OFF;
DBCC CHECKIDENT ('bac_si', RESEED, 50);
GO

-- ============================================================
-- 6. DỊCH VỤ KHÁM (10 dịch vụ)
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
(9,  9,  N'Khám Phụ khoa & Siêu âm',         450000.00, N'Siêu âm thai, tầm soát phụ khoa',          1),
(10, 10, N'Khám Hô hấp & Đo thông khí',      350000.00, N'Khám hen suyễn, viêm phế quản',             1);
SET IDENTITY_INSERT dich_vu OFF;
DBCC CHECKIDENT ('dich_vu', RESEED, 10);
GO

-- ============================================================
-- 7. TRIỆU CHỨNG (50 triệu chứng)
-- ============================================================
SET IDENTITY_INSERT trieu_chung ON;
INSERT INTO trieu_chung (id, ten_trieu_chung, chuyen_khoa_id) VALUES
-- Khoa 1: Thần kinh (1-5)
(1,  N'Đau đầu nửa đầu',            1),
(2,  N'Mất ngủ kéo dài',            1),
(3,  N'Chóng mặt hoa mắt',          1),
(4,  N'Tê bì tay chân',             1),
(5,  N'Suy giảm trí nhớ',           1),
-- Khoa 2: Tim mạch (6-10)
(6,  N'Đau tức ngực',                2),
(7,  N'Hồi hộp đánh trống ngực',    2),
(8,  N'Tăng huyết áp',              2),
(9,  N'Khó thở khi vận động',       2),
(10, N'Sưng phù chân tay',          2),
-- Khoa 3: Nhi khoa (11-15)
(11, N'Sốt cao ở trẻ em',            3),
(12, N'Ho khò khè ở trẻ',            3),
(13, N'Biếng ăn chậm lớn',          3),
(14, N'Nôn trớ ở trẻ nhỏ',          3),
(15, N'Quấy khóc đêm ở trẻ',        3),
-- Khoa 4: Tai Mũi Họng (16-20)
(16, N'Đau họng khó nuốt',          4),
(17, N'Ù tai đau tai',              4),
(18, N'Nghẹt mũi chảy nước mũi',    4),
(19, N'Khàn tiếng mất tiếng',       4),
(20, N'Hắt hơi liên tục',           4),
-- Khoa 5: Da liễu (21-25)
(21, N'Nổi mẩn đỏ ngứa da',         5),
(22, N'Mụn trứng cá nặng',          5),
(23, N'Rụng tóc bất thường',        5),
(24, N'Vảy nến bong tróc da',       5),
(25, N'Dị ứng mề đay',              5),
-- Khoa 6: Xương khớp (26-30)
(26, N'Đau lưng mỏi cổ',            6),
(27, N'Đau khớp gối khi đi lại',    6),
(28, N'Cứng khớp buổi sáng',        6),
(29, N'Tê sưng các khớp',            6),
(30, N'Đau nhức cột sống',          6),
-- Khoa 7: Tiêu hóa (31-35)
(31, N'Đau thượng vị dạ dày',       7),
(32, N'Trào ngược ợ chua',          7),
(33, N'Đầy hơi khó tiêu',            7),
(34, N'Rối loạn tiêu hóa',          7),
(35, N'Táo bón hoặc tiêu chảy',     7),
-- Khoa 8: Mắt (36-40)
(36, N'Nhìn mờ mỏi mắt',            8),
(37, N'Đau mắt đỏ chảy nước mắt',   8),
(38, N'Khô mắt rát mắt',            8),
(39, N'Sợ ánh sáng',                8),
(40, N'Nhìn thấy đốm đen',          8),
-- Khoa 9: Sản phụ khoa (41-45)
(41, N'Chậm kinh đau bụng dưới',    9),
(42, N'Khám thai định kỳ',          9),
(43, N'Rối loạn kinh nguyệt',       9),
(44, N'Khí hư bất thường',          9),
(45, N'Ngứa rát vùng kín',          9),
-- Khoa 10: Hô hấp (46-50)
(46, N'Ho kéo dài có đờm',         10),
(47, N'Tức ngực thở khò khè',      10),
(48, N'Sốt ho tức ngực',           10),
(49, N'Khó thở về đêm',            10),
(50, N'Thở gấp hụt hơi',           10);
SET IDENTITY_INSERT trieu_chung OFF;
DBCC CHECKIDENT ('trieu_chung', RESEED, 50);
GO

-- ============================================================
-- 8. MAP TRIỆU CHỨNG - BÁC SĨ (100 mapping)
-- ============================================================
INSERT INTO trieu_chung_bac_si (trieu_chung_id, bac_si_id) VALUES
-- Khoa 1: Thần kinh (BS 1-5, TC 1-5)
(1, 1), (2, 1), (1, 2), (3, 2), (4, 3), (5, 3),
(2, 4), (3, 4), (4, 5), (1, 5),
-- Khoa 2: Tim mạch (BS 6-10, TC 6-10)
(6, 6), (7, 6), (8, 7), (9, 7), (6, 8), (10, 8),
(7, 9), (9, 9), (8, 10), (10, 10),
-- Khoa 3: Nhi khoa (BS 11-15, TC 11-15)
(11, 11), (12, 11), (13, 12), (14, 12), (11, 13), (15, 13),
(12, 14), (14, 14), (13, 15), (15, 15),
-- Khoa 4: Tai Mũi Họng (BS 16-20, TC 16-20)
(16, 16), (18, 16), (17, 17), (19, 17), (16, 18), (20, 18),
(17, 19), (18, 19), (19, 20), (20, 20),
-- Khoa 5: Da liễu (BS 21-25, TC 21-25)
(21, 21), (22, 21), (23, 22), (24, 22), (21, 23), (25, 23),
(22, 24), (24, 24), (23, 25), (25, 25),
-- Khoa 6: Xương khớp (BS 26-30, TC 26-30)
(26, 26), (27, 26), (28, 27), (30, 27), (26, 28), (29, 28),
(27, 29), (28, 29), (29, 30), (30, 30),
-- Khoa 7: Tiêu hóa (BS 31-35, TC 31-35)
(31, 31), (32, 31), (33, 32), (34, 32), (31, 33), (35, 33),
(32, 34), (34, 34), (33, 35), (35, 35),
-- Khoa 8: Mắt (BS 36-40, TC 36-40)
(36, 36), (37, 36), (38, 37), (39, 37), (36, 38), (40, 38),
(37, 39), (38, 39), (39, 40), (40, 40),
-- Khoa 9: Sản phụ khoa (BS 41-45, TC 41-45)
(41, 41), (42, 41), (43, 42), (44, 42), (41, 43), (45, 43),
(42, 44), (43, 44), (44, 45), (45, 45),
-- Khoa 10: Hô hấp (BS 46-50, TC 46-50)
(46, 46), (47, 46), (48, 47), (49, 47), (46, 48), (50, 48),
(47, 49), (48, 49), (49, 50), (50, 50);
GO

-- ============================================================
-- 9. LỊCH LÀM VIỆC MẪU (3 ngày tới cho tất cả bác sĩ)
-- ============================================================
INSERT INTO lich_lam_viec (bac_si_id, ngay_kham, khung_gio, con_trong)
SELECT id, CAST(DATEADD(day, 1, GETDATE()) AS DATE), N'08:00 - 09:00', 1 FROM bac_si
UNION ALL
SELECT id, CAST(DATEADD(day, 1, GETDATE()) AS DATE), N'09:00 - 10:00', 1 FROM bac_si
UNION ALL
SELECT id, CAST(DATEADD(day, 1, GETDATE()) AS DATE), N'14:00 - 15:00', 1 FROM bac_si
UNION ALL
SELECT id, CAST(DATEADD(day, 2, GETDATE()) AS DATE), N'08:00 - 09:00', 1 FROM bac_si
UNION ALL
SELECT id, CAST(DATEADD(day, 2, GETDATE()) AS DATE), N'10:00 - 11:00', 1 FROM bac_si
UNION ALL
SELECT id, CAST(DATEADD(day, 3, GETDATE()) AS DATE), N'14:00 - 15:00', 1 FROM bac_si;
GO

PRINT N'✅ Seed dữ liệu MedBooking thành công!';
PRINT N'   - 10 chuyên khoa';
PRINT N'   - 62 người dùng (2 admin + 7 lễ tân + 50 bác sĩ + 3 bệnh nhân)';
PRINT N'   - 2 tài khoản admin (bảng admin)';
PRINT N'   - 50 bác sĩ';
PRINT N'   - 10 dịch vụ';
PRINT N'   - 50 triệu chứng';
PRINT N'   - 100 mapping triệu chứng - bác sĩ';
PRINT N'   - 300 lịch làm việc mẫu (50 BS × 6 ca)';
GO
