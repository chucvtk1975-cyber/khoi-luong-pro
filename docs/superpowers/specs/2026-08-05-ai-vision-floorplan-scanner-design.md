# AI Vision Floorplan & Room Survey Scanner Design Specification

## Overview
Integrate an AI Vision feature into the Room Creation/Editing Modal Wizard (Step 1) using **Google Gemini 2.0 Flash Lite Vision API**. The feature allows users to upload a floorplan drawing or room photo (JPG, PNG, HEIC, PDF). The AI analyzes the image and automatically extracts structured data in millimeters (`mm`) formatted with thousands separator dots (e.g. `5.400`, `4.200`, `3.000`) and categorizes item notes so they strictly match the app's internal calculation rules (`src/calc.js`) and Vietnamese Excel template export structures (`src/excel.js`).

## User Intent & Requirements
- **Primary Goal**: Auto-extract room dimensions and notes from floorplan drawings/survey photos using Gemini 2.0 Flash Lite Vision API.
- **Unit of Measurement & Formatting Constraint**: Dimensions (`length`, `width`, `height`) must be strictly in **millimeters (`mm`) formatted with thousands separator dots** (e.g. `5.400`, `4.200`, `3.000`), matching the app's Vietnamese number formatting rules (`fmtNum`).
- **Excel & Calculation Structure Alignment Constraint**: Extracted text notes (`roomNote`, `elecNoteLights`, `noteWoodwork`, `notePlumbing`) must strictly follow the natural language syntax expected by `src/calc.js` so that Excel export sheets ("Tổng hợp", "Chi tiết phòng", "Vật Tư Cần Mua") generate identical Roman numeral group headers, formulas, and material breakdowns as manual input.
- **Client-Side Execution**: Pure Vanilla JS execution via direct REST fetch to Google Gemini API. API key stored in `localStorage` under `gemini_api_key`.
- **Non-breaking Constraint**: All existing form fields, IDs, event bindings, and calculations remain intact.

## Detailed Architecture & UI Changes

### 1. API Key Configuration
- Add a Gemini API Key input field in the Supabase/Cloud Settings Modal (`#modal-supabase`).
- Persist in `localStorage.setItem('gemini_api_key', key)`.
- If key is missing when the user clicks `✨ AI Quét Bản Vẽ / Ảnh`, prompt user to enter their API key.

### 2. UI Component in Modal Step 1 (`#step-content-1`)
- Add a button **`✨ AI Quét Bản Vẽ / Ảnh`** near the top of `#step-content-1`.
- Hidden file input `#ai-vision-file-input` supporting images (`image/*`, `.heic`, `.heif`, `.pdf`).
- Loading status container `#ai-vision-loading-status` with spinner animation.

### 3. Gemini 2.0 Flash Lite Vision API Integration & System Instructions
- Endpoint: `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-lite:generateContent?key=${API_KEY}`
- Payload: Base64 image + System Instruction Prompt crafted specifically for Vietnamese construction takeoff:

```json
{
  "roomName": "Phòng Khách",
  "length": 5400,
  "width": 4200,
  "height": 3000,
  "elecNoteLights": "đèn downlight 6 bộ, đèn tuyp 2 bộ, panel 4 bộ",
  "noteWoodwork": "Tủ bếp trên 2,4m dài, tủ bếp dưới 2,4m dài, mặt đá granite\nTủ quần áo 3 cánh 1,8×2,4m, cửa gỗ HDF 2 cái",
  "notePlumbing": "Bồn cầu TOTO 1 cái, chậu rửa 1 cái, Chống thấm sàn WC Sika 2 lớp 4m²",
  "roomNote": "Trần cao 3.000, ốp gạch 1.800, nội 1.200, sơn nước 600 mm\nThêm máy lạnh 2 cái, quạt hút 1 cái, ổ cắm 3 bộ"
}
```

### 4. Auto-Fill Execution & Excel Integration
Upon successful AI response:
- Populates `#room-name`.
- Formats extracted dimensions using `fmtNum` to ensure thousand dot separators: `#room-length` (`5.400`), `#room-width` (`4.200`), `#room-height` (`3.000`).
- Populates `#note-woodwork`, `#note-plumbing`, `#room-note`, `#elec-note-lights` with exact natural language syntax.
- Existing calculation hooks in `src/calc.js` parse the filled notes into exact Roman numeral sections in Excel exports.

## Verification Plan

### Automated Verification
1. Run `node -c main.js src/*.js` to ensure 0 syntax errors.
2. Run `python check_final.py` to confirm HTML tag balance.

### Manual Verification
1. Click `✨ AI Quét Bản Vẽ / Ảnh` in Add Room modal.
2. Enter Gemini API key if prompted.
3. Upload sample floorplan/room photo.
4. Verify auto-filled dimensions are displayed with thousands separator dots (e.g. `5.400`, `4.200`, `3.000`).
5. Verify auto-filled notes trigger correct calculations and generate standard Excel export sheets.
