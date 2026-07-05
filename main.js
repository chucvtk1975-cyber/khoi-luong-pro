// =============================================
// MAIN ENTRY POINT (Root Controller)
// =============================================

import { DB, onDbSave, setCloudSync, migratePhotosToIndexedDB } from './src/db.js';
import { triggerAutoSync } from './src/excel.js';
import { initTakeoffUI } from './src/takeoff.js';
import { CloudSync } from './src/cloud-sync.js';

// Application state definition
export let state = {
  currentProjectId: null,
  editingRoomId: null,
  selMat: { floor: 'none', wall: 'none', ceilMats: [], wallZ1: 'none', wallZ2: 'none' },
  wallZoneMode: false,
  originalRoomData: null,
  elecPhotos: [],
};

// Bind state to window for debugging or manual console checks if needed
window.state = state;

document.addEventListener('DOMContentLoaded', async () => {
  console.log('[MAIN] Khởi chạy ứng dụng Bóc Khối Lượng Pro (Modular ES6)...');

  // 1. Chạy tiến trình di chuyển ảnh cũ sang IndexedDB nếu có
  try {
    await migratePhotosToIndexedDB();
  } catch (e) {
    printError('[MAIN] Lỗi di chuyển ảnh cũ:', e);
  }

  // 2. Liên kết hook lưu DB: kích hoạt Excel sync + Cloud push
  // (được gọi 1 lần, sau khi CloudSync khởi tạo xong)

  // 3. Khởi tạo giao diện bóc khối lượng
  try {
    initTakeoffUI();
  } catch (e) {
    console.error('[MAIN] Lỗi khởi tạo giao diện bóc khối lượng:', e);
  }

  // 4. Khởi tạo Cloud Sync (Supabase) và bind sự kiện modal
  try {
    CloudSync.init();
    CloudSync.bindEvents();
    setCloudSync(CloudSync);

    // Hook duy nhất: Excel auto-sync + Cloud push mỗi khi DB.save được gọi
    onDbSave(async () => {
      try { await triggerAutoSync(); } catch (e) {
        console.warn('[MAIN] Tự động đồng bộ Excel thất bại:', e);
      }
      if (CloudSync.client && window.state?.currentProjectId) {
        const proj = DB.get(window.state.currentProjectId);
        if (proj) CloudSync.pushProject(proj);
      }
    });

    // Tự động đồng bộ nền nếu đã cấu hình
    if (CloudSync.client) {
      CloudSync.pullAndSync();
    }
    console.log('[MAIN] CloudSync đã khởi tạo.');
  } catch (e) {
    console.warn('[MAIN] CloudSync khởi tạo thất bại:', e);
  }
});

function printError(msg, err) {
  console.error(msg, err);
}
