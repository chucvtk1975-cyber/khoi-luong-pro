# Excel Print Setup & Row Heights Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Configure Excel print setup for A4 Landscape with exact margins (Left 1.8cm, Right 1.0cm, Top 1.4cm, Bottom 1.4cm) and increase all data row heights by 1.5x (27pt for data, 30-36pt for headers) across 100% of exported worksheets.

**Architecture:** Update `applyPageSetup(ws)` in `src/excel.js` with exact inch margins (`left: 0.71, right: 0.39, top: 0.55, bottom: 0.55`), create `applyRowHeights(ws)` helper to populate `ws['!rows']` with 1.5x height values, and update `triggerAutoSync()` pageMargins XML.

**Tech Stack:** Vanilla JavaScript ES6, SheetJS (`xlsx-js-style`).

## Global Constraints
- Left Margin = 1.8cm (0.71 in), Right Margin = 1.0cm (0.39 in), Top Margin = 1.4cm (0.55 in), Bottom Margin = 1.4cm (0.55 in).
- Data row height = 27pt (36px), Header row height = 36pt (48px), Section row height = 30pt (40px).
- Preserve Column B left alignment and 15px indent.
- Bump cache buster query string in `index.html` and ES6 module imports to `?v=20260803-v7`.

---

### Task 1: Update Page Margins and Add Row Heights in `src/excel.js`

**Files:**
- Modify: `src/excel.js`

**Interfaces:**
- Produces: `applyRowHeights(ws, numRows)` helper function.

- [ ] **Step 1: Update `applyPageSetup(ws)` margins in `src/excel.js`**

Update `ws['!margins']` in `applyPageSetup`:
```javascript
  ws['!margins'] = {
    left:   0.71,  // 1.8 cm = 0.70866 in
    right:  0.39,  // 1.0 cm = 0.39370 in
    top:    0.55,  // 1.4 cm = 0.55118 in
    bottom: 0.55,  // 1.4 cm = 0.55118 in
    header: 0.2,
    footer: 0.2,
  };
```

- [ ] **Step 2: Add `applyRowHeights(ws)` helper in `src/excel.js`**

Add `applyRowHeights(ws)` helper to set `ws['!rows']`:
```javascript
function applyRowHeights(ws, headerCount = 8) {
  if (!ws || !ws['!ref']) return;
  const range = XLSX.utils.decode_range(ws['!ref']);
  const rows = [];
  for (let R = 0; R <= range.e.r; R++) {
    if (R < 4) {
      rows.push({ hpt: 20, hpx: 27 });
    } else if (R >= 4 && R <= 6) {
      rows.push({ hpt: 19, hpx: 25 });
    } else if (R >= 8 && R <= headerCount) {
      rows.push({ hpt: 36, hpx: 48 }); // Table headers (1.5x 24pt)
    } else {
      const cellA = ws[XLSX.utils.encode_cell({ r: R, c: 0 })];
      const valA = cellA && cellA.v != null ? String(cellA.v).trim() : '';
      const isRoman = ['I','II','III','IV','V','VI','VII','VIII','IX','X'].includes(valA);
      if (isRoman) {
        rows.push({ hpt: 30, hpx: 40 }); // Section headers (1.5x 20pt)
      } else {
        rows.push({ hpt: 27, hpx: 36 }); // Data rows (1.5x 18pt)
      }
    }
  }
  ws['!rows'] = rows;
}
```

- [ ] **Step 3: Call `applyRowHeights` on `wsSum`, `roomSheets`, `wsVT` in `generateWorkbook`**

Call `applyRowHeights(wsSum, 8)` and `applyRowHeights(s.ws, 9)` for room sheets before returning workbook.

- [ ] **Step 4: Update module version query strings to `?v=20260803-v7`**

Update query string parameters in `main.js`, `src/takeoff.js`, `src/excel.js`, `src/db.js`, `src/cloud-sync.js`, and `index.html` to `?v=20260803-v7`.

- [ ] **Step 5: Run `check_final.py`**

Run: `python check_final.py`
Expected: `Modal divs: opens=94, closes=94, net=0`.

- [ ] **Step 6: Commit and push**

```bash
git add main.js src/excel.js src/takeoff.js src/db.js src/cloud-sync.js index.html
git commit -m "feat: configure A4 landscape print margins and 1.5x 27pt row heights in excel export"
git push origin main
```
