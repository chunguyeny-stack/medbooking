/* ============================================================
   MEDBOOKING ADMIN — UI Controller (v13)
   Update: Hoạt động thông báo (Notifications) đầy đủ
   ============================================================ */
(function () {
    'use strict';

    console.log('[admin.js] Bắt đầu load...');

    function waitForAPI(cb) {
        if (window.MedBookingAPI) return cb(window.MedBookingAPI);
        let tries = 0;
        const t = setInterval(() => {
            tries++;
            if (window.MedBookingAPI) {
                clearInterval(t);
                cb(window.MedBookingAPI);
            } else if (tries > 50) {
                clearInterval(t);
                console.error('[admin.js] ❌ MedBookingAPI không load!');
            }
        }, 100);
    }

    const $ = (s, r = document) => r.querySelector(s);
    const $$ = (s, r = document) => [...r.querySelectorAll(s)];

    /* ============================================================
       1. TOAST NOTIFICATION
       ============================================================ */
    function toast(msg, type = 'info', title = null) {
        let container = document.getElementById('mb-toast-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'mb-toast-container';
            container.style.cssText = 'position:fixed;top:20px;right:20px;z-index:99999;display:flex;flex-direction:column;gap:10px;pointer-events:none;';
            document.body.appendChild(container);
        }

        const cfg = {
            success: { bg: '#10B981', icon: 'check', title: 'Thành công' },
            error:   { bg: '#EF4444', icon: 'xmark', title: 'Lỗi' },
            warning: { bg: '#F59E0B', icon: 'triangle-exclamation', title: 'Cảnh báo' },
            info:    { bg: '#8B5CF6', icon: 'circle-info', title: 'Thông báo' }
        };
        const c = cfg[type] || cfg.info;

        if (!document.getElementById('mb-toast-keyframes')) {
            const style = document.createElement('style');
            style.id = 'mb-toast-keyframes';
            style.textContent = '@keyframes mbToastProgress{from{transform:scaleX(1)}to{transform:scaleX(0)}}';
            document.head.appendChild(style);
        }

        const el = document.createElement('div');
        el.style.cssText = `
            display:flex;align-items:center;gap:12px;
            padding:14px 18px;border-radius:14px;
            background:var(--bg-card,#fff);
            border:1px solid var(--border-glass,rgba(139,92,246,0.15));
            box-shadow:0 12px 32px rgba(0,0,0,0.18);
            font-family:Inter,sans-serif;font-size:13.5px;font-weight:500;
            color:var(--secondary-color,#1A1428);
            min-width:300px;max-width:420px;pointer-events:auto;
            transform:translateX(120%);
            transition:transform .4s cubic-bezier(.16,1,.3,1);
            position:relative;overflow:hidden;
        `;
        el.innerHTML = `
            <div style="width:36px;height:36px;border-radius:10px;background:${c.bg};color:#fff;display:flex;align-items:center;justify-content:center;font-size:15px;flex-shrink:0;">
                <i class="fas fa-${c.icon}"></i>
            </div>
            <div style="flex:1;min-width:0;line-height:1.45;">
                <div style="font-weight:700;font-size:13.5px;margin-bottom:2px;">${title || c.title}</div>
                <div style="font-size:12.5px;color:var(--text-gray,#6B6480);">${msg}</div>
            </div>
            <button style="background:none;border:none;color:var(--text-gray,#6B6480);cursor:pointer;font-size:14px;padding:4px;border-radius:6px;width:auto;flex-shrink:0;">
                <i class="fas fa-xmark"></i>
            </button>
            <div style="position:absolute;bottom:0;left:0;height:3px;width:100%;background:${c.bg};transform-origin:left;animation:mbToastProgress 3.2s linear forwards;"></div>
        `;

        container.appendChild(el);
        requestAnimationFrame(() => el.style.transform = 'translateX(0)');

        const remove = () => {
            el.style.transform = 'translateX(120%)';
            setTimeout(() => el.remove(), 400);
        };
        el.querySelector('button').addEventListener('click', remove);
        setTimeout(remove, 3200);
    }

    /* ============================================================
       2. KEYFRAMES DÙNG CHUNG CHO MODAL
       ============================================================ */
    function ensureModalKeyframes() {
        if (document.getElementById('mb-modal-keyframes')) return;
        const style = document.createElement('style');
        style.id = 'mb-modal-keyframes';
        style.textContent = `
            @keyframes modalIn{from{opacity:0;transform:translateY(20px) scale(0.95)}to{opacity:1;transform:translateY(0) scale(1)}}
            @keyframes pulseWarn{0%,100%{box-shadow:0 0 0 0 rgba(220,38,38,0.5)}50%{box-shadow:0 0 0 10px rgba(220,38,38,0)}}
            @keyframes pulseAmber{0%,100%{box-shadow:0 0 0 0 rgba(245,158,11,0.5)}50%{box-shadow:0 0 0 10px rgba(245,158,11,0)}}
        `;
        document.head.appendChild(style);
    }

    /* ============================================================
       3. MODAL XÁC NHẬN XÓA MỀM (Chuyển vào Thùng rác)
       ============================================================ */
    window.MedBookingConfirmDelete = function (options) {
        const opts = options || {};
        const title    = opts.title    || 'Xác nhận xóa';
        const itemName = opts.itemName || '';
        const itemType = opts.itemType || 'bản ghi';
        const onConfirm = opts.onConfirm;

        ensureModalKeyframes();

        const overlay = document.createElement('div');
        overlay.style.cssText = 'position:fixed;inset:0;background:rgba(13,8,32,0.6);backdrop-filter:blur(6px);z-index:99998;display:flex;align-items:center;justify-content:center;padding:20px;';

        const modal = document.createElement('div');
        modal.style.cssText = `
            background:var(--bg-card,#fff); border-radius:20px; padding:24px;
            max-width:460px; width:100%; box-shadow:0 25px 60px rgba(0,0,0,0.3);
            border:1px solid var(--border-glass,rgba(139,92,246,0.15));
            font-family:Inter,sans-serif; animation: modalIn 0.3s cubic-bezier(0.16,1,0.3,1);
        `;

        const typeLabel = itemType.charAt(0).toUpperCase() + itemType.slice(1);

        modal.innerHTML = `
            <h3 style="font-size:18px;font-weight:700;color:var(--secondary-color,#1A1428);margin-bottom:16px;padding-bottom:16px;border-bottom:1px solid var(--border-glass,rgba(139,92,246,0.15));display:flex;align-items:center;gap:10px;">
                <i class="fas fa-trash-can" style="color:#F59E0B;"></i> ${title}
            </h3>

            <div style="display:flex;gap:14px;padding:16px;background:#FFFBEB;border:1px solid #FDE68A;border-radius:14px;margin-bottom:18px;">
                <div style="width:42px;height:42px;border-radius:50%;background:#F59E0B;color:#fff;display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0;animation:pulseAmber 1.6s infinite;">
                    <i class="fas fa-triangle-exclamation"></i>
                </div>
                <div style="font-size:13px;color:#92400E;line-height:1.55;">
                    ${typeLabel} sẽ được <strong>chuyển vào Thùng rác hệ thống</strong>.
                    Bạn có thể khôi phục lại sau này.
                </div>
            </div>

            ${itemName ? `<div style="background:var(--bg-body,#F7F5FC);border:1px solid var(--border-glass,rgba(139,92,246,0.15));border-radius:12px;padding:12px 16px;margin-bottom:18px;font-size:13px;">
                <strong>Đối tượng:</strong> ${itemName}
            </div>` : ''}

            <div style="display:flex;gap:10px;justify-content:flex-end;">
                <button type="button" id="mb-del-cancel" style="padding:10px 20px;border-radius:50px;font-size:14px;font-weight:600;cursor:pointer;border:1px solid var(--border-glass,#DDD6FE);color:var(--text-gray,#6B6480);background:transparent;font-family:inherit;transition:all 0.2s;">
                    Hủy bỏ
                </button>
                <button type="button" id="mb-del-ok" style="padding:10px 20px;border-radius:50px;font-size:14px;font-weight:600;cursor:pointer;border:none;color:#fff;background:#F59E0B;box-shadow:0 5px 15px rgba(245,158,11,0.4);font-family:inherit;display:inline-flex;align-items:center;gap:8px;transition:all 0.2s;">
                    <i class="fas fa-trash-can"></i> Xóa & chuyển vào thùng rác
                </button>
            </div>
        `;

        overlay.appendChild(modal);
        document.body.appendChild(overlay);

        const close = () => {
            modal.style.animation = 'modalIn 0.2s reverse forwards';
            setTimeout(() => overlay.remove(), 200);
        };

        document.getElementById('mb-del-cancel').onclick = close;
        document.getElementById('mb-del-ok').onclick = () => {
            close();
            if (typeof onConfirm === 'function') onConfirm();
        };
        overlay.addEventListener('click', (e) => { if (e.target === overlay) close(); });

        const escHandler = (e) => {
            if (e.key === 'Escape') { close(); document.removeEventListener('keydown', escHandler); }
        };
        document.addEventListener('keydown', escHandler);
    };

    /* ============================================================
       4. MODAL XÁC NHẬN XÓA VĨNH VIỄN (Chỉ dùng cho trang Thùng Rác)
       ============================================================ */
    window.MedBookingConfirmPurge = function (title, message, itemName, onConfirm) {
        ensureModalKeyframes();

        const overlay = document.createElement('div');
        overlay.style.cssText = 'position:fixed;inset:0;background:rgba(13,8,32,0.6);backdrop-filter:blur(6px);z-index:99998;display:flex;align-items:center;justify-content:center;padding:20px;';

        const modal = document.createElement('div');
        modal.style.cssText = `
            background:var(--bg-card,#fff); border-radius:20px; padding:24px;
            max-width:440px; width:100%; box-shadow:0 25px 60px rgba(0,0,0,0.3);
            border:1px solid var(--border-glass,rgba(139,92,246,0.15));
            font-family:Inter,sans-serif; animation: modalIn 0.3s cubic-bezier(0.16,1,0.3,1);
        `;

        modal.innerHTML = `
            <h3 style="font-size:18px;font-weight:700;color:var(--secondary-color,#1A1428);margin-bottom:16px;padding-bottom:16px;border-bottom:1px solid var(--border-glass,rgba(139,92,246,0.15));display:flex;align-items:center;gap:10px;">
                <i class="fas fa-triangle-exclamation" style="color:#DC2626;"></i> ${title}
            </h3>

            <div style="display:flex;gap:14px;padding:16px;background:#FEF2F2;border:1px solid #FECACA;border-radius:14px;margin-bottom:18px;">
                <div style="width:42px;height:42px;border-radius:50%;background:#DC2626;color:#fff;display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0;animation:pulseWarn 1.6s infinite;">
                    <i class="fas fa-skull-crossbones"></i>
                </div>
                <div style="font-size:13px;color:#991B1B;line-height:1.55;">
                    ${message} Hành động này <strong>không thể hoàn tác</strong>.
                </div>
            </div>

            ${itemName ? `<div style="background:var(--bg-body,#F7F5FC);border:1px solid var(--border-glass,rgba(139,92,246,0.15));border-radius:12px;padding:12px 16px;margin-bottom:18px;font-size:13px;">
                <strong>Đối tượng:</strong> ${itemName}
            </div>` : ''}

            <label style="display:block;font-size:13px;color:var(--text-gray,#6B6480);margin-bottom:8px;">
                Nhập <code style="background:var(--primary-light,#EDE9FE);color:var(--primary-color,#8B5CF6);padding:2px 8px;border-radius:6px;font-weight:700;font-family:monospace;">XOA</code> để xác nhận:
            </label>
            <input type="text" id="mb-confirm-input" placeholder="XOA" maxlength="3" autocomplete="off"
                   style="width:100%;text-align:center;letter-spacing:4px;font-weight:700;text-transform:uppercase;padding:12px;border:1px solid var(--input-border,#DDD6FE);border-radius:12px;background:var(--input-bg,#fff);color:var(--secondary-color,#1A1428);font-family:inherit;outline:none;margin-bottom:20px;">

            <div style="display:flex;gap:10px;justify-content:flex-end;">
                <button type="button" id="mb-confirm-cancel" style="padding:10px 20px;border-radius:50px;font-size:14px;font-weight:600;cursor:pointer;border:1px solid var(--border-glass,#DDD6FE);color:var(--text-gray,#6B6480);background:transparent;font-family:inherit;transition:all 0.2s;">
                    Hủy bỏ
                </button>
                <button type="button" id="mb-confirm-ok" style="padding:10px 20px;border-radius:50px;font-size:14px;font-weight:600;cursor:pointer;border:none;color:#fff;background:#DC2626;box-shadow:0 5px 15px rgba(220,38,38,0.4);font-family:inherit;display:inline-flex;align-items:center;gap:8px;transition:all 0.2s;">
                    <i class="fas fa-trash-can"></i> Xóa vĩnh viễn
                </button>
            </div>
        `;

        overlay.appendChild(modal);
        document.body.appendChild(overlay);

        const input = document.getElementById('mb-confirm-input');
        setTimeout(() => input.focus(), 100);

        const close = () => {
            modal.style.animation = 'modalIn 0.2s reverse forwards';
            setTimeout(() => overlay.remove(), 200);
        };

        document.getElementById('mb-confirm-cancel').onclick = close;
        document.getElementById('mb-confirm-ok').onclick = () => {
            if (input.value.trim().toUpperCase() !== 'XOA') {
                toast('Vui lòng nhập đúng chữ XOA để xác nhận.', 'error', 'Sai xác nhận');
                input.focus();
                return;
            }
            close();
            if (typeof onConfirm === 'function') onConfirm();
        };
        overlay.addEventListener('click', (e) => { if (e.target === overlay) close(); });
    };

    function openModal(id) {
        const m = document.getElementById(id);
        if (m) { m.style.display = 'block'; document.body.classList.add('modal-open'); }
    }
    function closeModal(id) {
        const m = document.getElementById(id);
        if (m) { m.style.display = 'none'; document.body.classList.remove('modal-open'); }
    }

    const roleText = { admin: 'Quản trị viên', doctor: 'Bác sĩ', receptionist: 'Lễ tân', patient: 'Bệnh nhân' };

    /* ============================================================
       5. TRANG QUẢN LÝ TÀI KHOẢN
       ============================================================ */
    function initAccountPage(API) {
        const tbody = document.getElementById('account-table-body');
        if (!tbody) return;

        const searchEl = document.getElementById('search-account');
        const roleEl = document.getElementById('filter-role');
        const statusEl = document.getElementById('filter-status');
        const btnAdd = document.getElementById('btn-add-account');
        const form = document.getElementById('form-account-info');
        const modalId = 'account-form-modal';
        const lockModalId = 'lock-modal';
        let editingId = null;

        function escapeHtml(str) {
            return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#39;');
        }

        async function refresh() {
            const res = await API.getAccounts({
                search: searchEl?.value || '',
                role: roleEl?.value || 'all',
                status: statusEl?.value || 'all'
            });
            if (!res.data.length) {
                tbody.innerHTML = `<tr><td colspan="7" style="text-align:center;padding:40px;color:#8B7FA8;">Không có tài khoản nào.</td></tr>`;
                return;
            }
            tbody.innerHTML = res.data.map(a => {
                const isActive = a.status === 'active';
                const lockTitle = (!isActive && a.lockReason) ? `title="Lý do khóa: ${escapeHtml(a.lockReason)}"` : '';
                return `<tr>
                    <td><strong>${a.id}</strong></td>
                    <td>${a.name}</td>
                    <td>${a.email}</td>
                    <td>${a.phone}</td>
                    <td>${roleText[a.role] || a.role}</td>
                    <td><span class="badge ${isActive ? 'success' : 'danger'}" ${lockTitle} style="cursor:${isActive ? 'default' : 'help'};">${isActive ? 'Đang hoạt động' : 'Đã khóa'}</span></td>
                    <td>
                        <button type="button" class="btn-edit-account" data-id="${a.id}">Sửa</button>
                        <button type="button" class="btn-toggle-lock" data-id="${a.id}" data-action="${isActive ? 'lock' : 'unlock'}">${isActive ? 'Khóa' : 'Mở khóa'}</button>
                        <button type="button" class="btn-delete-account" data-id="${a.id}" style="background:#FEF2F2;color:#DC2626;border-color:#FECACA;">Xóa</button>
                    </td>
                </tr>`;
            }).join('');

            $$('.btn-edit-account', tbody).forEach(btn => btn.onclick = async () => {
                const res = await API.getAccounts();
                const acc = res.data.find(x => x.id === btn.dataset.id);
                if (!acc) return;
                editingId = acc.id;
                $('#form-account-title').textContent = 'Chỉnh sửa tài khoản';
                $('#acc-name').value = acc.name;
                $('#acc-email').value = acc.email;
                $('#acc-phone').value = acc.phone;
                $('#acc-role').value = acc.role;
                $('#acc-password').value = '';
                openModal(modalId);
            });

            $$('.btn-toggle-lock', tbody).forEach(btn => btn.onclick = () => {
                const id = btn.dataset.id;
                if (btn.dataset.action === 'lock') {
                    $('#lock-target-id').value = id;
                    $('#lock-reason-text').value = '';
                    openModal(lockModalId);
                    setTimeout(() => $('#lock-reason-text').focus(), 200);
                } else {
                    API.toggleAccountStatus(id).then(() => { toast('Tài khoản đã được mở khóa.', 'success', 'Mở khóa thành công'); refresh(); }).catch(err => toast(err.message, 'error'));
                }
            });

            $$('.btn-delete-account', tbody).forEach(btn => btn.onclick = () => {
                const id = btn.dataset.id;
                const row = btn.closest('tr');
                const name = row ? row.children[1].textContent.trim() : id;
                const email = row ? row.children[2].textContent.trim() : '';
                window.MedBookingConfirmDelete({
                    title: 'Xóa tài khoản',
                    itemName: `${name}${email ? ' — ' + email : ''} (${id})`,
                    itemType: 'tài khoản',
                    onConfirm: async () => {
                        try {
                            await API.deleteAccount(id);
                            toast('Tài khoản đã được chuyển vào Thùng rác.', 'success', 'Đã xóa');
                            refresh();
                        } catch (err) {
                            toast(err.message || 'Không thể xóa tài khoản', 'error');
                        }
                    }
                });
            });
        }

        if (searchEl) searchEl.addEventListener('input', refresh);
        if (roleEl) roleEl.addEventListener('change', refresh);
        if (statusEl) statusEl.addEventListener('change', refresh);
        if (btnAdd) btnAdd.onclick = () => {
            editingId = null;
            form.reset();
            $('#form-account-title').textContent = 'Thêm Tài khoản Mới';
            openModal(modalId);
        };
        if (form) form.onsubmit = async (e) => {
            e.preventDefault();
            const data = { name: $('#acc-name').value.trim(), email: $('#acc-email').value.trim(), phone: $('#acc-phone').value.trim(), role: $('#acc-role').value };
            if (!data.name || !data.email || !data.phone) return toast('Thiếu thông tin', 'error');
            if (editingId) { await API.updateAccount(editingId, data); toast('Đã cập nhật', 'success'); }
            else { await API.createAccount(data); toast('Đã thêm tài khoản', 'success'); }
            closeModal(modalId); refresh();
        };
        const btnCancel = $('#btn-cancel-account');
        if (btnCancel) btnCancel.onclick = () => closeModal(modalId);

        const lockForm = $('#form-lock-reason');
        if (lockForm) lockForm.onsubmit = async (e) => {
            e.preventDefault();
            const reason = $('#lock-reason-text').value.trim();
            if (reason.length < 5) return toast('Lý do quá ngắn', 'error');
            await API.toggleAccountStatus($('#lock-target-id').value, reason);
            toast('Đã khóa tài khoản', 'warning', 'Đã khóa');
            closeModal(lockModalId); refresh();
        };
        const btnCancelLock = $('#btn-cancel-lock');
        if (btnCancelLock) btnCancelLock.onclick = () => closeModal(lockModalId);

        refresh();
    }

    /* ============================================================
       6. TRANG QUẢN LÝ BÁC SĨ
       ============================================================ */
    function initDoctorPage(API) {
        const tbody = document.getElementById('doctor-table-body');
        if (!tbody) return;
        const searchEl = $('#search-doctor');
        const filterSpec = $('#filter-specialty');
        const btnAdd = $('#btn-add-doctor');
        const form = $('#form-doctor-info');
        const modalId = 'doctor-form-modal';
        let editingId = null;

        API.getSpecialties().then(specRes => {
            if (filterSpec) filterSpec.innerHTML = '<option value="all">Tất cả chuyên khoa</option>' + specRes.data.map(s => `<option value="${s.id}">${s.name}</option>`).join('');
            if ($('#doc-specialty')) $('#doc-specialty').innerHTML = specRes.data.map(s => `<option value="${s.id}">${s.name}</option>`).join('');
        });

        function fillDoctorForm(d) {
            $('#doc-name').value = d.name || '';
            $('#doc-specialty').value = d.specialtyId || '';
            $('#doc-email').value = d.email || '';
            $('#doc-phone').value = d.phone || '';
            if ($('#doc-degree')) $('#doc-degree').value = d.degree || '';
            if ($('#doc-exp')) $('#doc-exp').value = d.experience || '';
            if ($('#doc-avatar')) $('#doc-avatar').value = d.avatar || '';
            if ($('#doc-bio')) $('#doc-bio').value = d.bio || '';
            if ($('#doc-training')) $('#doc-training').value = d.training || '';
            if ($('#doc-work-history')) $('#doc-work-history').value = d.workHistory || '';
            if ($('#doc-strengths')) $('#doc-strengths').value = d.strengths || '';
            if ($('#doc-fee')) $('#doc-fee').value = d.fee || 300000;
        }

        function readDoctorForm() {
            return {
                name: $('#doc-name').value.trim(),
                specialtyId: $('#doc-specialty').value,
                email: $('#doc-email').value.trim(),
                phone: $('#doc-phone').value.trim(),
                degree: $('#doc-degree') ? $('#doc-degree').value.trim() : '',
                experience: $('#doc-exp') ? Number($('#doc-exp').value) || 0 : 0,
                avatar: $('#doc-avatar') ? $('#doc-avatar').value.trim() : '',
                bio: $('#doc-bio') ? $('#doc-bio').value.trim() : '',
                training: $('#doc-training') ? $('#doc-training').value.trim() : '',
                workHistory: $('#doc-work-history') ? $('#doc-work-history').value.trim() : '',
                strengths: $('#doc-strengths') ? $('#doc-strengths').value.trim() : '',
                fee: $('#doc-fee') ? Number($('#doc-fee').value) || 300000 : 300000
            };
        }

        async function refresh() {
            const res = await API.getDoctors({ search: searchEl?.value || '', specialtyId: filterSpec?.value || 'all' });
            if (!res.data.length) return tbody.innerHTML = `<tr><td colspan="7" style="text-align:center;padding:40px;color:#8B7FA8;">Không có bác sĩ nào.</td></tr>`;

            tbody.innerHTML = res.data.map(d => `<tr>
                <td><strong>${d.id}</strong></td>
                <td>${d.name}</td>
                <td>${d.specialtyName}</td>
                <td>${d.email}<br><small style="color:var(--text-gray);">${d.phone || ''}</small></td>
                <td><span class="badge ${d.status === 'available' ? 'success' : 'danger'}">${d.status === 'available' ? 'Đang trực' : 'Nghỉ'}</span></td>
                <td><span style="color:#F59E0B;">★</span> ${(d.rating || 0).toFixed(1)}</td>
                <td>
                    <button type="button" class="btn-edit-doctor" data-id="${d.id}">Sửa</button>
                    <button type="button" class="btn-delete-doctor" data-id="${d.id}" style="background:#FEF2F2;color:#DC2626;border-color:#FECACA;">Xóa</button>
                </td>
            </tr>`).join('');

            $$('.btn-edit-doctor', tbody).forEach(btn => btn.onclick = async () => {
                const r = await API.getDoctors();
                const d = r.data.find(x => x.id === btn.dataset.id);
                if (!d) return;
                editingId = d.id;
                $('#form-title').textContent = 'Chỉnh sửa Bác sĩ';
                fillDoctorForm(d);
                openModal(modalId);
            });

            $$('.btn-delete-doctor', tbody).forEach(btn => btn.onclick = () => {
                const id = btn.dataset.id;
                const row = btn.closest('tr');
                const name = row ? row.children[1].textContent.trim() : id;
                const spec = row ? row.children[2].textContent.trim() : '';
                window.MedBookingConfirmDelete({
                    title: 'Xóa bác sĩ',
                    itemName: `${name}${spec ? ' — ' + spec : ''} (${id})`,
                    itemType: 'bác sĩ',
                    onConfirm: async () => {
                        try {
                            await API.deleteDoctor(id);
                            toast('Bác sĩ đã được chuyển vào Thùng rác.', 'success', 'Đã xóa');
                            refresh();
                        } catch (err) {
                            toast(err.message || 'Không thể xóa bác sĩ', 'error');
                        }
                    }
                });
            });
        }
        if (searchEl) searchEl.addEventListener('input', refresh);
        if (filterSpec) filterSpec.addEventListener('change', refresh);
        if (btnAdd) btnAdd.onclick = () => {
            editingId = null;
            form.reset();
            $('#form-title').textContent = 'Thêm Bác sĩ Mới';
            if ($('#doc-fee')) $('#doc-fee').value = 300000;
            openModal(modalId);
        };
        if (form) form.onsubmit = async (e) => {
            e.preventDefault();
            const data = readDoctorForm();
            if (!data.name || !data.email) return toast('Thiếu thông tin bắt buộc', 'error');
            if (editingId) { await API.updateDoctor(editingId, data); toast('Đã cập nhật bác sĩ', 'success'); }
            else { await API.createDoctor(data); toast('Đã thêm bác sĩ', 'success'); }
            closeModal(modalId); refresh();
        };
        const btnCancel = $('#btn-cancel-doctor');
        if (btnCancel) btnCancel.onclick = () => closeModal(modalId);
        refresh();
    }

    /* ============================================================
       7. TRANG QUẢN LÝ CHUYÊN KHOA
       ============================================================ */
    function initSpecialtyPage(API) {
        const tbody = document.getElementById('specialty-table-body');
        if (!tbody) return;

        const searchEl = document.getElementById('search-specialty');
        const btnAdd = document.getElementById('btn-add-specialty');
        const form = document.getElementById('form-specialty-info');
        const modalId = 'specialty-form-modal';
        let editingId = null;

        async function refresh() {
            const res = await API.getSpecialties({ search: searchEl?.value || '' });
            if (!res.data.length) {
                tbody.innerHTML = `<tr><td colspan="5" style="text-align:center;padding:40px;color:#8B7FA8;">Không có chuyên khoa nào.</td></tr>`;
                return;
            }
            tbody.innerHTML = res.data.map(s => `<tr>
                <td><strong>${s.id}</strong></td>
                <td>${s.name}</td>
                <td>${s.desc || '—'}</td>
                <td>${s.doctorCount || 0}</td>
                <td>
                    <button type="button" class="btn-edit-spec" data-id="${s.id}">Sửa</button>
                    <button type="button" class="btn-delete-spec" data-id="${s.id}" style="background:#FEF2F2;color:#DC2626;border-color:#FECACA;">Xóa</button>
                </td>
            </tr>`).join('');

            tbody.querySelectorAll('.btn-edit-spec').forEach(btn => btn.onclick = async () => {
                const r = await API.getSpecialties();
                const item = r.data.find(x => x.id === btn.dataset.id);
                if (!item) return;
                editingId = item.id;
                document.getElementById('form-specialty-title').textContent = 'Chỉnh sửa chuyên khoa';
                document.getElementById('spec-name').value = item.name;
                document.getElementById('spec-desc').value = item.desc || '';
                openModal(modalId);
            });

            tbody.querySelectorAll('.btn-delete-spec').forEach(btn => btn.onclick = () => {
                const id = btn.dataset.id;
                const row = btn.closest('tr');
                const name = row ? row.children[1].textContent.trim() : id;
                window.MedBookingConfirmDelete({
                    title: 'Xóa chuyên khoa',
                    itemName: `${name} (${id})`,
                    itemType: 'chuyên khoa',
                    onConfirm: async () => {
                        try {
                            await API.deleteSpecialty(id);
                            toast('Chuyên khoa đã được chuyển vào Thùng rác.', 'success', 'Đã xóa');
                            refresh();
                        } catch (err) {
                            toast(err.message || 'Không thể xóa chuyên khoa', 'error');
                        }
                    }
                });
            });
        }

        if (searchEl) searchEl.addEventListener('input', refresh);
        if (btnAdd) btnAdd.onclick = () => {
            editingId = null;
            form.reset();
            document.getElementById('form-specialty-title').textContent = 'Thêm Chuyên khoa Mới';
            openModal(modalId);
        };
        if (form) form.onsubmit = async (e) => {
            e.preventDefault();
            const data = {
                name: document.getElementById('spec-name').value.trim(),
                desc: document.getElementById('spec-desc').value.trim()
            };
            if (!data.name) return toast('Vui lòng nhập tên chuyên khoa', 'error');
            if (editingId) { await API.updateSpecialty(editingId, data); toast('Đã cập nhật chuyên khoa', 'success'); }
            else { await API.createSpecialty(data); toast('Đã thêm chuyên khoa', 'success'); }
            closeModal(modalId); refresh();
        };
        const btnCancel = document.getElementById('btn-cancel-specialty');
        if (btnCancel) btnCancel.onclick = () => closeModal(modalId);

        refresh();
    }

    /* ============================================================
       8. TRANG QUẢN LÝ DỊCH VỤ
       ============================================================ */
    function initServicePage(API) {
        const tbody = document.getElementById('service-table-body');
        if (!tbody) return;

        const searchEl = document.getElementById('search-service');
        const filterSpec = document.getElementById('filter-service-specialty');
        const btnAdd = document.getElementById('btn-add-service');
        const form = document.getElementById('form-service-info');
        const modalId = 'service-form-modal';
        let editingId = null;

        function fmtMoney(n) { return new Intl.NumberFormat('vi-VN').format(n) + ' ₫'; }

        API.getSpecialties().then(r => {
            if (filterSpec) filterSpec.innerHTML = '<option value="all">Tất cả chuyên khoa</option>' + r.data.map(s => `<option value="${s.id}">${s.name}</option>`).join('');
            const sel = document.getElementById('serv-specialty');
            if (sel) sel.innerHTML = r.data.map(s => `<option value="${s.id}">${s.name}</option>`).join('');
        });

        async function refresh() {
            const res = await API.getServices({ search: searchEl?.value || '', specialtyId: filterSpec?.value || 'all' });
            if (!res.data.length) {
                tbody.innerHTML = `<tr><td colspan="6" style="text-align:center;padding:40px;color:#8B7FA8;">Không có dịch vụ nào.</td></tr>`;
                return;
            }
            tbody.innerHTML = res.data.map(s => `<tr>
                <td><strong>${s.id}</strong></td>
                <td>${s.name}</td>
                <td>${s.specialtyName || '—'}</td>
                <td style="color:#10B981;font-weight:700;">${fmtMoney(s.price)}</td>
                <td>${s.desc || '—'}</td>
                <td>
                    <button type="button" class="btn-edit-serv" data-id="${s.id}">Sửa</button>
                    <button type="button" class="btn-delete-serv" data-id="${s.id}" style="background:#FEF2F2;color:#DC2626;border-color:#FECACA;">Xóa</button>
                </td>
            </tr>`).join('');

            tbody.querySelectorAll('.btn-edit-serv').forEach(btn => btn.onclick = async () => {
                const r = await API.getServices();
                const item = r.data.find(x => x.id === btn.dataset.id);
                if (!item) return;
                editingId = item.id;
                document.getElementById('form-service-title').textContent = 'Chỉnh sửa dịch vụ';
                document.getElementById('serv-name').value = item.name;
                document.getElementById('serv-specialty').value = item.specialtyId;
                document.getElementById('serv-price').value = item.price;
                document.getElementById('serv-desc').value = item.desc || '';
                openModal(modalId);
            });

            tbody.querySelectorAll('.btn-delete-serv').forEach(btn => btn.onclick = () => {
                const id = btn.dataset.id;
                const row = btn.closest('tr');
                const name = row ? row.children[1].textContent.trim() : id;
                window.MedBookingConfirmDelete({
                    title: 'Xóa dịch vụ',
                    itemName: `${name} (${id})`,
                    itemType: 'dịch vụ',
                    onConfirm: async () => {
                        try {
                            await API.deleteService(id);
                            toast('Dịch vụ đã được chuyển vào Thùng rác.', 'success', 'Đã xóa');
                            refresh();
                        } catch (err) {
                            toast(err.message || 'Không thể xóa dịch vụ', 'error');
                        }
                    }
                });
            });
        }

        if (searchEl) searchEl.addEventListener('input', refresh);
        if (filterSpec) filterSpec.addEventListener('change', refresh);
        if (btnAdd) btnAdd.onclick = () => {
            editingId = null; form.reset();
            document.getElementById('form-service-title').textContent = 'Thêm Dịch Vụ Mới';
            openModal(modalId);
        };
        if (form) form.onsubmit = async (e) => {
            e.preventDefault();
            const data = {
                name: document.getElementById('serv-name').value.trim(),
                specialtyId: document.getElementById('serv-specialty').value,
                price: Number(document.getElementById('serv-price').value),
                desc: document.getElementById('serv-desc').value.trim()
            };
            if (!data.name || !data.specialtyId) return toast('Thiếu thông tin', 'error');
            if (editingId) { await API.updateService(editingId, data); toast('Đã cập nhật dịch vụ', 'success'); }
            else { await API.createService(data); toast('Đã thêm dịch vụ', 'success'); }
            closeModal(modalId); refresh();
        };
        const btnCancel = document.getElementById('btn-cancel-service');
        if (btnCancel) btnCancel.onclick = () => closeModal(modalId);
        refresh();
    }

    /* ============================================================
       9. TRANG QUẢN LÝ MAPPING
       ============================================================ */
    function initMappingPage(API) {
        const tbody = document.getElementById('mapping-table-body');
        if (!tbody) return;

        const searchEl = document.getElementById('search-mapping');
        const filterSpec = document.getElementById('filter-mapping-specialty');
        const btnAdd = document.getElementById('btn-add-mapping');
        const form = document.getElementById('form-mapping-info');
        const modalId = 'mapping-form-modal';
        let editingId = null;

        API.getSpecialties().then(r => {
            if (filterSpec) filterSpec.innerHTML = '<option value="all">Tất cả chuyên khoa đích</option>' + r.data.map(s => `<option value="${s.id}">${s.name}</option>`).join('');
            const sel = document.getElementById('map-specialty');
            if (sel) sel.innerHTML = r.data.map(s => `<option value="${s.id}">${s.name}</option>`).join('');
        });
        API.getDoctors().then(r => {
            const sel = document.getElementById('map-doctor');
            if (sel) sel.innerHTML = '<option value="">-- Không chỉ định cụ thể --</option>' + r.data.map(d => `<option value="${d.id}">${d.name}</option>`).join('');
        });

        async function refresh() {
            const res = await API.getMappings({ search: searchEl?.value || '', specialtyId: filterSpec?.value || 'all' });
            if (!res.data.length) {
                tbody.innerHTML = `<tr><td colspan="6" style="text-align:center;padding:40px;color:#8B7FA8;">Không có quy tắc nào.</td></tr>`;
                return;
            }
            tbody.innerHTML = res.data.map(m => `<tr>
                <td><strong>${m.id}</strong></td>
                <td>${m.keywords}</td>
                <td>${m.specialtyName || '—'}</td>
                <td>${m.doctorName || '—'}</td>
                <td>${m.priority}</td>
                <td>
                    <button type="button" class="btn-edit-map" data-id="${m.id}">Sửa</button>
                    <button type="button" class="btn-delete-map" data-id="${m.id}" style="background:#FEF2F2;color:#DC2626;border-color:#FECACA;">Xóa</button>
                </td>
            </tr>`).join('');

            tbody.querySelectorAll('.btn-edit-map').forEach(btn => btn.onclick = async () => {
                const r = await API.getMappings();
                const item = r.data.find(x => x.id === btn.dataset.id);
                if (!item) return;
                editingId = item.id;
                document.getElementById('form-mapping-title').textContent = 'Chỉnh sửa quy tắc Mapping';
                document.getElementById('map-keywords').value = item.keywords;
                document.getElementById('map-specialty').value = item.specialtyId;
                document.getElementById('map-doctor').value = item.doctorId || '';
                document.getElementById('map-priority').value = item.priority;
                openModal(modalId);
            });

            tbody.querySelectorAll('.btn-delete-map').forEach(btn => btn.onclick = () => {
                const id = btn.dataset.id;
                const row = btn.closest('tr');
                const name = row ? row.children[1].textContent.trim() : id;
                window.MedBookingConfirmDelete({
                    title: 'Xóa quy tắc Mapping',
                    itemName: `Từ khóa: "${name}" (${id})`,
                    itemType: 'quy tắc mapping',
                    onConfirm: async () => {
                        try {
                            await API.deleteMapping(id);
                            toast('Quy tắc đã được chuyển vào Thùng rác.', 'success', 'Đã xóa');
                            refresh();
                        } catch (err) {
                            toast(err.message || 'Không thể xóa quy tắc', 'error');
                        }
                    }
                });
            });
        }

        if (searchEl) searchEl.addEventListener('input', refresh);
        if (filterSpec) filterSpec.addEventListener('change', refresh);
        if (btnAdd) btnAdd.onclick = () => {
            editingId = null; form.reset();
            document.getElementById('form-mapping-title').textContent = 'Thêm Quy tắc Mapping Mới';
            document.getElementById('map-priority').value = 1;
            openModal(modalId);
        };
        if (form) form.onsubmit = async (e) => {
            e.preventDefault();
            const data = {
                keywords: document.getElementById('map-keywords').value.trim(),
                specialtyId: document.getElementById('map-specialty').value,
                doctorId: document.getElementById('map-doctor').value || null,
                priority: Number(document.getElementById('map-priority').value) || 1
            };
            if (!data.keywords || !data.specialtyId) return toast('Thiếu thông tin', 'error');
            if (editingId) { await API.updateMapping(editingId, data); toast('Đã cập nhật quy tắc', 'success'); }
            else { await API.createMapping(data); toast('Đã thêm quy tắc', 'success'); }
            closeModal(modalId); refresh();
        };
        const btnCancel = document.getElementById('btn-cancel-mapping');
        if (btnCancel) btnCancel.onclick = () => closeModal(modalId);
        refresh();
    }

    /* ============================================================
       10. TRANG THÙNG RÁC
       ============================================================ */
    function initRecycleBinPage(API) {
        const tbody = document.getElementById('recycle-bin-body');
        if (!tbody) return;

        async function refreshRecycleBin() {
            try {
                const res = await API.getRecycleBin();
                const list = res && res.data ? res.data : [];
                if (!list.length) {
                    tbody.innerHTML = `<tr><td colspan="5" style="text-align:center;padding:40px;color:#8B7FA8;">
                        <i class="fas fa-trash" style="font-size:32px;opacity:0.3;display:block;margin-bottom:8px;"></i>
                        Thùng rác đang trống.
                    </td></tr>`;
                    return;
                }
                tbody.innerHTML = list.map(item => `<tr>
                    <td><strong>${item.id}</strong></td>
                    <td>${item.type}</td>
                    <td>${item.name}</td>
                    <td>${item.deletedAt || '—'}</td>
                    <td>
                        <button type="button" class="btn-restore" data-id="${item.id}"
                            style="background:linear-gradient(135deg,#10B981,#059669);color:#fff;border:none;">
                            Khôi phục
                        </button>
                        <button type="button" class="btn-delete-forever" data-id="${item.id}" data-name="${item.name}"
                            style="background:#FEF2F2;color:#DC2626;border-color:#FECACA;">
                            Xóa vĩnh viễn
                        </button>
                    </td>
                </tr>`).join('');

                tbody.querySelectorAll('.btn-restore').forEach(btn => {
                    btn.onclick = async () => {
                        try {
                            await API.restoreItem(btn.dataset.id);
                            toast('Bản ghi đã được khôi phục thành công.', 'success', 'Khôi phục');
                            refreshRecycleBin();
                        } catch (err) {
                            toast(err.message || 'Không thể khôi phục', 'error');
                        }
                    };
                });

                tbody.querySelectorAll('.btn-delete-forever').forEach(btn => {
                    btn.onclick = () => {
                        const id = btn.dataset.id;
                        const name = btn.dataset.name;
                        if (typeof window.MedBookingConfirmPurge === 'function') {
                            window.MedBookingConfirmPurge(
                                'Xóa vĩnh viễn',
                                'Bản ghi sẽ bị xóa hoàn toàn khỏi cơ sở dữ liệu.',
                                `${name} (${id})`,
                                async () => {
                                    try {
                                        await API.deleteItemForever(id);
                                        toast('Bản ghi đã bị xóa vĩnh viễn khỏi hệ thống.', 'error', 'Đã xóa');
                                        refreshRecycleBin();
                                    } catch (err) {
                                        toast(err.message || 'Không thể xóa', 'error');
                                    }
                                }
                            );
                        } else {
                            if (confirm('Xóa vĩnh viễn không thể hoàn tác. Tiếp tục?')) {
                                API.deleteItemForever(id).then(() => {
                                    toast('Đã xóa vĩnh viễn', 'error', 'Đã xóa');
                                    refreshRecycleBin();
                                });
                            }
                        }
                    };
                });
            } catch (err) {
                console.error('[RecycleBin]', err);
                tbody.innerHTML = `<tr><td colspan="5" style="text-align:center;padding:40px;color:#DC2626;">
                    <i class="fas fa-exclamation-triangle"></i> Có lỗi khi tải dữ liệu: ${err.message || 'Unknown'}
                </td></tr>`;
            }
        }

        refreshRecycleBin();
    }

    /* ============================================================
       11. KHỞI TẠO CHUNG
       ============================================================ */
    document.addEventListener('DOMContentLoaded', () => {
        waitForAPI((API) => {
            initAccountPage(API);
            initDoctorPage(API);
            initSpecialtyPage(API);
            initServicePage(API);
            initMappingPage(API);
            initRecycleBinPage(API);
            initNotifications(API);
        });
    });

    window.MedBookingToast = toast;

    /* ============================================================
       12. HỆ THỐNG THÔNG BÁO (NOTIFICATIONS) - STATIC VERSION
       ============================================================ */
    function initNotifications(API) {
        const header = document.querySelector('header');
        if (!header || document.getElementById('notif-wrapper')) return;

        // 1. Tạo khung giao diện
        const wrapper = document.createElement('div');
        wrapper.id = 'notif-wrapper';
        wrapper.className = 'notif-wrapper';
        wrapper.innerHTML = `
            <button class="notif-bell" id="notif-bell">
                <i class="fas fa-bell"></i>
                <span class="notif-badge" id="notif-badge" style="display:none;">0</span>
            </button>
            <div class="notif-panel" id="notif-panel">
                <div class="notif-header">
                    <h4>Thông báo</h4>
                    <button class="mark-all" id="mark-all-read">Đánh dấu đã đọc</button>
                </div>
                <div class="notif-list" id="notif-list"></div>
            </div>
        `;
        
        const themeBtn = header.querySelector('.theme-toggle');
        if (themeBtn) themeBtn.parentNode.insertBefore(wrapper, themeBtn);

        // 2. Khai báo element
        const bellBtn = document.getElementById('notif-bell');
        const panel = document.getElementById('notif-panel');
        const listContainer = document.getElementById('notif-list');
        const badge = document.getElementById('notif-badge');
        const markAllBtn = document.getElementById('mark-all-read');

        // 3. Hàm render thông báo
        async function loadNotifs() {
            try {
                const res = await API.getNotifications();
                const notifs = res.data || [];
                const unreadCount = notifs.filter(n => !n.read).length;

                // Cập nhật số lượng trên badge (chấm đỏ)
                if (unreadCount > 0) {
                    badge.textContent = unreadCount;
                    badge.style.display = 'flex';
                } else {
                    badge.style.display = 'none';
                }

                // Nếu đang mở bảng thì mới render HTML (tránh load ngầm gây nháy)
                if (panel.classList.contains('open') || listContainer.innerHTML === '') {
                    if (!notifs.length) {
                        listContainer.innerHTML = `
                            <div class="notif-empty">
                                <i class="fas fa-bell-slash"></i>
                                Không có thông báo nào.
                            </div>`;
                        return;
                    }

                    listContainer.innerHTML = notifs.map(n => {
                        let iconClass = 'notif-icon info';
                        let iconHtml = '<i class="fas fa-circle-info"></i>';
                        
                        if (n.title.includes('Xóa') || n.title.includes('Cảnh báo')) {
                            iconClass = 'notif-icon danger';
                            iconHtml = '<i class="fas fa-triangle-exclamation"></i>';
                        } else if (n.title.includes('Khôi phục') || n.title.includes('Thành công')) {
                            iconClass = 'notif-icon success';
                            iconHtml = '<i class="fas fa-check"></i>';
                        } else if (n.title.includes('Mới') || n.title.includes('Đánh giá')) {
                            iconClass = 'notif-icon warning';
                            iconHtml = '<i class="fas fa-star"></i>';
                        }

                        return `
                        <div class="notif-item ${n.read ? '' : 'unread'}" data-id="${n.id}">
                            <div class="${iconClass}">${iconHtml}</div>
                            <div class="notif-body">
                                <div class="notif-title">
                                    ${n.title}
                                    <span class="notif-time">${n.time}</span>
                                </div>
                                <div class="notif-message">${n.message}</div>
                            </div>
                        </div>
                        `;
                    }).join('');
                }
            } catch (err) {
                console.error('Lỗi tải thông báo:', err);
            }
        }

        // 4. Gắn sự kiện Click
        bellBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            const isOpen = panel.classList.contains('open');
            
            if (isOpen) {
                panel.classList.remove('open');
            } else {
                panel.classList.add('open');
                loadNotifs(); // Chỉ load lại danh sách 1 lần khi bấm mở
            }
        });

        // Click ra ngoài thì đóng
        document.addEventListener('click', (e) => {
            if (!wrapper.contains(e.target)) {
                panel.classList.remove('open');
            }
        });

        // Đánh dấu tất cả đã đọc
        markAllBtn.addEventListener('click', async () => {
            await API.markAllRead();
            loadNotifs(); // Cập nhật lại giao diện ngay
        });

        // Load lần đầu để lấy số lượng thông báo (chưa mở bảng)
        loadNotifs();

        // (Không dùng setInterval tự động load liên tục để tránh bị "nháy")
        // Thay vào đó, mỗi khi bạn xóa/thêm dữ liệu ở trang khác, quay lại trang này nó sẽ tự lấy data mới.
    }

})();