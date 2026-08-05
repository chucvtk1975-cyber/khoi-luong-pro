# Move Furniture Section Above Room Note Design Specification

## Overview
In the Room Survey Modal (Step 3 wizard: `step-content-3`), reorder the UI form sections so that **THIẾT BỊ NỘI THẤT** (Furniture Equipment) is placed at the top of the step, directly above **GHI CHÚ PHÒNG (TÙY CHỌN)** (Room Notes).

## User Intent & Requirements
- **Goal**: Place "THIẾT BỊ NỘI THẤT" at the top of Step 3 in the room creation/editing wizard modal.
- **Visual Alignment**: The section will occupy the orange-boxed region in the user's provided mockup, above "GHI CHÚ PHÒNG (TÙY CHỌN)".
- **Non-breaking Constraint**: All DOM element IDs (`note-woodwork`, `room-photo-input-noithat`, `room-photo-thumbs-noithat`) and JavaScript event bindings must remain unchanged to preserve existing calculations, state management, IndexedDB storage, and Excel exports.

## Detailed Layout Changes

### Target File
- [index.html](file:///d:/1_Kho%20tri%20th%E1%BB%A9c/khoi-luong-pro/index.html) (inside `#step-content-3`)

### Reordered Structure in `#step-content-3`
1. **THIẾT BỊ NỘI THẤT**
   - Section Title: `<i data-lucide="sofa"></i> Thiết Bị Nội Thất (tủ bếp, tủ quần áo, cửa nội thất, kệ, cầu thang...)`
   - Textarea: `id="note-woodwork"`
   - Photo Upload Button: `id="room-photo-input-noithat"` & Thumbs container `id="room-photo-thumbs-noithat"`
2. **GHI CHÚ PHÒNG (TÙY CHỌN)** (with `margin-top: 16px`)
   - Section Title: `<i data-lucide="file-text"></i> Ghi chú phòng (tùy chọn)`
   - Textarea: `id="room-note"`
   - Photo Upload Button: `id="room-photo-input-overview"` & Thumbs container `id="room-photo-thumbs-overview"`
3. **THIẾT BỊ ĐIỆN (KHẢO SÁT NHẬP TAY VÀO Ô GHI CHÚ)**
4. **NHÀ VỆ SINH: THIẾT BỊ VỆ SINH VÀ CHỐNG THẤM**
5. **Ảnh hiện trạng khác**

## Verification Plan

### Manual Verification
1. Open the app in browser.
2. Click "Thêm phòng" (Add Room) or edit a room.
3. Navigate to Step 3 in the modal wizard.
4. Verify that "THIẾT BỊ NỘI THẤT" is displayed at the top, followed by "GHI CHÚ PHÒNG (TÙY CHỌN)".
5. Test entering data into "THIẾT BỊ NỘI THẤT", attaching photos, saving the room, and verifying data persists accurately.
