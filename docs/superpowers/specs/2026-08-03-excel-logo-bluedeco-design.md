# Design Spec: Thêm Logo Bluedeco vào File Excel (Bảo Toàn Tỷ Lệ Gốc 1.80:1)

**Ngày:** 2026-08-03  
**Trạng thái:** Đã duyệt bởi người dùng (Phương án 1 - oneCellAnchor 108px x 60px)

---

## 1. Mục tiêu
Bảo toàn 100% tỷ lệ khung hình gốc (Aspect Ratio 1.80:1) của tệp ảnh logo thương hiệu BlueDeco (`logo-bluedecor.png` - 931px x 517px) khi hiển thị trong tất cả các trang tính Excel. Ngăn chặn hoàn toàn hiện tượng logo bị biến dạng hay kéo giãn.

---

## 2. Thông số Kỹ thuật Logo

- **Tệp nguồn ảnh**: `logo-bluedecor.png` (Gốc: 931px × 517px, tỷ lệ 1.8008 : 1).
- **Vị trí neo (Anchor)**: Neo góc trên trái tại **ô B1** (Col = 1, Row = 0).
- **Cấu trúc Anchor**: Khóa bằng `<xdr:oneCellAnchor editAs="oneCell">`.
- **Kích thước hiển thị**:
  - Chiều rộng (`width`): `108px` (`cx = 1028700` EMUs).
  - Chiều cao (`height`): `60px` (`cy = 571500` EMUs).
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
    <xdr:ext cx="1028700" cy="571500"/>
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
          <a:ext cx="1028700" cy="571500"/>
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
- `src/excel.js`: Cập nhật chuỗi XML trong `injectLogoToBuffer()` và `triggerAutoSync()` sang `oneCellAnchor` với `cx=1028700, cy=571500`.
- `main.js`, `index.html`: Cập nhật phiên bản Cache-Buster `?v=20260803-v6`.

---

## 5. Verification Plan
- [ ] Xuất file Excel: Logo xuất hiện ở B1 sắc nét, đúng tỷ lệ `1.80:1` (108px x 60px), không bị méo hay biến dạng.
- [ ] Chạy `check_final.py` xác minh cú pháp và HTML.
