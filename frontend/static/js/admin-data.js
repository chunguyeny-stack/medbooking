/* ============================================================
   MEDBOOKING — Mock Data Layer (v7 - Lock Reason Sync)
   ============================================================ */
(function (global) {
    'use strict';

    const STORAGE_KEY = 'medbooking_admin_db';
    const REVIEWS_KEY = 'medbooking_doctor_reviews';

    // --- HÀM HỖ TRỢ NGÀY THÁNG ---
    function getTodayStr() {
        const d = new Date();
        return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
    }

    function getOffsetDateStr(offset) {
        const d = new Date();
        d.setDate(d.getDate() + offset);
        return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
    }

    function getOffsetDateTimeStr(offset, timeStr = '10:00') {
        return `${getOffsetDateStr(offset)} ${timeStr}`;
    }

    // --- SCHEDULE MẪU DÙNG CHUNG ---
    function defaultSchedule() {
        return [
            { day: 'Thứ Hai',  morning: true,  afternoon: true  },
            { day: 'Thứ Ba',   morning: true,  afternoon: false },
            { day: 'Thứ Tư',   morning: true,  afternoon: true  },
            { day: 'Thứ Năm',  morning: false, afternoon: true  },
            { day: 'Thứ Sáu',  morning: true,  afternoon: true  },
            { day: 'Thứ Bảy',  morning: true,  afternoon: false }
        ];
    }

    // ============================================================
    // SEED DATA
    // ============================================================
    const seedData = {
        accounts: [
            { id: 'TK001', name: 'Nguyễn Văn A', email: 'admin@medbooking.com', phone: '0901234567', role: 'admin', status: 'active', createdAt: getOffsetDateStr(-100) },
            { id: 'TK002', name: 'Trần Thị B', email: 'bacsi.b@medbooking.com', phone: '0912345678', role: 'doctor', status: 'active', createdAt: getOffsetDateStr(-80) },
            { id: 'TK003', name: 'Lê Văn C', email: 'letan.c@medbooking.com', phone: '0923456789', role: 'receptionist', status: 'active', createdAt: getOffsetDateStr(-60) },
            { id: 'TK004', name: 'Phạm Thị D', email: 'benhnhan.d@gmail.com', phone: '0934567890', role: 'patient', status: 'active', createdAt: getOffsetDateStr(-40) },
            {
                id: 'TK005',
                name: 'Hoàng Văn E',
                email: 'bacsi.e@medbooking.com',
                phone: '0945678901',
                role: 'doctor',
                status: 'locked',
                lockReason: 'Tài khoản bị khóa do vi phạm điều khoản sử dụng: cung cấp thông tin chuyên môn không chính xác.',
                createdAt: getOffsetDateStr(-30)
            },
            { id: 'TK006', name: 'Vũ Thị F', email: 'benhnhan.f@gmail.com', phone: '0956789012', role: 'patient', status: 'active', createdAt: getOffsetDateStr(-20) },
            { id: 'TK007', name: 'Đặng Văn G', email: 'letan.g@medbooking.com', phone: '0967890123', role: 'receptionist', status: 'active', createdAt: getOffsetDateStr(-10) },
            { id: 'TK008', name: 'Bùi Thị H', email: 'bacsi.h@medbooking.com', phone: '0978901234', role: 'doctor', status: 'active', createdAt: getOffsetDateStr(-5) }
        ],
        specialties: [
            { id: 'CK001', name: 'Tim mạch', desc: 'Khám và điều trị các bệnh về tim mạch, huyết áp', doctorCount: 3 },
            { id: 'CK002', name: 'Nha khoa', desc: 'Khám, điều trị răng miệng, nhổ răng, trồng răng implant', doctorCount: 2 },
            { id: 'CK003', name: 'Mắt', desc: 'Khám và điều trị các bệnh về mắt, đo thị lực', doctorCount: 2 },
            { id: 'CK004', name: 'Nội tổng quát', desc: 'Khám tổng quát, tầm soát sức khỏe định kỳ', doctorCount: 4 },
            { id: 'CK005', name: 'Da liễu', desc: 'Khám và điều trị các bệnh về da, thẩm mỹ da', doctorCount: 2 },
            { id: 'CK006', name: 'Tai Mũi Họng', desc: 'Khám và điều trị các bệnh về tai mũi họng', doctorCount: 3 }
        ],
        doctors: [
            {
                id: 'BS001', name: 'BS. Nguyễn Văn A', specialtyId: 'CK001', specialtyName: 'Tim mạch',
                email: 'bacsi.a@medbooking.com', phone: '0901111111',
                status: 'available', rating: 4.9,
                degree: 'Thạc sĩ - Bác sĩ nội trú',
                experience: 12,
                avatar: 'https://images.unsplash.com/photo-1612349317150-e413f6a5b16d?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80',
                bio: 'ThS.BS Nguyễn Văn A là chuyên gia hàng đầu trong lĩnh vực Tim mạch với hơn 12 năm kinh nghiệm công tác tại các bệnh viện lớn trên địa bàn Hà Nội.',
                training: 'Tốt nghiệp Bác sĩ Đa khoa và Thạc sĩ Y học tại Trường Đại học Y Hà Nội.',
                workHistory: 'Từng công tác tại Khoa Tim mạch - Bệnh viện Bạch Mai hơn 10 năm.',
                strengths: 'Chẩn đoán và điều trị các bệnh lý tim mạch, tăng huyết áp, suy tim, rối loạn nhịp tim.',
                fee: 300000,
                patientCount: 5000,
                schedule: defaultSchedule()
            },
            {
                id: 'BS002', name: 'BS. Trần Thị B', specialtyId: 'CK002', specialtyName: 'Nha khoa',
                email: 'bacsi.b@medbooking.com', phone: '0902222222',
                status: 'available', rating: 4.8,
                degree: 'Bác sĩ Chuyên khoa I',
                experience: 10,
                avatar: 'https://images.unsplash.com/photo-1594824476967-48c8b964273f?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80',
                bio: 'BS.CKI Trần Thị B là bác sĩ chuyên khoa Nha khoa với hơn 10 năm kinh nghiệm.',
                training: 'Tốt nghiệp Bác sĩ Đa khoa và Chuyên khoa I Nha khoa tại Đại học Y Dược TP.HCM.',
                workHistory: 'Nguyên bác sĩ Khoa Răng Hàm Mặt - Bệnh viện Chợ Rẫy.',
                strengths: 'Nhổ răng khôn, trồng răng implant, điều trị nha chu, thẩm mỹ răng.',
                fee: 350000,
                patientCount: 3200,
                schedule: defaultSchedule()
            },
            {
                id: 'BS003', name: 'BS. Lê Văn C', specialtyId: 'CK001', specialtyName: 'Tim mạch',
                email: 'bacsi.c@medbooking.com', phone: '0903333333',
                status: 'available', rating: 4.7,
                degree: 'Tiến sĩ - Bác sĩ',
                experience: 15,
                avatar: 'https://images.unsplash.com/photo-1622253692010-333f2da6031d?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80',
                bio: 'TS.BS Lê Văn C là Tiến sĩ Y học chuyên ngành Tim mạch với hơn 15 năm kinh nghiệm.',
                training: 'Tiến sĩ Y học tại Đại học Y Hà Nội, tu nghiệp tại Pháp.',
                workHistory: 'Trưởng khoa Tim mạch - Bệnh viện Việt Đức.',
                strengths: 'Can thiệp tim mạch, đặt stent mạch vành, điều trị suy tim nặng.',
                fee: 500000,
                patientCount: 6800,
                schedule: defaultSchedule()
            },
            {
                id: 'BS004', name: 'BS. Phạm Thị D', specialtyId: 'CK003', specialtyName: 'Mắt',
                email: 'bacsi.d@medbooking.com', phone: '0904444444',
                status: 'available', rating: 4.9,
                degree: 'Bác sĩ Chuyên khoa II',
                experience: 14,
                avatar: 'https://images.unsplash.com/photo-1559839734-2b71ea197ec2?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80',
                bio: 'BS.CKII Phạm Thị D là chuyên gia Nhãn khoa với hơn 14 năm kinh nghiệm.',
                training: 'Bác sĩ Chuyên khoa II Nhãn khoa tại Đại học Y Hà Nội.',
                workHistory: 'Nguyên bác sĩ Khoa Mắt - Bệnh viện Mắt Trung ương.',
                strengths: 'Phẫu thuật Phaco, điều trị glaucoma, khô mắt, tật khúc xạ.',
                fee: 320000,
                patientCount: 4100,
                schedule: defaultSchedule()
            },
            {
                id: 'BS005', name: 'BS. Hoàng Văn E', specialtyId: 'CK004', specialtyName: 'Nội tổng quát',
                email: 'bacsi.e@medbooking.com', phone: '0905555555',
                status: 'off', rating: 4.6,
                degree: 'Bác sĩ Đa khoa',
                experience: 8,
                avatar: 'https://images.unsplash.com/photo-1537368910025-700350fe46c7?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80',
                bio: 'BS. Hoàng Văn E là bác sĩ Nội tổng quát với 8 năm kinh nghiệm.',
                training: 'Tốt nghiệp Bác sĩ Đa khoa tại Đại học Y Hà Nội.',
                workHistory: 'Công tác tại Khoa Nội tổng hợp - Bệnh viện E.',
                strengths: 'Khám tổng quát, tầm soát sức khỏe định kỳ, quản lý bệnh mãn tính.',
                fee: 280000,
                patientCount: 2200,
                schedule: defaultSchedule()
            },
            {
                id: 'BS006', name: 'BS. Vũ Thị F', specialtyId: 'CK005', specialtyName: 'Da liễu',
                email: 'bacsi.f@medbooking.com', phone: '0906666666',
                status: 'available', rating: 4.8,
                degree: 'Thạc sĩ - Bác sĩ',
                experience: 11,
                avatar: 'https://images.unsplash.com/photo-1582750433449-648ed127bb54?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80',
                bio: 'ThS.BS Vũ Thị F là bác sĩ Da liễu với hơn 11 năm kinh nghiệm.',
                training: 'Thạc sĩ Y học tại Đại học Y Dược TP.HCM.',
                workHistory: 'Nguyên bác sĩ Khoa Da liễu - Bệnh viện Da liễu Trung ương.',
                strengths: 'Điều trị mụn trứng cá, nám, sẹo rỗ, thẩm mỹ da bằng laser.',
                fee: 400000,
                patientCount: 3800,
                schedule: defaultSchedule()
            },
            {
                id: 'BS007', name: 'BS. Đặng Văn G', specialtyId: 'CK006', specialtyName: 'Tai Mũi Họng',
                email: 'bacsi.g@medbooking.com', phone: '0907777777',
                status: 'available', rating: 4.5,
                degree: 'Bác sĩ Chuyên khoa I',
                experience: 9,
                avatar: 'https://images.unsplash.com/photo-1612349317150-e413f6a5b16d?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80',
                bio: 'BS.CKI Đặng Văn G là bác sĩ Tai Mũi Họng với 9 năm kinh nghiệm.',
                training: 'Bác sĩ Chuyên khoa I Tai Mũi Họng tại Đại học Y Hà Nội.',
                workHistory: 'Công tác tại Khoa Tai Mũi Họng - Bệnh viện Tai Mũi Họng Trung ương.',
                strengths: 'Nội soi tai mũi họng, điều trị viêm xoang, viêm họng, ù tai.',
                fee: 300000,
                patientCount: 2900,
                schedule: defaultSchedule()
            },
            {
                id: 'BS008', name: 'BS. Bùi Thị H', specialtyId: 'CK004', specialtyName: 'Nội tổng quát',
                email: 'bacsi.h@medbooking.com', phone: '0908888888',
                status: 'available', rating: 4.9,
                degree: 'Tiến sĩ - Bác sĩ',
                experience: 16,
                avatar: 'https://images.unsplash.com/photo-1559839734-2b71ea197ec2?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80',
                bio: 'TS.BS Bùi Thị H là chuyên gia Nội tổng quát với hơn 16 năm kinh nghiệm.',
                training: 'Tiến sĩ Y học tại Đại học Y Hà Nội.',
                workHistory: 'Phó Trưởng khoa Nội tổng hợp - Bệnh viện Bạch Mai.',
                strengths: 'Khám tổng quát nâng cao, quản lý đái tháo đường, tăng huyết áp.',
                fee: 450000,
                patientCount: 5200,
                schedule: defaultSchedule()
            }
        ],
        services: [
            { id: 'DV001', name: 'Khám tim mạch tổng quát', specialtyId: 'CK001', specialtyName: 'Tim mạch', price: 500000, desc: 'Khám, đo huyết áp, điện tim' },
            { id: 'DV002', name: 'Siêu âm tim', specialtyId: 'CK001', specialtyName: 'Tim mạch', price: 650000, desc: 'Siêu âm tim Doppler màu' },
            { id: 'DV003', name: 'Nhổ răng khôn', specialtyId: 'CK002', specialtyName: 'Nha khoa', price: 1200000, desc: 'Nhổ răng khôn có gây tê' },
            { id: 'DV004', name: 'Trám răng', specialtyId: 'CK002', specialtyName: 'Nha khoa', price: 300000, desc: 'Trám răng sâu composite' },
            { id: 'DV005', name: 'Khám mắt tổng quát', specialtyId: 'CK003', specialtyName: 'Mắt', price: 320000, desc: 'Đo thị lực, soi đáy mắt' },
            { id: 'DV006', name: 'Khám tổng quát', specialtyId: 'CK004', specialtyName: 'Nội tổng quát', price: 450000, desc: 'Khám lâm sàng toàn diện' },
            { id: 'DV007', name: 'Xét nghiệm máu', specialtyId: 'CK004', specialtyName: 'Nội tổng quát', price: 280000, desc: 'Tổng phân tích tế bào máu' },
            { id: 'DV008', name: 'Điều trị mụn', specialtyId: 'CK005', specialtyName: 'Da liễu', price: 800000, desc: 'Điều trị mụn chuyên sâu' },
            { id: 'DV009', name: 'Nội soi tai mũi họng', specialtyId: 'CK006', specialtyName: 'Tai Mũi Họng', price: 380000, desc: 'Nội soi ống mềm' }
        ],
        mappings: [
            { id: 'MP001', keywords: 'đau ngực, khó thở, tim đập nhanh', specialtyId: 'CK001', specialtyName: 'Tim mạch', doctorId: 'BS001', doctorName: 'BS. Nguyễn Văn A', priority: 1 },
            { id: 'MP002', keywords: 'đau răng, sưng nướu, ê buốt', specialtyId: 'CK002', specialtyName: 'Nha khoa', doctorId: 'BS002', doctorName: 'BS. Trần Thị B', priority: 2 },
            { id: 'MP003', keywords: 'mờ mắt, đau mắt, chảy nước mắt', specialtyId: 'CK003', specialtyName: 'Mắt', doctorId: 'BS004', doctorName: 'BS. Phạm Thị D', priority: 1 },
            { id: 'MP004', keywords: 'mệt mỏi, chóng mặt, đau đầu', specialtyId: 'CK004', specialtyName: 'Nội tổng quát', doctorId: '', doctorName: '', priority: 3 },
            { id: 'MP005', keywords: 'mụn, ngứa da, nổi mẩn', specialtyId: 'CK005', specialtyName: 'Da liễu', doctorId: 'BS006', doctorName: 'BS. Vũ Thị F', priority: 2 }
        ],
        recycleBin: [
            { id: 'BS992', type: 'Bác sĩ', name: 'BS. Lê Văn Xóa', deletedAt: getOffsetDateTimeStr(-1, '08:00') },
            { id: 'TK899', type: 'Tài khoản', name: 'Nguyễn Thị Xóa', deletedAt: getOffsetDateTimeStr(-1, '14:30') },
            { id: 'CK880', type: 'Chuyên khoa', name: 'Chuyên khoa cũ', deletedAt: getOffsetDateTimeStr(0, '09:15') },
            { id: 'DV770', type: 'Dịch vụ', name: 'Dịch vụ khai trương', deletedAt: getOffsetDateTimeStr(0, '11:00') }
        ],
        transactions: [
            { id: 'GD001', date: getOffsetDateStr(0), patient: 'Nguyễn Văn A', revenue: 450000, profit: 180000, doctorConfirm: 'BS. Nguyễn Văn A', receptionConfirm: 'Lễ tân C', updatedAt: getOffsetDateTimeStr(0, '10:42'), status: 'completed' },
            { id: 'GD002', date: getOffsetDateStr(0), patient: 'Trần Thị B', revenue: 1200000, profit: 500000, doctorConfirm: 'BS. Trần Thị B', receptionConfirm: 'Lễ tân G', updatedAt: getOffsetDateTimeStr(0, '09:21'), status: 'completed' },
            { id: 'GD003', date: getOffsetDateStr(0), patient: 'Lê Văn C', revenue: 650000, profit: 250000, doctorConfirm: 'BS. Lê Văn C', receptionConfirm: 'Lễ tân C', updatedAt: getOffsetDateTimeStr(0, '08:15'), status: 'completed' },
            { id: 'GD004', date: getOffsetDateStr(-1), patient: 'Phạm Thị D', revenue: 320000, profit: 120000, doctorConfirm: 'BS. Phạm Thị D', receptionConfirm: 'Lễ tân G', updatedAt: getOffsetDateTimeStr(-1, '16:20'), status: 'completed' },
            { id: 'GD005', date: getOffsetDateStr(-1), patient: 'Hoàng Văn E', revenue: 500000, profit: 0, doctorConfirm: '', receptionConfirm: '', updatedAt: getOffsetDateTimeStr(-1, '15:00'), status: 'cancelled' },
            { id: 'GD006', date: getOffsetDateStr(-2), patient: 'Vũ Thị F', revenue: 800000, profit: 320000, doctorConfirm: 'BS. Vũ Thị F', receptionConfirm: 'Lễ tân C', updatedAt: getOffsetDateTimeStr(-2, '14:30'), status: 'completed' },
            { id: 'GD007', date: getOffsetDateStr(-2), patient: 'Đặng Văn G', revenue: 380000, profit: 140000, doctorConfirm: 'BS. Đặng Văn G', receptionConfirm: 'Lễ tân G', updatedAt: getOffsetDateTimeStr(-2, '11:15'), status: 'completed' },
            { id: 'GD008', date: getOffsetDateStr(-3), patient: 'Bùi Thị H', revenue: 280000, profit: 100000, doctorConfirm: 'BS. Bùi Thị H', receptionConfirm: 'Lễ tân C', updatedAt: getOffsetDateTimeStr(-3, '10:00'), status: 'completed' }
        ],
        notifications: [
            { id: 'N001', title: 'Lịch hẹn mới', message: 'Bệnh nhân Nguyễn Văn A vừa đặt lịch khám Tim mạch', time: '5 phút trước', read: false },
            { id: 'N002', title: 'Thanh toán thành công', message: 'Giao dịch GD002 đã hoàn tất 1.200.000₫', time: '1 giờ trước', read: false },
            { id: 'N003', title: 'Cảnh báo hệ thống', message: 'Có 3 bản ghi trong thùng rác cần xử lý', time: '2 giờ trước', read: false },
            { id: 'N004', title: 'Đánh giá mới', message: 'BS. Phạm Thị D vừa nhận đánh giá 5 sao', time: '1 ngày trước', read: true }
        ],
        currentUser: {
            id: 'AD001',
            name: 'Nguyễn Văn Quản Trị',
            email: 'admin@medbooking.vn',
            avatar: 'A'
        }
    };

    // ============================================================
    // SEED REVIEWS
    // ============================================================
    const seedReviews = [
        { id: 'RV001', doctorId: 'BS001', patientName: 'Nguyễn Thị B', rating: 5, comment: 'Bác sĩ A rất tận tâm, nhẹ nhàng và giải thích chi tiết cho bệnh nhân.', date: '2026-09-10' },
        { id: 'RV002', doctorId: 'BS001', patientName: 'Trần Văn H', rating: 5, comment: 'Dịch vụ đặt lịch rất nhanh chóng, đến nơi được khám đúng giờ.', date: '2026-08-25' },
        { id: 'RV003', doctorId: 'BS002', patientName: 'Lê Thị D', rating: 5, comment: 'Bác sĩ C rất chuyên nghiệp, giải thích cặn kẽ, nhổ răng không đau.', date: '2026-09-15' },
        { id: 'RV004', doctorId: 'BS002', patientName: 'Phạm Văn K', rating: 4, comment: 'Bác sĩ giỏi nhưng phòng khám hơi đông, phải chờ lâu.', date: '2026-08-20' },
        { id: 'RV005', doctorId: 'BS003', patientName: 'Hoàng Thị M', rating: 5, comment: 'Bác sĩ C rất giỏi về tim mạch, chẩn đoán chính xác.', date: '2026-09-20' },
        { id: 'RV006', doctorId: 'BS004', patientName: 'Vũ Đức P', rating: 5, comment: 'Bác sĩ D khám mắt rất kỹ, tư vấn tận tình.', date: '2026-09-05' },
        { id: 'RV007', doctorId: 'BS006', patientName: 'Đỗ Thị N', rating: 5, comment: 'Bác sĩ F điều trị mụn cho tôi rất hiệu quả, da đẹp hơn hẳn.', date: '2026-09-18' },
        { id: 'RV008', doctorId: 'BS008', patientName: 'Ngô Văn T', rating: 5, comment: 'Bác sĩ H rất giỏi, tư vấn kỹ về sức khỏe tổng quát.', date: '2026-09-12' }
    ];

    // ============================================================
    // LOAD/SAVE
    // ============================================================
    function loadDB() {
        try {
            const raw = localStorage.getItem(STORAGE_KEY);
            if (!raw) {
                localStorage.setItem(STORAGE_KEY, JSON.stringify(seedData));
                return JSON.parse(JSON.stringify(seedData));
            }
            const db = JSON.parse(raw);
            let changed = false;
            for (const k of Object.keys(seedData)) {
                if (!db[k]) { db[k] = JSON.parse(JSON.stringify(seedData[k])); changed = true; }
            }
            if (changed) {
                localStorage.setItem(STORAGE_KEY, JSON.stringify(db));
            }
            return db;
        } catch (e) {
            localStorage.setItem(STORAGE_KEY, JSON.stringify(seedData));
            return JSON.parse(JSON.stringify(seedData));
        }
    }

    function saveDB(db) {
        try {
            localStorage.setItem(STORAGE_KEY, JSON.stringify(db));
        } catch (e) {
            console.error('[admin-data.js] Save DB lỗi:', e);
        }
    }

    function loadReviews() {
        try {
            const raw = localStorage.getItem(REVIEWS_KEY);
            if (!raw) {
                localStorage.setItem(REVIEWS_KEY, JSON.stringify(seedReviews));
                return JSON.parse(JSON.stringify(seedReviews));
            }
            return JSON.parse(raw);
        } catch (e) {
            return JSON.parse(JSON.stringify(seedReviews));
        }
    }

    function saveReviews(list) {
        try {
            localStorage.setItem(REVIEWS_KEY, JSON.stringify(list));
        } catch (e) {
            console.error('[admin-data.js] Save Reviews lỗi:', e);
        }
    }

    let DB = loadDB();
    let REVIEWS = loadReviews();

    // ============================================================
    // HELPERS
    // ============================================================
    function nextId(prefix, list) {
        const nums = list.map(item => parseInt((item.id || '').replace(prefix, ''), 10)).filter(n => !isNaN(n));
        const next = (nums.length ? Math.max(...nums) : 0) + 1;
        return prefix + String(next).padStart(3, '0');
    }

    function formatMoney(n) {
        return new Intl.NumberFormat('vi-VN').format(n) + ' ₫';
    }

    function formatDate(iso) {
        if (!iso) return '';
        return new Date(iso).toLocaleDateString('vi-VN');
    }

    function calcAvgRating(doctorId) {
        const revs = REVIEWS.filter(r => r.doctorId === doctorId);
        if (!revs.length) {
            const doc = DB.doctors.find(d => d.id === doctorId);
            return doc ? doc.rating : 5.0;
        }
        return parseFloat((revs.reduce((s, r) => s + r.rating, 0) / revs.length).toFixed(1));
    }

    // ============================================================
    // API
    // ============================================================
    const mockAPI = {
        /* ============ ACCOUNTS ============ */
        getAccounts(filters = {}) {
            let list = [...DB.accounts];
            if (filters.role && filters.role !== 'all') list = list.filter(a => a.role === filters.role);
            if (filters.status && filters.status !== 'all') list = list.filter(a => a.status === filters.status);
            if (filters.search) {
                const q = filters.search.toLowerCase();
                list = list.filter(a =>
                    a.name.toLowerCase().includes(q) ||
                    a.email.toLowerCase().includes(q) ||
                    a.phone.includes(q)
                );
            }
            return Promise.resolve({ data: list, total: list.length });
        },
        createAccount(data) {
            const acc = {
                id: nextId('TK', DB.accounts),
                ...data,
                status: 'active',
                lockReason: '',
                createdAt: getTodayStr()
            };
            DB.accounts.unshift(acc);
            DB.notifications.unshift({
                id: 'N' + String(Date.now()).slice(-6),
                title: 'Tài khoản mới',
                message: `Đã tạo tài khoản "${acc.name}" với vai trò ${acc.role}`,
                time: 'Vừa xong',
                read: false
            });
            saveDB(DB);
            return Promise.resolve({ data: acc });
        },
        updateAccount(id, data) {
            const i = DB.accounts.findIndex(a => a.id === id);
            if (i === -1) return Promise.reject({ message: 'Không tìm thấy' });
            DB.accounts[i] = { ...DB.accounts[i], ...data };
            saveDB(DB);
            return Promise.resolve({ data: DB.accounts[i] });
        },
        deleteAccount(id) {
            const i = DB.accounts.findIndex(a => a.id === id);
            if (i === -1) return Promise.reject({ message: 'Không tìm thấy' });
            const acc = DB.accounts[i];
            DB.accounts.splice(i, 1);
            DB.recycleBin.unshift({
                id: acc.id,
                type: 'Tài khoản',
                name: acc.name,
                deletedAt: new Date().toLocaleString('vi-VN')
            });
            DB.notifications.unshift({
                id: 'N' + String(Date.now()).slice(-6),
                title: 'Cảnh báo hệ thống',
                message: `Tài khoản "${acc.name}" đã được chuyển vào thùng rác`,
                time: 'Vừa xong',
                read: false
            });
            saveDB(DB);
            return Promise.resolve({ data: true });
        },
        /**
         * Khóa / Mở khóa tài khoản.
         * - Khi khóa: bắt buộc truyền `reason` (≥ 5 ký tự)
         * - Khi mở khóa: xóa `lockReason` cũ
         * - Đồng bộ luôn sang medbooking_users (nếu có) để dn.html check
         */
        toggleAccountStatus(id, reason) {
            const acc = DB.accounts.find(a => a.id === id);
            if (!acc) return Promise.reject({ message: 'Không tìm thấy' });

            const willLock = acc.status === 'active';
            const cleanReason = (reason === undefined || reason === null)
                ? ''
                : String(reason).trim();

            if (willLock) {
                if (cleanReason.length < 5) {
                    return Promise.reject({
                        message: 'Lý do khóa phải có ít nhất 5 ký tự'
                    });
                }
                if (cleanReason.length > 300) {
                    return Promise.reject({
                        message: 'Lý do khóa không quá 300 ký tự'
                    });
                }
                acc.status = 'locked';
                acc.lockReason = cleanReason;
                acc.lockedAt = new Date().toISOString();
            } else {
                acc.status = 'active';
                acc.lockReason = '';
                delete acc.lockedAt;
            }

            saveDB(DB);
            syncLockStatusToUsers(acc);
            return Promise.resolve({ data: acc });
        },

        /* ============ DOCTORS ============ */
        getDoctors(filters = {}) {
            let list = [...DB.doctors];
            if (filters.specialtyId && filters.specialtyId !== 'all') list = list.filter(d => d.specialtyId === filters.specialtyId);
            if (filters.search) {
                const q = filters.search.toLowerCase();
                list = list.filter(d => d.name.toLowerCase().includes(q) || d.email.toLowerCase().includes(q));
            }
            list = list.map(d => {
                const revs = REVIEWS.filter(r => r.doctorId === d.id);
                return {
                    ...d,
                    rating: calcAvgRating(d.id),
                    reviewCount: revs.length
                };
            });
            return Promise.resolve({ data: list, total: list.length });
        },
        getDoctorById(id) {
            const d = DB.doctors.find(x => x.id === id);
            if (!d) return Promise.resolve({ data: null });
            const revs = REVIEWS.filter(r => r.doctorId === id).sort((a, b) => b.date.localeCompare(a.date));
            return Promise.resolve({
                data: {
                    ...d,
                    rating: calcAvgRating(id),
                    reviews: revs,
                    reviewCount: revs.length
                }
            });
        },
        createDoctor(data) {
            const spec = DB.specialties.find(s => s.id === data.specialtyId);
            const doc = {
                id: nextId('BS', DB.doctors),
                ...data,
                specialtyName: spec ? spec.name : '',
                status: 'available',
                rating: 5.0,
                degree: data.degree || '',
                experience: data.experience || 0,
                avatar: data.avatar || '',
                bio: data.bio || '',
                training: data.training || '',
                workHistory: data.workHistory || '',
                strengths: data.strengths || '',
                fee: data.fee || 300000,
                patientCount: 0,
                schedule: data.schedule && data.schedule.length ? data.schedule : defaultSchedule()
            };
            DB.doctors.unshift(doc);
            if (spec) spec.doctorCount = (spec.doctorCount || 0) + 1;
            DB.notifications.unshift({
                id: 'N' + String(Date.now()).slice(-6),
                title: 'Bác sĩ mới',
                message: `Đã thêm ${doc.name} vào chuyên khoa ${doc.specialtyName}`,
                time: 'Vừa xong',
                read: false
            });
            saveDB(DB);
            return Promise.resolve({ data: doc });
        },
        updateDoctor(id, data) {
            const i = DB.doctors.findIndex(d => d.id === id);
            if (i === -1) return Promise.reject({ message: 'Không tìm thấy' });
            const spec = DB.specialties.find(s => s.id === data.specialtyId);
            DB.doctors[i] = {
                ...DB.doctors[i],
                ...data,
                specialtyName: spec ? spec.name : DB.doctors[i].specialtyName
            };
            saveDB(DB);
            return Promise.resolve({ data: DB.doctors[i] });
        },
        deleteDoctor(id) {
            const i = DB.doctors.findIndex(d => d.id === id);
            if (i === -1) return Promise.reject({ message: 'Không tìm thấy' });
            const doc = DB.doctors[i];
            DB.doctors.splice(i, 1);
            DB.recycleBin.unshift({
                id: doc.id,
                type: 'Bác sĩ',
                name: doc.name,
                deletedAt: new Date().toLocaleString('vi-VN')
            });
            saveDB(DB);
            return Promise.resolve({ data: true });
        },

        /* ============ REVIEWS ============ */
        getReviewsByDoctor(doctorId) {
            const list = REVIEWS.filter(r => r.doctorId === doctorId).sort((a, b) => b.date.localeCompare(a.date));
            return Promise.resolve({ data: list });
        },
        addReview(data) {
            const doc = DB.doctors.find(d => d.id === data.doctorId);
            const rv = {
                id: 'RV' + String(Date.now()).slice(-6),
                doctorId: data.doctorId,
                patientName: (data.patientName || '').trim() || 'Bệnh nhân ẩn danh',
                rating: Math.max(1, Math.min(5, parseInt(data.rating, 10) || 5)),
                comment: (data.comment || '').trim(),
                date: getTodayStr()
            };
            REVIEWS.unshift(rv);
            saveReviews(REVIEWS);

            if (doc) {
                doc.rating = calcAvgRating(data.doctorId);
                saveDB(DB);
                DB.notifications.unshift({
                    id: 'N' + String(Date.now()).slice(-6),
                    title: 'Đánh giá mới',
                    message: `Bệnh nhân ${rv.patientName} vừa đánh giá ${rv.rating} sao cho bác sĩ ${doc.name}`,
                    time: 'Vừa xong',
                    read: false
                });
                saveDB(DB);
            }
            return Promise.resolve({ data: rv });
        },

        /* ============ SPECIALTIES ============ */
        getSpecialties(filters = {}) {
            let list = [...DB.specialties];
            if (filters.search) {
                const q = filters.search.toLowerCase();
                list = list.filter(s => s.name.toLowerCase().includes(q));
            }
            return Promise.resolve({ data: list, total: list.length });
        },
        createSpecialty(data) {
            const spec = { id: nextId('CK', DB.specialties), ...data, doctorCount: 0 };
            DB.specialties.unshift(spec);
            saveDB(DB);
            return Promise.resolve({ data: spec });
        },
        updateSpecialty(id, data) {
            const i = DB.specialties.findIndex(s => s.id === id);
            if (i === -1) return Promise.reject({ message: 'Không tìm thấy' });
            DB.specialties[i] = { ...DB.specialties[i], ...data };
            saveDB(DB);
            return Promise.resolve({ data: DB.specialties[i] });
        },
        deleteSpecialty(id) {
            const i = DB.specialties.findIndex(s => s.id === id);
            if (i === -1) return Promise.reject({ message: 'Không tìm thấy' });
            const spec = DB.specialties[i];
            DB.specialties.splice(i, 1);
            DB.recycleBin.unshift({
                id: spec.id,
                type: 'Chuyên khoa',
                name: spec.name,
                deletedAt: new Date().toLocaleString('vi-VN')
            });
            saveDB(DB);
            return Promise.resolve({ data: true });
        },

        /* ============ SERVICES ============ */
        getServices(filters = {}) {
            let list = [...DB.services];
            if (filters.specialtyId && filters.specialtyId !== 'all') list = list.filter(s => s.specialtyId === filters.specialtyId);
            if (filters.search) {
                const q = filters.search.toLowerCase();
                list = list.filter(s => s.name.toLowerCase().includes(q) || s.id.toLowerCase().includes(q));
            }
            return Promise.resolve({ data: list, total: list.length });
        },
        createService(data) {
            const spec = DB.specialties.find(s => s.id === data.specialtyId);
            const serv = { id: nextId('DV', DB.services), ...data, specialtyName: spec ? spec.name : '' };
            DB.services.unshift(serv);
            saveDB(DB);
            return Promise.resolve({ data: serv });
        },
        updateService(id, data) {
            const i = DB.services.findIndex(s => s.id === id);
            if (i === -1) return Promise.reject({ message: 'Không tìm thấy' });
            const spec = DB.specialties.find(s => s.id === data.specialtyId);
            DB.services[i] = { ...DB.services[i], ...data, specialtyName: spec ? spec.name : DB.services[i].specialtyName };
            saveDB(DB);
            return Promise.resolve({ data: DB.services[i] });
        },
        deleteService(id) {
            const i = DB.services.findIndex(s => s.id === id);
            if (i === -1) return Promise.reject({ message: 'Không tìm thấy' });
            const serv = DB.services[i];
            DB.services.splice(i, 1);
            DB.recycleBin.unshift({
                id: serv.id,
                type: 'Dịch vụ',
                name: serv.name,
                deletedAt: new Date().toLocaleString('vi-VN')
            });
            saveDB(DB);
            return Promise.resolve({ data: true });
        },

        /* ============ MAPPINGS ============ */
        getMappings(filters = {}) {
            let list = [...DB.mappings];
            if (filters.specialtyId && filters.specialtyId !== 'all') list = list.filter(m => m.specialtyId === filters.specialtyId);
            if (filters.search) {
                const q = filters.search.toLowerCase();
                list = list.filter(m => m.keywords.toLowerCase().includes(q));
            }
            return Promise.resolve({ data: list, total: list.length });
        },
        createMapping(data) {
            const spec = DB.specialties.find(s => s.id === data.specialtyId);
            const doc = data.doctorId ? DB.doctors.find(d => d.id === data.doctorId) : null;
            const map = { id: nextId('MP', DB.mappings), ...data, specialtyName: spec ? spec.name : '', doctorName: doc ? doc.name : '' };
            DB.mappings.unshift(map);
            saveDB(DB);
            return Promise.resolve({ data: map });
        },
        updateMapping(id, data) {
            const i = DB.mappings.findIndex(m => m.id === id);
            if (i === -1) return Promise.reject({ message: 'Không tìm thấy' });
            const spec = DB.specialties.find(s => s.id === data.specialtyId);
            const doc = data.doctorId ? DB.doctors.find(d => d.id === data.doctorId) : null;
            DB.mappings[i] = { ...DB.mappings[i], ...data, specialtyName: spec ? spec.name : '', doctorName: doc ? doc.name : '' };
            saveDB(DB);
            return Promise.resolve({ data: DB.mappings[i] });
        },
        deleteMapping(id) {
            const i = DB.mappings.findIndex(m => m.id === id);
            if (i === -1) return Promise.reject({ message: 'Không tìm thấy' });
            DB.mappings.splice(i, 1);
            saveDB(DB);
            return Promise.resolve({ data: true });
        },

        /* ============ RECYCLE BIN ============ */
        getRecycleBin() { return Promise.resolve({ data: [...DB.recycleBin] }); },
        restoreItem(id) {
            const i = DB.recycleBin.findIndex(r => r.id === id);
            if (i === -1) return Promise.reject({ message: 'Không tìm thấy' });
            const item = DB.recycleBin[i];
            DB.recycleBin.splice(i, 1);
            DB.notifications.unshift({
                id: 'N' + String(Date.now()).slice(-6),
                title: 'Khôi phục thành công',
                message: `Đã khôi phục "${item.name}" (${item.type})`,
                time: 'Vừa xong',
                read: false
            });
            saveDB(DB);
            return Promise.resolve({ data: true });
        },
        deleteItemForever(id) {
            const i = DB.recycleBin.findIndex(r => r.id === id);
            if (i === -1) return Promise.reject({ message: 'Không tìm thấy' });
            DB.recycleBin.splice(i, 1);
            saveDB(DB);
            return Promise.resolve({ data: true });
        },
        emptyRecycleBin() {
            DB.recycleBin = [];
            saveDB(DB);
            return Promise.resolve({ data: true });
        },

        /* ============ TRANSACTIONS ============ */
        getTransactions(filters = {}) {
            let list = [...DB.transactions];
            if (filters.year) list = list.filter(t => t.date.startsWith(filters.year));
            if (filters.month && filters.month !== 'all') {
                list = list.filter(t => parseInt(t.date.split('-')[1], 10) === parseInt(filters.month, 10));
            }
            if (filters.status && filters.status !== 'all') list = list.filter(t => t.status === filters.status);
            return Promise.resolve({ data: list, total: list.length });
        },

        /* ============ DASHBOARD ============ */
        getDashboardStats(year, quarter) {
            let list = [...DB.transactions];
            if (year) list = list.filter(t => t.date.startsWith(String(year)));
            if (quarter && quarter !== 'all') {
                const q = parseInt(quarter.replace('Q', ''), 10);
                const from = (q - 1) * 3 + 1, to = from + 2;
                list = list.filter(t => {
                    const m = parseInt(t.date.split('-')[1], 10);
                    return m >= from && m <= to;
                });
            }
            const totalAppointments = list.length;
            const totalRevenue = list.filter(t => t.status === 'completed').reduce((s, t) => s + t.revenue, 0);
            const totalProfit = list.filter(t => t.status === 'completed').reduce((s, t) => s + t.profit, 0);
            const cancelled = list.filter(t => t.status === 'cancelled').length;
            const cancelRate = totalAppointments ? ((cancelled / totalAppointments) * 100).toFixed(1) : 0;
            const topDoctor = [...DB.doctors].sort((a, b) => b.rating - a.rating)[0];

            const daysOfWeek = ['T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'CN'];
            const revenueByMonth = daysOfWeek.map((label) => ({
                label,
                value: Math.floor(Math.random() * 30) + 10,
                prev: Math.floor(Math.random() * 20) + 5
            }));

            return Promise.resolve({
                data: {
                    totalAppointments, totalRevenue, totalProfit, cancelRate,
                    topDoctor: topDoctor ? { name: topDoctor.name, rating: topDoctor.rating } : null,
                    revenueByMonth
                }
            });
        },

        /* ============ NOTIFICATIONS ============ */
        getNotifications() { return Promise.resolve({ data: [...DB.notifications] }); },
        markAllRead() {
            DB.notifications.forEach(n => n.read = true);
            saveDB(DB);
            return Promise.resolve({ data: true });
        },
        pushNotification(notif) {
            const newNotif = {
                id: 'N' + String(Date.now()).slice(-6),
                title: notif.title || 'Thông báo mới',
                message: notif.message || '',
                time: 'Vừa xong',
                read: false
            };
            DB.notifications.unshift(newNotif);
            if (DB.notifications.length > 20) DB.notifications = DB.notifications.slice(0, 20);
            saveDB(DB);
            return Promise.resolve({ data: newNotif });
        },

        /* ============ CURRENT USER ============ */
        getCurrentUser() { return Promise.resolve({ data: { ...DB.currentUser } }); },
        updateCurrentUser(data) {
            DB.currentUser = { ...DB.currentUser, ...data };
            saveDB(DB);
            return Promise.resolve({ data: DB.currentUser });
        },

        /* ============ RESET ============ */
        resetAll() {
            localStorage.removeItem(STORAGE_KEY);
            localStorage.removeItem(REVIEWS_KEY);
            DB = loadDB();
            REVIEWS = loadReviews();
            return Promise.resolve({ data: true });
        }
    };

    // ============================================================
    // ĐỒNG BỘ TRẠNG THÁI KHÓA SANG medbooking_users
    // (để dn.html có thể đọc lý do khóa)
    // ============================================================
    function syncLockStatusToUsers(adminAcc) {
        try {
            const USERS_KEY = 'medbooking_users';
            let users = JSON.parse(localStorage.getItem(USERS_KEY)) || [];
            const idx = users.findIndex(u => u.email === adminAcc.email);
            if (idx === -1) return; // Không có user bên kho dk.html -> bỏ qua

            if (adminAcc.status === 'locked') {
                users[idx].status = 'locked';
                users[idx].lockReason = adminAcc.lockReason || 'Không có lý do cụ thể';
                users[idx].lockedAt = adminAcc.lockedAt || new Date().toISOString();
            } else {
                users[idx].status = 'active';
                delete users[idx].lockReason;
                delete users[idx].lockedAt;
            }
            localStorage.setItem(USERS_KEY, JSON.stringify(users));
        } catch (e) {
            console.warn('[admin-data.js] Không đồng bộ được lock status:', e);
        }
    }

    global.MedBookingAPI = mockAPI;
    global.MedBookingUtils = { formatMoney, formatDate };
    console.log('[admin-data.js] ✅ Đã export MedBookingAPI (v7 - Lock Reason Sync)');

})(window);