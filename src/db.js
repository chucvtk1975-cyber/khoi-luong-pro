// =============================================
// DATABASE (localStorage & IndexedDB) MODULE
// =============================================

import { showToast } from './takeoff.js';

let onSaveCallback = null;

export function onDbSave(callback) {
  onSaveCallback = callback;
}

export function genId() {
  return Date.now().toString(36) + Math.random().toString(36).slice(2, 7);
}

export const DB = {
  KEY: 'bkl_v1_projects',

  load() {
    try {
      return JSON.parse(localStorage.getItem(this.KEY) || '[]');
    } catch {
      return [];
    }
  },

  save(data) {
    const cloned = JSON.parse(JSON.stringify(data));
    cloned.forEach(proj => {
      if (proj.sitePhotos) {
        proj.sitePhotos.forEach(p => { delete p.data; });
      }
      if (proj.rooms) {
        proj.rooms.forEach(room => {
          if (room.photos) {
            const categories = ['overview', 'den', 'tudien', 'maylanh', 'noithat', 'wc', 'other'];
            categories.forEach(cat => {
              const list = room.photos[cat] || [];
              list.forEach(p => { delete p.data; });
            });
          }
        });
      }
    });

    try {
      localStorage.setItem(this.KEY, JSON.stringify(cloned));
    } catch (e) {
      if (e.name === 'QuotaExceededError') {
        showToast('Bộ nhớ trình duyệt đã đầy! Vui lòng xóa bớt ảnh hoặc dự án cũ để tiếp tục.', 'error');
      } else {
        console.error('localStorage save error:', e);
      }
    }

    if (onSaveCallback) {
      onSaveCallback();
    }
  },

  all() {
    return this.load();
  },

  get(id) {
    return this.load().find(p => p.id === id) || null;
  },

  create(data) {
    const projects = this.load();
    const project = { id: genId(), rooms: [], createdAt: Date.now(), ...data };
    projects.push(project);
    this.save(projects);
    return project;
  },

  update(id, patch) {
    const projects = this.load();
    const i = projects.findIndex(p => p.id === id);
    if (i === -1) return null;
    projects[i] = { ...projects[i], ...patch };
    this.save(projects);
    return projects[i];
  },

  remove(id) {
    this.save(this.load().filter(p => p.id !== id));
  },

  addRoom(projectId, roomData) {
    const p = this.get(projectId);
    if (!p) return null;
    const room = { id: genId(), ...roomData };
    p.rooms.push(room);
    this.update(projectId, { rooms: p.rooms });
    return room;
  },

  updateRoom(projectId, roomId, patch) {
    const p = this.get(projectId);
    if (!p) return;
    const i = p.rooms.findIndex(r => r.id === roomId);
    if (i === -1) return;
    p.rooms[i] = { ...p.rooms[i], ...patch };
    this.update(projectId, { rooms: p.rooms });
  },

  removeRoom(projectId, roomId) {
    const p = this.get(projectId);
    if (!p) return;
    this.update(projectId, { rooms: p.rooms.filter(r => r.id !== roomId) });
  }
};

// =============================================
// PHOTO INDEXEDDB UTILITIES
// =============================================

export const PhotoDB = {
  DB_NAME: 'BocKhoiLuongPhotosDB',
  DB_VERSION: 1,
  STORE_NAME: 'photos',
  db: null,

  open() {
    return new Promise((resolve, reject) => {
      if (this.db) return resolve(this.db);
      const request = indexedDB.open(this.DB_NAME, this.DB_VERSION);
      
      request.onerror = (e) => reject(request.error);
      request.onsuccess = (e) => {
        this.db = request.result;
        resolve(this.db);
      };
      
      request.onupgradeneeded = (e) => {
        const db = request.result;
        if (!db.objectStoreNames.contains(this.STORE_NAME)) {
          db.createObjectStore(this.STORE_NAME);
        }
      };
    });
  },

  async getPhoto(id) {
    const db = await this.open();
    return new Promise((resolve, reject) => {
      const transaction = db.transaction(this.STORE_NAME, 'readonly');
      const store = transaction.objectStore(this.STORE_NAME);
      const request = store.get(id);
      
      request.onerror = () => reject(request.error);
      request.onsuccess = () => resolve(request.result || null);
    });
  },

  async savePhoto(id, blob) {
    const db = await this.open();
    return new Promise((resolve, reject) => {
      const transaction = db.transaction(this.STORE_NAME, 'readwrite');
      const store = transaction.objectStore(this.STORE_NAME);
      const request = store.put(blob, id);
      
      request.onerror = () => reject(request.error);
      request.onsuccess = () => resolve();
    });
  },

  async deletePhoto(id) {
    const db = await this.open();
    return new Promise((resolve, reject) => {
      const transaction = db.transaction(this.STORE_NAME, 'readwrite');
      const store = transaction.objectStore(this.STORE_NAME);
      const request = store.delete(id);
      
      request.onerror = () => reject(request.error);
      request.onsuccess = () => resolve();
    });
  }
};

export function dataURLtoBlob(dataurl) {
  try {
    const arr = dataurl.split(',');
    const mime = arr[0].match(/:(.*?);/)[1];
    const bstr = atob(arr[1]);
    let n = bstr.length;
    const u8arr = new Uint8Array(n);
    while (n--) {
      u8arr[n] = bstr.charCodeAt(n);
    }
    return new Blob([u8arr], { type: mime });
  } catch (e) {
    console.error('Failed to convert dataurl to blob', e);
    return null;
  }
}

export function blobToBase64(blob) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onerror = () => reject(reader.error);
    reader.onload = () => {
      const dataUrl = reader.result;
      const base64 = dataUrl.split(',')[1];
      resolve(base64);
    };
    reader.readAsDataURL(blob);
  });
}

export async function migratePhotosToIndexedDB() {
  const projects = DB.load();
  let migratedCount = 0;
  let hasChanges = false;

  for (const proj of projects) {
    if (proj.sitePhotos && Array.isArray(proj.sitePhotos)) {
      for (let i = 0; i < proj.sitePhotos.length; i++) {
        const p = proj.sitePhotos[i];
        if (p.data && p.data.startsWith('data:')) {
          const blob = dataURLtoBlob(p.data);
          if (blob) {
            const id = genId();
            await PhotoDB.savePhoto(id, blob);
            proj.sitePhotos[i] = { id, name: p.name, date: p.date || new Date().toISOString() };
            migratedCount++;
            hasChanges = true;
          }
        }
      }
    }

    if (!proj.rooms) continue;
    for (const room of proj.rooms) {
      if (!room.photos) continue;
      
      if (Array.isArray(room.photos)) {
        const legacyPhotos = room.photos;
        room.photos = {
          overview: [], den: [], tudien: [], maylanh: [], noithat: [], wc: [], other: []
        };
        for (const p of legacyPhotos) {
          if (p.data && p.data.startsWith('data:')) {
            const blob = dataURLtoBlob(p.data);
            if (blob) {
              const id = genId();
              await PhotoDB.savePhoto(id, blob);
              room.photos.overview.push({ id, name: p.name, date: p.date || new Date().toISOString() });
              migratedCount++;
              hasChanges = true;
            }
          }
        }
      } else {
        const categories = ['overview', 'den', 'tudien', 'maylanh', 'noithat', 'wc', 'other'];
        for (const cat of categories) {
          const list = room.photos[cat];
          if (!list || !Array.isArray(list)) continue;
          
          for (let i = 0; i < list.length; i++) {
            const p = list[i];
            if (p.data && p.data.startsWith('data:')) {
              const blob = dataURLtoBlob(p.data);
              if (blob) {
                const id = genId();
                await PhotoDB.savePhoto(id, blob);
                list[i] = { id, name: p.name, date: p.date || new Date().toISOString() };
                migratedCount++;
                hasChanges = true;
              }
            }
          }
        }
      }
    }
  }

  if (hasChanges) {
    try {
      localStorage.setItem(DB.KEY, JSON.stringify(projects));
      console.log(`[MIGRATION] Đã chuyển đổi ${migratedCount} ảnh cũ sang IndexedDB thành công.`);
    } catch (e) {
      console.error('[MIGRATION] Lưu database lỗi:', e);
    }
  }
}

export async function isBlobHEIC(blob) {
  if (blob.type === 'image/heic' || blob.type === 'image/heif') return true;
  try {
    const buffer = await blob.slice(0, 16).arrayBuffer();
    const arr = new Uint8Array(buffer);
    if (arr.length < 12) return false;
    const ftyp = String.fromCharCode(...arr.slice(4, 12));
    return ftyp === 'ftypheic' || ftyp === 'ftypheix' || ftyp === 'ftypmif1' || ftyp === 'ftypmsf1';
  } catch (e) {
    return false;
  }
}
