# Replace Gỗ CN 18mm with Gạch 40×40 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the floor material option "Gỗ CN 18mm +10%" with "Gạch 40×40 +5%" in `src/calc.js` and bump the cache-buster version to `20260805-v3`.

**Architecture:** Modify `MATERIALS.floor` in `src/calc.js`, update cache-buster query parameters in `index.html` and `main.js`, verify compilation, and push to GitHub.

**Tech Stack:** JavaScript (ES6 Modules), HTML5.

## Global Constraints

- Target Files: `src/calc.js`, `index.html`, `main.js`
- Replacement entry: `{ id: 'gach4040', label: 'Gạch 40×40', unit: 'm²', waste: 0.05 }`
- Bump Cache-Buster Query Param to `?v=20260805-v3`.

---

### Task 1: Update `MATERIALS.floor` in `src/calc.js` and bump Cache-Buster

**Files:**
- Modify: `src/calc.js:13`, `index.html:1799`, `main.js:5-8`

- [ ] **Step 1: Replace `goCN18` with `gach4040` in `src/calc.js`**

Replace line 13 in `src/calc.js`:
```javascript
{ id: 'gach4040',  label: 'Gạch 40×40',    unit: 'm²', waste: 0.05 },
```

- [ ] **Step 2: Update Cache-Buster version to `20260805-v3`**

In `index.html`: `main.js?v=20260805-v3`
In `main.js`: `./src/*.js?v=20260805-v3`

- [ ] **Step 3: Run node syntax and HTML verification**

Run: `node -c main.js src/calc.js src/cloud-sync.js src/db.js src/excel.js src/takeoff.js ; python check_final.py`

- [ ] **Step 4: Commit and Push to GitHub origin main**

Run: `git add src/calc.js index.html main.js ; git commit -m "feat: replace wood 18mm with tile 40x40 floor material" ; git push origin main`
