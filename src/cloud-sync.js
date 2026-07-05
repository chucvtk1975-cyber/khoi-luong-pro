// =============================================
// CLOUD SYNC MODULE (Supabase)
// =============================================

import { DB } from './db.js';
import { showToast, renderProjectList } from './takeoff.js';

export const CloudSync = {
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
    if (url && key && typeof window.supabase !== 'undefined') {
      try {
        this.client = window.supabase.createClient(url, key);
        this.updateStatusUI(true, 'Da cau hinh ket noi');
        console.log('[CloudSync] Da khoi tao Supabase client.');
      } catch (e) {
        console.error('[CloudSync] Loi khoi tao:', e);
        this.client = null;
        this.updateStatusUI(false, 'Loi khoi tao Supabase');
      }
    } else {
      this.client = null;
      this.updateStatusUI(false, 'Chua cau hinh dam may');
    }
  },

  updateStatusUI(ok, msg) {
    const dot = document.getElementById('supabase-status-dot');
    const text = document.getElementById('supabase-status-text');
    const cloudBtn = document.getElementById('btn-cloud-sync');
    if (dot) dot.style.background = ok ? '#16A34A' : '#EF4444';
    if (text) text.textContent = msg;
    if (cloudBtn) {
      cloudBtn.style.color = ok ? '#16A34A' : '#9CA3AF';
      cloudBtn.title = ok ? 'Dam may: Da ket noi - Nhan de cau hinh' : 'Cau hinh dong bo dam may';
    }
  },

  async testConnection(url, key) {
    if (!url || !key) return { ok: false, msg: 'Vui long nhap day du thong tin' };
    if (typeof window.supabase === 'undefined') return { ok: false, msg: 'Khong tim thay thu vien Supabase' };
    try {
      const testClient = window.supabase.createClient(url, key);
      const { error } = await testClient.from('projects').select('id').limit(1);
      if (error) throw error;
      return { ok: true, msg: 'Ket noi thanh cong!' };
    } catch (e) {
      console.error('[CloudSync] Test ket noi loi:', e);
      return { ok: false, msg: 'Loi ket noi hoac bang "projects" chua duoc tao!' };
    }
  },

  async pushProject(project) {
    if (!this.client) return;
    try {
      const payload = {
        id: project.id,
        name: project.name || 'Chua dat ten',
        client: project.client || '',
        data: project,
        updated_at: new Date().toISOString()
      };
      const { error } = await this.client.from('projects').upsert(payload);
      if (error) throw error;
      console.log('[CloudSync] Da luu du an "' + project.name + '" len Cloud.');
    } catch (e) {
      console.error('[CloudSync] Push loi:', e);
    }
  },

  async deleteProject(id) {
    if (!this.client) return;
    try {
      const { error } = await this.client.from('projects').delete().eq('id', id);
      if (error) throw error;
      console.log('[CloudSync] Da xoa du an ' + id + ' tren Cloud.');
    } catch (e) {
      console.error('[CloudSync] Delete loi:', e);
    }
  },

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
        if (!cloudProj || !cloudProj.id) return;
        const localProjIdx = localProjects.findIndex(p => p.id === cloudItem.id);

        if (localProjIdx === -1) {
          localProjects.push(cloudProj);
          updatedLocal = true;
          console.log('[CloudSync] Tai moi du an "' + cloudProj.name + '"');
        } else {
          const cloudTime = new Date(cloudItem.updated_at).getTime();
          const localProj = localProjects[localProjIdx];
          const localTime = localProj.updatedAt || localProj.createdAt || 0;
          if (cloudTime > localTime) {
            localProjects[localProjIdx] = cloudProj;
            updatedLocal = true;
            console.log('[CloudSync] Cap nhat du an "' + cloudProj.name + '" tu Cloud');
          } else if (localTime > cloudTime) {
            this.pushProject(localProj);
          }
        }
      });

      if (updatedLocal) {
        localStorage.setItem(DB.KEY, JSON.stringify(localProjects));
        if (typeof renderProjectList === 'function') renderProjectList();
        showToast('Dong bo du lieu dam may hoan tat!', 'success');
      }
    } catch (e) {
      console.error('[CloudSync] Pull loi:', e);
    }
  },

  bindEvents() {
    document.getElementById('btn-cloud-sync')?.addEventListener('click', () => {
      const { url, key } = this.getSettings();
      const urlInput = document.getElementById('supabase-url');
      const keyInput = document.getElementById('supabase-key');
      if (urlInput) urlInput.value = url;
      if (keyInput) keyInput.value = key;
      document.getElementById('modal-supabase')?.classList.add('open');
    });

    document.getElementById('btn-close-supabase-modal')?.addEventListener('click', () => {
      document.getElementById('modal-supabase')?.classList.remove('open');
    });

    document.getElementById('btn-test-supabase')?.addEventListener('click', async () => {
      const url = document.getElementById('supabase-url')?.value.trim();
      const key = document.getElementById('supabase-key')?.value.trim();
      const testBtn = document.getElementById('btn-test-supabase');
      if (testBtn) { testBtn.textContent = 'Dang ket noi...'; testBtn.disabled = true; }
      const res = await this.testConnection(url, key);
      if (testBtn) { testBtn.textContent = 'Kiem tra ket noi'; testBtn.disabled = false; }
      showToast(res.msg, res.ok ? 'success' : 'error');
    });

    document.getElementById('btn-save-supabase')?.addEventListener('click', () => {
      const url = document.getElementById('supabase-url')?.value.trim();
      const key = document.getElementById('supabase-key')?.value.trim();
      if (!url || !key) { showToast('Vui long nhap day du URL va API Key!', 'error'); return; }
      this.saveSettings(url, key);
      document.getElementById('modal-supabase')?.classList.remove('open');
      showToast('Da luu cau hinh dong bo dam may!', 'success');
      this.pullAndSync();
    });

    document.getElementById('modal-supabase')?.addEventListener('click', (e) => {
      if (e.target.id === 'modal-supabase') {
        document.getElementById('modal-supabase').classList.remove('open');
      }
    });
  }
};
