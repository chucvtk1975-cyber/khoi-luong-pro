# Reorder Room Note Above Furniture Design Specification

## Overview
In the Room Survey Modal (Step 3 wizard: `step-content-3`), reorder the UI form sections so that **GHI CHÚ PHÒNG (TÙY CHỌN)** (Room Notes) is placed at the top of the step, directly above **THIẾT BỊ NỘI THẤT** (Furniture Equipment).

## User Intent & Requirements
- **Goal**: Place "GHI CHÚ PHÒNG (TÙY CHỌN)" as item #1 in Step 3, followed by "THIẾT BỊ NỘI THẤT" as item #2.
- **Non-breaking Constraint**: All DOM element IDs (`room-note`, `room-photo-input-overview`, `room-photo-thumbs-overview`, `note-woodwork`, `room-photo-input-noithat`, `room-photo-thumbs-noithat`) and JavaScript event bindings must remain unchanged.

## Detailed Layout Changes

### Target File
- [index.html](file:///d:/1_Kho%20tri%20th%E1%BB%A9c/khoi-luong-pro/index.html) (inside `#step-content-3`)

### Reordered Structure in `#step-content-3`
1. **GHI CHÚ PHÒNG (TÙY CHỌN)**
   - Section Title: `<i data-lucide="file-text"></i> Ghi chú phòng (tùy chọn)`
   - Textarea: `id="room-note"`
   - Photo Upload Button: `id="room-photo-input-overview"` & Thumbs container `id="room-photo-thumbs-overview"`
2. **THIẾT BỊ NỘI THẤT** (with `margin-top: 16px`)
   - Section Title: `<i data-lucide="sofa"></i> Thiết Bị Nội Thất (tủ bếp, tủ quần áo, cửa nội thất, kệ, cầu thang...)`
   - Textarea: `id="note-woodwork"`
   - Photo Upload Button: `id="room-photo-input-noithat"` & Thumbs container `id="room-photo-thumbs-noithat"`
3. **THIẾT BỊ ĐIỆN (KHẢO SÁT NHẬP TAY VÀO Ô GHI CHÚ)**
4. **NHÀ VỆ SINH: THIẾT BỊ VỆ SINH VÀ CHỐNG THẤM**
5. **Ảnh hiện trạng khác**

## Verification Plan

### Manual Verification
1. Open the app in browser.
2. Click "Thêm phòng" or edit a room.
3. Navigate to Step 3 in the modal wizard.
4. Verify that "GHI CHÚ PHÒNG (TÙY CHỌN)" is at the top, followed by "THIẾT BỊ NỘI THẤT".
5. Test saving and verifying data persistence.
