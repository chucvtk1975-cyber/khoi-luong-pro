# Excel Logo 1.3x Aspect Ratio Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Enlarge the Bluedeco logo by 1.3x to 140px x 78px (`cx=1333500`, `cy=742950`) maintaining exact 1.80:1 aspect ratio using `oneCellAnchor` XML in `src/excel.js` so Excel never stretches or distorts the logo across 100% of exported worksheets.

**Architecture:** Replace `twoCellAnchor` or older `ext` values in `injectLogoToBuffer()` and `triggerAutoSync()` in `src/excel.js` with explicit 1.3x dimensions `cx="1333500" cy="742950"`.

**Tech Stack:** Vanilla JavaScript ES6, SheetJS (`xlsx-js-style`), JSZip, OpenXML SpreadsheetDrawing.

## Global Constraints
- Logo must start at Column B Row 1 (`col=1, row=0`) and preserve aspect ratio 1.80:1 (140px x 78px).
- Bump cache buster query string in `index.html` and ES6 module imports to `?v=20260803-v9`.

---

### Task 1: Update Logo Drawing XML in `src/excel.js` to 1.3x Dimensions

**Files:**
- Modify: `src/excel.js`

**Interfaces:**
- Updates: `injectLogoToBuffer(binBuf)` and `triggerAutoSync()`.

- [ ] **Step 1: Update `drawingXml` in `injectLogoToBuffer()` and `triggerAutoSync()` in `src/excel.js`**

Update `drawingXml` string definition with 1.3x dimensions (`cx="1333500" cy="742950"`):
```javascript
const drawingXml = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<xdr:wsDr xmlns:xdr="http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">\n<xdr:oneCellAnchor editAs="oneCell">\n<xdr:from>\n<xdr:col>1</xdr:col>\n<xdr:colOff>38100</xdr:colOff>\n<xdr:row>0</xdr:row>\n<xdr:rowOff>38100</xdr:rowOff>\n</xdr:from>\n<xdr:ext cx="1333500" cy="742950"/>\n<xdr:pic>\n<xdr:nvPicPr>\n<xdr:cNvPr id="2" name="Picture 3"/>\n<xdr:cNvPicPr>\n<a:picLocks noChangeAspect="1" noChangeArrowheads="1"/>\n</xdr:cNvPicPr>\n</xdr:nvPicPr>\n<xdr:blipFill>\n<a:blip xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" r:embed="rId1" cstate="print"/>\n<a:srcRect/>\n<a:stretch>\n<a:fillRect/>\n</a:stretch>\n</xdr:blipFill>\n<xdr:spPr bwMode="auto">\n<a:xfrm>\n<a:off x="38100" y="38100"/>\n<a:ext cx="1333500" cy="742950"/>\n</a:xfrm>\n<a:prstGeom prst="rect">\n<a:avLst/>\n</a:prstGeom>\n<a:noFill/>\n<a:ln>\n<a:noFill/>\n</a:ln>\n</xdr:spPr>\n</xdr:pic>\n<xdr:clientData/>\n</xdr:oneCellAnchor>\n</xdr:wsDr>`;
```

- [ ] **Step 2: Update module version query strings to `?v=20260803-v9`**

Update query string parameters in `main.js`, `src/takeoff.js`, `src/excel.js`, `src/db.js`, `src/cloud-sync.js`, and `index.html` to `?v=20260803-v9`.

- [ ] **Step 3: Run `check_final.py`**

Run: `python check_final.py`
Expected: `Modal divs: opens=94, closes=94, net=0`.

- [ ] **Step 4: Commit and push**

```bash
git add main.js src/excel.js src/takeoff.js src/db.js src/cloud-sync.js index.html
git commit -m "feat: enlarge excel logo 1.3x to 140px x 78px maintaining 1.80:1 ratio and 100% sheet compliance"
git push origin main
```
