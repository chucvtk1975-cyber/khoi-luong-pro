# Reorder Room Note Above Furniture Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reorder the HTML form sections in `#step-content-3` (`index.html`) so that "GHI CHÚ PHÒNG (TÙY CHỌN)" is placed first at the top, and "THIẾT BỊ NỘI THẤT" is placed second below it.

**Architecture:** Swap the position of the DOM elements in `index.html` inside `#step-content-3`, update cache-buster version to `20260805-v2`, and push commits to GitHub to update GitHub Pages live.

**Tech Stack:** HTML5, Vanilla JavaScript (ES6).

## Global Constraints

- Target Files: `index.html`, `main.js`
- Element IDs preserved: `room-note`, `room-photo-input-overview`, `room-photo-thumbs-overview`, `note-woodwork`, `room-photo-input-noithat`, `room-photo-thumbs-noithat`.
- Bump Cache-Buster Query Param to `?v=20260805-v2`.

---

### Task 1: Reorder HTML elements in `index.html` and update Cache-Buster

**Files:**
- Modify: `index.html:566-646`, `index.html:1799`, `main.js:5-8`

- [ ] **Step 1: Swap section positions in `index.html`**

Set "GHI CHÚ PHÒNG (TÙY CHỌN)" as section #1 and "THIẾT BỊ NỘI THẤT" as section #2 in `#step-content-3`.

- [ ] **Step 2: Update Cache-Buster version to `20260805-v2`**

In `index.html` line 1799: `main.js?v=20260805-v2`
In `main.js` lines 5-8: `?v=20260805-v2`

- [ ] **Step 3: Verify HTML syntax and compilation**

Run: `node -c main.js src/calc.js src/cloud-sync.js src/db.js src/excel.js src/takeoff.js ; python check_final.py`

- [ ] **Step 4: Commit and Push to GitHub origin main**

Run: `git add index.html main.js ; git commit -m "feat: reorder room note above furniture section in wizard step 3" ; git push origin main`
