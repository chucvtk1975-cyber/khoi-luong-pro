# Native SheetJS Excel Print Setup & Row Heights Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Configure native SheetJS A4 Landscape print setup with exact margins (Left 1.8cm, Right 1.0cm, Top 1.4cm, Bottom 1.4cm), row heights (24pt data, 26pt section, 34pt header), right footer page numbering formatted as `1/6`, `2/6` ... `&P/&N`, and purge all raw XML string manipulation from `triggerAutoSync()`.

**Architecture:** Update `applyPageSetup(ws)` in `src/excel.js` with exact inch margins (`left: 0.71, right: 0.39, top: 0.55, bottom: 0.55`) and footer format `&L&"Arial,Italic"Du-Toan-BlueAI Lab&R&"Arial,Bold"&P/&N`. Add `applyRowHeights(ws, headerCount)` helper to populate `ws['!rows']` with `{ hpt: 24, hpx: 32 }` for data rows, `{ hpt: 26, hpx: 35 }` for section headers, `{ hpt: 34, hpx: 45 }` for table headers. Completely remove XML replacement block from `triggerAutoSync()`.

**Tech Stack:** Vanilla JavaScript ES6, SheetJS (`xlsx-js-style`).

## Global Constraints
- Left Margin = 1.8cm (0.71 in), Right Margin = 1.0cm (0.39 in), Top Margin = 1.4cm (0.55 in), Bottom Margin = 1.4cm (0.55 in).
- Footer Right Page Numbering: Format `1/6`, `2/6` ... `&P/&N`.
- Data row height = 24pt (32px), Table header row height = 34pt (45px), Section row height = 26pt (35px).
- Zero raw XML string regex manipulation in `triggerAutoSync()`.
- Bump cache buster query string in `index.html` and ES6 module imports to `?v=20260803-v28`.

---

### Task 1: Implement Native SheetJS Page Setup, Footers & Row Heights in `src/excel.js`

**Files:**
- Modify: `src/excel.js`
- Modify: `main.js`
- Modify: `src/takeoff.js`
- Modify: `index.html`

**Interfaces:**
- Updates: `applyPageSetup(ws)`, `applyRowHeights(ws, headerCount)`, and `triggerAutoSync()`.

- [ ] **Step 1: Update `applyPageSetup` and add `applyRowHeights` in `src/excel.js`**

Update `applyPageSetup` and add `applyRowHeights` in `src/excel.js`:
```javascript
function applyPageSetup(ws, repeatRowsCount) {
  // Khổ giấy A4 ngang
  ws['!pageSetup'] = {
    paperSize:     9,           // 9 = A4
    orientation:   'landscape',
    fitToPage:     true,
    fitToWidth:    1,           // vừa 1 trang ngang (tự thu nhỏ nếu cần)
    fitToHeight:   0,           // tự do theo chiều dọc
    autoBreaks:    true,
    horizontalDpi: 300,
    verticalDpi:   300,
  };

  // Lề trang (đơn vị: inches)
  ws['!margins'] = {
    left:   0.71, // 1.8 cm
    right:  0.39, // 1.0 cm
    top:    0.55, // 1.4 cm
    bottom: 0.55, // 1.4 cm
    header: 0.2,
    footer: 0.2,
  };

  // Footer: góc trái = ngày giờ in | góc phải = &P/&N (1/6, 2/6 ...)
  ws['!headerFooter'] = {
    oddFooter:  '&L&"Arial,Italic"Du-Toan-BlueAI Lab&R&"Arial,Bold"&P/&N',
    evenFooter: '&L&"Arial,Italic"Du-Toan-BlueAI Lab&R&"Arial,Bold"&P/&N',
  };

  // Rows to repeat at top khi in: lặp lại từ dòng 0 đến repeatRowsCount-1 (0-indexed)
  const rpt = (repeatRowsCount && repeatRowsCount > 0) ? repeatRowsCount : 9;
  ws['!printHeader'] = { rows: { min: 0, max: rpt - 1 } };
}

function applyRowHeights(ws, headerCount = 8) {
  if (!ws || !ws['!ref']) return;
  const range = XLSX.utils.decode_range(ws['!ref']);
  const rows = [];
  const romanSet = new Set(['I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII']);
  for (let R = 0; R <= range.e.r; R++) {
    if (R < 4) {
      rows.push({ hpt: 20, hpx: 27 });
    } else if (R >= 4 && R <= 6) {
      rows.push({ hpt: 19, hpx: 25 });
    } else if (R >= 8 && R <= headerCount) {
      rows.push({ hpt: 34, hpx: 45 }); // Table headers (34pt)
    } else {
      const cellA = ws[XLSX.utils.encode_cell({ r: R, c: 0 })];
      const valA = cellA && cellA.v != null ? String(cellA.v).trim() : '';
      const isRoman = romanSet.has(valA);
      if (isRoman) {
        rows.push({ hpt: 26, hpx: 35 }); // Section headers (26pt)
      } else {
        rows.push({ hpt: 24, hpx: 32 }); // Data rows (24pt)
      }
    }
  }
  ws['!rows'] = rows;
}
```

- [ ] **Step 2: Attach `applyRowHeights` calls for `wsDetail`, `wsSum`, `wsVT` in `src/excel.js`**

Add `applyRowHeights(wsDetail, 8);`, `applyRowHeights(wsSum, 8);`, and `applyRowHeights(wsVT, 8);` after `applyPageSetup` calls.

- [ ] **Step 3: Purge XML string replacement from `triggerAutoSync()` in `src/excel.js`**

Remove the `xmlStr.includes("<pageMargins")` replacement block completely from `triggerAutoSync()`.

- [ ] **Step 4: Update module version query strings to `?v=20260803-v28`**

Update query string parameters in `main.js`, `src/takeoff.js`, `src/excel.js`, and `index.html` to `?v=20260803-v28`.

- [ ] **Step 5: Run `check_final.py`**

Run: `python check_final.py`
Expected: `Modal divs: opens=94, closes=94, net=0`.

- [ ] **Step 6: Commit and push**

```bash
git add main.js src/excel.js src/takeoff.js index.html docs/superpowers/plans/2026-08-03-excel-print-setup-native-plan.md
git commit -m "feat: configure native SheetJS A4 landscape print setup, 24pt row heights, and 1/6 footer page numbering"
git push origin main
```
