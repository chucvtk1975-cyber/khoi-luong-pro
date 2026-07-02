"""
Patch app.js:
- Cập nhật buildHeader theo chuẩn FILE MẪU (Times New Roman, đúng layout)
- Cập nhật applyBorders (cột liền, hàng đứt)
- Cập nhật applyStyleSheet (thêm cell style cho header)
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8') as f:
    content = f.read()

print("File size:", len(content), "chars")

# ============================================================
# 1. Thay thế buildHeader
# ============================================================
OLD_BUILD = "const buildHeader = (aoaArray, mergesArray, title, maxCols) => {"
NEW_BUILD = r"""const buildHeader = (aoaArray, mergesArray, title, maxCols) => {
    const blk = () => Array(maxCols).fill('');
    // Row 0 (Excel row 1): Tiêu đề chính — center từ C(idx 2) đến hết
    const r0 = blk(); r0[2] = title; aoaArray.push(r0);
    // Row 1 (Excel row 2): Subtitle / tên dự án
    const r1 = blk(); r1[2] = project.subtitle || project.name || ''; aoaArray.push(r1);
    // Row 2 (Excel row 3): CÔNG TRÌNH: [tên]
    const r2 = blk(); r2[2] = `CÔNG TRÌNH: ${project.name || ''}`.toUpperCase(); aoaArray.push(r2);
    // Row 3 (Excel row 4): Blank
    aoaArray.push(blk());
    // Row 4 (Excel row 5): Từ | Kính gởi
    const r4 = blk(); r4[0] = `Từ : ${project.sender || ''}`; r4[4] = `Kính gởi: ${project.recipient || project.client || ''}`; aoaArray.push(r4);
    // Row 5 (Excel row 6): Công Ty bên A | Công Ty bên B
    const r5 = blk(); r5[0] = `Công Ty: ${project.company || ''}`; r5[4] = `Công Ty: ${project.clientCo || ''}`; aoaArray.push(r5);
    // Row 6 (Excel row 7): Địa chỉ bên A | Địa chỉ bên B
    const r6 = blk(); r6[0] = `Địa chỉ : ${project.companyAddr || ''}`; r6[4] = `Địa chỉ : ${project.clientAddr || project.address || ''}`; aoaArray.push(r6);
    // Row 7 (Excel row 8): Blank
    aoaArray.push(blk());

    // Merges phần header thông tin (rows 0-6, tức Excel rows 1-7)
    // Row 0,1,2: C(2) → cuối = merge [2..maxCols-1], A(0) chỉ 1 ô
    [0,1,2].forEach(r => mergesArray.push({s:{r,c:2}, e:{r,c:maxCols-1}}));
    // Row 4,5,6: Từ = A(0)..C(3), Kính gởi = E(4)..cuối
    [4,5,6].forEach(r => {
      mergesArray.push({s:{r,c:0}, e:{r,c:3}});
      mergesArray.push({s:{r,c:4}, e:{r,c:maxCols-1}});
    });
  };"""

if OLD_BUILD in content:
    # Tìm điểm kết thúc hàm cũ (tìm "  };" sau OLD_BUILD)
    start_idx = content.find(OLD_BUILD)
    # Tìm "  };" kết thúc buildHeader - tìm pattern đặc trưng
    end_marker = "  };\n"
    end_idx = content.find(end_marker, start_idx + len(OLD_BUILD))
    if end_idx == -1:
        end_marker = "  };"
        end_idx = content.find(end_marker, start_idx + len(OLD_BUILD))
    
    if end_idx != -1:
        old_block = content[start_idx:end_idx + len(end_marker)]
        content = content.replace(old_block, NEW_BUILD + "\n", 1)
        print("✓ buildHeader replaced (chars", start_idx, "to", end_idx+len(end_marker), ")")
    else:
        print("✗ Could not find end of buildHeader")
else:
    print("✗ OLD_BUILD not found")

# ============================================================
# 2. Thêm hàm applyStyles sau applyBorders (style cell cho xlsx-style)
# ============================================================
APPLY_STYLES_MARKER = "function xlsxWrite(wb, fileName) {"

NEW_STYLES_FUNC = r"""// Áp dụng cell styles (font, fill, alignment) cho toàn sheet theo chuẩn FILE MẪU
// headerDataRow: row index (0-based) của dòng đầu tiên có data (thường row 8 = index 8)
function applySheetStyles(ws, headerDataRow) {
  if (!ws['!ref']) return;
  const range = XLSX.utils.decode_range(ws['!ref']);
  // Màu nền header bảng = theme:8 tint:0.8 ≈ #BDD7EE (xanh nhạt Excel)
  const HDR_BG  = 'BDD7EE';
  const WHITE   = 'FFFFFF';

  // Font mặc định toàn sheet: Times New Roman 12
  const baseFont = { name: 'Times New Roman', sz: 12, bold: false, color: { rgb: '000000' } };
  const boldFont = { name: 'Times New Roman', sz: 12, bold: true,  color: { rgb: '000000' } };

  // Borders
  const solidBlack  = { style: 'thin',   color: { rgb: '000000' } };
  const solidMedium = { style: 'medium', color: { rgb: '000000' } };
  const dashedBlack = { style: 'dashed', color: { rgb: '000000' } };

  const hdrRow = (headerDataRow !== undefined) ? headerDataRow : 8; // row index 8,9 = Excel row 9,10

  for (let R = range.s.r; R <= range.e.r; R++) {
    for (let C = range.s.c; C <= range.e.c; C++) {
      const ref = XLSX.utils.encode_cell({ r: R, c: C });
      if (!ws[ref]) ws[ref] = { t: 's', v: '' };
      ws[ref].s = ws[ref].s || {};

      const isHeaderRow  = (R === hdrRow || R === hdrRow + 1); // 2 dòng header bảng
      const isTitleRow   = (R < 8); // Các dòng tiêu đề phía trên
      const isBigTitle   = (R === 0); // Dòng tiêu đề lớn nhất (Times 24 bold)
      const isMedTitle   = (R === 1 || R === 2); // Times 14 bold

      // Font
      let font;
      if (isBigTitle) {
        font = { name: 'Times New Roman', sz: 24, bold: true, color: { rgb: '000000' } };
      } else if (isMedTitle) {
        font = { name: 'Times New Roman', sz: 14, bold: true, color: { rgb: '000000' } };
      } else if (isHeaderRow) {
        font = { ...boldFont };
      } else if (isTitleRow && (R === 4 || R === 5)) {
        font = { ...boldFont };
      } else {
        font = { ...baseFont };
      }
      ws[ref].s.font = font;

      // Fill
      if (isHeaderRow) {
        ws[ref].s.fill = { patternType: 'solid', fgColor: { rgb: HDR_BG }, bgColor: { rgb: HDR_BG } };
      }

      // Alignment
      if (R === 0 || R === 1 || R === 2) {
        ws[ref].s.alignment = { horizontal: 'center', vertical: 'center', wrapText: false };
      } else if (isHeaderRow) {
        ws[ref].s.alignment = { horizontal: 'center', vertical: 'center', wrapText: true };
      } else if (C === 0) {
        ws[ref].s.alignment = { horizontal: 'center', vertical: 'center', wrapText: true };
      } else if (C === 1) {
        ws[ref].s.alignment = { horizontal: 'left', vertical: 'center', wrapText: true };
      } else if (C >= range.e.c - 2) {
        ws[ref].s.alignment = { horizontal: 'right', vertical: 'center', wrapText: false };
      }

      // Borders: chỉ từ dòng header bảng trở xuống
      if (R >= hdrRow) {
        if (isHeaderRow) {
          ws[ref].s.border = {
            top: solidMedium, bottom: solidMedium,
            left: solidMedium, right: solidMedium,
          };
        } else {
          ws[ref].s.border = {
            top:    dashedBlack,
            bottom: dashedBlack,
            left:   solidBlack,
            right:  solidBlack,
          };
        }
      }
    }
  }
}

function xlsxWrite(wb, fileName) {"""

if APPLY_STYLES_MARKER in content:
    content = content.replace(APPLY_STYLES_MARKER, NEW_STYLES_FUNC, 1)
    print("✓ applySheetStyles inserted before xlsxWrite")
else:
    print("✗ xlsxWrite marker not found")

# ============================================================
# 3. Thay thế tất cả applyBorders(ws... → applySheetStyles(ws...
#    và điều chỉnh tham số
# ============================================================
import re

# Thay applyBorders(wsSum, 9) → applySheetStyles(wsSum, 8)
content = content.replace('applyBorders(wsSum, 9)', 'applySheetStyles(wsSum, 8)')
content = content.replace('applyBorders(wsVT, 9)', 'applySheetStyles(wsVT, 8)')
content = content.replace('applyBorders(wsDetail, 10)', 'applySheetStyles(wsDetail, 8)')
content = content.replace('applyBorders(wsSig, 9)', 'applySheetStyles(wsSig, 8)')
print("✓ applyBorders calls replaced with applySheetStyles")

# ============================================================
# 4. Cập nhật col widths cho sheet chi tiết phòng (10 cột A-J)
#    theo đúng file mẫu: A=6.33, B=35, C-H default(~8.43), I=13.41, J=12.75
# ============================================================
OLD_COLS_DETAIL = """    wsDetail['!cols'] = [
      { wch: 5  },  // STT
      { wch: 36 },  // HẠNG MỤC"""

NEW_COLS_DETAIL = """    wsDetail['!cols'] = [
      { wch: 6.33 },  // STT (A) - theo file mẫu
      { wch: 35.0 },  // HẠNG MỤC (B) - theo file mẫu"""

if OLD_COLS_DETAIL in content:
    content = content.replace(OLD_COLS_DETAIL, NEW_COLS_DETAIL, 1)
    print("✓ wsDetail col A,B widths updated")
else:
    print("✗ wsDetail cols not found - skipping")

# Cập nhật I và J của wsDetail
OLD_IJ = """      { wch: 12 },  // ĐƠN GIÁ
      { wch: 14 },  // THÀNH TIỀN
      { wch: 24 },  // ĐỊNH MỨC HAO HỤT
    ];  // Tổng = 134"""

NEW_IJ = """      { wch: 13.41 },  // ĐƠN GIÁ (I) - theo file mẫu
      { wch: 12.75 },  // THÀNH TIỀN (J) - theo file mẫu
      // Cột J là cuối - file mẫu chỉ có 10 cột A-J
    ];"""

if OLD_IJ in content:
    content = content.replace(OLD_IJ, NEW_IJ, 1)
    print("✓ wsDetail col I,J widths updated")
else:
    print("✗ wsDetail col I,J not found")

# ============================================================
# 5. Ghi lại file
# ============================================================
with open('app.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✅ Done! app.js updated successfully.")
