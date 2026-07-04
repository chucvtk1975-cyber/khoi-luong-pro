// =============================================
// MAIN ENTRY POINT (Root Controller)
// =============================================

import { DB, onDbSave, migratePhotosToIndexedDB } from './src/db.js';
import { triggerAutoSync } from './src/excel.js';
import { initTakeoffUI } from './src/takeoff.js';

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

  // 2. Liên kết hook lưu DB để kích hoạt tự động đồng bộ/sao lưu Excel nền
  onDbSave(async () => {
    try {
      await triggerAutoSync();
    } catch (e) {
      console.warn('[MAIN] Tự động đồng bộ Excel thất bại:', e);
    }
  });

  // 3. Khởi tạo giao diện bóc khối lượng
  try {
    initTakeoffUI();
  } catch (e) {
    console.error('[MAIN] Lỗi khởi tạo giao diện bóc khối lượng:', e);
  }
});

function printError(msg, err) {
  console.error(msg, err);
}
