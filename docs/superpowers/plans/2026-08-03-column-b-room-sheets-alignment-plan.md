# Room Detail Sheets Column B Alignment Lock-Down Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ensure 100% of room detail sheets (Sheet 2 onwards in Excel and dynamic room tables on Web UI) have Column B (HẠNG MỤC) data rows left-aligned with a 15px (indent = 1) offset.

**Architecture:** Implement a dedicated lock-down function `applyRoomSheetsLockdown(roomSheets)` in `src/excel.js` that executes AFTER all other style functions in `generateWorkbook()`. Update `src/takeoff.js` and `style.css` so Web UI room detail tables enforce `text-align: left !important; padding-left: 15px !important;` on Column B.

**Tech Stack:** Vanilla JavaScript ES6, SheetJS (`xlsx-js-style`), CSS3.

## Global Constraints
- Preserve left-alignment of Note Rows (`Bằng chữ:...`, `_ Báo giá...`, `_ Thời gian thi công...`) as required by `AGENTS.md`.
- Preserve merged header info rows (`Từ:`, `Kính gởi:`) left alignment.
- Bump cache buster query string in `index.html` to `?v=20260803-v3`.

---

### Task 1: Add Defensive Lock-Down for Room Detail Sheets in `src/excel.js`

**Files:**
- Modify: `src/excel.js`

**Interfaces:**
- Produces: `applyRoomSheetsLockdown(roomSheets)` helper function.

- [ ] **Step 1: Write `applyRoomSheetsLockdown` in `src/excel.js`**

Add the helper function in `src/excel.js` before `generateWorkbook`:
```javascript
function applyRoomSheetsLockdown(roomSheets) {
  const romanSet = new Set(['I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII']);
  roomSheets.forEach(s => {
    const ws = s.ws;
    if (!ws || !ws['!ref']) return;
    const range = XLSX.utils.decode_range(ws['!ref']);
    for (let R = 10; R <= range.e.r; R++) {
      const refB = XLSX.utils.encode_cell({ r: R, c: 1 });
      if (!ws[refB]) continue;
      const valB = ws[refB].v != null ? String(ws[refB].v).trim() : '';
      const cellA = ws[XLSX.utils.encode_cell({ r: R, c: 0 })];
      const valA = cellA && cellA.v != null ? String(cellA.v).trim() : '';
      const isRoman = romanSet.has(valA);
      const isTotalRow = valB.toLowerCase().includes('tổng cộng') || valB.startsWith('Bằng chữ:') || valB.includes('Cộng trước VAT');

      if (!ws[refB].s) ws[refB].s = {};

      if (isRoman) {
        ws[refB].s.alignment = { horizontal: 'left', vertical: 'center', wrapText: false };
      } else if (valB !== '' && !isTotalRow) {
        ws[refB].s.alignment = { horizontal: 'left', vertical: 'center', wrapText: true, indent: 1 };
      }
    }
  });
}
```

- [ ] **Step 2: Call `applyRoomSheetsLockdown(roomSheets)` in `generateWorkbook`**

Call `applyRoomSheetsLockdown(roomSheets)` right before returning `wbData` in `generateWorkbook(project)`.

- [ ] **Step 3: Verify Node test script**

Run: `node "C:\Users\Lenovo\.gemini\antigravity-ide\brain\7c226e78-c08b-460f-a852-69dd802ca0b2\scratch\check_align.js"`
Expected: PASS with all data rows in Sheet 2 having `alignment: {"horizontal":"left","vertical":"center","wrapText":true,"indent":1}`.

- [ ] **Step 4: Commit changes**

```bash
git add src/excel.js
git commit -m "fix: enforce room sheets Column B lockdown in excel.js"
```

---

### Task 2: Update Web UI & CSS for Room Detail Tables in `src/takeoff.js` and `style.css`

**Files:**
- Modify: `style.css`
- Modify: `src/takeoff.js`
- Modify: `index.html`

- [ ] **Step 1: Enforce Column B styling in `style.css`**

Ensure `#boq-tbody tr td:nth-child(2)` and `.ep-detail-table tr td:nth-child(2)` have explicit left alignment:
```css
#boq-tbody tr:not(.boq-room-title):not(.boq-room-header):not(.boq-elec-header):not(.boq-note-header):not(.boq-sub-header):not(.boq-other-header) td:nth-child(2),
.ep-detail-table tbody tr:not(.boq-room-title):not(.boq-room-header):not(.boq-elec-header):not(.boq-note-header):not(.boq-sub-header):not(.boq-other-header) td:nth-child(2) {
  text-align: left !important;
  padding-left: 15px !important;
}
```

- [ ] **Step 2: Bump version parameter in `index.html`**

Update `style.css?v=20260803-v3` and `main.js?v=20260803-v3`.

- [ ] **Step 3: Run `check_final.py`**

Run: `python check_final.py`
Expected: `Modal divs: opens=94, closes=94, net=0`

- [ ] **Step 4: Commit and push**

```bash
git add style.css src/takeoff.js src/excel.js index.html
git commit -m "fix: lock down room detail Column B alignment across Web UI and Excel export"
git push origin main
```
