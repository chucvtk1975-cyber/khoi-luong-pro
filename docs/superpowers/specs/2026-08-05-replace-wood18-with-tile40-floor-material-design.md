# Replace Gỗ CN 18mm with Gạch 40×40 Floor Material Design Specification

## Overview
In the room survey material options (Floor Materials catalog `MATERIALS.floor` in `src/calc.js`), replace the entry `{ id: 'goCN18', label: 'Gỗ CN 18mm', unit: 'm²', waste: 0.10 }` with `{ id: 'gach4040', label: 'Gạch 40×40', unit: 'm²', waste: 0.05 }`.

## User Intent & Requirements
- **Goal**: Replace the floor material option "Gỗ CN 18mm" with "Gạch 40×40 +5%".
- **Target Item**: `MATERIALS.floor` array in `src/calc.js`.
- **Label**: `Gạch 40×40`
- **Waste Factor**: `0.05` (+5% waste margin).

## Detailed Code Changes

### Target File
- [src/calc.js](file:///d:/1_Kho%20tri%20th%E1%BB%A9c/khoi-luong-pro/src/calc.js) (line 13)

### Material Catalog Modification (`MATERIALS.floor`)
```javascript
// Before:
{ id: 'goCN18',    label: 'Gỗ CN 18mm',    unit: 'm²', waste: 0.10 },

// After:
{ id: 'gach4040',  label: 'Gạch 40×40',    unit: 'm²', waste: 0.05 },
```

### Cache-Buster Bump
- Bump cache-buster version parameter in `index.html` and `main.js` from `20260805-v2` to `20260805-v3`.

## Verification Plan

### Automated Verification
1. Run `node -c main.js src/calc.js src/cloud-sync.js src/db.js src/excel.js src/takeoff.js` to ensure 0 syntax errors.
2. Run `python check_final.py` to confirm HTML integrity.

### Manual Verification
1. Open the app in browser.
2. Navigate to room survey floor material selection.
3. Confirm that the pill "Gạch 40×40 +5%" is displayed in place of "Gỗ CN 18mm +10%".
4. Select "Gạch 40×40 +5%" and verify calculation and room save behavior.
