/**
 * LT_Store.js - Lễ Tân Store (Realtime) - BẢN TEST CỐ ĐỊNH NGÀY 02/11/2026
 * Prefix: medbooking_
 * Mốc dữ liệu: 02/11/2026 (cố định để test luôn đúng)
 */

(function () {
    'use strict';

    const PREFIX = 'medbooking_';

    const KEYS = {
        APPOINTMENTS: PREFIX + 'appointments',
        PAYMENTS: PREFIX + 'payments',
        CHECKINS: PREFIX + 'checkins',
        INITIALIZED: PREFIX + 'initialized'
    };

    const STATUS = {
        WAITING: 'waiting',
        PENDING: 'pending',
        CONFIRMED: 'confirmed',
        CHECKED: 'checked',
        NOSHOW: 'noshow',
        CANCELLED: 'cancelled'
    };

    const STATUS_LABEL = {
        waiting: 'Chờ xác nhận',
        pending: 'Chờ khám',
        confirmed: 'Đã xác nhận',
        checked: 'Đã check-in',
        noshow: 'Không đến',
        cancelled: 'Đã hủy'
    };

    // ====== MỐC NGÀY CỐ ĐỊNH ĐỂ TEST ======
    const TEST_TODAY = new Date(2026, 10, 2); // 02/11/2026 (tháng 10 = November)

    function formatDate(date) {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    }

    function todayStr() {
        return formatDate(TEST_TODAY);
    }

    // Trả về ngày lệch N ngày so với MỐC TEST 02/11/2026
    function offsetDateStr(offset) {
        const date = new Date(TEST_TODAY.getTime());
        date.setHours(0, 0, 0, 0);
        date.setDate(date.getDate() + offset);
        return formatDate(date);
    }

    function readJSON(key, fallback) {
        try {
            const raw = localStorage.getItem(key);
            if (!raw) return fallback;
            return JSON.parse(raw);
        } catch (error) {
            console.error('LT_Store read error:', key, error);
            return fallback;
        }
    }

    function writeJSON(key, value) {
        try {
            localStorage.setItem(key, JSON.stringify(value));
            return true;
        } catch (error) {
            console.error('LT_Store write error:', key, error);
            return false;
        }
    }

    function makeQueueNo(index) {
        return 'STT' + String(index).padStart(3, '0');
    }

    // Helper tạo nhanh bệnh nhân với giá trị mặc định
    function mk(o) {
        const nowIso = new Date().toISOString();
        return Object.assign({
            email: '', gender: 'male', dob: '1990-01-01', cccd: '',
            address: 'TP.HCM', insuranceCode: '', insuranceExpiry: '',
            occupation: '', emergencyContactName: '', emergencyContactPhone: '',
            emergencyRelationship: '', medicalHistory: 'Không', allergies: 'Không',
            notes: '', channel: 'app', priority: 'normal',
            status: STATUS.WAITING, items: [],
            createdAt: nowIso, updatedAt: nowIso
        }, o);
    }

    function seedAppointments() {
        const d_today     = offsetDateStr(0);   // 2026-11-02
        const d_tomorrow  = offsetDateStr(1);   // 2026-11-03
        const d_yesterday = offsetDateStr(-1);  // 2026-11-01
        const d_2ago      = offsetDateStr(-2);  // 2026-10-31
        const d_3ago      = offsetDateStr(-3);  // 2026-10-30

        return [
            // ================= HÔM NAY 02/11/2026 — 18 CA =================
            // ---- CA SÁNG (07:30 - 11:30) ----
            mk({ id:'LH201', patientName:'Nguyễn Văn An', patientId:'BN101', phone:'0901000001',
                gender:'male', dob:'1985-03-12', cccd:'001085003456',
                queueNo: makeQueueNo(1), doctor:'ThS.BS Nguyễn Văn A', doctorId:'bs01',
                specialty:'Tim mạch', ca:'sang', time:'07:30-08:30', date:d_today,
                symptom:'Đau ngực khi vận động', status: STATUS.WAITING, priority:'high',
                items:[{name:'Phí khám Tim mạch',qty:1,price:200000},
                       {name:'Điện tâm đồ (ECG)',qty:1,price:150000}] }),

            mk({ id:'LH202', patientName:'Trần Thị Bích', patientId:'BN102', phone:'0901000002',
                gender:'female', dob:'1992-07-25', cccd:'079192007890',
                queueNo: makeQueueNo(2), doctor:'BS.CKI Trần Thị C', doctorId:'bs02',
                specialty:'Nội tổng quát', ca:'sang', time:'08:00-09:00', date:d_today,
                symptom:'Sốt cao 3 ngày', status: STATUS.CONFIRMED, priority:'normal',
                allergies:'Penicillin', notes:'Dị ứng Penicillin',
                items:[{name:'Phí khám Nội tổng quát',qty:1,price:180000},
                       {name:'Xét nghiệm máu',qty:1,price:250000}] }),

            mk({ id:'LH203', patientName:'Lê Thị Mai', patientId:'BN103', phone:'0901000003',
                gender:'female', dob:'1978-11-02', cccd:'001178002345',
                queueNo: makeQueueNo(3), doctor:'BS.CKI Trần Thị C', doctorId:'bs02',
                specialty:'Nội tổng quát', ca:'sang', time:'08:30-09:30', date:d_today,
                symptom:'Đau bụng, buồn nôn', status: STATUS.CHECKED, priority:'normal',
                items:[{name:'Phí khám Nội tổng quát',qty:1,price:180000},
                       {name:'Siêu âm bụng',qty:1,price:300000}] }),

            mk({ id:'LH204', patientName:'Phạm Văn Khoa', patientId:'BN104', phone:'0901000004',
                gender:'male', dob:'1969-05-19', cccd:'001069009876',
                queueNo: makeQueueNo(4), doctor:'ThS.BS Nguyễn Văn A', doctorId:'bs01',
                specialty:'Tim mạch', ca:'sang', time:'09:00-10:00', date:d_today,
                symptom:'Tăng huyết áp tái khám', status: STATUS.CHECKED, priority:'urgent',
                medicalHistory:'Tăng huyết áp',
                items:[{name:'Phí khám Tim mạch',qty:1,price:200000}] }),

            mk({ id:'LH205', patientName:'Hoàng Thị Ngọc', patientId:'BN105', phone:'0901000005',
                gender:'female', dob:'1980-12-30', cccd:'001180006677',
                queueNo: makeQueueNo(5), doctor:'ThS.BS Nguyễn Văn A', doctorId:'bs01',
                specialty:'Tim mạch', ca:'sang', time:'09:30-10:30', date:d_today,
                symptom:'Tái khám định kỳ', status: STATUS.PENDING, priority:'normal',
                channel:'hotline',
                items:[{name:'Phí khám Tim mạch',qty:1,price:200000}] }),

            mk({ id:'LH206', patientName:'Vũ Đức Phong', patientId:'BN106', phone:'0901000006',
                gender:'male', dob:'1998-02-14', cccd:'001098001122',
                queueNo: makeQueueNo(6), doctor:'BS.CKI Trần Thị C', doctorId:'bs02',
                specialty:'Nội tổng quát', ca:'sang', time:'10:00-11:00', date:d_today,
                symptom:'Ho khan, đau họng', status: STATUS.WAITING, priority:'normal',
                channel:'walk-in',
                items:[{name:'Phí khám Nội tổng quát',qty:1,price:180000},
                       {name:'Test Covid',qty:1,price:100000}] }),

            mk({ id:'LH207', patientName:'Đỗ Minh Anh', patientId:'BN107', phone:'0901000007',
                gender:'female', dob:'1990-09-09', cccd:'079190003344',
                queueNo: makeQueueNo(7), doctor:'TS.BS Lê Hoàng D', doctorId:'bs03',
                specialty:'Thần kinh', ca:'sang', time:'10:30-11:30', date:d_today,
                symptom:'Đau nửa đầu', status: STATUS.CONFIRMED, priority:'high',
                items:[{name:'Phí khám Thần kinh',qty:1,price:250000}] }),

            // ---- CA CHIỀU (13:30 - 17:30) ----
            mk({ id:'LH208', patientName:'Ngô Văn Tú', patientId:'BN108', phone:'0901000008',
                gender:'male', dob:'1960-08-08', cccd:'001060008899',
                queueNo: makeQueueNo(8), doctor:'ThS.BS Nguyễn Văn A', doctorId:'bs01',
                specialty:'Tim mạch', ca:'chieu', time:'13:30-14:30', date:d_today,
                symptom:'Huyết áp cao, đau ngực nhẹ', status: STATUS.CHECKED, priority:'urgent',
                allergies:'Aspirin', notes:'Dị ứng Aspirin',
                items:[{name:'Phí khám Tim mạch',qty:1,price:200000}] }),

            mk({ id:'LH209', patientName:'Lý Thị Mai', patientId:'BN109', phone:'0901000009',
                gender:'female', dob:'1995-10-10', cccd:'079195007766',
                queueNo: makeQueueNo(9), doctor:'BS.CKI Trần Thị C', doctorId:'bs02',
                specialty:'Nội tổng quát', ca:'chieu', time:'14:00-15:00', date:d_today,
                symptom:'Đau dạ dày, ợ nóng', status: STATUS.WAITING, priority:'normal',
                items:[{name:'Phí khám Nội tổng quát',qty:1,price:180000},
                       {name:'Siêu âm bụng',qty:1,price:300000}] }),

            mk({ id:'LH210', patientName:'Đinh Công Sơn', patientId:'BN110', phone:'0901000010',
                gender:'male', dob:'1983-03-03', cccd:'001083005544',
                queueNo: makeQueueNo(10), doctor:'TS.BS Lê Hoàng D', doctorId:'bs03',
                specialty:'Thần kinh', ca:'chieu', time:'14:30-15:30', date:d_today,
                symptom:'Mất ngủ kéo dài', status: STATUS.CONFIRMED, priority:'normal',
                items:[{name:'Phí khám Thần kinh',qty:1,price:250000}] }),

            mk({ id:'LH211', patientName:'Bùi Thị Hồng', patientId:'BN111', phone:'0901000011',
                gender:'female', dob:'1975-04-22', cccd:'001175004455',
                queueNo: makeQueueNo(11), doctor:'BS.CKI Trần Thị C', doctorId:'bs02',
                specialty:'Nội tổng quát', ca:'chieu', time:'15:00-16:00', date:d_today,
                symptom:'Mệt mỏi, chán ăn', status: STATUS.PENDING, priority:'normal',
                channel:'hotline',
                items:[{name:'Phí khám Nội tổng quát',qty:1,price:180000},
                       {name:'Xét nghiệm máu',qty:1,price:250000}] }),

            mk({ id:'LH212', patientName:'Trần Quốc Bảo', patientId:'BN112', phone:'0901000012',
                gender:'male', dob:'1987-01-01', cccd:'079187002233',
                queueNo: makeQueueNo(12), doctor:'TS.BS Lê Hoàng D', doctorId:'bs03',
                specialty:'Thần kinh', ca:'chieu', time:'15:30-16:30', date:d_today,
                symptom:'Đau đầu, chóng mặt', status: STATUS.WAITING, priority:'high',
                items:[{name:'Phí khám Thần kinh',qty:1,price:250000}] }),

            mk({ id:'LH213', patientName:'Nguyễn Thu Hà', patientId:'BN113', phone:'0901000013',
                gender:'female', dob:'2001-06-18', cccd:'001101001188',
                queueNo: makeQueueNo(13), doctor:'BS.CKI Trần Thị C', doctorId:'bs02',
                specialty:'Nội tổng quát', ca:'chieu', time:'16:00-17:00', date:d_today,
                symptom:'Đau họng, ho nhẹ', status: STATUS.CANCELLED, priority:'normal',
                statusReason:'Bệnh nhân bận việc',
                items:[{name:'Phí khám Nội tổng quát',qty:1,price:180000}] }),

            // ---- CA TỐI (18:00 - 20:30) ----
            mk({ id:'LH214', patientName:'Nguyễn Văn X', patientId:'BN114', phone:'0901000014',
                gender:'male', dob:'1985-03-12', cccd:'001085003456',
                queueNo: makeQueueNo(14), doctor:'TS.BS Lê Hoàng D', doctorId:'bs03',
                specialty:'Thần kinh', ca:'toi', time:'18:00-19:00', date:d_today,
                symptom:'Đau đầu kéo dài', status: STATUS.WAITING, priority:'urgent',
                items:[{name:'Phí khám Thần kinh (ngoài giờ)',qty:1,price:330000},
                       {name:'Chụp CT sọ não',qty:1,price:800000}] }),

            mk({ id:'LH215', patientName:'Trần Thị Cẩm', patientId:'BN115', phone:'0901000015',
                gender:'female', dob:'1993-08-08', cccd:'079193008877',
                queueNo: makeQueueNo(15), doctor:'ThS.BS Nguyễn Văn A', doctorId:'bs01',
                specialty:'Tim mạch', ca:'toi', time:'18:30-19:30', date:d_today,
                symptom:'Hồi hộp, tim đập nhanh', status: STATUS.CONFIRMED, priority:'high',
                items:[{name:'Phí khám Tim mạch (ngoài giờ)',qty:1,price:300000}] }),

            mk({ id:'LH216', patientName:'Lê Quang Huy', patientId:'BN116', phone:'0901000016',
                gender:'male', dob:'1970-01-15', cccd:'001070001234',
                queueNo: makeQueueNo(16), doctor:'TS.BS Lê Hoàng D', doctorId:'bs03',
                specialty:'Thần kinh', ca:'toi', time:'19:00-20:00', date:d_today,
                symptom:'Tê tay chân', status: STATUS.NOSHOW, priority:'normal',
                statusReason:'Không đến theo lịch',
                items:[{name:'Phí khám Thần kinh (ngoài giờ)',qty:1,price:330000}] }),

            mk({ id:'LH217', patientName:'Phan Thị Yến', patientId:'BN117', phone:'0901000017',
                gender:'female', dob:'1988-05-20', cccd:'079188005566',
                queueNo: makeQueueNo(17), doctor:'ThS.BS Nguyễn Văn A', doctorId:'bs01',
                specialty:'Tim mạch', ca:'toi', time:'19:30-20:30', date:d_today,
                symptom:'Khó thở khi nằm', status: STATUS.PENDING, priority:'urgent',
                channel:'hotline',
                items:[{name:'Phí khám Tim mạch (ngoài giờ)',qty:1,price:300000}] }),

            mk({ id:'LH218', patientName:'Võ Minh Tuấn', patientId:'BN118', phone:'0901000018',
                gender:'male', dob:'1999-12-12', cccd:'001099001122',
                queueNo: makeQueueNo(18), doctor:'BS.CKI Trần Thị C', doctorId:'bs02',
                specialty:'Nội tổng quát', ca:'toi', time:'20:00-20:30', date:d_today,
                symptom:'Đau lưng', status: STATUS.WAITING, priority:'normal',
                channel:'walk-in',
                items:[{name:'Phí khám Nội tổng quát (ngoài giờ)',qty:1,price:220000}] }),

            // ================= NGÀY MAI 03/11/2026 =================
            mk({ id:'LH301', patientName:'Hoàng Thị Nga', patientId:'BN201', phone:'0902000001',
                gender:'female', dob:'1980-12-30', cccd:'001180006677',
                queueNo: makeQueueNo(1), doctor:'ThS.BS Nguyễn Văn A', doctorId:'bs01',
                specialty:'Tim mạch', ca:'sang', time:'10:30-11:30', date:d_tomorrow,
                symptom:'Tái khám định kỳ', status: STATUS.CONFIRMED,
                items:[{name:'Phí khám Tim mạch',qty:1,price:200000}] }),

            mk({ id:'LH302', patientName:'Trần Quốc Bảo', patientId:'BN202', phone:'0902000002',
                gender:'male', dob:'1987-01-01', cccd:'079187002233',
                queueNo: makeQueueNo(2), doctor:'TS.BS Lê Hoàng D', doctorId:'bs03',
                specialty:'Thần kinh', ca:'toi', time:'19:30-20:30', date:d_tomorrow,
                symptom:'Đau đầu', status: STATUS.WAITING, priority:'high',
                items:[{name:'Phí khám Thần kinh (ngoài giờ)',qty:1,price:330000}] }),

            // ================= QUÁ KHỨ =================
            mk({ id:'LH401', patientName:'Bùi Thị Hồng', patientId:'BN301', phone:'0903000001',
                gender:'female', dob:'1975-04-22', cccd:'001175004455',
                queueNo: makeQueueNo(1), doctor:'BS.CKI Trần Thị C', doctorId:'bs02',
                specialty:'Nội tổng quát', ca:'sang', time:'08:30-09:30', date:d_2ago,
                symptom:'Mệt mỏi', status: STATUS.CHECKED,
                items:[{name:'Phí khám Nội tổng quát',qty:1,price:180000}] }),

            mk({ id:'LH402', patientName:'Ngô Văn Tú', patientId:'BN302', phone:'0903000002',
                gender:'male', dob:'1960-08-08', cccd:'001060008899',
                queueNo: makeQueueNo(2), doctor:'ThS.BS Nguyễn Văn A', doctorId:'bs01',
                specialty:'Tim mạch', ca:'chieu', time:'15:30-16:30', date:d_2ago,
                symptom:'Đau ngực', status: STATUS.NOSHOW, priority:'urgent',
                statusReason:'Không đến theo lịch',
                items:[{name:'Phí khám Tim mạch',qty:1,price:200000}] }),

            mk({ id:'LH403', patientName:'Lý Thị Mai', patientId:'BN303', phone:'0903000003',
                gender:'female', dob:'1995-10-10', cccd:'079195007766',
                queueNo: makeQueueNo(1), doctor:'BS.CKI Trần Thị C', doctorId:'bs02',
                specialty:'Nội tổng quát', ca:'sang', time:'09:30-10:30', date:d_3ago,
                symptom:'Đau dạ dày', status: STATUS.CHECKED,
                items:[{name:'Phí khám Nội tổng quát',qty:1,price:180000}] }),

            mk({ id:'LH404', patientName:'Đinh Công Sơn', patientId:'BN304', phone:'0903000004',
                gender:'male', dob:'1983-03-03', cccd:'001083005544',
                queueNo: makeQueueNo(2), doctor:'TS.BS Lê Hoàng D', doctorId:'bs03',
                specialty:'Thần kinh', ca:'toi', time:'19:30-20:30', date:d_3ago,
                symptom:'Mất ngủ', status: STATUS.CANCELLED,
                statusReason:'Bệnh nhân bận việc',
                items:[{name:'Phí khám Thần kinh (ngoài giờ)',qty:1,price:330000}] }),

            // Quá hạn hôm qua (để test processOvernightAppointments)
            mk({ id:'LH405', patientName:'Đặng Văn Lâm', patientId:'BN305', phone:'0903000005',
                gender:'male', dob:'1991-06-06', cccd:'001091006677',
                queueNo: makeQueueNo(1), doctor:'BS.CKI Trần Thị C', doctorId:'bs02',
                specialty:'Nội tổng quát', ca:'sang', time:'08:00-09:00', date:d_yesterday,
                symptom:'Sốt', status: STATUS.CONFIRMED,
                items:[{name:'Phí khám Nội tổng quát',qty:1,price:180000}] })
        ];
    }

    function initIfNeeded() {
        if (!localStorage.getItem(KEYS.INITIALIZED)) {
            writeJSON(KEYS.APPOINTMENTS, seedAppointments());
            writeJSON(KEYS.PAYMENTS, []);
            writeJSON(KEYS.CHECKINS, []);
            localStorage.setItem(KEYS.INITIALIZED, '1');
        }
    }

    const LT_Store = {
        STATUS,
        STATUS_LABEL,
        todayStr,

        getAppointments() {
            return readJSON(KEYS.APPOINTMENTS, []);
        },

        getAppointmentById(id) {
            return this.getAppointments().find(a => a.id === id) || null;
        },

        searchAppointments({ keyword, status, date, doctorId, specialty, ca, priority } = {}) {
            let list = this.getAppointments();
            if (keyword) {
                const k = keyword.trim().toLowerCase();
                list = list.filter(a =>
                    (a.id && a.id.toLowerCase().includes(k)) ||
                    (a.patientName && a.patientName.toLowerCase().includes(k)) ||
                    (a.patientId && a.patientId.toLowerCase().includes(k)) ||
                    (a.phone && a.phone.includes(k)) ||
                    (a.cccd && a.cccd.includes(k)) ||
                    (a.email && a.email.toLowerCase().includes(k))
                );
            }
            if (status) list = list.filter(a => a.status === status);
            if (date) list = list.filter(a => a.date === date);
            if (doctorId) list = list.filter(a => a.doctorId === doctorId);
            if (specialty) list = list.filter(a => a.specialty === specialty);
            if (ca) list = list.filter(a => a.ca === ca);
            if (priority) list = list.filter(a => a.priority === priority);
            return list;
        },

        updateAppointmentStatus(id, newStatus, reason) {
            const appointments = this.getAppointments();
            const index = appointments.findIndex(a => a.id === id);
            if (index === -1) return { success: false, error: 'Không tìm thấy lịch hẹn' };
            if (!Object.values(STATUS).includes(newStatus)) {
                return { success: false, error: 'Trạng thái không hợp lệ: ' + newStatus };
            }
            const oldStatus = appointments[index].status;
            appointments[index].status = newStatus;
            appointments[index].statusUpdatedAt = new Date().toISOString();
            appointments[index].statusReason = reason || '';
            appointments[index].updatedAt = new Date().toISOString();
            const saved = writeJSON(KEYS.APPOINTMENTS, appointments);
            if (!saved) return { success: false, error: 'Không thể lưu trạng thái' };
            return { success: true, oldStatus, newStatus };
        },

        confirmAppointment(id, reason) {
            return this.updateAppointmentStatus(id, STATUS.CONFIRMED, reason || 'Lễ tân xác nhận');
        },

        cancelAppointment(id, reason) {
            return this.updateAppointmentStatus(id, STATUS.CANCELLED, reason || 'Hủy bởi lễ tân');
        },

        updateAppointmentInfo(id, patch) {
            const appointments = this.getAppointments();
            const index = appointments.findIndex(a => a.id === id);
            if (index === -1) return { success: false, error: 'Không tìm thấy lịch hẹn' };
            const safePatch = Object.assign({}, patch);
            delete safePatch.id;
            delete safePatch.status;
            appointments[index] = Object.assign({}, appointments[index], safePatch);
            appointments[index].updatedAt = new Date().toISOString();
            const saved = writeJSON(KEYS.APPOINTMENTS, appointments);
            if (!saved) return { success: false, error: 'Không thể lưu' };
            return { success: true, appointment: appointments[index] };
        },

        changeAppointmentTime(id, newTime, newCa) {
            const appointments = this.getAppointments();
            const index = appointments.findIndex(a => a.id === id);
            if (index === -1) return { success: false, error: 'Không tìm thấy lịch hẹn' };
            appointments[index].time = newTime;
            if (newCa) appointments[index].ca = newCa;
            appointments[index].timeUpdatedAt = new Date().toISOString();
            appointments[index].updatedAt = new Date().toISOString();
            const saved = writeJSON(KEYS.APPOINTMENTS, appointments);
            if (!saved) return { success: false, error: 'Không thể lưu khung giờ' };
            return { success: true };
        },

        isSlotAvailable(doctorId, date, timeSlot, excludeApptId) {
            const appointments = this.getAppointments();
            return !appointments.some(a =>
                a.id !== excludeApptId &&
                a.doctorId === doctorId &&
                a.date === date &&
                a.time === timeSlot &&
                a.status !== STATUS.CANCELLED &&
                a.status !== STATUS.NOSHOW
            );
        },

        createCheckin(data) {
            const checkins = readJSON(KEYS.CHECKINS, []);
            const checkin = {
                id: 'CI' + Date.now(),
                appointmentId: data.appointmentId,
                patientId: data.patientId,
                cashierId: data.cashierId,
                cashierName: data.cashierName,
                vitals: data.vitals || {},
                checkedAt: new Date().toISOString()
            };
            checkins.push(checkin);
            const saved = writeJSON(KEYS.CHECKINS, checkins);
            if (!saved) return { success: false, error: 'Không thể lưu check-in' };
            const statusResult = this.updateAppointmentStatus(data.appointmentId, STATUS.CHECKED, 'Check-in tại quầy');
            if (!statusResult.success) return statusResult;
            return { success: true, checkin };
        },

        getCheckins() {
            return readJSON(KEYS.CHECKINS, []);
        },

        getPayments() {
            return readJSON(KEYS.PAYMENTS, []);
        },

        addPayment(transaction) {
            const payments = this.getPayments();
            payments.push(transaction);
            return { success: writeJSON(KEYS.PAYMENTS, payments) };
        },

        createPayment(data) {
            if (!data || !data.appointmentId) {
                return { success: false, message: 'Thiếu mã lịch hẹn' };
            }
            if (this.isAlreadyPaid(data.appointmentId)) {
                return { success: false, message: 'Hóa đơn đã được thu rồi' };
            }

            const payments = this.getPayments();
            const now = new Date();
            const year = now.getFullYear();

            const payment = {
                id: 'PM' + Date.now(),
                invoiceId: data.invoiceId || ('HD-' + year + '-' + data.appointmentId.replace('LH', '')),
                appointmentId: data.appointmentId,
                patientId: data.patientId || null,
                patientName: data.patientName || '',
                doctorId: data.doctorId || null,
                doctorName: data.doctorName || '',
                specialty: data.specialty || '',
                ca: data.ca || '',
                date: data.date || todayStr(),
                items: Array.isArray(data.items) ? data.items : [],
                totalAmount: parseInt(data.totalAmount, 10) || 0,
                paymentMethod: data.paymentMethod || 'cash',
                cashierId: data.cashierId || null,
                cashierName: data.cashierName || '',
                paidAt: now.toISOString(),
                createdAt: now.toISOString()
            };

            payments.push(payment);
            const saved = writeJSON(KEYS.PAYMENTS, payments);
            if (!saved) return { success: false, message: 'Không thể lưu giao dịch vào hệ thống' };
            return { success: true, payment };
        },

        isAlreadyPaid(appointmentId) {
            const payments = this.getPayments();
            return payments.some(p => p.appointmentId === appointmentId);
        },

        getDashboardStats() {
            const appointments = this.getAppointments();
            const payments = this.getPayments();
            const today = todayStr();

            const todayAppointments = appointments.filter(a => a.date === today);

            const byCa = {
                sang: todayAppointments.filter(a => a.ca === 'sang').length,
                chieu: todayAppointments.filter(a => a.ca === 'chieu').length,
                toi: todayAppointments.filter(a => a.ca === 'toi').length
            };

            const byStatus = {};
            Object.values(STATUS).forEach(s => {
                byStatus[s] = todayAppointments.filter(a => a.status === s).length;
            });

            const byPriority = {
                normal: todayAppointments.filter(a => a.priority === 'normal').length,
                high: todayAppointments.filter(a => a.priority === 'high').length,
                urgent: todayAppointments.filter(a => a.priority === 'urgent').length
            };

            const byChannel = {};
            todayAppointments.forEach(a => {
                const ch = a.channel || 'unknown';
                byChannel[ch] = (byChannel[ch] || 0) + 1;
            });

            const todayPayments = payments.filter(p => {
                if (!p.paidAt) return false;
                return formatDate(new Date(p.paidAt)) === today;
            });

            const revenueToday = todayPayments.reduce(
                (sum, p) => sum + (parseInt(p.totalAmount, 10) || 0), 0
            );

            return {
                totalToday: todayAppointments.length,
                waiting: byStatus[STATUS.WAITING] || 0,
                pending: byStatus[STATUS.PENDING] || 0,
                confirmed: byStatus[STATUS.CONFIRMED] || 0,
                checkedIn: byStatus[STATUS.CHECKED] || 0,
                cancelled: byStatus[STATUS.CANCELLED] || 0,
                noshow: byStatus[STATUS.NOSHOW] || 0,
                byCa,
                byStatus,
                byPriority,
                byChannel,
                revenueToday,
                paymentCountToday: todayPayments.length
            };
        },

        getTodayActionable() {
            const today = todayStr();
            return this.getAppointments().filter(a =>
                a.date === today &&
                (a.status === STATUS.WAITING ||
                 a.status === STATUS.PENDING ||
                 a.status === STATUS.CONFIRMED)
            );
        },

        getByStatus(status) {
            return this.getAppointments().filter(a => a.status === status);
        },

        getAppointmentsByPatient(patientId) {
            return this.getAppointments()
                .filter(a => a.patientId === patientId)
                .sort((a, b) => (a.date < b.date ? 1 : -1));
        },

        countWaiting() {
            return this.getAppointments().filter(a => a.status === STATUS.WAITING).length;
        },

        processOvernightAppointments() {
            const appointments = this.getAppointments();
            const today = todayStr();
            const changed = [];

            appointments.forEach(a => {
                if (
                    a.date < today &&
                    (a.status === STATUS.WAITING ||
                     a.status === STATUS.PENDING ||
                     a.status === STATUS.CONFIRMED)
                ) {
                    a.status = STATUS.NOSHOW;
                    a.statusUpdatedAt = new Date().toISOString();
                    a.statusReason = 'Tự động: Qua ngày';
                    a.updatedAt = new Date().toISOString();
                    changed.push(a.id);
                }
            });

            if (changed.length > 0) {
                writeJSON(KEYS.APPOINTMENTS, appointments);
                console.log('🕛 LT_Store: Đã chuyển', changed.length, 'lịch quá hạn sang noshow.');
            }
            return changed;
        },

        reset() {
            Object.values(KEYS).forEach(key => {
                localStorage.removeItem(key);
            });
            initIfNeeded();
        }
    };

    window.LT_Store = LT_Store;
    initIfNeeded();
    console.log('LT_Store.js loaded (Test build - Fixed date 02/11/2026)');
})();/**
 * LT_Store.js - Lễ Tân Store (Realtime) - BẢN HOÀN CHỈNH
 * Prefix: medbooking_
 * Mốc dữ liệu: NGÀY HÔM NAY THỰC TẾ (để test luôn đúng)
 */

(function () {
    'use strict';

    const PREFIX = 'medbooking_';

    const KEYS = {
        APPOINTMENTS: PREFIX + 'appointments',
        PAYMENTS: PREFIX + 'payments',
        CHECKINS: PREFIX + 'checkins',
        INITIALIZED: PREFIX + 'initialized'
    };

    const STATUS = {
        WAITING: 'waiting',
        PENDING: 'pending',
        CONFIRMED: 'confirmed',
        CHECKED: 'checked',
        NOSHOW: 'noshow',
        CANCELLED: 'cancelled'
    };

    const STATUS_LABEL = {
        waiting: 'Chờ xác nhận',
        pending: 'Chờ khám',
        confirmed: 'Đã xác nhận',
        checked: 'Đã check-in',
        noshow: 'Không đến',
        cancelled: 'Đã hủy'
    };

    function formatDate(date) {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    }

    function todayStr() {
        return formatDate(new Date());
    }

    // Trả về ngày lệch N ngày so với HÔM NAY THỰC TẾ
    function offsetDateStr(offset) {
        const date = new Date();
        date.setHours(0, 0, 0, 0);
        date.setDate(date.getDate() + offset);
        return formatDate(date);
    }

    function readJSON(key, fallback) {
        try {
            const raw = localStorage.getItem(key);
            if (!raw) return fallback;
            return JSON.parse(raw);
        } catch (error) {
            console.error('LT_Store read error:', key, error);
            return fallback;
        }
    }

    function writeJSON(key, value) {
        try {
            localStorage.setItem(key, JSON.stringify(value));
            return true;
        } catch (error) {
            console.error('LT_Store write error:', key, error);
            return false;
        }
    }

    function makeQueueNo(index) {
        return 'STT' + String(index).padStart(3, '0');
    }

    function seedAppointments() {
        const d_today = offsetDateStr(0);
        const d_tomorrow = offsetDateStr(1);
        const d_yesterday = offsetDateStr(-1);
        const d_2ago = offsetDateStr(-2);
        const d_3ago = offsetDateStr(-3);
        const nowIso = new Date().toISOString();

        return [
            // ===== HÔM NAY =====
            {
                id: 'LH101',
                patientName: 'Nguyễn Văn X',
                patientId: 'BN001',
                phone: '0912345678',
                email: 'nguyenvanx@example.com',
                gender: 'male',
                dob: '1985-03-12',
                cccd: '001085003456',
                address: '12 Lê Lợi, Q.1, TP.HCM',
                insuranceCode: 'HS4012345678',
                insuranceExpiry: '2027-12-31',
                occupation: 'Kỹ sư',
                emergencyContactName: 'Nguyễn Thị Y',
                emergencyContactPhone: '0909111222',
                emergencyRelationship: 'Vợ',
                medicalHistory: 'Tăng huyết áp nhẹ (2020)',
                allergies: 'Không',
                notes: 'Bệnh nhân lớn tuổi, cần hỗ trợ di chuyển.',
                channel: 'hotline',
                priority: 'normal',
                queueNo: makeQueueNo(1),
                doctor: 'ThS.BS Nguyễn Văn A',
                doctorId: 'bs01',
                specialty: 'Tim mạch',
                ca: 'sang',
                time: '08:30-09:30',
                date: d_today,
                symptom: 'Đau ngực, khó thở khi vận động',
                status: STATUS.WAITING,
                items: [
                    { name: 'Phí khám Tim mạch', qty: 1, price: 200000 },
                    { name: 'Điện tâm đồ (ECG)', qty: 1, price: 150000 }
                ],
                createdAt: nowIso,
                updatedAt: nowIso
            },
            {
                id: 'LH102',
                patientName: 'Trần Thị B',
                patientId: 'BN002',
                phone: '0912345679',
                email: 'tranthib@example.com',
                gender: 'female',
                dob: '1992-07-25',
                cccd: '079192007890',
                address: '45 Nguyễn Trãi, Q.5, TP.HCM',
                insuranceCode: 'HS4098765432',
                insuranceExpiry: '2026-11-30',
                occupation: 'Nhân viên văn phòng',
                emergencyContactName: 'Trần Văn C',
                emergencyContactPhone: '0909333444',
                emergencyRelationship: 'Cha',
                medicalHistory: 'Viêm dạ dày (2021)',
                allergies: 'Penicillin',
                notes: 'Dị ứng Penicillin - cần lưu ý khi kê đơn.',
                channel: 'app',
                priority: 'high',
                queueNo: makeQueueNo(2),
                doctor: 'BS.CKI Trần Thị C',
                doctorId: 'bs02',
                specialty: 'Nội tổng quát',
                ca: 'chieu',
                time: '14:30-15:30',
                date: d_today,
                symptom: 'Sốt cao 3 ngày, mệt mỏi',
                status: STATUS.CONFIRMED,
                items: [
                    { name: 'Phí khám Nội tổng quát', qty: 1, price: 180000 },
                    { name: 'Xét nghiệm máu', qty: 1, price: 250000 },
                    { name: 'X-quang ngực', qty: 1, price: 200000 }
                ],
                createdAt: nowIso,
                updatedAt: nowIso
            },
            {
                id: 'LH103',
                patientName: 'Lê Thị M',
                patientId: 'BN003',
                phone: '0912345680',
                email: 'lethim@example.com',
                gender: 'female',
                dob: '1978-11-02',
                cccd: '001178002345',
                address: '78 Cách Mạng Tháng 8, Q.3, TP.HCM',
                insuranceCode: 'HS4056781234',
                insuranceExpiry: '2027-06-30',
                occupation: 'Giáo viên',
                emergencyContactName: 'Lê Văn D',
                emergencyContactPhone: '0909555666',
                emergencyRelationship: 'Chồng',
                medicalHistory: 'Không',
                allergies: 'Không',
                notes: '',
                channel: 'website',
                priority: 'normal',
                queueNo: makeQueueNo(3),
                doctor: 'BS.CKI Trần Thị C',
                doctorId: 'bs02',
                specialty: 'Nội tổng quát',
                ca: 'sang',
                time: '09:30-10:30',
                date: d_today,
                symptom: 'Đau bụng, buồn nôn',
                status: STATUS.CHECKED,
                items: [
                    { name: 'Phí khám Nội tổng quát', qty: 1, price: 180000 },
                    { name: 'Siêu âm bụng', qty: 1, price: 300000 }
                ],
                createdAt: nowIso,
                updatedAt: nowIso
            },
            {
                id: 'LH104',
                patientName: 'Phạm Văn K',
                patientId: 'BN004',
                phone: '0912345681',
                email: 'phamvank@example.com',
                gender: 'male',
                dob: '1969-05-19',
                cccd: '001069009876',
                address: '23 Điện Biên Phủ, Q.Bình Thạnh, TP.HCM',
                insuranceCode: 'HS4011223344',
                insuranceExpiry: '2027-01-31',
                occupation: 'Hưu trí',
                emergencyContactName: 'Phạm Thị E',
                emergencyContactPhone: '0909777888',
                emergencyRelationship: 'Con gái',
                medicalHistory: 'Mất ngủ mạn tính, đau đầu Migraine',
                allergies: 'Không',
                notes: 'Cần khám ngoài giờ.',
                channel: 'hotline',
                priority: 'urgent',
                queueNo: makeQueueNo(4),
                doctor: 'TS.BS Lê Hoàng D',
                doctorId: 'bs03',
                specialty: 'Thần kinh',
                ca: 'toi',
                time: '18:30-19:30',
                date: d_today,
                symptom: 'Đau đầu kéo dài, mất ngủ',
                status: STATUS.CHECKED,
                items: [
                    { name: 'Phí khám Thần kinh (ngoài giờ)', qty: 1, price: 330000 },
                    { name: 'Chụp CT sọ não', qty: 1, price: 800000 }
                ],
                createdAt: nowIso,
                updatedAt: nowIso
            },
            {
                id: 'LH106',
                patientName: 'Vũ Đức P',
                patientId: 'BN006',
                phone: '0912345683',
                email: 'vuducp@example.com',
                gender: 'male',
                dob: '1998-02-14',
                cccd: '001098001122',
                address: '56 Trần Hưng Đạo, Q.1, TP.HCM',
                insuranceCode: '',
                insuranceExpiry: '',
                occupation: 'Sinh viên',
                emergencyContactName: 'Vũ Thị F',
                emergencyContactPhone: '0909999000',
                emergencyRelationship: 'Mẹ',
                medicalHistory: 'Không',
                allergies: 'Không',
                notes: '',
                channel: 'walk-in',
                priority: 'normal',
                queueNo: makeQueueNo(5),
                doctor: 'BS.CKI Trần Thị C',
                doctorId: 'bs02',
                specialty: 'Nội tổng quát',
                ca: 'chieu',
                time: '15:30-16:30',
                date: d_today,
                symptom: 'Ho khan, đau họng',
                status: STATUS.WAITING,
                items: [
                    { name: 'Phí khám Nội tổng quát', qty: 1, price: 180000 },
                    { name: 'Test Covid', qty: 1, price: 100000 }
                ],
                createdAt: nowIso,
                updatedAt: nowIso
            },
            {
                id: 'LH107',
                patientName: 'Đỗ Minh Anh',
                patientId: 'BN007',
                phone: '0912345684',
                email: 'dominhanh@example.com',
                gender: 'female',
                dob: '1990-09-09',
                cccd: '079190003344',
                address: '90 Võ Văn Tần, Q.3, TP.HCM',
                insuranceCode: 'HS4077889900',
                insuranceExpiry: '2027-08-31',
                occupation: 'Kế toán',
                emergencyContactName: 'Đỗ Văn G',
                emergencyContactPhone: '0909123123',
                emergencyRelationship: 'Anh trai',
                medicalHistory: 'Không',
                allergies: 'Không',
                notes: 'Khám sức khỏe định kỳ.',
                channel: 'app',
                priority: 'normal',
                queueNo: makeQueueNo(6),
                doctor: 'ThS.BS Nguyễn Văn A',
                doctorId: 'bs01',
                specialty: 'Tim mạch',
                ca: 'sang',
                time: '07:30-08:30',
                date: d_today,
                symptom: 'Khám sức khỏe định kỳ',
                status: STATUS.CONFIRMED,
                items: [
                    { name: 'Phí khám Tim mạch', qty: 1, price: 200000 }
                ],
                createdAt: nowIso,
                updatedAt: nowIso
            },

            // ===== NGÀY MAI =====
            {
                id: 'LH105',
                patientName: 'Hoàng Thị N',
                patientId: 'BN005',
                phone: '0912345682',
                email: 'hoangthin@example.com',
                gender: 'female',
                dob: '1980-12-30',
                cccd: '001180006677',
                address: '34 Lý Thường Kiệt, Q.10, TP.HCM',
                insuranceCode: 'HS4099887766',
                insuranceExpiry: '2027-03-31',
                occupation: 'Nội trợ',
                emergencyContactName: 'Hoàng Văn H',
                emergencyContactPhone: '0909456456',
                emergencyRelationship: 'Chồng',
                medicalHistory: 'Rối loạn lipid máu',
                allergies: 'Không',
                notes: 'Tái khám định kỳ.',
                channel: 'hotline',
                priority: 'normal',
                queueNo: makeQueueNo(1),
                doctor: 'ThS.BS Nguyễn Văn A',
                doctorId: 'bs01',
                specialty: 'Tim mạch',
                ca: 'sang',
                time: '10:30-11:30',
                date: d_tomorrow,
                symptom: 'Tái khám định kỳ',
                status: STATUS.CONFIRMED,
                items: [
                    { name: 'Phí khám Tim mạch', qty: 1, price: 200000 }
                ],
                createdAt: nowIso,
                updatedAt: nowIso
            },
            {
                id: 'LH108',
                patientName: 'Nguyễn Thu Hà',
                patientId: 'BN008',
                phone: '0912345685',
                email: 'nguyenthuha@example.com',
                gender: 'female',
                dob: '2001-06-18',
                cccd: '001101001188',
                address: '11 Pasteur, Q.1, TP.HCM',
                insuranceCode: '',
                insuranceExpiry: '',
                occupation: 'Sinh viên',
                emergencyContactName: 'Nguyễn Văn I',
                emergencyContactPhone: '0909789789',
                emergencyRelationship: 'Cha',
                medicalHistory: 'Không',
                allergies: 'Không',
                notes: '',
                channel: 'website',
                priority: 'normal',
                queueNo: makeQueueNo(2),
                doctor: 'BS.CKI Trần Thị C',
                doctorId: 'bs02',
                specialty: 'Nội tổng quát',
                ca: 'chieu',
                time: '13:30-14:30',
                date: d_tomorrow,
                symptom: 'Đau họng, ho nhẹ',
                status: STATUS.WAITING,
                items: [
                    { name: 'Phí khám Nội tổng quát', qty: 1, price: 180000 }
                ],
                createdAt: nowIso,
                updatedAt: nowIso
            },
            {
                id: 'LH109',
                patientName: 'Trần Quốc Bảo',
                patientId: 'BN009',
                phone: '0912345686',
                email: 'tranquocbao@example.com',
                gender: 'male',
                dob: '1987-01-01',
                cccd: '079187002233',
                address: '67 Nguyễn Đình Chiểu, Q.3, TP.HCM',
                insuranceCode: 'HS4033445566',
                insuranceExpiry: '2027-09-30',
                occupation: 'Kinh doanh',
                emergencyContactName: 'Trần Thị J',
                emergencyContactPhone: '0909332211',
                emergencyRelationship: 'Mẹ',
                medicalHistory: 'Đau đầu, chóng mặt',
                allergies: 'Không',
                notes: 'Ưu tiên khám sớm.',
                channel: 'app',
                priority: 'high',
                queueNo: makeQueueNo(3),
                doctor: 'TS.BS Lê Hoàng D',
                doctorId: 'bs03',
                specialty: 'Thần kinh',
                ca: 'toi',
                time: '19:30-20:30',
                date: d_tomorrow,
                symptom: 'Đau đầu, chóng mặt',
                status: STATUS.CONFIRMED,
                items: [
                    { name: 'Phí khám Thần kinh (ngoài giờ)', qty: 1, price: 330000 }
                ],
                createdAt: nowIso,
                updatedAt: nowIso
            },

            // ===== QUÁ KHỨ =====
            {
                id: 'LH110',
                patientName: 'Bùi Thị Hồng',
                patientId: 'BN010',
                phone: '0912345687',
                email: 'buithihong@example.com',
                gender: 'female',
                dob: '1975-04-22',
                cccd: '001175004455',
                address: '22 Bà Huyện Thanh Quan, Q.3, TP.HCM',
                insuranceCode: 'HS4012341234',
                insuranceExpiry: '2026-12-31',
                occupation: 'Công nhân',
                emergencyContactName: 'Bùi Văn K',
                emergencyContactPhone: '0909112233',
                emergencyRelationship: 'Chồng',
                medicalHistory: 'Thiếu máu nhẹ',
                allergies: 'Không',
                notes: '',
                channel: 'hotline',
                priority: 'normal',
                queueNo: makeQueueNo(1),
                doctor: 'BS.CKI Trần Thị C',
                doctorId: 'bs02',
                specialty: 'Nội tổng quát',
                ca: 'sang',
                time: '08:30-09:30',
                date: d_2ago,
                symptom: 'Mệt mỏi, chán ăn',
                status: STATUS.CHECKED,
                items: [
                    { name: 'Phí khám Nội tổng quát', qty: 1, price: 180000 },
                    { name: 'Xét nghiệm máu', qty: 1, price: 250000 }
                ],
                createdAt: nowIso,
                updatedAt: nowIso
            },
            {
                id: 'LH111',
                patientName: 'Ngô Văn Tú',
                patientId: 'BN011',
                phone: '0912345688',
                email: 'ngovantu@example.com',
                gender: 'male',
                dob: '1960-08-08',
                cccd: '001060008899',
                address: '89 Trần Phú, Q.5, TP.HCM',
                insuranceCode: 'HS4099881122',
                insuranceExpiry: '2026-10-31',
                occupation: 'Hưu trí',
                emergencyContactName: 'Ngô Thị L',
                emergencyContactPhone: '0909445566',
                emergencyRelationship: 'Vợ',
                medicalHistory: 'Tăng huyết áp, đau thắt ngực',
                allergies: 'Aspirin',
                notes: 'Dị ứng Aspirin.',
                channel: 'hotline',
                priority: 'urgent',
                queueNo: makeQueueNo(2),
                doctor: 'ThS.BS Nguyễn Văn A',
                doctorId: 'bs01',
                specialty: 'Tim mạch',
                ca: 'chieu',
                time: '15:30-16:30',
                date: d_2ago,
                symptom: 'Huyết áp cao, đau ngực nhẹ',
                status: STATUS.NOSHOW,
                items: [
                    { name: 'Phí khám Tim mạch', qty: 1, price: 200000 }
                ],
                createdAt: nowIso,
                updatedAt: nowIso,
                statusReason: 'Không đến theo lịch'
            },
            {
                id: 'LH112',
                patientName: 'Lý Thị Mai',
                patientId: 'BN012',
                phone: '0912345689',
                email: 'lythimai@example.com',
                gender: 'female',
                dob: '1995-10-10',
                cccd: '079195007766',
                address: '15 Nguyễn Thị Minh Khai, Q.1, TP.HCM',
                insuranceCode: '',
                insuranceExpiry: '',
                occupation: 'Nhân viên bán hàng',
                emergencyContactName: 'Lý Văn M',
                emergencyContactPhone: '0909223344',
                emergencyRelationship: 'Anh trai',
                medicalHistory: 'Viêm loét dạ dày (2022)',
                allergies: 'Không',
                notes: '',
                channel: 'app',
                priority: 'normal',
                queueNo: makeQueueNo(1),
                doctor: 'BS.CKI Trần Thị C',
                doctorId: 'bs02',
                specialty: 'Nội tổng quát',
                ca: 'sang',
                time: '09:30-10:30',
                date: d_3ago,
                symptom: 'Đau dạ dày, ợ nóng',
                status: STATUS.CHECKED,
                items: [
                    { name: 'Phí khám Nội tổng quát', qty: 1, price: 180000 },
                    { name: 'Siêu âm bụng', qty: 1, price: 300000 }
                ],
                createdAt: nowIso,
                updatedAt: nowIso
            },
            {
                id: 'LH113',
                patientName: 'Đinh Công Sơn',
                patientId: 'BN013',
                phone: '0912345690',
                email: 'dinhcongson@example.com',
                gender: 'male',
                dob: '1983-03-03',
                cccd: '001083005544',
                address: '101 Lê Văn Sỹ, Q.Phú Nhuận, TP.HCM',
                insuranceCode: 'HS4077665544',
                insuranceExpiry: '2027-05-31',
                occupation: 'Tài xế',
                emergencyContactName: 'Đinh Thị N',
                emergencyContactPhone: '0909667788',
                emergencyRelationship: 'Vợ',
                medicalHistory: 'Mất ngủ kéo dài',
                allergies: 'Không',
                notes: 'Bệnh nhân xin hủy do bận việc.',
                channel: 'hotline',
                priority: 'normal',
                queueNo: makeQueueNo(2),
                doctor: 'TS.BS Lê Hoàng D',
                doctorId: 'bs03',
                specialty: 'Thần kinh',
                ca: 'toi',
                time: '19:30-20:30',
                date: d_3ago,
                symptom: 'Mất ngủ kéo dài',
                status: STATUS.CANCELLED,
                items: [
                    { name: 'Phí khám Thần kinh (ngoài giờ)', qty: 1, price: 330000 }
                ],
                createdAt: nowIso,
                updatedAt: nowIso,
                statusReason: 'Bệnh nhân bận việc đột xuất'
            }
        ];
    }

    function initIfNeeded() {
        if (!localStorage.getItem(KEYS.INITIALIZED)) {
            writeJSON(KEYS.APPOINTMENTS, seedAppointments());
            writeJSON(KEYS.PAYMENTS, []);
            writeJSON(KEYS.CHECKINS, []);
            localStorage.setItem(KEYS.INITIALIZED, '1');
        }
    }

    // Khởi tạo tự động khi load file
    initIfNeeded();

    const LT_Store = {
        STATUS,
        STATUS_LABEL,

        getAppointments() {
            return readJSON(KEYS.APPOINTMENTS, []);
        },

        getAppointmentById(id) {
            return this.getAppointments().find(a => a.id === id) || null;
        },

        searchAppointments({ keyword, status, date, doctorId, specialty, ca, priority } = {}) {
            let list = this.getAppointments();
            if (keyword) {
                const k = keyword.trim().toLowerCase();
                list = list.filter(a =>
                    (a.id && a.id.toLowerCase().includes(k)) ||
                    (a.patientName && a.patientName.toLowerCase().includes(k)) ||
                    (a.patientId && a.patientId.toLowerCase().includes(k)) ||
                    (a.phone && a.phone.includes(k)) ||
                    (a.cccd && a.cccd.includes(k)) ||
                    (a.email && a.email.toLowerCase().includes(k))
                );
            }
            if (status) list = list.filter(a => a.status === status);
            if (date) list = list.filter(a => a.date === date);
            if (doctorId) list = list.filter(a => a.doctorId === doctorId);
            if (specialty) list = list.filter(a => a.specialty === specialty);
            if (ca) list = list.filter(a => a.ca === ca);
            if (priority) list = list.filter(a => a.priority === priority);
            return list;
        },

        updateAppointmentStatus(id, newStatus, reason) {
            const appointments = this.getAppointments();
            const index = appointments.findIndex(a => a.id === id);
            if (index === -1) return { success: false, error: 'Không tìm thấy lịch hẹn' };
            if (!Object.values(STATUS).includes(newStatus)) {
                return { success: false, error: 'Trạng thái không hợp lệ: ' + newStatus };
            }
            const oldStatus = appointments[index].status;
            appointments[index].status = newStatus;
            appointments[index].statusUpdatedAt = new Date().toISOString();
            appointments[index].statusReason = reason || '';
            appointments[index].updatedAt = new Date().toISOString();
            const saved = writeJSON(KEYS.APPOINTMENTS, appointments);
            if (!saved) return { success: false, error: 'Không thể lưu trạng thái' };
            return { success: true, oldStatus, newStatus };
        },

        confirmAppointment(id, reason) {
            return this.updateAppointmentStatus(id, STATUS.CONFIRMED, reason || 'Lễ tân xác nhận');
        },

        cancelAppointment(id, reason) {
            return this.updateAppointmentStatus(id, STATUS.CANCELLED, reason || 'Hủy bởi lễ tân');
        },

        updateAppointmentInfo(id, patch) {
            const appointments = this.getAppointments();
            const index = appointments.findIndex(a => a.id === id);
            if (index === -1) return { success: false, error: 'Không tìm thấy lịch hẹn' };
            const safePatch = Object.assign({}, patch);
            delete safePatch.id;
            delete safePatch.status;
            appointments[index] = Object.assign({}, appointments[index], safePatch);
            appointments[index].updatedAt = new Date().toISOString();
            const saved = writeJSON(KEYS.APPOINTMENTS, appointments);
            if (!saved) return { success: false, error: 'Không thể lưu' };
            return { success: true, appointment: appointments[index] };
        },

        changeAppointmentTime(id, newTime, newCa) {
            const appointments = this.getAppointments();
            const index = appointments.findIndex(a => a.id === id);
            if (index === -1) return { success: false, error: 'Không tìm thấy lịch hẹn' };
            appointments[index].time = newTime;
            if (newCa) appointments[index].ca = newCa;
            appointments[index].timeUpdatedAt = new Date().toISOString();
            appointments[index].updatedAt = new Date().toISOString();
            const saved = writeJSON(KEYS.APPOINTMENTS, appointments);
            if (!saved) return { success: false, error: 'Không thể lưu khung giờ' };
            return { success: true };
        },

        isSlotAvailable(doctorId, date, timeSlot, excludeApptId) {
            const appointments = this.getAppointments();
            return !appointments.some(a =>
                a.id !== excludeApptId &&
                a.doctorId === doctorId &&
                a.date === date &&
                a.time === timeSlot &&
                a.status !== STATUS.CANCELLED &&
                a.status !== STATUS.NOSHOW
            );
        },

        createCheckin(data) {
            const checkins = readJSON(KEYS.CHECKINS, []);
            const checkin = {
                id: 'CI' + Date.now(),
                appointmentId: data.appointmentId,
                patientId: data.patientId,
                cashierId: data.cashierId,
                cashierName: data.cashierName,
                vitals: data.vitals || {},
                checkedAt: new Date().toISOString()
            };
            checkins.push(checkin);
            const saved = writeJSON(KEYS.CHECKINS, checkins);
            if (!saved) return { success: false, error: 'Không thể lưu check-in' };
            const statusResult = this.updateAppointmentStatus(data.appointmentId, STATUS.CHECKED, 'Check-in tại quầy');
            if (!statusResult.success) return statusResult;
            return { success: true, checkin };
        },

        getCheckins() {
            return readJSON(KEYS.CHECKINS, []);
        },

        getPayments() {
            return readJSON(KEYS.PAYMENTS, []);
        },

        addPayment(transaction) {
            const payments = this.getPayments();
            payments.push(transaction);
            return { success: writeJSON(KEYS.PAYMENTS, payments) };
        },

        createPayment(data) {
            if (!data || !data.appointmentId) {
                return { success: false, message: 'Thiếu mã lịch hẹn' };
            }
            if (this.isAlreadyPaid(data.appointmentId)) {
                return { success: false, message: 'Hóa đơn đã được thu rồi' };
            }

            const payments = this.getPayments();
            const now = new Date();
            const year = now.getFullYear();

            const payment = {
                id: 'PM' + Date.now(),
                invoiceId: data.invoiceId || ('HD-' + year + '-' + data.appointmentId.replace('LH', '')),
                appointmentId: data.appointmentId,
                patientId: data.patientId || null,
                patientName: data.patientName || '',
                doctorId: data.doctorId || null,
                doctorName: data.doctorName || '',
                specialty: data.specialty || '',
                ca: data.ca || '',
                date: data.date || todayStr(),
                items: Array.isArray(data.items) ? data.items : [],
                totalAmount: parseInt(data.totalAmount, 10) || 0,
                paymentMethod: data.paymentMethod || 'cash',
                cashierId: data.cashierId || null,
                cashierName: data.cashierName || '',
                paidAt: now.toISOString(),
                createdAt: now.toISOString()
            };

            payments.push(payment);
            const saved = writeJSON(KEYS.PAYMENTS, payments);
            if (!saved) return { success: false, message: 'Không thể lưu giao dịch vào hệ thống' };
            return { success: true, payment };
        },

        isAlreadyPaid(appointmentId) {
            const payments = this.getPayments();
            return payments.some(p => p.appointmentId === appointmentId);
        },

        getDashboardStats() {
            const appointments = this.getAppointments();
            const payments = this.getPayments();
            const today = todayStr();

            const todayAppointments = appointments.filter(a => a.date === today);

            const byCa = {
                sang: todayAppointments.filter(a => a.ca === 'sang').length,
                chieu: todayAppointments.filter(a => a.ca === 'chieu').length,
                toi: todayAppointments.filter(a => a.ca === 'toi').length
            };

            const byStatus = {};
            Object.values(STATUS).forEach(s => {
                byStatus[s] = todayAppointments.filter(a => a.status === s).length;
            });

            const byPriority = {
                normal: todayAppointments.filter(a => a.priority === 'normal').length,
                high: todayAppointments.filter(a => a.priority === 'high').length,
                urgent: todayAppointments.filter(a => a.priority === 'urgent').length
            };

            const byChannel = {};
            todayAppointments.forEach(a => {
                const ch = a.channel || 'unknown';
                byChannel[ch] = (byChannel[ch] || 0) + 1;
            });

            const todayPayments = payments.filter(p => {
                if (!p.paidAt) return false;
                return formatDate(new Date(p.paidAt)) === today;
            });

            const revenueToday = todayPayments.reduce(
                (sum, p) => sum + (parseInt(p.totalAmount, 10) || 0), 0
            );

            return {
                totalToday: todayAppointments.length,
                waiting: byStatus[STATUS.WAITING] || 0,
                pending: byStatus[STATUS.PENDING] || 0,
                confirmed: byStatus[STATUS.CONFIRMED] || 0,
                checkedIn: byStatus[STATUS.CHECKED] || 0,
                cancelled: byStatus[STATUS.CANCELLED] || 0,
                noshow: byStatus[STATUS.NOSHOW] || 0,
                byCa,
                byStatus,
                byPriority,
                byChannel,
                revenueToday,
                paymentCountToday: todayPayments.length
            };
        },

        getTodayActionable() {
            const today = todayStr();
            return this.searchAppointments({ date: today }).filter(a => 
                a.status !== STATUS.CANCELLED && a.status !== STATUS.NOSHOW
            );
        }
    };

    // Đưa ra global scope để các script/module khác gọi được
    window.LT_Store = LT_Store;
})();