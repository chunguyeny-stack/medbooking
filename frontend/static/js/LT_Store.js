/**
 * LT_Store.js - Lễ Tân Store
 * Quản lý dữ liệu localStorage cho module Lễ Tân
 * Prefix: medbooking_
 */

(function() {
    'use strict';

    const PREFIX = 'medbooking_';
    const KEYS = {
        APPOINTMENTS: PREFIX + 'appointments',
        PAYMENTS: PREFIX + 'payments',
        CHECKINS: PREFIX + 'checkins',
        INITIALIZED: PREFIX + 'initialized'
    };

    function todayStr() {
        return new Date().toISOString().split('T')[0];
    }

    function tomorrowStr() {
        const d = new Date();
        d.setDate(d.getDate() + 1);
        return d.toISOString().split('T')[0];
    }

    function readJSON(key, fallback) {
        try {
            const raw = localStorage.getItem(key);
            if (!raw) return fallback;
            return JSON.parse(raw);
        } catch (e) {
            console.error('LT_Store read error:', key, e);
            return fallback;
        }
    }

    function writeJSON(key, value) {
        try {
            localStorage.setItem(key, JSON.stringify(value));
            return true;
        } catch (e) {
            console.error('LT_Store write error:', key, e);
            return false;
        }
    }

    function seedAppointments() {
        const today = todayStr();
        const tomorrow = tomorrowStr();

        return [
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
                date: today,
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
                date: today,
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
                date: today,
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
                date: today,
                symptom: 'Đau đầu kéo dài, mất ngủ',
                status: 'checked',
                items: [
                    { name: 'Phí khám Thần kinh (ngoài giờ)', qty: 1, price: 330000 },
                    { name: 'Chụp CT sọ não', qty: 1, price: 800000 }
                ]
            },
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
                date: tomorrow,
                symptom: 'Tái khám định kỳ',
                status: 'confirmed',
                items: [
                    { name: 'Phí khám Tim mạch', qty: 1, price: 200000 }
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
                date: today,
                symptom: 'Ho khan, đau họng',
                status: 'pending',
                items: [
                    { name: 'Phí khám Nội tổng quát', qty: 1, price: 180000 },
                    { name: 'Test Covid', qty: 1, price: 100000 }
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
        }
    }

    const LT_Store = {
        getAppointments() {
            initIfNeeded();
            return readJSON(KEYS.APPOINTMENTS, []);
        },

        getAppointmentById(id) {
            const appts = this.getAppointments();
            return appts.find(a => a.id === id) || null;
        },

        updateAppointmentStatus(id, newStatus, reason) {
            const appts = this.getAppointments();
            const idx = appts.findIndex(a => a.id === id);
            if (idx === -1) return { success: false, error: 'Không tìm thấy lịch hẹn' };

            const oldStatus = appts[idx].status;
            appts[idx].status = newStatus;
            appts[idx].statusUpdatedAt = new Date().toISOString();
            appts[idx].statusReason = reason || '';
            writeJSON(KEYS.APPOINTMENTS, appts);

            return { success: true, oldStatus, newStatus };
        },

        changeAppointmentTime(id, newTime, newCa) {
            const appts = this.getAppointments();
            const idx = appts.findIndex(a => a.id === id);
            if (idx === -1) return { success: false, error: 'Không tìm thấy lịch hẹn' };

            appts[idx].time = newTime;
            appts[idx].ca = newCa;
            appts[idx].timeUpdatedAt = new Date().toISOString();
            writeJSON(KEYS.APPOINTMENTS, appts);

            return { success: true };
        },

        isSlotAvailable(doctorId, date, timeSlot, excludeApptId) {
            const appts = this.getAppointments();
            return !appts.some(a =>
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
            writeJSON(KEYS.CHECKINS, checkins);

            this.updateAppointmentStatus(data.appointmentId, 'checked', 'Check-in tại quầy');

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
            writeJSON(KEYS.PAYMENTS, payments);
            return { success: true };
        },

        // ⭐ HÀM MỚI: Tạo payment hoàn chỉnh (dùng cho vien_phi.html)
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
                totalAmount: parseInt(data.totalAmount) || 0,
                paymentMethod: data.paymentMethod || 'cash',
                cashierId: data.cashierId || null,
                cashierName: data.cashierName || '',
                paidAt: now.toISOString(),
                createdAt: now.toISOString()
            };

            payments.push(payment);
            const ok = writeJSON(KEYS.PAYMENTS, payments);

            if (!ok) {
                return { success: false, message: 'Không thể lưu giao dịch vào hệ thống' };
            }

            return { success: true, payment };
        },

        markAsPaid(appointmentId) {
            return { success: true };
        },

        isAlreadyPaid(appointmentId) {
            const payments = this.getPayments();
            return payments.some(p => p.appointmentId === appointmentId);
        },

        getDashboardStats() {
            const appts = this.getAppointments();
            const payments = this.getPayments();
            const today = todayStr();

            const todayAppts = appts.filter(a => a.date === today);

            const byCa = {
                sang: todayAppts.filter(a => a.ca === 'sang').length,
                chieu: todayAppts.filter(a => a.ca === 'chieu').length,
                toi: todayAppts.filter(a => a.ca === 'toi').length
            };

            const todayPayments = payments.filter(p => {
                if (!p.paidAt) return false;
                return new Date(p.paidAt).toDateString() === new Date().toDateString();
            });

            const revenueToday = todayPayments.reduce((sum, p) => sum + (parseInt(p.totalAmount) || 0), 0);

            return {
                totalToday: todayAppts.length,
                checkedIn: todayAppts.filter(a => a.status === 'checked').length,
                pending: todayAppts.filter(a => a.status === 'pending').length,
                confirmed: todayAppts.filter(a => a.status === 'confirmed').length,
                cancelled: todayAppts.filter(a => a.status === 'cancelled').length,
                noshow: todayAppts.filter(a => a.status === 'noshow').length,
                revenueToday,
                byCa
            };
        },

        processOvernightAppointments() {
            const appts = this.getAppointments();
            const today = todayStr();
            const changed = [];

            appts.forEach(a => {
                if (a.date < today && (a.status === 'pending' || a.status === 'confirmed')) {
                    a.status = 'noshow';
                    a.statusUpdatedAt = new Date().toISOString();
                    a.statusReason = 'Tự động: Qua ngày';
                    changed.push(a.id);
                }
            });

            if (changed.length > 0) {
                writeJSON(KEYS.APPOINTMENTS, appts);
            }

            return changed;
        },

        reset() {
            Object.values(KEYS).forEach(k => localStorage.removeItem(k));
            initIfNeeded();
        }
    };

    window.LT_Store = LT_Store;
    initIfNeeded();
    console.log('✅ LT_Store.js loaded');
})();