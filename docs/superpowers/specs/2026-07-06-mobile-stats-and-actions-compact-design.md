# Dac ta Thiet ke: Thu Gon Stats Bar & Mo Rong Hang Nut Hanh Dong Tren Mobile

## Muc tieu
Cai thien trai nghiem mobile bang 2 thay doi:
1. **Thu nho 4 o thong ke** (Phong, Hang muc, M2 san, M2 tuong) ~50% chieu cao.
2. **Mo rong hang nut hanh dong** (Sua / Xoa / Don bo nho + Loc phong) full-width man hinh.
3. **Bat cuon toan trang** tren mobile.

---

## 1. Thu Nho 4 O Thong Ke

Giu bo cuc 2x2, giam padding va font-size:

| Thuoc tinh | Hien tai | Moi |
|---|---|---|
| .stat-item padding | 14px 16px | 8px 10px |
| .stat-value font-size | 22px | 16px |
| .stat-label font-size | 10px | 9px |
| .stats-bar gap | 12px | 8px |
| .stats-bar margin-bottom | 20px | 10px |

---

## 2. Mo Rong Hang Nut Hanh Dong Full-Width

### Cau truc HTML moi

Tach project-actions thanh 2 sub-div:
- project-btn-row: chua 3 nut (Sua, Xoa, Don bo nho)
- project-filter-row: chua Loc phong + select

Tren mobile (<=600px):
- .project-btn-row: display:flex; width:100%; gap:8px
- Moi nut: flex:1; justify-content:center; min-height:42px
- .project-filter-row: width:100%; display:flex; align-items:center; gap:8px
- select: flex:1

---

## 3. Cuon Toan Trang Tren Mobile

Them vao @media (max-width: 600px):
- .app-wrapper: height:auto; overflow:visible
- .main-layout: overflow:visible
- .workspace: overflow-y:visible; height:auto

---

## Kiem thu

- node -c src/takeoff.js
- python check_final.py
- Kiem tra tren DevTools mobile: stats nho gon, nut full-width, trang cuon duoc
