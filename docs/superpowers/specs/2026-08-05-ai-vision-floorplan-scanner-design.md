# AI Vision Floorplan & Room Survey Scanner Design Specification

## Overview
Integrate an AI Vision feature into the Room Creation/Editing Modal Wizard (Step 1) using **Google Gemini 2.0 Flash Lite Vision API**. The feature allows users to upload a floorplan drawing or room photo (JPG, PNG, HEIC, PDF). The AI analyzes the image and automatically extracts structured data in millimeters (`mm`) to auto-fill the room inputs.

## User Intent & Requirements
- **Primary Goal**: Auto-extract room dimensions and notes from floorplan drawings/survey photos using Gemini 2.0 Flash Lite Vision API.
- **Unit of Measurement**: Dimensions (`length`, `width`, `height`) must be strictly in **millimeters (`mm`)** (e.g., `5400`, `4200`, `3000`), matching the app's standard dimension input fields.
- **Client-Side Execution**: Pure Vanilla JS execution via direct REST fetch to Google Gemini API. API key stored in `localStorage` under `gemini_api_key`.
- **Non-breaking Constraint**: All existing form fields, IDs, event bindings, and calculations remain intact.

## Detailed Architecture & UI Changes

### 1. API Key Configuration
- Add a Gemini API Key input field in the Supabase/Cloud Settings Modal (`#modal-supabase` or new modal section).
- Persist in `localStorage.setItem('gemini_api_key', key)`.
- If key is missing when the user clicks `✨ AI Quét Bản Vẽ / Ảnh`, prompt user to enter their API key.

### 2. UI Component in Modal Step 1 (`#step-content-1`)
- Add a button **`✨ AI Quét Bản Vẽ / Ảnh`** near the top of `#step-content-1`.
- Hidden file input `#ai-vision-file-input` supporting images (`image/*`, `.heic`, `.heif`, `.pdf`).
- Loading status container `#ai-vision-loading-status` with spinner animation.

### 3. Gemini 2.0 Flash Lite Vision API Integration
- Endpoint: `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-lite:generateContent?key=${API_KEY}`
- Payload: Base64 image + System Instruction Prompt explicitly demanding JSON output with dimensions in **millimeters (`mm`)**:

```json
{
  "roomName": "Phòng Khách",
  "length": 5400,
  "width": 4200,
  "height": 3000,
  "elecNoteLights": "đèn downlight 6 bộ, đèn led dây 12m",
  "noteWoodwork": "Kệ TV treo tường 2,0m dài, tủ giày 1,2m",
  "roomNote": "Trần thạch cao phẳng 3000mm, sơn nước màu kem"
}
```

### 4. Auto-Fill Execution
Upon successful AI response:
- Populates `#room-name`, `#room-length`, `#room-width`, `#room-height` (in mm).
- Populates `#note-woodwork`, `#room-note`, `#elec-note-lights` if extracted.
- Displays success badge: `✅ Đã trích xuất dữ liệu tự động (Đơn vị: mm)`.

## Verification Plan

### Automated Verification
1. Run `node -c main.js src/*.js` to ensure 0 syntax errors.
2. Run `python check_final.py` to confirm HTML tag balance.

### Manual Verification
1. Click `✨ AI Quét Bản Vẽ / Ảnh` in Add Room modal.
2. Enter Gemini API key if prompted.
3. Upload sample floorplan/room photo.
4. Verify auto-filled dimensions are in **millimeters (`mm`)** and notes are accurately populated.
