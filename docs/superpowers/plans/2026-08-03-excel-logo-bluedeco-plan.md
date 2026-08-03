# Excel Logo Bluedeco Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Automatically inject the Bluedeco brand logo (`logo-bluedecor.png`) at Column B, Row 1 (B1) left-aligned in 100% of exported Excel worksheets.

**Architecture:** Implement `injectLogoToBuffer(binBuf)` in `src/excel.js` using `JSZip` to load SheetJS binary buffers, inject XML drawing relationships and drawing1.xml for B1 left-aligned logo positioning, and write the updated buffer before file download in `xlsxWriteSheetJS` and `exportExcel`.

**Tech Stack:** Vanilla JavaScript ES6, SheetJS (`xlsx-js-style`), JSZip.

## Global Constraints
- Preserve left-alignment of Note Rows (`Bằng chữ:...`, `_ Báo giá...`) and Column B hạng mục data rows.
- Logo must start at Column B (col=1), Row 1 (row=0) and be left-aligned.
- Bump cache buster query string in `index.html` and ES6 module imports to `?v=20260803-v5`.

---

### Task 1: Add `injectLogoToBuffer` Helper and Integrate into Excel Export in `src/excel.js`

**Files:**
- Modify: `src/excel.js`

**Interfaces:**
- Produces: `injectLogoToBuffer(binBuf)` helper function.

- [ ] **Step 1: Write `injectLogoToBuffer` in `src/excel.js`**

Add `injectLogoToBuffer(binBuf)` helper in `src/excel.js`:
```javascript
export async function injectLogoToBuffer(binBuf) {
  if (typeof JSZip === 'undefined' || !logoArrayBuffer) {
    return binBuf;
  }
  try {
    const zip = await JSZip.loadAsync(binBuf);
    const sheetFiles = Object.keys(zip.files).filter(name => name.startsWith("xl/worksheets/sheet") && name.endsWith(".xml"));

    for (const file of sheetFiles) {
      let xmlStr = await zip.file(file).async("string");

      if (xmlStr.includes("<pageMargins") && !xmlStr.includes("<headerFooter")) {
        const pageSetupXml = '<pageSetup paperSize="9" orientation="landscape" fitToWidth="1" fitToHeight="0" fitToPage="1"/>';
        const footerText = '&amp;L&amp;&quot;Arial,Italic&quot;Du-Toan-BlueAI Lab&amp;R&amp;&quot;Arial,Bold&quot;Trang &amp;P/&amp;N';
        const headerFooterXml = `<headerFooter oddFooter="${footerText}" evenFooter="${footerText}"/>`;
        xmlStr = xmlStr.replace(/(<pageMargins[^>]*\/>)/, `$1${pageSetupXml}${headerFooterXml}`);
      }

      if (!xmlStr.includes("<drawing")) {
        xmlStr = xmlStr.replace("</worksheet>", '<drawing r:id="rId2"/></worksheet>');
        const match = file.match(/sheet(\d+)\.xml/);
        if (match) {
          const sheetNum = match[1];
          const relsFile = `xl/worksheets/_rels/sheet${sheetNum}.xml.rels`;
          const sheetRelsXml = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">\n<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/drawing" Target="../drawings/drawing1.xml"/>\n</Relationships>`;
          zip.file(relsFile, sheetRelsXml);
        }
      }

      zip.file(file, xmlStr);
    }

    const drawingXml = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<xdr:wsDr xmlns:xdr="http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">\n<xdr:twoCellAnchor editAs="oneCell">\n<xdr:from>\n<xdr:col>1</xdr:col>\n<xdr:colOff>100000</xdr:colOff>\n<xdr:row>0</xdr:row>\n<xdr:rowOff>63500</xdr:rowOff>\n</xdr:from>\n<xdr:to>\n<xdr:col>1</xdr:col>\n<xdr:colOff>1976156</xdr:colOff>\n<xdr:row>3</xdr:row>\n<xdr:rowOff>100000</xdr:rowOff>\n</xdr:to>\n<xdr:pic>\n<xdr:nvPicPr>\n<xdr:cNvPr id="2" name="Picture 3"/>\n<xdr:cNvPicPr>\n<a:picLocks noChangeAspect="1" noChangeArrowheads="1"/>\n</xdr:cNvPicPr>\n</xdr:nvPicPr>\n<xdr:blipFill>\n<a:blip xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" r:embed="rId1" cstate="print"/>\n<a:srcRect/>\n<a:stretch>\n<a:fillRect/>\n</a:stretch>\n</xdr:blipFill>\n<xdr:spPr bwMode="auto">\n<a:xfrm>\n<a:off x="698500" y="63501"/>\n<a:ext cx="1476156" cy="844549"/>\n</a:xfrm>\n<a:prstGeom prst="rect">\n<a:avLst/>\n</a:prstGeom>\n<a:noFill/>\n<a:ln>\n<a:noFill/>\n</a:ln>\n</xdr:spPr>\n</xdr:pic>\n<xdr:clientData/>\n</xdr:twoCellAnchor>\n</xdr:wsDr>`;
    const drawingRelsXml = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">\n<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/image1.png"/>\n</Relationships>`;

    zip.file("xl/drawings/drawing1.xml", drawingXml);
    zip.file("xl/drawings/_rels/drawing1.xml.rels", drawingRelsXml);
    zip.file("xl/media/image1.png", logoArrayBuffer);

    let contentTypes = await zip.file("[Content_Types].xml").async("string");
    if (!contentTypes.includes("/xl/drawings/drawing1.xml")) {
      contentTypes = contentTypes.replace("</Types>", '<Override PartName="/xl/drawings/drawing1.xml" ContentType="application/vnd.openxmlformats-officedocument.drawing+xml"/></Types>');
      zip.file("[Content_Types].xml", contentTypes);
    }

    return await zip.generateAsync({ type: "arraybuffer" });
  } catch (err) {
    console.warn("Logo injection failed, returning original buffer:", err);
    return binBuf;
  }
}
```

- [ ] **Step 2: Update `xlsxWriteSheetJS` to call `injectLogoToBuffer`**

Update `xlsxWriteSheetJS(wb, fileName)` to be `async` and inject logo before creating blob download:
```javascript
async function xlsxWriteSheetJS(wb, fileName) {
  try {
    if (typeof XLSX === 'undefined') {
      throw new Error('Thư viện SheetJS (XLSX) chưa được tải thành công.');
    }
    const out = XLSX.write(wb, { bookType: 'xlsx', bookSST: false, type: 'binary' });
    let buf = s2ab(out);
    buf = await injectLogoToBuffer(buf);
    const blob = new Blob([buf], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = fileName;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  } catch (err) {
    console.error('Lỗi khi xuất file Excel:', err);
    alert('❌ Lỗi khi xuất file Excel: ' + err.message);
  }
}
```

- [ ] **Step 3: Update `exportExcel()` to be `async`**

Make `exportExcel()` `async` and call `await xlsxWriteSheetJS(wbData.wb, fileName)`.

- [ ] **Step 4: Update module version query strings to `?v=20260803-v5`**

Update query string parameters in `main.js`, `src/takeoff.js`, `src/excel.js`, `src/db.js`, `src/cloud-sync.js`, and `index.html` to `?v=20260803-v5`.

- [ ] **Step 5: Run verification script**

Run `python check_final.py` to confirm syntax validity.

- [ ] **Step 6: Commit and push**

```bash
git add main.js src/excel.js src/takeoff.js src/db.js src/cloud-sync.js index.html
git commit -m "feat: inject Bluedeco logo into Excel export at B1 left-aligned across all sheets"
git push origin main
```
