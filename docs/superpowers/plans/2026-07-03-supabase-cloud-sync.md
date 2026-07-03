# Tích hợp Đồng bộ Cơ sở dữ liệu đám mây Supabase Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Tích hợp thư viện Supabase, thiết kế giao diện cấu hình Supabase URL và API Key động, viết logic đồng bộ 2 chiều (Local-First + Cloud Sync) tự động giữa thiết bị và đám mây.

**Architecture:** Tích hợp CDN trong HTML, thêm UI modal cấu hình cài đặt kết nối và điều khiển đồng bộ, viết module đồng bộ trong Javascript.

**Tech Stack:** Vanilla JS + Supabase JS Client v2 (CDN) + Vanilla CSS3.

---

### Task 1: Bổ sung thư viện Supabase và giao diện Modal trong index.html

**Files:**
- Modify: [index.html](file:///d:/Kho%20tri%20th%E1%BB%A9c/khoi-luong-pro/index.html)

- [ ] **Step 1: Tích hợp Supabase CDN vào thẻ `<head>`**

Thêm dòng script vào `<head>` của [index.html](file:///d:/Kho%20tri%20th%E1%BB%A9c/khoi-luong-pro/index.html) ngay trước file `style.css`.
```html
  <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
```

- [ ] **Step 2: Thêm nút bấm Cấu hình đám mây vào Sidebar**

Sửa đổi phần `sidebar-brand-area` (khoảng dòng ~769-781) để chèn nút cấu hình mây.
Thay thế:
```html
        <div class="sidebar-brand-area">
          <div class="brand-icon-orange">
            <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="2" width="16" height="20" rx="2" ry="2"></rect><line x1="9" y1="22" x2="9" y2="16"></line><line x1="15" y1="22" x2="15" y2="16"></line><line x1="9" y1="16" x2="15" y2="16"></line><path d="M9 12h.01"></path><path d="M15 12h.01"></path><path d="M9 8h.01"></path><path d="M15 8h.01"></path></svg>
          </div>
          <div class="brand-info">
            <div class="brand-title-row">
              <span class="brand-title">BỐC KHỐI LƯỢNG PRO</span>
              <span class="brand-version">v1.2</span>
            </div>
            <div class="brand-copyright">Bản quyền thuộc BlueDecor Design & Build</div>
          </div>
        </div>
```
Bằng:
```html
        <div class="sidebar-brand-area">
          <div class="brand-icon-orange">
            <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="2" width="16" height="20" rx="2" ry="2"></rect><line x1="9" y1="22" x2="9" y2="16"></line><line x1="15" y1="22" x2="15" y2="16"></line><line x1="9" y1="16" x2="15" y2="16"></line><path d="M9 12h.01"></path><path d="M15 12h.01"></path><path d="M9 8h.01"></path><path d="M15 8h.01"></path></svg>
          </div>
          <div class="brand-info">
            <div class="brand-title-row">
              <span class="brand-title">BỐC KHỐI LƯỢNG PRO</span>
              <span class="brand-version">v1.2</span>
            </div>
            <div class="brand-copyright" style="display: flex; align-items: center; justify-content: space-between; width: 100%;">
              <span>BlueDecor Design & Build</span>
              <button id="btn-cloud-sync" class="btn-icon-xs" title="Cấu hình đồng bộ đám mây" style="border: none; background: transparent; padding: 2px; color: var(--sidebar-text-muted); cursor: pointer; display: flex; align-items: center; justify-content: center;">
                <i data-lucide="cloud"></i>
              </button>
            </div>
          </div>
        </div>
```

- [ ] **Step 3: Thêm Modal cấu hình Supabase**

Thêm đoạn mã HTML của `#modal-supabase` vào ngay sau `</div><!-- end modal-room -->` (khoảng dòng ~639).
```html
  <!-- ========== MODAL: CẤU HÌNH ĐỒNG BỘ CLOUD (SUPABASE) ========== -->
  <div class="modal-overlay" id="modal-supabase">
    <div class="modal-card" style="max-width: 420px;">
      <div class="modal-header">
        <h3>☁️ Cấu Hình Đồng Bộ Đám Mây</h3>
        <button class="modal-close" id="btn-close-supabase-modal"><i data-lucide="x"></i></button>
      </div>
      <div class="modal-body" style="padding: 16px 22px;">
        <div style="font-size:12px; color:var(--text-muted); margin-bottom:14px; line-height:1.5;">
          Kết nối cơ sở dữ liệu đám mây Supabase để tự động đồng bộ dự án giữa Máy tính và Điện thoại di động.
        </div>
        <div class="form-group">
          <label style="color:#1E293B !important;">Supabase URL</label>
          <input type="text" id="supabase-url" placeholder="VD: https://xxxx.supabase.co">
        </div>
        <div class="form-group">
          <label style="color:#1E293B !important;">Supabase Anon Key (API Key)</label>
          <input type="password" id="supabase-key" placeholder="Nhập API Key (Anon Key) của dự án">
        </div>
        <div id="supabase-status-info" style="font-size:12px; margin-top:12px; display:flex; align-items:center; gap:6px;">
          <span style="width:8px; height:8px; border-radius:50%; background:#CBD5E1; display:inline-block;" id="supabase-status-dot"></span>
          <span id="supabase-status-text" style="color:var(--text-muted); font-weight: 500;">Chưa cấu hình</span>
        </div>
      </div>
      <div class="modal-footer" style="gap: 8px;">
        <button class="btn-secondary" id="btn-test-supabase" style="flex: 1;">Kiểm tra kết nối</button>
        <button class="btn-primary" id="btn-save-supabase" style="flex: 1;">Lưu Cấu Hình</button>
      </div>
    </div>
  </div>
```

---

### Task 2: Viết logic khởi tạo và đồng bộ Supabase trong app.js

**Files:**
- Modify: [app.js](file:///d:/Kho%20tri%20th%E1%BB%A9c/khoi-luong-pro/app.js)

- [ ] **Step 1: Khởi tạo module CloudSync**

Khai báo biến toàn cục và lớp cấu hình Supabase ở đầu file `app.js` hoặc phần quản lý cơ sở dữ liệu.
Định nghĩa đối tượng `CloudSync`:
```javascript
const CloudSync = {
  client: null,
  
  getSettings() {
    return {
      url: localStorage.getItem('supabase_sync_url') || '',
      key: localStorage.getItem('supabase_sync_key') || ''
    };
  },

  saveSettings(url, key) {
    localStorage.setItem('supabase_sync_url', url.trim());
    localStorage.setItem('supabase_sync_key', key.trim());
    this.init();
  },

  init() {
    const { url, key } = this.getSettings();
    if (url && key && typeof supabase !== 'undefined') {
      try {
        this.client = supabase.createClient(url, key);
        this.updateStatusUI(true, 'Đã cấu hình kết nối');
      } catch (e) {
        console.error('Supabase init error:', e);
        this.client = null;
        this.updateStatusUI(false, 'Lỗi khởi tạo Supabase');
      }
    } else {
      this.client = null;
      this.updateStatusUI(false, 'Chưa cấu hình đám mây');
    }
  },

  updateStatusUI(ok, msg) {
    const dot = document.getElementById('supabase-status-dot');
    const text = document.getElementById('supabase-status-text');
    const cloudBtn = document.getElementById('btn-cloud-sync');
    
    if (dot) dot.style.background = ok ? '#16A34A' : '#EF4444';
    if (text) text.textContent = msg;
    if (cloudBtn) {
      cloudBtn.style.color = ok ? '#16A34A' : 'var(--sidebar-text-muted)';
    }
  },

  async testConnection(url, key) {
    if (!url || !key) return { ok: false, msg: 'Vui lòng nhập đầy đủ thông tin' };
    if (typeof supabase === 'undefined') return { ok: false, msg: 'Không tìm thấy thư viện Supabase' };
    
    try {
      const testClient = supabase.createClient(url, key);
      const { data, error } = await testClient.from('projects').select('id').limit(1);
      if (error) throw error;
      return { ok: true, msg: 'Kết nối thành công!' };
    } catch (e) {
      console.error('Test connection error:', e);
      return { ok: false, msg: 'Lỗi kết nối hoặc bảng "projects" chưa được tạo!' };
    }
  },

  // Đẩy 1 dự án lên Supabase (Upsert)
  async pushProject(project) {
    if (!this.client) return;
    try {
      const payload = {
        id: project.id,
        name: project.name,
        client: project.client || '',
        data: project,
        updated_at: new Date().toISOString()
      };
      const { error } = await this.client.from('projects').upsert(payload);
      if (error) throw error;
      console.log(`CloudSync: Đã lưu dự án ${project.name} lên Cloud.`);
    } catch (e) {
      console.error('CloudSync push error:', e);
    }
  },

  // Xóa dự án khỏi Supabase
  async deleteProject(id) {
    if (!this.client) return;
    try {
      const { error } = await this.client.from('projects').delete().eq('id', id);
      if (error) throw error;
      console.log(`CloudSync: Đã xóa dự án ${id} trên Cloud.`);
    } catch (e) {
      console.error('CloudSync delete error:', e);
    }
  },

  // Tải dự án từ Supabase và đồng bộ 2 chiều vào local
  async pullAndSync() {
    if (!this.client) return;
    try {
      const { data, error } = await this.client.from('projects').select('*');
      if (error) throw error;

      if (!data || data.length === 0) return;

      const localProjects = DB.load();
      let updatedLocal = false;

      data.forEach(cloudItem => {
        const cloudProj = cloudItem.data;
        const localProjIdx = localProjects.findIndex(p => p.id === cloudItem.id);

        if (localProjIdx === -1) {
          // Dự án chưa có ở local -> Thêm mới
          localProjects.push(cloudProj);
          updatedLocal = true;
          console.log(`CloudSync: Tải mới dự án ${cloudProj.name}`);
        } else {
          // Dự án đã có ở cả 2 bên -> so sánh ngày cập nhật/ngày tạo
          const cloudTime = cloudProj.updatedAt || cloudProj.createdAt || 0;
          const localProj = localProjects[localProjIdx];
          const localTime = localProj.updatedAt || localProj.createdAt || 0;

          if (cloudTime > localTime) {
            // Mây mới hơn -> Ghi đè local
            localProjects[localProjIdx] = cloudProj;
            updatedLocal = true;
            console.log(`CloudSync: Cập nhật dự án ${cloudProj.name} từ Cloud`);
          } else if (localTime > cloudTime) {
            // Local mới hơn -> Đẩy lên mây (chạy nền)
            this.pushProject(localProj);
          }
        }
      });

      if (updatedLocal) {
        // Lưu lại local
        localStorage.setItem(DB.KEY, JSON.stringify(localProjects));
        // Refresh giao diện
        if (typeof renderProjectList === 'function') renderProjectList();
        if (typeof updateDashboardStats === 'function') updateDashboardStats();
        showToast('Đồng bộ dữ liệu đám mây hoàn tất!', 'success');
      }
    } catch (e) {
      console.error('CloudSync pull error:', e);
    }
  }
};
```

- [ ] **Step 2: Móc nối CloudSync vào DB.save và DB.remove**

Sửa phương thức `DB.save` để đẩy dự án lên Supabase:
Tìm hàm `DB.save(data)` trong `app.js` (khoảng dòng ~888-920).
Bổ sung đoạn code đẩy dự án lên cloud:
```javascript
  save(data) {
    // ... code lưu local cũ giữ nguyên ...
    
    // Đẩy dự án đang hoạt động lên cloud
    if (typeof CloudSync !== 'undefined' && CloudSync.client) {
      const activeProj = DB.get(state.currentProjectId);
      if (activeProj) {
        // Gán thời gian cập nhật mới nhất cho dự án
        activeProj.updatedAt = Date.now();
        // Cập nhật lại trong mảng data để lưu local đồng bộ
        const idx = data.findIndex(p => p.id === activeProj.id);
        if (idx !== -1) data[idx].updatedAt = Date.now();
        
        // Gọi đẩy lên cloud
        CloudSync.pushProject(activeProj);
      }
    }
  }
```

Sửa phương thức `DB.remove` để xóa dự án trên Supabase:
Tìm hàm `DB.remove(id)` trong `app.js` (khoảng dòng ~956-960).
Thêm:
```javascript
  remove(id) {
    this.save(this.load().filter(p => p.id !== id));
    if (typeof CloudSync !== 'undefined' && CloudSync.client) {
      CloudSync.deleteProject(id);
    }
  }
```

- [ ] **Step 3: Gắn sự kiện điều khiển và nút bấm Modal**

Thêm các trình lắng nghe sự kiện (Event Listeners) của `#btn-cloud-sync`, `#btn-close-supabase-modal`, `#btn-save-supabase`, và `#btn-test-supabase` vào phần khởi tạo DOM ở cuối file `app.js`.
```javascript
// Sự kiện điều khiển cấu hình Supabase
document.getElementById('btn-cloud-sync')?.addEventListener('click', () => {
  const { url, key } = CloudSync.getSettings();
  const urlInput = document.getElementById('supabase-url');
  const keyInput = document.getElementById('supabase-key');
  
  if (urlInput) urlInput.value = url || 'https://repvqjjptxaofwbzivvj.supabase.co';
  if (keyInput) keyInput.value = key;
  
  document.getElementById('modal-supabase')?.classList.add('open');
});

document.getElementById('btn-close-supabase-modal')?.addEventListener('click', () => {
  document.getElementById('modal-supabase')?.classList.remove('open');
});

document.getElementById('btn-test-supabase')?.addEventListener('click', async () => {
  const url = document.getElementById('supabase-url').value.trim();
  const key = document.getElementById('supabase-key').value.trim();
  const testBtn = document.getElementById('btn-test-supabase');
  
  testBtn.textContent = 'Đang kết nối...';
  testBtn.disabled = true;
  
  const res = await CloudSync.testConnection(url, key);
  
  testBtn.textContent = 'Kiểm tra kết nối';
  testBtn.disabled = false;
  
  showToast(res.msg, res.ok ? 'success' : 'error');
});

document.getElementById('btn-save-supabase')?.addEventListener('click', () => {
  const url = document.getElementById('supabase-url').value.trim();
  const key = document.getElementById('supabase-key').value.trim();
  
  CloudSync.saveSettings(url, key);
  document.getElementById('modal-supabase')?.classList.remove('open');
  showToast('Đã lưu cấu hình đồng bộ đám mây!', 'success');
  
  // Tiến hành đồng bộ ngay lập tức
  CloudSync.pullAndSync();
});
```

- [ ] **Step 4: Khởi chạy và đồng bộ tự động khi tải trang**

Thêm lệnh khởi tạo và tự động đồng bộ khi ứng dụng khởi động (ở cuối file `app.js` hoặc trong sự kiện `DOMContentLoaded`):
```javascript
// Khởi tạo Supabase và đồng bộ tự động
CloudSync.init();
if (CloudSync.client) {
  CloudSync.pullAndSync();
}
```

---

### Task 3: Xác minh dự án và đóng gói

- [ ] **Step 1: Cập nhật Query Parameter index.html**

Cập nhật lại tham số `?v=...` của file `app.js` và `style.css` trong `index.html` để ép trình duyệt xóa cache.

- [ ] **Step 2: Chạy kiểm tra tự động**

Chạy script kiểm tra cú pháp HTML & JavaScript:
```powershell
python check_final.py
node -c app.js
```
Expected: Cả hai lệnh chạy thành công, không báo lỗi.

- [ ] **Step 3: Commit và đẩy lên GitHub**

```bash
git add index.html app.js
git commit -m "feat: integrate Supabase cloud database sync"
git push
```
