# Reorder Furniture Section Above Room Note Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Move the "THIẾT BỊ NỘI THẤT" section to the top of Step 3 in the room survey modal wizard (`index.html`), directly above "GHI CHÚ PHÒNG (TÙY CHỌN)".

**Architecture:** Reorder the HTML DOM structure inside `#step-content-3` in `index.html` without changing any element IDs, event handlers, or JavaScript logic to ensure zero regression in data persistence or calculations.

**Tech Stack:** HTML5, Vanilla JavaScript (ES6).

## Global Constraints

- Target File: `index.html`
- Do not alter element IDs: `note-woodwork`, `room-photo-input-noithat`, `room-photo-thumbs-noithat`, `room-note`, `room-photo-input-overview`, `room-photo-thumbs-overview`.
- Preserve cache-buster version parameters `?v=20260804-v1` in `index.html`.

---

### Task 1: Reorder HTML elements in `#step-content-3` in `index.html`

**Files:**
- Modify: `index.html:566-676`

**Interfaces:**
- Consumes: Existing DOM structure in `index.html`.
- Produces: Updated `#step-content-3` DOM layout with "THIẾT BỊ NỘI THẤT" at the top.

- [ ] **Step 1: Move THIẾT BỊ NỘI THẤT section above GHI CHÚ PHÒNG**

Edit `index.html` inside `<div class="wizard-step-content" id="step-content-3" style="display:none;">` so that the `THIẾT BỊ NỘI THẤT` title and form-group are placed first, and `GHI CHÚ PHÒNG (TÙY CHỌN)` follows it with `margin-top: 16px;`.

Target replacement in `index.html`:
```html
        <div class="wizard-step-content" id="step-content-3" style="display:none;">

          <!-- THIẾT BỊ NỘI THẤT -->
          <div class="section-title">
            <i data-lucide="sofa" class="section-icon"></i> Thiết Bị Nội Thất <span style="font-size:11px;color:var(--text-muted);font-weight:400;">(tủ bếp, tủ quần áo, cửa nội thất, kệ, cầu thang...)</span>
          </div>

          <div class="form-group">
            <textarea id="note-woodwork" rows="3"
              placeholder="VD: Tủ bếp trên 2,4m dài, tủ bếp dưới 2,4m dài, mặt đá granite&#10;Tủ quần áo 3 cánh 1,8×2,4m, cửa gỗ HDF 2 cái&#10;Kệ TV treo tường 1,6m, kệ sách 0,8m"
              style="width:100%;resize:vertical;"></textarea>
            <div style="margin-top: 4px;">
              <button type="button" class="btn-primary" style="padding: 2px 8px; font-size: 11px; height: auto; text-transform: none;" onclick="document.getElementById('room-photo-input-noithat').click()">📷 Đính kèm ảnh Nội thất</button>
              <input type="file" id="room-photo-input-noithat" accept="image/png, image/jpeg, image/heic, image/heif, .png, .jpg, .jpeg, .heic, .heif" multiple style="display:none;" onchange="handleRoomPhotoSelect(this.files, 'noithat')">
              <div class="room-photo-thumbs" id="room-photo-thumbs-noithat" style="margin-top: 6px;"></div>
            </div>
          </div>

          <!-- GHI CHÚ PHÒNG -->
          <div class="section-title" style="margin-top:16px;">
            <i data-lucide="file-text" class="section-icon"></i> Ghi chú phòng (tùy chọn)
          </div>

          <div class="form-group">
            <textarea id="room-note" rows="4"
              placeholder="VD: Trần cao 3.000, ốp gạch 1.800, nội 1.200, sơn nước 600 mm&#10;VD: Thêm máy lạnh 2 cái, quạt hút 1 cái, ổ cắm 3 bộ...&#10;(Ghi chú sẽ tự động phân tích các thiết bị)"
              style="width:100%;resize:vertical;"></textarea>
            <div style="margin-top: 4px;">
              <button type="button" class="btn-primary" style="padding: 2px 8px; font-size: 11px; height: auto; text-transform: none;" onclick="document.getElementById('room-photo-input-overview').click()">📷 Đính kèm ảnh Toàn cảnh</button>
              <input type="file" id="room-photo-input-overview" accept="image/png, image/jpeg, image/heic, image/heif, .png, .jpg, .jpeg, .heic, .heif" multiple style="display:none;" onchange="handleRoomPhotoSelect(this.files, 'overview')">
              <div class="room-photo-thumbs" id="room-photo-thumbs-overview" style="margin-top: 6px;"></div>
            </div>
          </div>
```

- [ ] **Step 2: Run verification python script**

Run: `python check_final.py`
Expected output: Modal open/close tags net = 0 (Passed).

- [ ] **Step 3: Commit changes**

Run: `git add index.html ; git commit -m "feat: move furniture section above room note in wizard step 3"`
