# -*- coding: utf-8 -*-
import os

filepath = "d:/Kho tri thức/du-toan/app.js"

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Helper function parseNoteDimensionLine
helper_code = """\
function parseNoteDimensionLine(line) {
  line = line.trim();
  if (!line) return { label: '', dai: '', rong: '', cao: '', qty: 1, unit: 'cái' };
  
  let cleanedLine = line.replace(/^\d+\\s*[.\\-\\)\\s]+/, '').trim();
  const matchDim = cleanedLine.match(/(\\d+)\\s*[x*]\\s*(\\d+)(?:\\s*[x*]\\s*(\\d+))?/i);
  
  let label = cleanedLine;
  let dai = '';
  let rong = '';
  let cao = '';
  let qty = 1;
  let unit = 'cái';
  
  if (matchDim) {
    dai = parseInt(matchDim[1]) || '';
    rong = parseInt(matchDim[2]) || '';
    cao = matchDim[3] ? (parseInt(matchDim[3]) || '') : '';
    
    label = cleanedLine.substring(0, matchDim.index).trim();
    label = label.replace(/[:\\-–—\\s]+$/, '').trim();
    
    const rest = cleanedLine.substring(matchDim.index + matchDim[0].length).trim();
    if (rest) {
      const matchQty = rest.match(/^(\\d+(?:[.,]\\d+)?)\\s*([a-zA-Zà-ỹÀ-Ỹ\\s]*)$/i);
      if (matchQty) {
        qty = parseFloat(matchQty[1].replace(',', '.'));
        const parsedUnit = matchQty[2].trim();
        if (parsedUnit) unit = parsedUnit;
      }
    }
  } else {
    const matchQtyEnd = cleanedLine.match(/^(.*?)\\s+(\\d+(?:[.,]\\d+)?)\\s*([a-zA-Zà-ỹÀ-Ỹ\\s]*)$/i);
    if (matchQtyEnd) {
      label = matchQtyEnd[1].trim().replace(/[:\\-–—\\s]+$/, '');
      qty = parseFloat(matchQtyEnd[2].replace(',', '.'));
      const parsedUnit = matchQtyEnd[3].trim();
      if (parsedUnit) unit = parsedUnit;
    }
  }
  
  if (label) {
    label = label.charAt(0).toUpperCase() + label.slice(1);
  }
  
  return {
    label: label || cleanedLine,
    dai,
    rong,
    cao,
    qty,
    unit
  };
}

"""

target_inject = "function parseNoteItems(room) {"
if target_inject in content:
    content = content.replace(target_inject, helper_code + target_inject)
    print("app.js: Injected parseNoteDimensionLine helper successfully")
else:
    print("app.js: ERROR - Target function for injection NOT found")
    exit(1)

# 2. Update Excel sheet generation notes block
excel_old = """\
    // Notes sections

    [

      { text: room.noteWoodwork,   label: 'THIẾT BỊ NỘI THẤT' },

      { text: room.notePlumbing,   label: 'PHẦN NƯỚC' },

      { text: room.noteWaterproof, label: 'CHỐNG THẤM' },

    ].forEach(({ text, label }) => {

      if (!text || !text.trim()) return;

      const hdrN = blkDetail();

      hdrN[0] = romanNums[excelSubRomIdx] || excelSubRomIdx;

      hdrN[1] = label;

      excelSubRomIdx++;

      aoa.push(hdrN);

      curRow++;

      itemStt = 1;

      const noteLines = text.split('\\n').map(l => l.trim()).filter(l => l);

      noteLines.forEach((line, li) => {

        const lr = blkDetail();

        lr[0] = li + 1;

        lr[1] = line;

        lr[5] = 'cái';

        lr[6] = 1;

        aoa.push(lr);

        merges.push({ s: { r: curRow, c: 1 }, e: { r: curRow, c: 4 } });

        curRow++;

      });

    });"""

excel_new = """\
    // Notes sections
    [
      { text: room.noteWoodwork,   label: 'THIẾT BỊ NỘI THẤT' },
      { text: room.notePlumbing,   label: 'PHẦN NƯỚC' },
      { text: room.noteWaterproof, label: 'CHỐNG THẤM' },
    ].forEach(({ text, label }) => {
      if (!text || !text.trim()) return;
      const hdrN = blkDetail();
      hdrN[0] = romanNums[excelSubRomIdx] || excelSubRomIdx;
      hdrN[1] = label;
      excelSubRomIdx++;
      aoa.push(hdrN);
      curRow++;
      itemStt = 1;
      const noteLines = text.split('\\n').map(l => l.trim()).filter(l => l);
      noteLines.forEach((line, li) => {
        const parsed = parseNoteDimensionLine(line);
        const lr = blkDetail();
        lr[0] = li + 1;
        lr[1] = parsed.label;
        lr[2] = parsed.dai;
        lr[3] = parsed.rong;
        lr[4] = parsed.cao;
        lr[5] = parsed.unit;
        lr[6] = parsed.qty;
        aoa.push(lr);
        if (!parsed.dai && !parsed.rong && !parsed.cao) {
          merges.push({ s: { r: curRow, c: 1 }, e: { r: curRow, c: 4 } });
        }
        curRow++;
      });
    });"""

if excel_old in content:
    content = content.replace(excel_old, excel_new)
    print("app.js: Updated Excel sheet notes block successfully")
else:
    excel_old_lf = excel_old.replace("\r\n", "\n")
    if excel_old_lf in content:
        content = content.replace(excel_old_lf, excel_new)
        print("app.js: Updated Excel sheet notes block successfully (LF matched)")
    else:
        print("app.js: ERROR - Excel sheet notes block NOT found")

# 3. Update Web preview rendering notes block
web_old = """\
      const noteLines = text.split('\\n').map(l => l.trim()).filter(l => l);

      noteLines.forEach((line, li) => {

        html += `<tr class="pv-item">

          <td class="pv-stt">${stt++}</td>

          <td colspan="4" style="padding-left:15px !important;">${line}</td>

          <td class="pv-center">cái</td>

          <td class="pv-num">1</td>

          <td class="pv-num"></td>

          <td class="pv-num"></td>

          <td class="pv-note"></td>

        </tr>`;

      });"""

web_new = """\
      const noteLines = text.split('\\n').map(l => l.trim()).filter(l => l);
      noteLines.forEach((line, li) => {
        const parsed = parseNoteDimensionLine(line);
        if (parsed.dai || parsed.rong || parsed.cao) {
          html += `<tr class="pv-item">
            <td class="pv-stt">${stt++}</td>
            <td style="padding-left:15px !important; text-align:left;">${parsed.label}</td>
            <td class="pv-num">${parsed.dai ? fmtMM(parsed.dai) : ''}</td>
            <td class="pv-num">${parsed.rong ? fmtMM(parsed.rong) : ''}</td>
            <td class="pv-num">${parsed.cao ? fmtMM(parsed.cao) : ''}</td>
            <td class="pv-center">${parsed.unit}</td>
            <td class="pv-num">${fmt(parsed.qty)}</td>
            <td class="pv-num"></td>
            <td class="pv-num"></td>
            <td class="pv-note"></td>
          </tr>`;
        } else {
          html += `<tr class="pv-item">
            <td class="pv-stt">${stt++}</td>
            <td colspan="4" style="padding-left:15px !important; text-align:left;">${parsed.label}</td>
            <td class="pv-center">${parsed.unit}</td>
            <td class="pv-num">${fmt(parsed.qty)}</td>
            <td class="pv-num"></td>
            <td class="pv-num"></td>
            <td class="pv-note"></td>
          </tr>`;
        }
      });"""

if web_old in content:
    content = content.replace(web_old, web_new)
    print("app.js: Updated Web BOQ preview notes block successfully")
else:
    web_old_lf = web_old.replace("\r\n", "\n")
    if web_old_lf in content:
        content = content.replace(web_old_lf, web_new)
        print("app.js: Updated Web BOQ preview notes block successfully (LF matched)")
    else:
        print("app.js: ERROR - Web BOQ preview notes block NOT found")

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)
print("app.js: Refactoring complete")
