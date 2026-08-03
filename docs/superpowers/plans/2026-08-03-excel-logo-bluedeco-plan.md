# Excel Logo Aspect Ratio Fix Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Lock the logo aspect ratio to exact 1.80:1 (108px x 60px) using `oneCellAnchor` XML in `src/excel.js` so Excel never stretches or distorts the Bluedeco logo.

**Architecture:** Replace `twoCellAnchor` with `<xdr:oneCellAnchor editAs="oneCell">` in `injectLogoToBuffer()` and `triggerAutoSync()` in `src/excel.js` with explicit dimensions `cx="1028700" cy="571500"`.

**Tech Stack:** Vanilla JavaScript ES6, SheetJS (`xlsx-js-style`), JSZip, OpenXML SpreadsheetDrawing.

## Global Constraints
- Preserve left-alignment of Note Rows (`Bằng chữ:...`, `_ Báo giá...`) and Column B hạng mục data rows.
- Logo must start at Column B Row 1 (`col=1, row=0`) and preserve aspect ratio 1.80:1 (108px x 60px).
- Bump cache buster query string in `index.html` and ES6 module imports to `?v=20260803-v6`.

---

### Task 1: Update Logo Drawing XML in `src/excel.js` to `oneCellAnchor`

**Files:**
- Modify: `src/excel.js`

**Interfaces:**
- Updates: `injectLogoToBuffer(binBuf)` and `triggerAutoSync()`.

- [ ] **Step 1: Update `drawingXml` in `injectLogoToBuffer()` and `triggerAutoSync()` in `src/excel.js`**

Update `drawingXml` string definition:
```javascript
const drawingXml = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<xdr:wsDr xmlns:xdr="http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">\n<xdr:oneCellAnchor editAs="oneCell">\n<xdr:from>\n<xdr:col>1</xdr:col>\n<xdr:colOff>38100</xdr:colOff>\n<xdr:row>0</xdr:row>\n<xdr:rowOff>38100</xdr:rowOff>\n</xdr:from>\n<xdr:ext cx="1028700" cy="571500"/>\n<xdr:pic>\n<xdr:nvPicPr>\n<xdr:cNvPr id="2" name="Picture 3"/>\n<xdr:cNvPicPr>\n<a:picLocks noChangeAspect="1" noChangeArrowheads="1"/>\n</xdr:cNvPicPr>\n</xdr:nvPicPr>\n<xdr:blipFill>\n<a:blip xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" r:embed="rId1" cstate="print"/>\n<a:srcRect/>\n<a:stretch>\n<a:fillRect/>\n</a:stretch>\n</xdr:blipFill>\n<xdr:spPr bwMode="auto">\n<a:xfrm>\n<a:off x="38100" y="38100"/>\n<a:ext cx="1028700" cy="571500"/>\n</a:xfrm>\n<a:prstGeom prst="rect">\n<a:avLst/>\n</a:prstGeom>\n<a:noFill/>\n<a:ln>\n<a:noFill/>\n</a:ln>\n</xdr:spPr>\n</xdr:pic>\n<xdr:clientData/>\n</xdr:oneCellAnchor>\n</xdr:wsDr>`;
```

- [ ] **Step 2: Update module version query strings to `?v=20260803-v6`**

Update query parameters in `main.js`, `src/takeoff.js`, `src/excel.js`, `src/db.js`, `src/cloud-sync.js`, and `index.html` to `?v=20260803-v6`.

- [ ] **Step 3: Run `check_final.py`**

Run: `python check_final.py`
Expected: `Modal divs: opens=94, closes=94, net=0`.

- [ ] **Step 4: Commit and push**

```bash
git add main.js src/excel.js src/takeoff.js src/db.js src/cloud-sync.js index.html
git commit -m "fix: lock logo aspect ratio to 1.80:1 (108px x 60px) using oneCellAnchor XML"
git push origin main
```
