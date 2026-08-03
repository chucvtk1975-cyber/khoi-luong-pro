# Excel Print Setup, Row Heights & Page Numbering 1/6 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Configure Excel print setup for A4 Landscape with exact margins (Left 1.8cm, Right 1.0cm, Top 1.4cm, Bottom 1.4cm), fine-tuned row heights (24pt data, 26pt section, 30pt header), and right footer page numbering formatted as `1/6`, `2/6` ... `&P/&N` across 100% of exported worksheets.

**Architecture:** Update `applyPageSetup(ws)` and `triggerAutoSync()` in `src/excel.js` with exact inch margins (`left: 0.71, right: 0.39, top: 0.55, bottom: 0.55`) and footer format `&R&"Arial,Bold"&P/&N`. Update `applyRowHeights(ws)` helper to populate `ws['!rows']` with `{ hpt: 24, hpx: 32 }` for data rows, `{ hpt: 26, hpx: 35 }` for section headers, `{ hpt: 30, hpx: 40 }` for table headers.

**Tech Stack:** Vanilla JavaScript ES6, SheetJS (`xlsx-js-style`).

## Global Constraints
- Left Margin = 1.8cm (0.71 in), Right Margin = 1.0cm (0.39 in), Top Margin = 1.4cm (0.55 in), Bottom Margin = 1.4cm (0.55 in).
- Footer Right Page Numbering: Format `1/6`, `2/6` ... `&P/&N`.
- Data row height = 24pt (32px), Table header row height = 30pt (40px), Section row height = 26pt (35px).
- Preserve Column B left alignment and 15px indent.
- Bump cache buster query string in `index.html` and ES6 module imports to `?v=20260803-v8`.

---

### Task 1: Update Page Setup, Footers & Row Heights in `src/excel.js`

**Files:**
- Modify: `src/excel.js`

**Interfaces:**
- Updates: `applyPageSetup(ws)`, `applyRowHeights(ws, headerCount)`, and `triggerAutoSync()`.

- [ ] **Step 1: Update `applyPageSetup` footers and margins in `src/excel.js`**

Update `applyPageSetup` in `src/excel.js`:
```javascript
  ws['!margins'] = {
    left:   0.71, // 1.8 cm
    right:  0.39, // 1.0 cm
    top:    0.55, // 1.4 cm
    bottom: 0.55, // 1.4 cm
    header: 0.2,
    footer: 0.2,
  };

  ws['!headerFooter'] = {
    oddFooter:  '&L&"Arial,Italic"Du-Toan-BlueAI Lab&R&"Arial,Bold"&P/&N',
    evenFooter: '&L&"Arial,Italic"Du-Toan-BlueAI Lab&R&"Arial,Bold"&P/&N',
  };
```

- [ ] **Step 2: Update `applyRowHeights` function in `src/excel.js`**

Update `applyRowHeights` in `src/excel.js`:
```javascript
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
      rows.push({ hpt: 30, hpx: 40 }); // Table headers (30pt)
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

- [ ] **Step 3: Update `footerText` in `triggerAutoSync()` in `src/excel.js`**

Update `footerText` in `triggerAutoSync()`:
```javascript
const footerText = '&amp;L&amp;&quot;Arial,Italic&quot;Du-Toan-BlueAI Lab&amp;R&amp;&quot;Arial,Bold&quot;&amp;P/&amp;N';
```

- [ ] **Step 4: Update module version query strings to `?v=20260803-v8`**

Update query string parameters in `main.js`, `src/takeoff.js`, `src/excel.js`, `src/db.js`, `src/cloud-sync.js`, and `index.html` to `?v=20260803-v8`.

- [ ] **Step 5: Run `check_final.py`**

Run: `python check_final.py`
Expected: `Modal divs: opens=94, closes=94, net=0`.

- [ ] **Step 6: Commit and push**

```bash
git add main.js src/excel.js src/takeoff.js src/db.js src/cloud-sync.js index.html
git commit -m "feat: configure A4 landscape margins, 24pt row heights, and right footer 1/6 page numbering in excel export"
git push origin main
```
