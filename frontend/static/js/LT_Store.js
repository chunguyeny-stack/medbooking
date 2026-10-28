/**
 * LT_Store.js - Lễ Tân Store (Realtime)
 * Quản lý dữ liệu localStorage cho module Lễ Tân
 * Prefix: medbooking_
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

    // Lấy ngày theo múi giờ địa phương
    function formatDate(date) {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    }

    function todayStr() {
        return formatDate(new Date());
    }

    function tomorrowStr() {
        const date = new Date();
        date.setDate(date.getDate() + 1);
        return formatDate(date);
    }

    // Trả về ngày lệch N ngày so với hôm nay
   function offsetDateStr(offset) {
    const date = new Date(2026, 9, 28); // Tháng 9 = tháng 10
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

    // Dữ liệu mẫu ban đầu - Ngày động
    function seedAppointments() {
        const d_today = offsetDateStr(0);  // Hôm nay
        const d_tomorrow = offsetDateStr(1); // Ngày mai
        const d_yesterday = offsetDateStr(-1); // Hôm qua
        const d_2ago = offsetDateStr(-2); // 2 ngày trước
        const d_3ago = offsetDateStr(-3); // 3 ngày trước

        return [
            // ===== HÔM NAY =====
            {
                id: 'LH101',
                patientName: 'Nguyễn Văn X',
                patientId: 'BN001',
                phone: '0912345678',
                doctor: 'ThS.BS Nguyễn Văn A',
                doctorId: 'bs01',
                specialty: 'Tim mạch',
                ca: 'sang',
                time: '08:30-09:30',
                date: d_today,
                symptom: 'Đau ngực, khó thở khi vận động',
                status: 'pending',
                items: [
                    { name: 'Phí khám Tim mạch', qty: 1, price: 200000 },
                    { name: 'Điện tâm đồ (ECG)', qty: 1, price: 150000 }
                ]
            },
            {
                id: 'LH102',
                patientName: 'Trần Thị B',
                patientId: 'BN002',
                phone: '0912345679',
                doctor: 'BS.CKI Trần Thị C',
                doctorId: 'bs02',
                specialty: 'Nội tổng quát',
                ca: 'chieu',
                time: '14:30-15:30',
                date: d_today,
                symptom: 'Sốt cao 3 ngày, mệt mỏi',
                status: 'confirmed',
                items: [
                    { name: 'Phí khám Nội tổng quát', qty: 1, price: 180000 },
                    { name: 'Xét nghiệm máu', qty: 1, price: 250000 },
                    { name: 'X-quang ngực', qty: 1, price: 200000 }
                ]
            },
            {
                id: 'LH103',
                patientName: 'Lê Thị M',
                patientId: 'BN003',
                phone: '0912345680',
                doctor: 'BS.CKI Trần Thị C',
                doctorId: 'bs02',
                specialty: 'Nội tổng quát',
                ca: 'sang',
                time: '09:30-10:30',
                date: d_today,
                symptom: 'Đau bụng, buồn nôn',
                status: 'checked',
                items: [
                    { name: 'Phí khám Nội tổng quát', qty: 1, price: 180000 },
                    { name: 'Siêu âm bụng', qty: 1, price: 300000 }
                ]
            },
            {
                id: 'LH104',
                patientName: 'Phạm Văn K',
                patientId: 'BN004',
                phone: '0912345681',
                doctor: 'TS.BS Lê Hoàng D',
                doctorId: 'bs03',
                specialty: 'Thần kinh',
                ca: 'toi',
                time: '18:30-19:30',
                date: d_today,
                symptom: 'Đau đầu kéo dài, mất ngủ',
                status: 'checked',
                items: [
                    { name: 'Phí khám Thần kinh (ngoài giờ)', qty: 1, price: 330000 },
                    { name: 'Chụp CT sọ não', qty: 1, price: 800000 }
                ]
            },
            {
                id: 'LH106',
                patientName: 'Vũ Đức P',
                patientId: 'BN006',
                phone: '0912345683',
                doctor: 'BS.CKI Trần Thị C',
                doctorId: 'bs02',
                specialty: 'Nội tổng quát',
                ca: 'chieu',
                time: '15:30-16:30',
                date: d_today,
                symptom: 'Ho khan, đau họng',
                status: 'pending',
                items: [
                    { name: 'Phí khám Nội tổng quát', qty: 1, price: 180000 },
                    { name: 'Test Covid', qty: 1, price: 100000 }
                ]
            },
            {
                id: 'LH107',
                patientName: 'Đỗ Minh Anh',
                patientId: 'BN007',
                phone: '0912345684',
                doctor: 'ThS.BS Nguyễn Văn A',
                doctorId: 'bs01',
                specialty: 'Tim mạch',
                ca: 'sang',
                time: '07:30-08:30',
                date: d_today,
                symptom: 'Khám sức khỏe định kỳ',
                status: 'confirmed',
                items: [
                    { name: 'Phí khám Tim mạch', qty: 1, price: 200000 }
                ]
            },

            // ===== NGÀY MAI =====
            {
                id: 'LH105',
                patientName: 'Hoàng Thị N',
                patientId: 'BN005',
                phone: '0912345682',
                doctor: 'ThS.BS Nguyễn Văn A',
                doctorId: 'bs01',
                specialty: 'Tim mạch',
                ca: 'sang',
                time: '10:30-11:30',
                date: d_tomorrow,
                symptom: 'Tái khám định kỳ',
                status: 'confirmed',
                items: [
                    { name: 'Phí khám Tim mạch', qty: 1, price: 200000 }
                ]
            },
            {
                id: 'LH108',
                patientName: 'Nguyễn Thu Hà',
                patientId: 'BN008',
                phone: '0912345685',
                doctor: 'BS.CKI Trần Thị C',
                doctorId: 'bs02',
                specialty: 'Nội tổng quát',
                ca: 'chieu',
                time: '13:30-14:30',
                date: d_tomorrow,
                symptom: 'Đau họng, ho nhẹ',
                status: 'pending',
                items: [
                    { name: 'Phí khám Nội tổng quát', qty: 1, price: 180000 }
                ]
            },
            {
                id: 'LH109',
                patientName: 'Trần Quốc Bảo',
                patientId: 'BN009',
                phone: '0912345686',
                doctor: 'TS.BS Lê Hoàng D',
                doctorId: 'bs03',
                specialty: 'Thần kinh',
                ca: 'toi',
                time: '19:30-20:30',
                date: d_tomorrow,
                symptom: 'Đau đầu, chóng mặt',
                status: 'confirmed',
                items: [
                    { name: 'Phí khám Thần kinh (ngoài giờ)', qty: 1, price: 330000 }
                ]
            },

            // ===== QUÁ KHỨ =====
            {
                id: 'LH110',
                patientName: 'Bùi Thị Hồng',
                patientId: 'BN010',
                phone: '0912345687',
                doctor: 'BS.CKI Trần Thị C',
                doctorId: 'bs02',
                specialty: 'Nội tổng quát',
                ca: 'sang',
                time: '08:30-09:30',
                date: d_2ago,
                symptom: 'Mệt mỏi, chán ăn',
                status: 'checked',
                items: [
                    { name: 'Phí khám Nội tổng quát', qty: 1, price: 180000 },
                    { name: 'Xét nghiệm máu', qty: 1, price: 250000 }
                ]
            },
            {
                id: 'LH111',
                patientName: 'Ngô Văn Tú',
                patientId: 'BN011',
                phone: '0912345688',
                doctor: 'ThS.BS Nguyễn Văn A',
                doctorId: 'bs01',
                specialty: 'Tim mạch',
                ca: 'chieu',
                time: '15:30-16:30',
                date: d_2ago,
                symptom: 'Huyết áp cao, đau ngực nhẹ',
                status: 'noshow',
                items: [
                    { name: 'Phí khám Tim mạch', qty: 1, price: 200000 }
                ]
            },
            {
                id: 'LH112',
                patientName: 'Lý Thị Mai',
                patientId: 'BN012',
                phone: '0912345689',
                doctor: 'BS.CKI Trần Thị C',
                doctorId: 'bs02',
                specialty: 'Nội tổng quát',
                ca: 'sang',
                time: '09:30-10:30',
                date: d_3ago,
                symptom: 'Đau dạ dày, ợ nóng',
                status: 'checked',
                items: [
                    { name: 'Phí khám Nội tổng quát', qty: 1, price: 180000 },
                    { name: 'Siêu âm bụng', qty: 1, price: 300000 }
                ]
            },
            {
                id: 'LH113',
                patientName: 'Đinh Công Sơn',
                patientId: 'BN013',
                phone: '0912345690',
                doctor: 'TS.BS Lê Hoàng D',
                doctorId: 'bs03',
                specialty: 'Thần kinh',
                ca: 'toi',
                time: '19:30-20:30',
                date: d_3ago,
                symptom: 'Mất ngủ kéo dài',
                status: 'cancelled',
                items: [
                    { name: 'Phí khám Thần kinh (ngoài giờ)', qty: 1, price: 330000 }
                ]
            }
        ];
    }

    function initIfNeeded() {
        if (!localStorage.getItem(KEYS.INITIALIZED)) {
            writeJSON(KEYS.APPOINTMENTS, seedAppointments());
            writeJSON(KEYS.PAYMENTS, []);
            writeJSON(KEYS.CHECKINS, []);
            localStorage.setItem(KEYS.INITIALIZED, '1');
            return;
        }
        // Đồng bộ ngày cho các lịch mẫu (nếu đã có sẵn từ trước)
        LT_Store.syncDates();
    }

    const LT_Store = {
        getAppointments() {
            return readJSON(KEYS.APPOINTMENTS, []);
        },

        getAppointmentById(id) {
            const appointments = this.getAppointments();
            return appointments.find(a => a.id === id) || null;
        },

        // Tự động cập nhật ngày tháng cho các lịch mẫu theo thời gian thực
        syncDates() {
            const appointments = this.getAppointments();
            let changed = false;
            
            // Map ngày offset cho từng ID mẫu
            const seedOffsets = {
                'LH101': 0, 'LH102': 0, 'LH103': 0, 'LH104': 0, 'LH106': 0, 'LH107': 0,
                'LH105': 1, 'LH108': 1, 'LH109': 1,
                'LH110': -2, 'LH111': -2,
                'LH112': -3, 'LH113': -3
            };

            appointments.forEach(appt => {
                if (seedOffsets[appt.id] !== undefined) {
                    const expectedDate = offsetDateStr(seedOffsets[appt.id]);
                    if (appt.date !== expectedDate) {
                        appt.date = expectedDate;
                        changed = true;
                    }
                }
            });

            if (changed) {
                writeJSON(KEYS.APPOINTMENTS, appointments);
                console.log('🔄 LT_Store: Đã đồng bộ ngày tháng theo thời gian thực.');
            }
        },

        updateAppointmentStatus(id, newStatus, reason) {
            const appointments = this.getAppointments();
            const index = appointments.findIndex(a => a.id === id);
            if (index === -1) return { success: false, error: 'Không tìm thấy lịch hẹn' };

            appointments[index].status = newStatus;
            appointments[index].statusUpdatedAt = new Date().toISOString();
            appointments[index].statusReason = reason || '';

            const saved = writeJSON(KEYS.APPOINTMENTS, appointments);
            if (!saved) return { success: false, error: 'Không thể lưu trạng thái lịch hẹn' };
            return { success: true, oldStatus: appointments[index].status, newStatus };
        },

        changeAppointmentTime(id, newTime, newCa) {
            const appointments = this.getAppointments();
            const index = appointments.findIndex(a => a.id === id);
            if (index === -1) return { success: false, error: 'Không tìm thấy lịch hẹn' };

            appointments[index].time = newTime;
            appointments[index].ca = newCa;
            appointments[index].timeUpdatedAt = new Date().toISOString();

            const saved = writeJSON(KEYS.APPOINTMENTS, appointments);
            if (!saved) return { success: false, error: 'Không thể lưu khung giờ mới' };
            return { success: true };
        },

        isSlotAvailable(doctorId, date, timeSlot, excludeApptId) {
            const appointments = this.getAppointments();
            return !appointments.some(a =>
                a.id !== excludeApptId &&
                a.doctorId === doctorId &&
                a.date === date &&
                a.time === timeSlot &&
                a.status !== 'cancelled' &&
                a.status !== 'noshow'
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
            if (!saved) return { success: false, error: 'Không thể lưu thông tin check-in' };

            const statusResult = this.updateAppointmentStatus(data.appointmentId, 'checked', 'Check-in tại quầy');
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
            const saved = writeJSON(KEYS.PAYMENTS, payments);
            return { success: saved };
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

            const todayPayments = payments.filter(p => {
                if (!p.paidAt) return false;
                return formatDate(new Date(p.paidAt)) === today;
            });

            const revenueToday = todayPayments.reduce(
                (sum, p) => sum + (parseInt(p.totalAmount, 10) || 0), 0
            );

            return {
                totalToday: todayAppointments.length,
                checkedIn: todayAppointments.filter(a => a.status === 'checked').length,
                pending: todayAppointments.filter(a => a.status === 'pending').length,
                confirmed: todayAppointments.filter(a => a.status === 'confirmed').length,
                cancelled: todayAppointments.filter(a => a.status === 'cancelled').length,
                noshow: todayAppointments.filter(a => a.status === 'noshow').length,
                revenueToday,
                byCa
            };
        },

        processOvernightAppointments() {
            const appointments = this.getAppointments();
            const today = todayStr();
            const changed = [];

            appointments.forEach(a => {
                if (
                    a.date < today &&
                    (a.status === 'pending' || a.status === 'confirmed')
                ) {
                    a.status = 'noshow';
                    a.statusUpdatedAt = new Date().toISOString();
                    a.statusReason = 'Tự động: Qua ngày';
                    changed.push(a.id);
                }
            });

            if (changed.length > 0) {
                writeJSON(KEYS.APPOINTMENTS, appointments);
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
    console.log('LT_Store.js loaded (Realtime)');
})();