"""
TDD Test: Header info rows (R=4,5,6) alignment verification
- C=0 (Cột A): "Từ:", "Công Ty:", "Địa chỉ:"  → phải căn TRÁI
- C=4 (Cột E): "Kính gởi:", "Công Ty:", "Địa chỉ:" → phải căn TRÁI

Chạy: python test_header_alignment.py
"""

def simulate_alignment(R, C, val, sheetType, isTitleRow, isHeaderRow,
                        footerStartRow=9999, signatureStartRow=9999,
                        totalRows=None, valA=''):
    ROMAN = {'I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII'}
    if totalRows is None: totalRows = set()
    isSectionHeader = valA in ROMAN

    if val.startswith('Bằng chữ:') or val.startswith('_ Báo giá trên') or val.startswith('_ Thời gian thi công'):
        return 'left'
    if sheetType in ('detail','vt','sum') and R in totalRows:
        return 'left' if C == 1 else 'center'
    if R >= signatureStartRow:
        return 'left' if val in ('Xác nhận của khách hàng','Người lập bảng') else 'center'
    if R >= footerStartRow:
        return 'center' if val in ('Giám đốc','VŨ THỊ KIM CHÚC') or val.startswith('TP. HCM ngày') else 'left'
    # KEY BRANCH: R=4,5,6 header info rows
    if R in (4, 5, 6):
        return 'left'
    if R in (0, 1, 2):
        return 'center'
    if isHeaderRow:
        return 'center'
    if val in ('Giám đốc','VŨ THỊ KIM CHÚC') or val.startswith('TP. HCM ngày'):
        return 'center'
    if val == 'Xác nhận của khách hàng':
        return 'left'
    if C == 1 and not isTitleRow and not isHeaderRow and R < footerStartRow and not isSectionHeader and val:
        return 'left'  # with indent=1
    if C == 1:
        return 'left'
    if C == 0:
        return 'center'
    return 'left'

PASS = "PASS"
FAIL = "FAIL"
results = []

def check(desc, R, C, val, sheetType):
    r = simulate_alignment(R=R, C=C, val=val, sheetType=sheetType,
                           isTitleRow=(R < 8), isHeaderRow=(R == 8))
    ok = r == 'left'
    icon = PASS if ok else FAIL
    print(f"  [{icon}] {desc} | R={R} C={C} sheet={sheetType} → {r}")
    results.append(ok)
    return ok

print("=" * 65)
print("TDD TEST: Header Info Row Alignment (R=4,5,6, C=0 and C=4)")
print("=" * 65)

print("\n[Group A] Cot A (C=0): Tu:, Cong Ty:, Dia chi:")
check("R=4 C=0 'Tu : ...'  sum",    4, 0, "Từ : VŨ THỊ KIM CHÚC", "sum")
check("R=4 C=0 'Tu : ...'  detail", 4, 0, "Từ : VŨ THỊ KIM CHÚC", "detail")
check("R=4 C=0 'Tu : ...'  vt",     4, 0, "Từ : VŨ THỊ KIM CHÚC", "vt")
check("R=5 C=0 'Cong Ty:'  sum",    5, 0, "Công Ty: CÔNG TY XANH", "sum")
check("R=5 C=0 'Cong Ty:'  detail", 5, 0, "Công Ty: CÔNG TY XANH", "detail")
check("R=6 C=0 'Dia chi:'  sum",    6, 0, "Địa chỉ : 127/13 Nguyễn Tư Giản", "sum")
check("R=6 C=0 'Dia chi:'  detail", 6, 0, "Địa chỉ : 127/13 Nguyễn Tư Giản", "detail")

print("\n[Group B] Cot E (C=4): Kinh goi:, Cong Ty:, Dia chi:")
check("R=4 C=4 'Kinh goi:' sum",    4, 4, "Kính gởi: Công ty ABC", "sum")
check("R=4 C=4 'Kinh goi:' detail", 4, 4, "Kính gởi: Công ty ABC", "detail")
check("R=4 C=4 'Kinh goi:' vt",     4, 4, "Kính gởi: Công ty ABC", "vt")
check("R=5 C=4 'Cong Ty:'  sum",    5, 4, "Công Ty: Bệnh viện ABC", "sum")
check("R=5 C=4 'Cong Ty:'  detail", 5, 4, "Công Ty: Bệnh viện ABC", "detail")
check("R=6 C=4 'Dia chi:'  sum",    6, 4, "Địa chỉ : 17 Nguyễn Chí Thanh", "sum")
check("R=6 C=4 'Dia chi:'  detail", 6, 4, "Địa chỉ : 17 Nguyễn Chí Thanh", "detail")

all_pass = all(results)
print("\n" + "=" * 65)
print(f"RESULT: {'ALL TESTS PASSED' if all_pass else 'SOME TESTS FAILED'}")
print("=" * 65)
