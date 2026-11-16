/* ============================================================
   MEDBOOKING ADMIN — Live SQL Backend Data Layer (v2)
   Kết nối trực tiếp với cơ sở dữ liệu SQL Server thông qua FastAPI
   ============================================================ */
(function (global) {
    'use strict';

    console.log('[admin-data.js] Bắt đầu load Live API Layer (v2)...');

    function getToken() {
        return localStorage.getItem('medbooking_token') || '';
    }

    async function apiRequest(endpoint, options = {}) {
        const token = getToken();

        // Tự động thêm tiền tố /auth nếu đường dẫn bắt đầu bằng /admin hoặc chưa có /auth
        let url = endpoint;
        if (url.startsWith('/admin/')) {
            url = `/auth${url}`;
        } else if (!url.startsWith('/auth/') && !url.startsWith('http')) {
            url = `/auth/${url.replace(/^\/+/, '')}`;
        }

        const headers = {
            'Content-Type': 'application/json',
            ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
            ...(options.headers || {})
        };

        try {
            const response = await fetch(url, { ...options, headers });
            if (!response.ok) {
                const errDetail = await response.json().catch(() => ({}));
                throw new Error(errDetail.detail || `Lỗi HTTP: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error(`[API Error] ${url}:`, error);
            throw error;
        }
    }

    function formatMoney(n) {
        if (typeof n !== 'number') n = Number(n) || 0;
        return new Intl.NumberFormat('vi-VN').format(n) + ' ₫';
    }

    function formatDate(iso) {
        if (!iso) return '';
        return new Date(iso).toLocaleDateString('vi-VN');
    }

    // Hàm chuẩn hóa dữ liệu trả về từ API (hỗ trợ cả mảng trực tiếp lẫn object bọc .data)
    function extractList(res) {
        if (Array.isArray(res)) return res;
        if (res && Array.isArray(res.data)) return res.data;
        return [];
    }

    const liveAPI = {
        /* ACCOUNTS */
        async getAccounts(filters = {}) {
            const res = await apiRequest('/admin/tai-khoan');
            let list = extractList(res);

            if (filters.role && filters.role !== 'all') {
                list = list.filter(a => {
                    const r = (a.role || '').toLowerCase();
                    if (filters.role === 'quan_tri_vien' || filters.role === 'admin') return r === 'admin' || r === 'quan_tri_vien';
                    if (filters.role === 'bac_si' || filters.role === 'doctor') return r === 'doctor' || r === 'bac_si';
                    if (filters.role === 'le_tan' || filters.role === 'receptionist') return r === 'receptionist' || r === 'le_tan';
                    if (filters.role === 'benh_nhan' || filters.role === 'patient') return r === 'patient' || r === 'benh_nhan';
                    return r === filters.role;
                });
            }
            if (filters.status && filters.status !== 'all') {
                list = list.filter(a => {
                    const isActive = a.status === 'active' || a.status === true;
                    return filters.status === 'active' ? isActive : !isActive;
                });
            }
            if (filters.search) {
                const q = filters.search.toLowerCase();
                list = list.filter(a => (a.name || a.ho_ten || '').toLowerCase().includes(q) || (a.email || '').toLowerCase().includes(q) || (a.phone || a.so_dien_thoai || '').includes(q));
            }
            return { data: list, total: list.length };
        },
        async createAccount(data) {
            const res = await apiRequest('/admin/tai-khoan', {
                method: 'POST',
                body: JSON.stringify(data)
            });
            return { data: res.data || res };
        },
        async updateAccount(id, data) {
            const res = await apiRequest(`/admin/tai-khoan/${id}`, {
                method: 'PUT',
                body: JSON.stringify(data)
            });
            return { data: res.data || res };
        },
        async deleteAccount(id) {
            const res = await apiRequest(`/admin/tai-khoan/${id}`, {
                method: 'DELETE'
            });
            return { data: res.data || true };
        },
        async toggleAccountStatus(id, reason) {
            const res = await apiRequest(`/admin/tai-khoan/${id}/trang-thai`, {
                method: 'PUT',
                body: JSON.stringify({ reason })
            });
            return { data: res.data || res };
        },

        /* DOCTORS */
        async getDoctors(filters = {}) {
            const res = await apiRequest('/admin/bac-si');
            let list = extractList(res);

            list = list.map(d => ({
                id: d.id || `BS${d.ma_bac_si || '001'}`,
                name: d.name || d.ho_ten || 'Chưa cập nhật tên',
                specialtyId: String(d.specialtyId || d.chuyen_khoa_id || 'all'),
                specialtyName: d.specialtyName || d.ten_chuyen_khoa || 'Chưa phân khoa',
                email: d.email || '',
                phone: d.phone || d.so_dien_thoai || '',
                status: d.status || 'available',
                rating: typeof d.rating === 'number' ? d.rating : (parseFloat(d.rating) || parseFloat(d.diem_danh_gia) || 5.0)
            }));

            if (filters.specialtyId && filters.specialtyId !== 'all') {
                list = list.filter(d => d.specialtyId === filters.specialtyId);
            }
            if (filters.search) {
                const q = filters.search.toLowerCase();
                list = list.filter(d => (d.name || '').toLowerCase().includes(q) || (d.email || '').toLowerCase().includes(q));
            }
            return { data: list, total: list.length };
        },


        /* SPECIALTIES */
        async getSpecialties(filters = {}) {
            const res = await apiRequest('/admin/chuyen-khoa');
            let list = extractList(res);
            if (filters.search) {
                const q = filters.search.toLowerCase();
                list = list.filter(s => (s.name || '').toLowerCase().includes(q));
            }
            return { data: list, total: list.length };
        },
        async createSpecialty(data) {
            const res = await apiRequest('/admin/chuyen-khoa', {
                method: 'POST',
                body: JSON.stringify(data)
            });
            return { data: res.data || res };
        },
        async updateSpecialty(id, data) {
            const res = await apiRequest(`/admin/chuyen-khoa/${id}`, {
                method: 'PUT',
                body: JSON.stringify(data)
            });
            return { data: res.data || res };
        },
        async deleteSpecialty(id) {
            const res = await apiRequest(`/admin/chuyen-khoa/${id}`, {
                method: 'DELETE'
            });
            return { data: res.data || true };
        },

        /* SERVICES */
        async getServices(filters = {}) {
            const res = await apiRequest('/admin/dich-vu');
            let list = extractList(res);

            // Ánh xạ chuẩn xác các trường dữ liệu, đặc biệt là 'price'
            list = list.map(s => ({
                id: s.id || `DV${s.ma_dich_vu || '001'}`,
                name: s.name || s.ten_dich_vu || 'Dịch vụ y tế',
                specialtyId: String(s.specialtyId || s.chuyen_khoa_id || 'all'),
                specialtyName: s.specialtyName || s.ten_chuyen_khoa || 'Chưa phân khoa',
                price: Number(s.price || s.gia || s.gia_niem_yet || s.don_gia || s.chi_phi || 0),
                desc: s.desc || s.mo_ta || 'Chưa có mô tả chi tiết'
            }));

            if (filters.specialtyId && filters.specialtyId !== 'all') list = list.filter(s => s.specialtyId === filters.specialtyId);
            if (filters.search) {
                const q = filters.search.toLowerCase();
                list = list.filter(s => (s.name || '').toLowerCase().includes(q) || (s.id || '').toLowerCase().includes(q));
            }
            return { data: list, total: list.length };
        },
        /* MAPPINGS */
        async getMappings(filters = {}) {
            const res = await apiRequest('/admin/mappings');
            let list = extractList(res);
            if (filters.specialtyId && filters.specialtyId !== 'all') list = list.filter(m => m.specialtyId === filters.specialtyId);
            if (filters.search) {
                const q = filters.search.toLowerCase();
                list = list.filter(m => (m.keywords || '').toLowerCase().includes(q));
            }
            return { data: list, total: list.length };
        },
        async createMapping(data) {
            const res = await apiRequest('/admin/mappings', {
                method: 'POST',
                body: JSON.stringify(data)
            });
            return { data: res.data || res };
        },
        async updateMapping(id, data) {
            const res = await apiRequest(`/admin/mappings/${id}`, {
                method: 'PUT',
                body: JSON.stringify(data)
            });
            return { data: res.data || res };
        },
        async deleteMapping(id) {
            const res = await apiRequest(`/admin/mappings/${id}`, {
                method: 'DELETE'
            });
            return { data: res.data || true };
        },

        /* RECYCLE BIN */
        async getRecycleBin() {
            const res = await apiRequest('/admin/thung-rac');
            return { data: extractList(res) };
        },
        async restoreItem(id) {
            const res = await apiRequest(`/admin/thung-rac/${id}/khoi-phuc`, { method: 'POST' });
            return { data: res.data || true };
        },
        async deleteItemForever(id) {
            const res = await apiRequest(`/admin/thung-rac/${id}`, { method: 'DELETE' });
            return { data: res.data || true };
        },
        async emptyRecycleBin() {
            const res = await apiRequest('/admin/thung-rac', { method: 'DELETE' });
            return { data: res.data || true };
        },

        /* TRANSACTIONS & AUDIT LOGS */
        async getTransactions(filters = {}) {
            const res = await apiRequest('/admin/nhat-ky-giao-dich');
            let list = extractList(res);
            if (filters.year) list = list.filter(t => (t.date || '').startsWith(filters.year));
            if (filters.month && filters.month !== 'all') {
                list = list.filter(t => parseInt((t.date || '').split('-')[1], 10) === parseInt(filters.month, 10));
            }
            if (filters.status && filters.status !== 'all') list = list.filter(t => t.status === filters.status);
            return { data: list, total: list.length };
        },

        /* DASHBOARD STATS */
        async getDashboardStats(year = '2026', quarter='all') {
            try {
                const res = await apiRequest(`/admin/dashboard-stats?year=${year}&quarter=${quarter}`);
                return res;
            } catch (e) {
                const txRes = await this.getTransactions({ year });
                const list = txRes.data || [];
                const totalAppointments = list.length;
                const totalRevenue = list.filter(t => t.status === 'completed').reduce((s, t) => s + (t.revenue || 0), 0);
                const totalProfit = list.filter(t => t.status === 'completed').reduce((s, t) => s + (t.profit || 0), 0);
                const cancelled = list.filter(t => t.status === 'cancelled').length;
                const cancelRate = totalAppointments ? ((cancelled / totalAppointments) * 100).toFixed(1) : 0;
                return {
                    data: {
                        totalAppointments, totalRevenue, totalProfit, cancelRate,
                        topDoctor: { name: 'Đang cập nhật', rating: 5.0 },
                        revenueByMonth: [
                            { label: 'T2', value: 12, prev: 8 }, { label: 'T3', value: 19, prev: 14 },
                            { label: 'T4', value: 15, prev: 10 }, { label: 'T5', value: 27, prev: 18 },
                            { label: 'T6', value: 24, prev: 15 }, { label: 'T7', value: 32, prev: 22 },
                            { label: 'CN', value: 22, prev: 16 }
                        ]
                    }
                };
            }
        },

        /* NOTIFICATIONS */
        async getNotifications() {
            try {
                const res = await apiRequest('/admin/notifications');
                return { data: extractList(res) };
            } catch (e) {
                return { data: [] };
            }
        },
        async markAllRead() {
            try {
                await apiRequest('/admin/notifications/mark-read', { method: 'POST' });
            } catch (e) {}
            return { data: true };
        },
        async pushNotification(notif) {
            try {
                const res = await apiRequest('/admin/notifications', {
                    method: 'POST',
                    body: JSON.stringify(notif)
                });
                return { data: res.data || res };
            } catch (e) {
                return { data: notif };
            }
        },

        /* CURRENT USER */
        async getCurrentUser() {
            try {
                const res = await apiRequest('/me');
                return {
                    data: {
                        id: res.id || res.ma_quan_tri || 'AD001',
                        name: res.ho_ten || res.name || 'Admin',
                        ho_ten: res.ho_ten || res.name || 'Admin',
                        email: res.email || 'admin@medbooking.com',
                        avatar: (res.ho_ten || res.name || 'A').charAt(0).toUpperCase()
                    }
                };
            } catch (e) {
                return { data: { id: 'AD001', name: 'Hệ Thống Admin', email: 'admin@medbooking.com', avatar: 'A' } };
            }
        },
        async updateCurrentUser(data) {
            const res = await apiRequest('/me', {
                method: 'PUT',
                body: JSON.stringify(data)
            });
            return { data: res.data || res };
        },

        async resetAll() {
            return { data: true };
        }
    };

    global.MedBookingAPI = liveAPI;
    global.MedBookingUtils = { formatMoney, formatDate };
    console.log('[admin-data.js] ✅ Đã cập nhật hàm extractList tự động nhận mảng trực tiếp thành công.');

})(window);