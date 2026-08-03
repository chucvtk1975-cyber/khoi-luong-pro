# Adjusted Excel Export Row Heights Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Configure native SheetJS row heights with 20pt for data rows, 30pt for single-line table headers, 19pt/row for multi-line table headers, and 26pt for section headers across 100% of exported worksheets.

**Architecture:** Update `applyRowHeights(ws, headerCount)` in `src/excel.js` with `{ hpt: 20, hpx: 27 }` for data rows, `{ hpt: 30, hpx: 40 }` for single-line table headers (`headerCount <= 8`), `{ hpt: 19, hpx: 25 }` for multi-line table headers (`headerCount > 8`), and `{ hpt: 26, hpx: 35 }` for section headers.

**Tech Stack:** Vanilla JavaScript ES6, SheetJS (`xlsx-js-style`).

## Global Constraints
- Data row height = 20pt (27px).
- Section row height = 26pt (35px).
- Single-line table header row height = 30pt (40px).
- Multi-line table header row height = 19pt/row (25px).
- Bump cache buster query string in `index.html` and ES6 module imports to `?v=20260804-v1`.

---

### Task 1: Update `applyRowHeights` in `src/excel.js` and Bump Version

**Files:**
- Modify: `src/excel.js`
- Modify: `main.js`
- Modify: `src/takeoff.js`
- Modify: `index.html`

**Interfaces:**
- Updates: `applyRowHeights(ws, headerCount)` helper function.

- [ ] **Step 1: Update `applyRowHeights` in `src/excel.js`**

Update `applyRowHeights` in `src/excel.js`:
```javascript
function applyRowHeights(ws, headerCount = 8) {
  if (!ws || !ws['!ref']) return;
  const range = XLSX.utils.decode_range(ws['!ref']);
  const rows = [];
  const romanSet = new Set(['I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII']);
  const isMultiHeader = (headerCount > 8); // Room detail sheets có 2 hàng header (R=8,9)

  for (let R = 0; R <= range.e.r; R++) {
    if (R < 4) {
      rows.push({ hpt: 20, hpx: 27 });
    } else if (R >= 4 && R <= 6) {
      rows.push({ hpt: 19, hpx: 25 });
    } else if (R >= 8 && R <= headerCount) {
      if (isMultiHeader) {
        rows.push({ hpt: 19, hpx: 25 }); // 2 hàng header: 19pt/hàng
      } else {
        rows.push({ hpt: 30, hpx: 40 }); // 1 hàng header: 30pt
      }
    } else {
      const cellA = ws[XLSX.utils.encode_cell({ r: R, c: 0 })];
      const valA = cellA && cellA.v != null ? String(cellA.v).trim() : '';
      const isRoman = romanSet.has(valA);
      if (isRoman) {
        rows.push({ hpt: 26, hpx: 35 }); // Section headers (26pt)
      } else {
        rows.push({ hpt: 20, hpx: 27 }); // Data rows (20pt)
      }
    }
  }
  ws['!rows'] = rows;
}
```

- [ ] **Step 2: Update module version query strings to `?v=20260804-v1`**

Update query string parameters in `main.js`, `src/takeoff.js`, `src/excel.js`, and `index.html` to `?v=20260804-v1`.

- [ ] **Step 3: Run `check_final.py`**

Run: `python check_final.py`
Expected: `Modal divs: opens=94, closes=94, net=0`.

- [ ] **Step 4: Commit and push**

```bash
git add main.js src/excel.js src/takeoff.js index.html docs/superpowers/plans/2026-08-04-excel-row-heights-adjust-plan.md
git commit -m "feat: adjust excel export row heights to 20pt data, 30pt/19pt table headers, 26pt section headers"
git push origin main
```
