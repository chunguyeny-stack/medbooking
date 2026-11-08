/* ============================================================
   bac_si.js - Logic dùng chung cho giao diện Bác sĩ MEDBOOKING (Realtime)
   ============================================================ */

// Hàm hỗ trợ lấy ngày YYYY-MM-DD
function getTodayStr() {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
}

// ================== 1. MOCK DATA ==================
const MB_MOCK = {
  get stats() {
    const today = getTodayStr();
    const todayAppts = this.appointments.filter(a => a.date === today);
    return {
      today: todayAppts.length,
      done: todayAppts.filter(a => a.status === 'completed').length,
      waiting: todayAppts.filter(a => a.status === 'waiting').length,
      weekShifts: 5
    };
  },
  appointments: [
    { id: 'LH00123', date: getTodayStr(), time: '08:00 - 08:30', name: 'Trần Thị Bích', age: 34, gender: 'Nữ', symptom: 'Đau đầu, chóng mặt, buồn nôn', status: 'waiting' },
    { id: 'LH00124', date: getTodayStr(), time: '08:30 - 09:00', name: 'Lê Văn Cường', age: 45, gender: 'Nam', symptom: 'Ho khan kéo dài, tức ngực', status: 'waiting' },
    { id: 'LH00125', date: getTodayStr(), time: '09:00 - 09:30', name: 'Phạm Thị Dung', age: 28, gender: 'Nữ', symptom: 'Sốt cao, đau họng, mệt mỏi', status: 'in-progress' },
    { id: 'LH00126', date: getTodayStr(), time: '09:30 - 10:00', name: 'Hoàng Văn Em', age: 52, gender: 'Nam', symptom: 'Đau lưng, tê chân', status: 'completed' },
    { id: 'LH00127', date: getTodayStr(), time: '10:00 - 10:30', name: 'Nguyễn Thị F', age: 60, gender: 'Nữ', symptom: 'Huyết áp cao, chóng mặt', status: 'waiting' },
    { id: 'LH00128', date: getTodayStr(), time: '10:30 - 11:00', name: 'Đỗ Văn G', age: 40, gender: 'Nam', symptom: 'Đau dạ dày, ợ chua', status: 'cancelled' },
    { id: 'LH00129', date: getTodayStr(), time: '13:30 - 14:00', name: 'Bùi Thị H', age: 22, gender: 'Nữ', symptom: 'Dị ứng da, ngứa', status: 'waiting' }
  ]
};

// ================== 2. LOCAL STORAGE HELPERS ==================
const MB_STORAGE = {
  get(key, defaultValue = null) {
    try {
      const raw = localStorage.getItem(key);
      return raw ? JSON.parse(raw) : defaultValue;
    } catch (e) { return defaultValue; }
  },
  set(key, value) {
    try { localStorage.setItem(key, JSON.stringify(value)); } catch (e) {}
  },
  remove(key) {
    try { localStorage.removeItem(key); } catch (e) {}
  }
};

// ================== 3. TOAST NOTIFICATION ==================
function showToast(message, type = 'info', duration = 3000) {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    container.style.cssText = `position: fixed; top: 24px; right: 24px; z-index: 9999; display: flex; flex-direction: column; gap: 10px;`;
    document.body.appendChild(container);
  }
  const colors = {
    success: { bg: '#dcfce7', border: '#22c55e', color: '#166534', icon: 'fa-circle-check' },
    error:   { bg: '#fee2e2', border: '#ef4444', color: '#991b1b', icon: 'fa-circle-xmark' },
    warning: { bg: '#fef3c7', border: '#f59e0b', color: '#92400e', icon: 'fa-triangle-exclamation' },
    info:    { bg: '#dbeafe', border: '#3b82f6', color: '#1e40af', icon: 'fa-circle-info' }
  };
  const style = colors[type] || colors.info;
  const toast = document.createElement('div');
  toast.style.cssText = `
    display: flex; align-items: center; gap: 12px;
    padding: 14px 20px; border-radius: 12px;
    background: ${style.bg}; border-left: 5px solid ${style.border};
    color: ${style.color}; font-weight: 500; font-size: 13.5px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    min-width: 280px; max-width: 400px;
    animation: slideInRight 0.3s ease-out;
    font-family: 'Poppins', sans-serif;
  `;
  toast.innerHTML = `<i class="fas ${style.icon}" style="font-size: 18px;"></i><span style="flex:1;">${message}</span>`;
  container.appendChild(toast);
  setTimeout(() => {
    toast.style.animation = 'slideOutRight 0.3s ease-in forwards';
    setTimeout(() => toast.remove(), 300);
  }, duration);
}

if (!document.getElementById('toast-keyframes')) {
  const style = document.createElement('style');
  style.id = 'toast-keyframes';
  style.textContent = `
    @keyframes slideInRight { from { opacity: 0; transform: translateX(100px); } to { opacity: 1; transform: translateX(0); } }
    @keyframes slideOutRight { from { opacity: 1; transform: translateX(0); } to { opacity: 0; transform: translateX(100px); } }
  `;
  document.head.appendChild(style);
}

// ================== 4. THEME TOGGLE (ĐÃ FIX LỖI) ==================
function initTheme() {
  // 1. Kiểm tra localStorage trước
  let theme = localStorage.getItem('medbooking_theme');
  
  // 2. Nếu chưa có, kiểm tra cài đặt hệ điều hành
  if (!theme) {
    theme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }
  
  // 3. Áp dụng theme
  document.documentElement.setAttribute('data-theme', theme);

  // 4. Gắn sự kiện cho nút toggle
  const toggleBtn = document.getElementById('theme-toggle');
  if (toggleBtn) {
    // Clone để xóa event listener cũ (tránh bị gắn 2 lần)
    const newBtn = toggleBtn.cloneNode(true);
    toggleBtn.parentNode.replaceChild(newBtn, toggleBtn);

    newBtn.addEventListener('click', () => {
      const current = document.documentElement.getAttribute('data-theme');
      const next = current === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      localStorage.setItem('medbooking_theme', next);
      showToast(`Đã chuyển sang chế độ ${next === 'dark' ? 'Tối' : 'Sáng'}`, 'info', 1500);
    });
  }
}

// ================== 5. SIDEBAR TOGGLE ==================
function initSidebar() {
  const toggleBtn = document.getElementById('sidebar-toggle');
  const sidebar = document.querySelector('.sidebar');
  const overlay = document.getElementById('sidebar-overlay');
  if (toggleBtn && sidebar) {
    const newBtn = toggleBtn.cloneNode(true);
    toggleBtn.parentNode.replaceChild(newBtn, toggleBtn);

    newBtn.addEventListener('click', () => {
      sidebar.classList.toggle('open');
      if (overlay) overlay.classList.toggle('active');
    });
  }
  if (overlay) {
    overlay.addEventListener('click', () => {
      sidebar.classList.remove('open');
      overlay.classList.remove('active');
    });
  }
}

// ================== 6. HIGHLIGHT ACTIVE NAV ==================
function highlightActiveNav() {
  const currentPath = window.location.pathname.split('/').pop() || 'home_bs.html';
  document.querySelectorAll('.nav-link').forEach(link => {
    const href = link.getAttribute('href');
    if (href && href.includes(currentPath)) {
      link.classList.add('active');
    } else {
      link.classList.remove('active');
    }
  });
}

// ================== 7. KHỞI TẠO CHUNG ==================
document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initSidebar();
  highlightActiveNav();

  if (typeof window.MB_PAGE_INIT === 'function') {
    window.MB_PAGE_INIT();
  }
});