# Excel Logo Injection — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Thêm logo Bluedeco vào tất cả các sheet Excel xuất ra (cột B, hàng 1-3), áp dụng cho cả luồng SheetJS (regular export) lẫn ExcelJS (photos export).

**Architecture:** Tạo shared helper `injectLogoToBuffer()` chứa logic JSZip logo injection, sau đó tích hợp vào `exportExcel()` (SheetJS) và `xlsxWritePhotos()` (ExcelJS). Refactor `autoSyncProjectFiles()` để dùng chung helper, xóa code trùng lặp.

**Tech Stack:** SheetJS (xlsx-js-style), ExcelJS, JSZip — tất cả đều đã có sẵn trong dự án.

## Global Constraints

- File: `src/excel.js` — module ES6, không được thay đổi cấu trúc import/export hiện tại
- Giữ nguyên `LOGO_BASE64` và `logoArrayBuffer` đã khai báo ở đầu file
- Drawing XML logo đặt tại: cột B (col index 1), hàng 1-3 (row 0→3)
- Mọi thay đổi đều phải có graceful fallback (không crash nếu JSZip hoặc logoArrayBuffer không có)
- Bump cache-buster trong `index.html` sau mỗi lần sửa `src/excel.js`
- Chạy `git commit` sau mỗi task

---

## Task 1: Tạo `injectLogoToBuffer()` shared helper

**Files:**
- Modify: `src/excel.js` (thêm function sau L31, trước `function applyPageSetup`)

**Interfaces:**
- Produces: `async function injectLogoToBuffer(binBuf: ArrayBuffer): Promise<ArrayBuffer>`
  - Input: SheetJS binary ArrayBuffer (từ `s2ab(XLSX.write(...))`)
  - Output: ArrayBuffer mới đã inject logo, hoặc `binBuf` gốc nếu JSZip/logo không available

- [ ] **Step 1: Thêm function vào excel.js sau L31**

Thêm đoạn code sau ngay sau dòng `let logoArrayBuffer = base64ToArrayBuffer(LOGO_BASE64);` (L31):

```javascript
// ─── SHARED HELPER: Inject logo vào SheetJS ZIP buffer ───────────────────
// Nhận ArrayBuffer từ XLSX.write, trả về ArrayBuffer mới có logo ở cột B, hàng 1-3.
// Graceful fallback: nếu JSZip hoặc logoArrayBuffer không có → trả về buffer gốc.
async function injectLogoToBuffer(binBuf) {
  const logoBuf = logoArrayBuffer || null;
  if (!logoBuf || typeof JSZip === 'undefined') return binBuf;

  const zip = await JSZip.loadAsync(binBuf);
  const sheetFiles = Object.keys(zip.files)
    .filter(name => name.startsWith('xl/worksheets/sheet') && name.endsWith('.xml'));

  for (const file of sheetFiles) {
    let xmlStr = await zip.file(file).async('string');
    if (!xmlStr.includes('<drawing')) {
      xmlStr = xmlStr.replace('</worksheet>', '<drawing r:id="rId2"/></worksheet>');
      const match = file.match(/sheet(\d+)\.xml/);
      if (match) {
        const sheetNum = match[1];
        const relsFile = `xl/worksheets/_rels/sheet${sheetNum}.xml.rels`;
        zip.file(relsFile,
          `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n` +
          `<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">\n` +
          `<Relationship Id="rId2" ` +
          `Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/drawing" ` +
          `Target="../drawings/drawing1.xml"/>\n` +
          `</Relationships>`
        );
      }
    }
    zip.file(file, xmlStr);
  }

  // Drawing XML: logo ở Cột B (col=1), Hàng 1-3 (row 0→3)
  const drawingXml =
    `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n` +
    `<xdr:wsDr xmlns:xdr="http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing" ` +
    `xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">\n` +
    `<xdr:twoCellAnchor editAs="oneCell">\n` +
    `<xdr:from>\n<xdr:col>1</xdr:col>\n<xdr:colOff>500000</xdr:colOff>\n` +
    `<xdr:row>0</xdr:row>\n<xdr:rowOff>63501</xdr:rowOff>\n</xdr:from>\n` +
    `<xdr:to>\n<xdr:col>1</xdr:col>\n<xdr:colOff>1976156</xdr:colOff>\n` +
    `<xdr:row>3</xdr:row>\n<xdr:rowOff>100000</xdr:rowOff>\n</xdr:to>\n` +
    `<xdr:pic>\n<xdr:nvPicPr>\n<xdr:cNvPr id="2" name="Picture 3"/>\n` +
    `<xdr:cNvPicPr>\n<a:picLocks noChangeAspect="1" noChangeArrowheads="1"/>\n` +
    `</xdr:cNvPicPr>\n</xdr:nvPicPr>\n` +
    `<xdr:blipFill>\n<a:blip xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" ` +
    `r:embed="rId1" cstate="print"/>\n<a:srcRect/>\n<a:stretch>\n<a:fillRect/>\n` +
    `</a:stretch>\n</xdr:blipFill>\n` +
    `<xdr:spPr bwMode="auto">\n<a:xfrm>\n<a:off x="698500" y="63501"/>\n` +
    `<a:ext cx="1476156" cy="844549"/>\n</a:xfrm>\n` +
    `<a:prstGeom prst="rect">\n<a:avLst/>\n</a:prstGeom>\n` +
    `<a:noFill/>\n<a:ln>\n<a:noFill/>\n</a:ln>\n</xdr:spPr>\n` +
    `</xdr:pic>\n<xdr:clientData/>\n</xdr:twoCellAnchor>\n</xdr:wsDr>`;

  const drawingRelsXml =
    `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n` +
    `<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">\n` +
    `<Relationship Id="rId1" ` +
    `Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" ` +
    `Target="../media/image1.png"/>\n` +
    `</Relationships>`;

  zip.file('xl/drawings/drawing1.xml', drawingXml);
  zip.file('xl/drawings/_rels/drawing1.xml.rels', drawingRelsXml);
  zip.file('xl/media/image1.png', logoBuf);

  let contentTypes = await zip.file('[Content_Types].xml').async('string');
  if (!contentTypes.includes('/xl/drawings/drawing1.xml')) {
    contentTypes = contentTypes.replace(
      '</Types>',
      '<Override PartName="/xl/drawings/drawing1.xml" ' +
      'ContentType="application/vnd.openxmlformats-officedocument.drawing+xml"/></Types>'
    );
    zip.file('[Content_Types].xml', contentTypes);
  }

  return await zip.generateAsync({ type: 'arraybuffer' });
}
// ─────────────────────────────────────────────────────────────────────────────
```

- [ ] **Step 2: Commit**

```bash
git add src/excel.js
git commit -m "feat: add injectLogoToBuffer() shared helper for Excel logo injection"
```

---

## Task 2: Sửa `exportExcel()` — dùng helper cho SheetJS download

**Files:**
- Modify: `src/excel.js` (~L3169, hàm `exportExcel`)

**Interfaces:**
- Consumes: `injectLogoToBuffer(binBuf: ArrayBuffer): Promise<ArrayBuffer>` (Task 1)
- Produces: `exportExcel()` là `async function`, download Excel có logo

- [ ] **Step 1: Sửa `exportExcel()` — thêm `async` và thay `xlsxWriteSheetJS`**

Tìm đoạn (khoảng L3169-3199):
```javascript
export function exportExcel() {
  try {
    ...
    const wbData = generateWorkbook(project);
    if (!wbData) return;

    const dateStr = ...
    const fileName = ...

    // Xuất trực tiếp bằng SheetJS
    xlsxWriteSheetJS(wbData.wb, fileName);

    // Increment export count
    ...
  } catch (err) {
```

Thay bằng:
```javascript
export async function exportExcel() {
  try {
    if (typeof XLSX === 'undefined') {
      throw new Error('Thư viện SheetJS (XLSX) chưa được tải thành công. Vui lòng kiểm tra kết nối mạng!');
    }

    const project = DB.get(state.currentProjectId);
    if (!project) {
      throw new Error('Không tìm thấy dự án hiện tại!');
    }

    const wbData = generateWorkbook(project);
    if (!wbData) return;

    const dateStr = new Date().toLocaleDateString('vi-VN').replace(/\//g, '-');
    const safeProjName = (project.name || 'Du_Toan').trim().replace(/[^a-zA-Z0-9À-ỹ]+/g, '_');
    const fileName = `${safeProjName}_KhoiLuong_${dateStr}.xlsx`;

    // Ghi workbook ra binary rồi inject logo qua JSZip
    const out = XLSX.write(wbData.wb, { bookType: 'xlsx', bookSST: false, type: 'binary' });
    const binBuf = s2ab(out);
    const finalBuf = await injectLogoToBuffer(binBuf);

    const blob = new Blob([finalBuf], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = fileName;
    document.body.appendChild(a);
    a.click();
    setTimeout(() => { URL.revokeObjectURL(url); document.body.removeChild(a); }, 100);

    // Increment export count in localStorage
    const currentCount = parseInt(localStorage.getItem('bkl_export_count') || '0');
    try {
      localStorage.setItem('bkl_export_count', (currentCount + 1).toString());
    } catch (e) {}
    if (typeof updateDashboardStats === 'function') updateDashboardStats();
  } catch (err) {
    console.error('Lỗi khi xuất khối lượng Excel:', err);
    alert('❌ Lỗi khi xuất khối lượng Excel: ' + err.message);
  }
}
```

- [ ] **Step 2: Kiểm tra thủ công**

  1. Mở app trong browser
  2. Tạo hoặc mở 1 dự án có phòng
  3. Nhấn **Xuất Excel** (nút regular, không phải nút ảnh)
  4. Mở file → kiểm tra logo xuất hiện ở cột B, hàng 1-3 trong **TẤT CẢ** sheets (Tổng Hợp, Chi Tiết Phòng, Vật Tư)
  5. Mở Developer Console → không có lỗi JS

- [ ] **Step 3: Commit**

```bash
git add src/excel.js
git commit -m "feat: exportExcel() now injects logo via injectLogoToBuffer helper"
```

---

## Task 3: Sửa `xlsxWritePhotos()` — thêm logo qua ExcelJS API

**Files:**
- Modify: `src/excel.js` (~L1497, trước `await workbook.xlsx.writeBuffer()`)

**Interfaces:**
- Consumes: `LOGO_BASE64` (đã khai báo đầu file), `workbook` (ExcelJS Workbook object đã có sheets)

- [ ] **Step 1: Thêm logo injection trước `writeBuffer()`**

Tìm đoạn (~L1491-1498):
```javascript
  // Cập nhật trạng thái lưu file Excel
  if (btn) {
    btn.innerHTML = `<i data-lucide="loader" class="spin"></i> Đang tạo file Excel...`;
    if (window.lucide) window.lucide.createIcons();
  }

  // Ghi tệp ExcelJS và kích hoạt tải về điện thoại/PC
  const finalBuffer = await workbook.xlsx.writeBuffer();
```

Thêm đoạn logo injection VÀO GIỮA hai block trên:

```javascript
  // Cập nhật trạng thái lưu file Excel
  if (btn) {
    btn.innerHTML = `<i data-lucide="loader" class="spin"></i> Đang tạo file Excel...`;
    if (window.lucide) window.lucide.createIcons();
  }

  // ── Thêm logo Bluedeco vào header mỗi sheet (Cột B, hàng 1-3) ──
  if (LOGO_BASE64) {
    try {
      const logoImageId = workbook.addImage({
        base64: LOGO_BASE64,
        extension: 'png',
      });
      workbook.worksheets.forEach(sheet => {
        sheet.addImage(logoImageId, {
          tl: { col: 1, row: 0 },
          br: { col: 2, row: 3 },
          editAs: 'oneCell',
        });
      });
    } catch (logoErr) {
      console.warn('Logo injection failed for ExcelJS:', logoErr);
    }
  }

  // Ghi tệp ExcelJS và kích hoạt tải về điện thoại/PC
  const finalBuffer = await workbook.xlsx.writeBuffer();
```

- [ ] **Step 2: Kiểm tra thủ công**

  1. Nhấn **Xuất Excel ảnh** (ExcelJS path)
  2. Mở file → kiểm tra logo xuất hiện ở cột B, hàng 1-3 trong header mỗi sheet ảnh
  3. Ảnh phòng vẫn hiển thị bình thường (không bị ghi đè)
  4. Không có lỗi JS console

- [ ] **Step 3: Commit**

```bash
git add src/excel.js
git commit -m "feat: add logo to ExcelJS photos export via workbook.addImage"
```

---

## Task 4: Refactor `autoSyncProjectFiles()` — dùng shared helper

**Files:**
- Modify: `src/excel.js` (~L3300-3343, hàm `autoSyncProjectFiles`)

**Interfaces:**
- Consumes: `injectLogoToBuffer(binBuf: ArrayBuffer): Promise<ArrayBuffer>` (Task 1)

- [ ] **Step 1: Refactor để xóa code duplicate trong autoSyncProjectFiles**

Tìm đoạn trong `autoSyncProjectFiles` (~L3300-3344):
```javascript
    const logoBuf = logoArrayBuffer || null;
    const zip = await JSZip.loadAsync(buf);

    const sheetFiles = Object.keys(zip.files).filter(name => name.startsWith("xl/worksheets/sheet") && name.endsWith(".xml"));

    for (const file of sheetFiles) {
      let xmlStr = await zip.file(file).async("string");

      if (xmlStr.includes("<pageMargins") && !xmlStr.includes("<headerFooter")) {
        const pageSetupXml = '...';
        const footerText = '...';
        const headerFooterXml = `...`;
        xmlStr = xmlStr.replace(/(<pageMargins[^>]*\/>)/, `$1${pageSetupXml}${headerFooterXml}`);
      }

      if (logoBuf && !xmlStr.includes("<drawing")) {
        xmlStr = xmlStr.replace("</worksheet>", '<drawing r:id="rId2"/></worksheet>');
        const match = file.match(/sheet(\d+)\.xml/);
        if (match) {
          const sheetNum = match[1];
          const relsFile = `xl/worksheets/_rels/sheet${sheetNum}.xml.rels`;
          const sheetRelsXml = `...`;
          zip.file(relsFile, sheetRelsXml);
        }
      }

      zip.file(file, xmlStr);
    }

    if (logoBuf) {
      const drawingXml = `...`;
      const drawingRelsXml = `...`;
      zip.file("xl/drawings/drawing1.xml", drawingXml);
      zip.file("xl/drawings/_rels/drawing1.xml.rels", drawingRelsXml);
      zip.file("xl/media/image1.png", logoBuf);
      let contentTypes = await zip.file("[Content_Types].xml").async("string");
      if (!contentTypes.includes("/xl/drawings/drawing1.xml")) {
        contentTypes = contentTypes.replace("</Types>", '...');
        zip.file("[Content_Types].xml", contentTypes);
      }
    }

    const zipBase64 = await zip.generateAsync({ type: "base64" });
```

Thay bằng (chỉ giữ page setup, dùng shared helper cho logo):
```javascript
    const zip = await JSZip.loadAsync(buf);

    const sheetFiles = Object.keys(zip.files).filter(name => name.startsWith("xl/worksheets/sheet") && name.endsWith(".xml"));

    // Chỉ fix page setup; logo sẽ được inject bởi injectLogoToBuffer()
    for (const file of sheetFiles) {
      let xmlStr = await zip.file(file).async("string");

      if (xmlStr.includes("<pageMargins") && !xmlStr.includes("<headerFooter")) {
        const pageSetupXml = '<pageSetup paperSize="9" orientation="landscape" fitToWidth="1" fitToHeight="0" fitToPage="1"/>';
        const footerText = '&amp;L&amp;"Arial,Italic"Du-Toan-BlueAI Lab&amp;R&amp;"Arial,Bold"Trang &amp;P/&amp;N';
        const headerFooterXml = `<headerFooter oddFooter="${footerText}" evenFooter="${footerText}"/>`;
        xmlStr = xmlStr.replace(/(<pageMargins[^>]*\/>)/, `$1${pageSetupXml}${headerFooterXml}`);
      }

      zip.file(file, xmlStr);
    }

    // Inject logo dùng shared helper
    const pageFixedBuf = await zip.generateAsync({ type: 'arraybuffer' });
    const logoInjectBuf = await injectLogoToBuffer(pageFixedBuf);
    const zipBase64 = await JSZip.loadAsync(logoInjectBuf).then(z => z.generateAsync({ type: "base64" }));
```

- [ ] **Step 2: Kiểm tra console.log sync hoạt động bình thường**

  Nếu có server sync endpoint, trigger nó và xem log. Nếu không, chỉ cần verify không có lỗi runtime.

- [ ] **Step 3: Commit**

```bash
git add src/excel.js
git commit -m "refactor: autoSyncProjectFiles uses injectLogoToBuffer, removes duplicate logo code"
```

---

## Task 5: Bump version & Deploy

**Files:**
- Modify: `index.html` (bump cache-buster)

- [ ] **Step 1: Bump cache-buster lên v17**

Trong `index.html`, tìm:
```html
<script type="module" src="main.js?v=20260707-v16"></script>
```

Thay bằng:
```html
<script type="module" src="main.js?v=20260707-v17"></script>
```

- [ ] **Step 2: Commit và push**

```bash
git add index.html
git commit -m "chore: bump cache-buster to v17 after Excel logo injection feature"
git push origin main
```

- [ ] **Step 3: Deploy Vercel**

```bash
npx vercel --prod --yes
```

Expected output cuối cùng:
```
Aliased: https://khoi-luong-pro.vercel.app
```

- [ ] **Step 4: Regression checklist cuối**

  - [ ] Xuất Excel thường → logo cột B, hàng 1-3 ở MỌI sheet (Tổng Hợp + Chi Tiết × N + Vật Tư)
  - [ ] Xuất Excel ảnh → logo ở header mỗi sheet ảnh
  - [ ] Alignment không bị ảnh hưởng: Từ/Công Ty/Địa chỉ căn trái, HẠNG MỤC căn trái + indent
  - [ ] Bằng chữ căn trái, Giám đốc căn giữa
  - [ ] Không có lỗi JS console
  - [ ] Fallback OK: file download được ngay cả khi logo injection gặp lỗi
