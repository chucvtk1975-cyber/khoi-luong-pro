# Design Spec: Thêm Logo Bluedeco vào File Excel (Bảo Toàn Tỷ Lệ Gốc 1.80:1 - Kích thước 1.3x 140px x 78px)

**Ngày:** 2026-08-03  
**Trạng thái:** Đã nâng kích thước logo lên 1.3 lần theo yêu cầu người dùng

---

## 1. Mục tiêu
Bảo toàn 100% tỷ lệ khung hình gốc (Aspect Ratio 1.80:1) của tệp ảnh logo thương hiệu BlueDeco (`logo-bluedecor.png` - 931px x 517px) với kích thước mở rộng **1.3 lần** (140px x 78px) hiển thị to nổi bật, sắc nét trong tất cả các trang tính Excel.

---

## 2. Thông số Kỹ thuật Logo (Tỷ lệ 1.3x)

- **Tệp nguồn ảnh**: `logo-bluedecor.png` (Gốc: 931px × 517px, tỷ lệ 1.8008 : 1).
- **Vị trí neo (Anchor)**: Neo góc trên trái tại **ô B1** (Col = 1, Row = 0).
- **Cấu trúc Anchor**: Khóa bằng `<xdr:oneCellAnchor editAs="oneCell">`.
- **Kích thước hiển thị MỚI (1.3x)**:
  - Chiều rộng (`width`): `140px` (`cx = 1333500` EMUs).
  - Chiều cao (`height`): `78px` (`cy = 742950` EMUs).
  - Tỷ lệ hiển thị: `1.80 : 1` (khớp hoàn hảo với ảnh gốc).
- **Khóa tỷ lệ hình ảnh**: Thêm thuộc tính `<a:picLocks noChangeAspect="1"/>` để Excel không kéo giãn khi thay đổi kích thước ô.

---

## 3. Kiến trúc XML Drawing (`xl/drawings/drawing1.xml`)

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<xdr:wsDr xmlns:xdr="http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
  <xdr:oneCellAnchor editAs="oneCell">
    <xdr:from>
      <xdr:col>1</xdr:col>
      <xdr:colOff>38100</xdr:colOff>
      <xdr:row>0</xdr:row>
      <xdr:rowOff>38100</xdr:rowOff>
    </xdr:from>
    <xdr:ext cx="1333500" cy="742950"/>
    <xdr:pic>
      <xdr:nvPicPr>
        <xdr:cNvPr id="2" name="Picture 3"/>
        <xdr:cNvPicPr>
          <a:picLocks noChangeAspect="1" noChangeArrowheads="1"/>
        </xdr:cNvPicPr>
      </xdr:nvPicPr>
      <xdr:blipFill>
        <a:blip xmlns:r="http://schemas.openxmlformats.org/package/2006/relationships" r:embed="rId1" cstate="print"/>
        <a:srcRect/>
        <a:stretch><a:fillRect/></a:stretch>
      </xdr:blipFill>
      <xdr:spPr bwMode="auto">
        <a:xfrm>
          <a:off x="38100" y="38100"/>
          <a:ext cx="1333500" cy="742950"/>
        </a:xfrm>
        <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
        <a:noFill/><a:ln><a:noFill/></a:ln>
      </xdr:spPr>
    </xdr:pic>
    <xdr:clientData/>
  </xdr:oneCellAnchor>
</xdr:wsDr>
```

---

## 4. File Thay Đổi
- `src/excel.js`: Cập nhật `cx=1333500, cy=742950` trong `injectLogoToBuffer()` và `triggerAutoSync()`.
- `main.js`, `index.html`: Cập nhật phiên bản Cache-Buster `?v=20260803-v9`.

---

## 5. Verification Plan
- [ ] Xuất file Excel: Logo xuất hiện ở B1 nổi bật, đúng tỷ lệ `1.80:1` (140px x 78px), không bị méo.
- [ ] Chạy `check_final.py` xác minh cú pháp.
