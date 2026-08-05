# AI Vision Floorplan & Room Survey Scanner Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Integrate an AI Vision feature into the Room Creation/Editing Modal Wizard (Step 1) using Google Gemini 2.0 Flash Lite Vision API to auto-fill room dimensions (formatted with thousand dot separators e.g. `5.400`, `4.200`, `3.000`) and survey notes.

**Architecture:** Client-side REST integration with `gemini-2.0-flash-lite:generateContent` using a custom system prompt that enforces strict JSON output format matching `src/calc.js` natural language parsing rules. API key is persisted in `localStorage` (`gemini_api_key`) and configurable via Supabase/Settings Modal.

**Tech Stack:** HTML5, Vanilla JavaScript (ES6 Modules), Google Gemini REST API.

## Global Constraints

- Target Files: `index.html`, `src/takeoff.js`, `src/cloud-sync.js`, `main.js`
- Dimensions must be formatted with thousand dot separators: `5.400`, `4.200`, `3.000` via `fmtNum`.
- Extracted text notes must match `src/calc.js` natural language parsing format.
- Bump Cache-Buster Query Param to `?v=20260805-v4`.

---

### Task 1: Add Gemini API Key setting UI in `index.html` and `src/cloud-sync.js`

**Files:**
- Modify: `index.html:1766-1796` (inside `#modal-supabase`)
- Modify: `src/cloud-sync.js`

**Interfaces:**
- Consumes: Supabase Modal UI.
- Produces: Gemini API Key setting persisted in `localStorage.getItem('gemini_api_key')`.

- [ ] **Step 1: Add Gemini API Key input in `#modal-supabase`**

Add input `#gemini-key` field inside `#modal-supabase` in `index.html`.

- [ ] **Step 2: Bind load and save handlers in `src/cloud-sync.js`**

Save key on `#btn-save-supabase` click and load key on modal open.

- [ ] **Step 3: Verify JS syntax**

Run: `node -c main.js src/*.js`

---

### Task 2: Add AI Scanner Button and AI Vision REST Logic in `index.html` and `src/takeoff.js`

**Files:**
- Modify: `index.html:266-280` (inside `#step-content-1`)
- Modify: `src/takeoff.js`

**Interfaces:**
- Consumes: Image file (JPG/PNG/HEIC/PDF base64) and `localStorage.getItem('gemini_api_key')`.
- Produces: Auto-filled `#room-name`, `#room-length` (`5.400`), `#room-width` (`4.200`), `#room-height` (`3.000`), `#note-woodwork`, `#note-plumbing`, `#room-note`, `#elec-note-lights`.

- [ ] **Step 1: Add AI Scanner UI elements in `#step-content-1` of `index.html`**

Add button `#btn-ai-scan-room`, hidden file input `#ai-vision-file-input`, and loading container `#ai-vision-loading-status`.

- [ ] **Step 2: Implement `triggerAiVisionScan(file)` function in `src/takeoff.js`**

Implement image conversion to base64, construct Gemini 2.0 Flash Lite Vision request payload with system prompt requesting JSON output, fetch response, parse JSON, format dimensions using `fmtNum`, and auto-fill modal form fields.

- [ ] **Step 3: Bump Cache-Buster version to `20260805-v4`**

Update `index.html` and `main.js` script query parameters to `?v=20260805-v4`.

- [ ] **Step 4: Verify JS syntax and HTML modal integrity**

Run: `node -c main.js src/*.js ; python check_final.py`

- [ ] **Step 5: Commit and Push to GitHub origin main**

Run: `git add index.html main.js src/takeoff.js src/cloud-sync.js ; git commit -m "feat: add AI Vision floorplan scanner using Gemini 2.0 Flash Lite" ; git push origin main`
