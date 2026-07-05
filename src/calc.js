// =============================================
// CALCULATION & MATERIALS MODULE
// =============================================

export const MATERIALS = {

  floor: [

    { id: 'none',      label: 'Bỏ qua',        unit: '',   waste: 0    },

    { id: 'goCN12',    label: 'Gỗ CN 12mm',    unit: 'm²', waste: 0.10 },

    { id: 'goCN18',    label: 'Gỗ CN 18mm',    unit: 'm²', waste: 0.10 },

    { id: 'gach6060',  label: 'Gạch 60×60',    unit: 'm²', waste: 0.05 },

    { id: 'gach8080',  label: 'Gạch 80×80',    unit: 'm²', waste: 0.07 },

    { id: 'gach12060', label: 'Gạch 120×60',   unit: 'm²', waste: 0.07 },

    { id: 'daTN',      label: 'Đá tự nhiên',   unit: 'm²', waste: 0.08 },

    { id: 'epoxy',     label: 'Epoxy',          unit: 'm²', waste: 0.05 },

    { id: 'sanNhua',   label: 'Sàn nhựa SPC',  unit: 'm²', waste: 0.08 },

  ],

  // Tường — Vùng 1 (phía dưới, có thể ốp gạch)

  wall: [

    { id: 'none',       label: 'Bỏ qua',           unit: '',   waste: 0    },

    { id: 'sonNuoc',    label: 'Sơn nước',         unit: 'm²', waste: 0.10 },

    { id: 'opG3060',    label: 'Gạch 30×60',       unit: 'm²', waste: 0.07 },

    { id: 'opG6060',    label: 'Gạch 60×60',       unit: 'm²', waste: 0.07 },

    { id: 'wallpaper',  label: 'Giấy dán tường',   unit: 'm²', waste: 0.15 },

    { id: 'opNhua',     label: 'Ốp nhựa PVC',      unit: 'm²', waste: 0.05 },

    { id: 'opGo',       label: 'Ốp gỗ trang trí',  unit: 'm²', waste: 0.12 },

    { id: 'other',      label: 'Khác',             unit: 'm²', waste: 0.07 },

  ],

  // Tường — Vùng 2 (phía trên, không có gạch)

  wallZ2: [

    { id: 'none',       label: 'Bỏ qua',           unit: '',   waste: 0    },

    { id: 'sonNuoc',    label: 'Sơn nước',         unit: 'm²', waste: 0.10 },

    { id: 'wallpaper',  label: 'Giấy dán tường',   unit: 'm²', waste: 0.15 },

    { id: 'opNhua',     label: 'Ốp nhựa PVC',      unit: 'm²', waste: 0.05 },

    { id: 'opGo',       label: 'Ốp gỗ trang trí',  unit: 'm²', waste: 0.12 },

    { id: 'other',      label: 'Khác',             unit: 'm²', waste: 0.07 },

  ],

  ceiling: [

    { id: 'none',       label: 'Bỏ qua',            unit: '',   waste: 0    },

    { id: 'sonNuoc',    label: 'Sơn nước',          unit: 'm²', waste: 0.10 },

    { id: 'tcPhang',    label: 'Thạch cao phẳng',    unit: 'm²', waste: 0.12 },

    { id: 'tcNoi',      label: 'Thạch cao nổi',     unit: 'm²', waste: 0.10 },

    { id: 'tcGiatCap',  label: 'TC giật cấp',        unit: 'm²', waste: 0.15 },

    { id: 'tcGo',       label: 'Trần gỗ',            unit: 'm²', waste: 0.12 },

    { id: 'nhomChinh',  label: 'Tấm nhôm',           unit: 'm²', waste: 0.08 },

    { id: 'tramAm',     label: 'Trần âm thanh',      unit: 'm²', waste: 0.10 },

  ],

};


export function hasKeyword(text, kw) {
  const kwNorm = kw.trim();
  if (!kwNorm) return false;
  const escaped = kwNorm.replace(/[-\/\^$*+?.()|[\]{}]/g, '\$&');
  const regex = new RegExp('\b' + escaped + '\b', 'i');
  return regex.test(text);
}

export function categorizeSummaryItem(item) {
  if (item.surface === 'woodworkNote') return 'furniture';
  if (item.surface === 'plumbingNote') return 'sanitary';
  if (item.surface === 'waterproofNote') return 'sanitary';

  // Thiết bị điện (từ wizard)
  if (item.surface === 'elec' || item.surface === 'elecManual') return 'elec';

  // 1. Kiểm tra loại bề mặt xây dựng cơ bản trước
  if (['floor', 'wall', 'ceiling', 'perimeter', 'window', 'ceilPerim'].includes(item.surface)) {
    return 'construction';
  }

  const labelNorm = (item.label || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/đ/g, 'd').trim();

  const elecKeywords = [
    'den', 'spotlight', 'panel', 'tuyp', 'led', 'cong tac', 'o cam', 'cb', 'pha', 'tu dien',
    'may lanh', 'dieu hoa', 'quat hut', 'day dien', 'vat tu phu dien', 'nep nhua', 'ong ruot ga', 'ong cung', 'cadivi', 'panasonic', 'downlight'
  ];

  if (elecKeywords.some(kw => hasKeyword(labelNorm, kw))) {
    return 'elec';
  }

  const sanitaryKeywords = [
    'bon cau', 'lavabo', 'chau rua', 'voi sen', 'sen tam', 'chau tam', 'tieu nam', 've sinh',
    'thoat san', 'ong nuoc', 'ro nuoc', 'thiet bi ve sinh', 'lap dat ve sinh', 'sen cay', 'voi rua'
  ];

  if (sanitaryKeywords.some(kw => hasKeyword(labelNorm, kw))) {
    return 'sanitary';
  }

  const furnitureKeywords = [
    'giuong', 'tu ao', 'tu bep', 'ban an', 'ban trang diem', 'ban lam viec', 'ghe', 'sofa',
    'ke tivi', 'tap dau giuong', 'quay bar', 'noi that', 'tu giay', 'quay le tan', 'dem', 'rem',
    'vach op', 'lam go', 'woodwork', 'ke sach', 'ke trang tri', 'ban tra', 'go'
  ];

  if (furnitureKeywords.some(kw => hasKeyword(labelNorm, kw))) {
    return 'furniture';
  }

  return 'construction';
}

export function fmt(n, dec = 2) {

  const v = parseFloat(n);

  if (isNaN(v)) return '0,' + '0'.repeat(dec);

  // Format fixed decimals dấu chấm, rồi chuyển sang vi-VN:

  // - dấu thập phân '.' → ','

  // - dấu phân cách nghìn: thêm '.' mỗi 3 chữ số phần nguyên

  const [intPart, decPart] = v.toFixed(dec).split('.');

  const intFormatted = intPart.replace(/\B(?=(\d{3})+(?!\d))/g, '.');

  return dec > 0 ? `${intFormatted},${decPart}` : intFormatted;

}

// Toggle hiển thị công thức tính khi click vào ô SỐ LƯỢNG

function toggleFormula(td) {

  const expanded = td.classList.toggle('formula-expanded');

  if (expanded) {

    td.dataset.qty = td.textContent.trim();

    td.innerHTML = `<span class="formula-text">= ${td.dataset.formula}</span>`;

  } else {

    td.textContent = td.dataset.qty;

  }

}

// Định dạng số nguyên mm: 8930 → 8.930

export function fmtMM(n) {

  const v = Math.round(parseFloat(n) || 0);

  return v.toLocaleString('vi-VN');

}

// Dùng cho Excel export (số thuần, không format string)


export function lamTron(so, soChuSoThapPhan = 2) {
  if (typeof so !== 'number') {
    const p = parseFloat(so);
    if (isNaN(p)) return 0;
    so = p;
  }
  return Number(Math.round(so + 'e' + soChuSoThapPhan) + 'e-' + soChuSoThapPhan);
}

export function fmtNum(n, dec = 2) {

  const v = parseFloat(n);

  return isNaN(v) ? 0 : Math.round(v * Math.pow(10, dec)) / Math.pow(10, dec);

}

export function getMat(type, id) {

  return MATERIALS[type].find(m => m.id === id) || MATERIALS[type][0];

}

export function today() {

  return new Date().toISOString().split('T')[0];

}

export function reIcons() {

  if (window.lucide) window.lucide.createIcons();

}

// ── Đọc số thành chữ tiếng Việt ─────────────────────────

export function numberToWords(n) {

  if (!n || isNaN(n)) return 'không đồng';

  const num = Math.round(+n);

  if (num === 0) return 'không đồng';

  const CH  = ['không','một','hai','ba','bốn','năm','sáu','bảy','tám','chín'];

  const DON = ['','nghìn','triệu','tỷ'];

  function readGroup(g) {

    let s = '';

    const h = Math.floor(g / 100);

    const t = Math.floor((g % 100) / 10);

    const u = g % 10;

    if (h) s += CH[h] + ' trăm ';

    if (t === 0 && u && h) s += 'linh ';

    else if (t === 1) s += 'mười ';

    else if (t > 1) s += CH[t] + ' mươi ';

    if (u === 1 && t > 1) s += 'mốt';

    else if (u === 5 && t > 0) s += 'lăm';

    else if (u) s += CH[u];

    return s.trim();

  }

  if (num < 0) return 'âm ' + numberToWords(-num);

  let parts = [], temp = num, idx = 0;

  while (temp > 0) {

    parts.push({ val: temp % 1000, don: DON[idx++] });

    temp = Math.floor(temp / 1000);

  }

  const words = parts.reverse().filter(p => p.val > 0)

    .map(p => readGroup(p.val) + (p.don ? ' ' + p.don : '')).join(', ');

  // Viết hoa chữ đầu

  return words.charAt(0).toUpperCase() + words.slice(1) + ' đồng';

}


export const ELEC_MAPPING = {
  // Đèn
  "downlight": { label: "Đèn downlight", unit: "bộ" },
  "downligh": { label: "Đèn downlight", unit: "bộ" },
  "spotlight": { label: "Đèn spotlight", unit: "bộ" },
  "sportlight": { label: "Đèn spotlight", unit: "bộ" },
  "panel": { label: "Đèn panel", unit: "bộ" },
  "tuyp": { label: "Đèn tuýp", unit: "bộ" },
  "tuyp 1200": { label: "Đèn tuýp 1200mm", unit: "bộ" },
  "tuyp 600": { label: "Đèn tuýp 600mm", unit: "bộ" },
  "led": { label: "Đèn LED dây", unit: "m" },
  "led day": { label: "Đèn LED dây", unit: "m" },
  "den ngu": { label: "Đèn ngủ", unit: "cái" },
  "den chum": { label: "Đèn chùm", unit: "bộ" },
  
  // Tủ điện
  "cb tong": { label: "CB tổng", unit: "cái" },
  "cb tep": { label: "CB tép", unit: "cái" },
  "o cam 2 chau": { label: "Ổ cắm 2 chấu", unit: "bộ" },
  "o cam 3 chau": { label: "Ổ cắm 3 chấu", unit: "bộ" },
  "cong tac": { label: "Công tắc", unit: "mặt" },
  "cb 1 pha": { label: "CB 1 pha", unit: "cái" },
  "cb 2 pha": { label: "CB 2 pha", unit: "cái" },
  "cb 3 pha": { label: "CB 3 pha", unit: "cái" },
  "tu dien": { label: "Tủ điện", unit: "bộ" },
  "quat hut": { label: "Quạt hút âm trần", unit: "cái" },
  
  // Máy lạnh
  "treo tuong": { label: "Máy lạnh treo tường", unit: "cái" },
  "am tran": { label: "Máy lạnh âm trần", unit: "cái" },
  "trung tam": { label: "Máy lạnh trung tâm", unit: "cái" }
};


export function parseElecNote(noteText) {
  if (!noteText || !noteText.trim()) return [];
  
  const parts = noteText.split(/[,;\n+]+/);
  const parsedItems = [];
  
  parts.forEach(part => {
    part = part.trim();
    if (!part) return;
    
    let rawName = '';
    let qty = 1;
    let unit = '';
    
    // Pattern 1: name then quantity then unit (e.g. "đèn downlight 3 bộ" or "treo tường 2 cái")
    // Note: character class does NOT contain \d to prevent swallowing numbers inside names like "ổ cắm 2 chấu"
    const matchEnd = part.match(/^(.*?)\s+(\d+(?:[.,]\d+)?)\s*([a-zA-Zà-ỹÀ-Ỹ\s²³\/]*)$/i);
    if (matchEnd) {
      rawName = matchEnd[1].trim();
      qty = parseFloat(matchEnd[2].replace(',', '.'));
      unit = matchEnd[3].trim();
    } else {
      // Pattern 2: quantity then unit then name (e.g. "3 bộ đèn downlight" or "2 cái máy lạnh")
      const matchStart = part.match(/^(\d+(?:[.,]\d+)?)\s*([a-zA-Zà-ỹÀ-Ỹ\s²³\/]*?)\s+(.+)$/i);
      if (matchStart) {
        qty = parseFloat(matchStart[1].replace(',', '.'));
        unit = matchStart[2].trim();
        rawName = matchStart[3].trim();
      } else {
        // Fallback
        rawName = part;
        qty = 1;
        unit = '';
      }
    }
    
    if (rawName) {
      rawName = rawName.replace(/[:\-–—\s]+$/, '').trim();
      rawName = rawName.replace(/^\d+\s*[.\-\)\s]+/, '').trim();
      
      if (!rawName) return;
      
      const norm = rawName.toLowerCase()
        .normalize('NFD')
        .replace(/[\u0300-\u036f]/g, '')
        .replace(/\u0111/g, 'd')
        .replace(/\u0110/g, 'd')
        .trim();
      
      let matchedLabel = '';
      let matchedUnit = '';
      
      for (const key in ELEC_MAPPING) {
        if (norm === key || norm.includes(key)) {
          matchedLabel = ELEC_MAPPING[key].label;
          matchedUnit = ELEC_MAPPING[key].unit;
          break;
        }
      }
      
      if (!matchedLabel) {
        matchedLabel = rawName.charAt(0).toUpperCase() + rawName.slice(1);
      }
      if (!matchedUnit) {
        matchedUnit = unit || (norm.includes('den') || norm.includes('led') || norm.includes('o cam') ? 'bộ' : 'cái');
      }
      
      parsedItems.push({
        label: matchedLabel,
        qty: qty,
        unit: matchedUnit
      });
    }
  });
  
  return parsedItems;
}

export function parseNoteDimensionLine(line) {
  line = line.trim();
  if (!line) return { label: '', dai: '', rong: '', cao: '', qty: 1, unit: 'cái' };
  
  let cleanedLine = line.replace(/^\d+\s*[.\-\)\s]+/, '').trim();
  const matchDim = cleanedLine.match(/(\d+)\s*[x*]\s*(\d+)(?:\s*[x*]\s*(\d+))?/i);
  
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
    label = label.replace(/[:\-–—\s]+$/, '').trim();
    
    const rest = cleanedLine.substring(matchDim.index + matchDim[0].length).trim();
    if (rest) {
      const matchQty = rest.match(/^(\d+(?:[.,]\d+)?)\s*([a-zA-Zà-ỹÀ-Ỹ\s]*)$/i);
      if (matchQty) {
        qty = parseFloat(matchQty[1].replace(',', '.'));
        const parsedUnit = matchQty[2].trim();
        if (parsedUnit) unit = parsedUnit;
      }
    }
  } else {
    const matchQtyEnd = cleanedLine.match(/^(.*?)\s+(\d+(?:[.,]\d+)?)\s*([a-zA-Zà-ỹÀ-Ỹ\s]*)$/i);
    if (matchQtyEnd) {
      label = matchQtyEnd[1].trim().replace(/[:\-–—\s]+$/, '');
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

export function parseNoteItems(room) {

  const note = room.roomNote || '';

  if (!note.trim()) return [];

  const D = (+room.D || 0) / 1000;

  const R = (+room.R || 0) / 1000;

  const perim = 2 * (D + R);

  const perimMm = Math.round(perim * 1000);

  const items = [];

  const ni = (label, unit, qty, formula, note2) => ({

    surface: 'noteItem', label, unit,

    qty: +qty || 0, dai: '', rong: '', cao: '',

    price: 0, total: 0,

    formula: formula || (qty ? `${qty} ${unit}` : ''),

    note: note2 || '',

  });

  // Normalize: bỏ dấu tiếng Việt để match ASCII-safe

  const norm = note.toLowerCase()

    .normalize('NFD')

    .replace(/[\u0300-\u036f]/g, '')

    .replace(/\u0111/g, 'd').replace(/\u0110/g, 'd');

  // Helper: đọc số có dấu phẩy ("1,8m" -> 1800)

  const parseM = (s) => {

    if (!s) return 0;

    // '1,8m' -> 1800, '1800' -> 1800, '1.8m' -> 1800

    const n = parseFloat(String(s).replace(',', '.'));

    return isNaN(n) ? 0 : (n < 20 ? Math.round(n * 1000) : n); // < 20 thì tính bằng m

  };

  // Luôn đặt hasAnyElec = true để bỏ qua việc parse điện trong phần note chung, tránh sinh lặp hạng mục điện
  const hasAnyElec = true;

  // ── XÂY DỰNG ──────────────────────────────────

  // Tường ốp gạch / đá cao X (nhiều biến thể)

  // "tường ốp gạch cao 1800", "ốp gạch tường cao 1,8m", "gạch ốp tường h = 1800"

  const rGach = norm.match(/(?:tuong\s*)?(?:op\s*)?(?:gach|da)(?:\s*op)?(?:\s*tuong)?\s*(?:cao|h\s*=\s*|h:\s*)([\d,.]+m?)/)

             || norm.match(/op\s*(?:gach|da)\s*cao\s*([\d,.]+m?)/);

  if (rGach) {

    const heightMm = parseM(rGach[1]);

    const area = perim * (heightMm / 1000);

    items.push(ni(`Tường ốp gạch/đá (cao ${fmtMM(heightMm)}mm)`, 'm²',

      +area.toFixed(2), `CV(${fmtMM(perimMm)}) x ${fmtMM(heightMm)}mm = ${fmt(area)} m²`, ''));

  }

  // Gạch hoa / gạch lát nền đặc biệt

  const rGachHoa = norm.match(/gach\s*hoa|gach\s*lat\s*hoa/);

  if (rGachHoa) {

    const area = D * R;

    items.push(ni('Gạch hoa ốp / lát nền', 'm²',

      +area.toFixed(2), `${fmtMM(+room.D)} x ${fmtMM(+room.R)} = ${fmt(area)} m²`, ''));

  }

  // Tường sơn cao X

  // "tường sơn cao 1800", "sơn 3 nước cao 2m", "sơn nước toàn bộ"

  const rSon = norm.match(/(?:tuong\s*)?son\s*(?:\d+\s*nuoc\s*)?cao\s*([\d,.]+m?)/)

            || norm.match(/son\s*nuoc\s*toan\s*bo/);

  if (rSon) {

    if (rSon[1]) {

      const heightMm = parseM(rSon[1]);

      const area = perim * (heightMm / 1000);

      items.push(ni(`Tường sơn (cao ${fmtMM(heightMm)}mm)`, 'm²',

        +area.toFixed(2), `CV(${fmtMM(perimMm)}) x ${fmtMM(heightMm)}mm = ${fmt(area)} m²`, ''));

    } else {

      // "sơn nước toàn bộ" = toàn bộ tường

      const area = perim * (+room.H || 0) / 1000;

      items.push(ni('Tường sơn toàn bộ', 'm²',

        +area.toFixed(2), `CV(${fmtMM(perimMm)}) x H(${fmtMM(+room.H)}) = ${fmt(area)} m²`, ''));

    }

  }

  // Chống thấm nền / tường

  if (/chong\s*tham/.test(norm)) {

    const area = D * R;

    const isWall = /chong\s*tham\s*tuong|tuong\s*chong\s*tham/.test(norm);

    if (isWall) {

      const wArea = perim * (+room.H || 0) / 1000;

      items.push(ni('Chống thấm tường', 'm²',

        +wArea.toFixed(2), `CV x H = ${fmt(wArea)} m²`, ''));

    } else {

      items.push(ni('Chống thấm nền/sàn', 'm²',

        +area.toFixed(2), `${fmtMM(+room.D)} x ${fmtMM(+room.R)} = ${fmt(area)} m²`, ''));

    }

  }

  // Ốp gỗ cao X

  const rGo = norm.match(/(?:op\s*)?go\s*(?:trang\s*tri\s*)?cao\s*([\d,.]+m?)/);

  if (rGo) {

    const heightMm = parseM(rGo[1]);

    const area = perim * (heightMm / 1000);

    items.push(ni(`Ốp gỗ trang trí (cao ${fmtMM(heightMm)}mm)`, 'm²',

      +area.toFixed(2), `CV(${fmtMM(perimMm)}) x ${fmtMM(heightMm)}mm = ${fmt(area)} m²`, ''));

  }

  // Tấm ốp trần / trần nhựa PVC

  if (/tam\s*op\s*tran|tran\s*nhua|tran\s*pvc|tam\s*tran/.test(norm)) {

    const area = D * R;

    items.push(ni('Tấm ốp trần PVC', 'm²',

      +area.toFixed(2), `${fmtMM(+room.D)} x ${fmtMM(+room.R)} = ${fmt(area)} m²`, ''));

  }

  // Rèm cửa

  if (/rem\s*cua/.test(norm)) {

    const nWin = +room.windows || 1;

    items.push(ni('Rèm cửa', 'bộ', nWin, `${nWin} bộ`, 'Tận dụng / lắp mới'));

  }

  // Bọc nilong

  if (/boc\s*ni.?long/.test(norm)) {

    items.push(ni('Bọc nilong bảo vệ cửa sổ', 'hạng mục', 1, '1 hạng mục', ''));

  }

  // Tháo gỡ

  if (/thao\s*go/.test(norm)) {

    items.push(ni('Công tháo gỡ vật tư cũ', 'hạng mục', 1, '1 hạng mục', ''));

  }

  // Phá dỡ / đập

  if (/pha\s*do|dap\s*(?:go|cot|tuong)/.test(norm)) {

    items.push(ni('Phá dỡ / đập cấu kiện cũ', 'hạng mục', 1, '1 hạng mục', ''));

  }

  // Sàn cũ làm lại

  if (/san.{0,25}lam\s*lai/.test(norm)) {

    const area = D * R;

    items.push(ni('Sàn cũ — thi công lại', 'm²',

      +area.toFixed(2), `${fmtMM(+room.D)} x ${fmtMM(+room.R)} = ${fmt(area)} m²`, ''));

  }

  // Trần cũ làm lại

  if (/tran.{0,25}lam\s*lai|lam\s*lai.{0,15}tran/.test(norm)) {

    const area = D * R;

    items.push(ni('Trần cũ — thi công lại', 'm²',

      +area.toFixed(2), `${fmtMM(+room.D)} x ${fmtMM(+room.R)} = ${fmt(area)} m²`, ''));

  }

  // Xi trát tường

  if (/xi\s*trat|trat\s*xi/.test(norm)) {

    const area = perim * (+room.H || 0) / 1000;

    items.push(ni('Xi trát tường', 'm²',

      +area.toFixed(2), `CV x H = ${fmt(area)} m²`, ''));

  }

  // ── ĐIỆN (chỉ khi chưa nhập modal) ───────────────────────

  if (!hasAnyElec) {

    // Đèn: "đèn X bộ", "X bộ đèn", "X đèn", "đèn panel X"

    const rDen = norm.match(/den\s+(?:\w+\s+){0,4}(\d+)\s*bo|(\d+)\s*(?:bo\s*)?den|den\s+(\d+)/);

    if (rDen) {

      const q = +(rDen[1] || rDen[2] || rDen[3] || 1);

      items.push(ni('Đèn panel Điện Quang', 'bộ', q, '', ''));

    }

    // Tủ điện / tủ CB: "tủ điện X đường"

    const rTu = norm.match(/tu\s*dien\s*(\d+)|(\d+)\s*duong.*cb|tu\s*cb\s*(\d+)/);

    if (rTu) {

      const q = +(rTu[1] || rTu[2] || rTu[3] || 1);

      items.push(ni(`Tủ điện ${q} đường`, 'cái', 1, '', ''));

    }

    // CB 40A

    const rCb40 = norm.match(/(\d+)\s*(?:cai\s*)?cb\s*40|cb\s*40\s*(?:a\s*)?(\d+)/);

    const hasCb40 = rCb40 || /cb\s*40/.test(norm);

    if (hasCb40) items.push(ni('CB 40A', 'cái', rCb40 ? +(rCb40[1]||rCb40[2]||1) : 1, '', ''));

    // CB 20A

    const rCb20 = norm.match(/(\d+)\s*(?:cai\s*)?cb\s*(?:o\s*cam|oc)?\s*20|cb\s*(?:o\s*cam\s*)?20\s*(?:a\s*)?(\d+)?/);

    const hasCb20 = rCb20 || /cb.*20/.test(norm);

    if (hasCb20) {

      const q = rCb20 ? +(rCb20[1]||rCb20[2]||1) : 1;

      items.push(ni('CB 20A', 'cái', q, '', ''));

    }

    // CB 15A / đèn 15A

    const rCb15 = norm.match(/(\d+)\s*(?:cai\s*)?cb\s*(?:den\s*)?15|cb\s*(?:den\s*)?15\s*(?:a\s*)?(\d+)?/);

    const hasCb15 = rCb15 || /cb.*15/.test(norm);

    if (hasCb15) items.push(ni('CB 15A', 'cái', rCb15 ? +(rCb15[1]||rCb15[2]||1) : 1, '', ''));

    // CB 10A

    const rCb10 = norm.match(/(\d+)\s*(?:cai\s*)?cb\s*10|cb\s*10\s*(?:a\s*)?(\d+)?/);

    const hasCb10 = rCb10 || /cb.*10[^a-z]/.test(norm);

    if (hasCb10) items.push(ni('CB 10A', 'cái', rCb10 ? +(rCb10[1]||rCb10[2]||1) : 1, '', ''));

    // Ổ cắm: "o cam X bo", "X bo o cam"

    const rOC = norm.match(/o\s*cam\s*(\d+)\s*bo/) || norm.match(/(\d+)\s*bo\s*o\s*cam/) || norm.match(/o\s*cam\s*(\d+)(?!\s*a)/);

    if (rOC) items.push(ni('Ổ cắm đôi 2 cực Panasonic', 'bộ', +(rOC[1]||rOC[2]||1), '', ''));

    // Quạt

    const rFan = norm.match(/(\d+)\s*quat|quat\s*(\d+)/);

    const hasFan = rFan || /quat/.test(norm);

    if (hasFan) items.push(ni('Quạt hút âm trần Panasonic', 'cái', rFan ? +(rFan[1]||rFan[2]||1) : 1, '', ''));

    // Máy lạnh / điều hòa

    const rAC = norm.match(/(\d+)\s*(?:may\s*lanh|dieu\s*hoa)|(?:may\s*lanh|dieu\s*hoa)\s*(\d+)/);

    const hasAC = rAC || /may\s*lanh|dieu\s*hoa/.test(norm);

    if (hasAC) items.push(ni('Máy lạnh (điều hòa)', 'cái', rAC ? +(rAC[1]||rAC[2]||1) : 1, '', ''));

    // Công tắc 2 mặt

    const rSw2 = norm.match(/(\d+)\s*(?:mat\s*)?(?:cong\s*tac\s*2|ct2)|mat\s*2\s*(?:cong\s*tac\s*)?(\d+)/);

    if (rSw2) items.push(ni('Mặt 2 công tắc Panasonic', 'mặt', +(rSw2[1]||rSw2[2]||1), '', ''));

    // Công tắc 1 mặt

    const rSw1 = norm.match(/(\d+)\s*(?:mat\s*)?(?:cong\s*tac\s*1|ct1)|mat\s*1\s*(?:cong\s*tac\s*)?(\d+)/);

    if (rSw1) items.push(ni('Mặt 1 công tắc Panasonic', 'mặt', +(rSw1[1]||rSw1[2]||1), '', ''));

    // Dây điện âm tường

    if (/day\s*dien/.test(norm)) {

      items.push(ni('Dây điện âm tường', 'bộ', 0, '', 'Xem mục dây điện ở phần Điện'));

    }

  }

  return items;

}


export const CALC = {

  room(room) {

    // Chuyển từ mm → m để tính diện tích

    const D  = (+room.D || 0) / 1000;

    const R  = (+room.R || 0) / 1000;

    const H  = (+room.H || 0) / 1000;

    const nd = +room.doors  || 0;

    const dw = (+room.doorW   || 900)  / 1000;

    const dh = (+room.doorH   || 2100) / 1000;

    const nw = +room.windows || 0;

    const ww = (+room.windowW || 1200) / 1000;

    const wh = (+room.windowH || 1200) / 1000;

    const da    = dw * dh;           // dt 1 cửa đi (m²)

    const wa    = ww * wh;           // dt 1 cửa sổ (m²)

    const perim = 2 * (D + R);       // chu vi phòng (m)

    const fMat = getMat('floor',   room.floorMat);

    const wMat = getMat('wall',    room.wallMat);

    // ceilMats là array; lấy phần tử đầu để tính waste (đại diện)

    const ceilMatId = Array.isArray(room.ceilMats) && room.ceilMats.length ? room.ceilMats[0] : (room.ceilMat || 'none');

    const cMat = getMat('ceiling', ceilMatId);

    const rawFloor = D * R;

    const rawCeil  = D * R;

    let   rawWall  = Math.max(0, perim * H - nd * da - nw * wa);

    // mm gốc cho hiển thị

    const Dmm    = +room.D || 0;

    const Rmm    = +room.R || 0;

    const Hmm    = +room.H || 0;

    const perimM = Math.round(perim * 1000);   // chu vi dạng mm (để fmtMM)

    const items = [];

    // ══════════════════════════════════════════════

    // 1. DIỆN TÍCH SÀN (luôn hiển thị)

    // ══════════════════════════════════════════════

    if (D > 0 && R > 0) {

      const hasMat = fMat.id !== 'none';

      const price  = hasMat ? (+room.floorPrice || 0) : 0;

      const qty    = hasMat ? rawFloor * (1 + fMat.waste) : rawFloor;

      items.push({

        surface: 'floor',

        label:   hasMat ? `Sàn ${fMat.label}` : 'Diện tích sàn',

        unit:    'm²',

        qty:     +qty.toFixed(2),

        dai: Dmm, rong: Rmm, cao: '',

        price, total: qty * price,

        formula: `${fmtMM(Dmm)} × ${fmtMM(Rmm)} = ${fmt(rawFloor)} m²${hasMat ? ` (+${(fMat.waste*100).toFixed(0)}% = ${fmt(qty)} m²)` : ''}`,

        note:    hasMat ? `+${(fMat.waste*100).toFixed(0)}% hao hụt` : '',

      });

    }

    // ══════════════════════════════════════════════

    // 2. DIEN TICH TUONG

    // ══════════════════════════════════════════════

    if (D > 0 && R > 0 && H > 0) {

      const grossWall = perim * H;

      const dDeduct   = nd * da;

      const wDeduct   = nw * wa;

      const doorFml   = nd > 0 ? ` − ${nd}×(${fmtMM(+room.doorW||900)}×${fmtMM(+room.doorH||2100)}) = ${fmt(dDeduct)} m²` : '';

      const winFml    = nw > 0 ? ` − ${nw}×(${fmtMM(+room.windowW||1200)}×${fmtMM(+room.windowH||1200)}) = ${fmt(wDeduct)} m²` : '';

      if (!room.wallZone) {

        // Chế độ 1 vùng

        const hasMat = wMat.id !== 'none';

        const price  = hasMat ? (+room.wallPrice || 0) : 0;

        const qty    = hasMat ? rawWall * (1 + wMat.waste) : rawWall;

        items.push({

          surface: 'wall',

          label:   hasMat ? `Tường ${wMat.label}` : 'Diện tích tường',

          unit:    'm²',

          qty:     +qty.toFixed(2),

          dai: perimM, rong: '', cao: Hmm,

          price, total: qty * price,

          formula: `CV(${fmtMM(perimM)}) × H(${fmtMM(Hmm)}) = ${fmt(grossWall)} m²${doorFml}${winFml} → ${fmt(rawWall)} m²${hasMat ? ` (+${(wMat.waste*100).toFixed(0)}% = ${fmt(qty)} m²)` : ''}`,

          note:    hasMat ? `+${(wMat.waste*100).toFixed(0)}% hao hụt` : '',

        });

      } else if (+room.wallZ1H > 0) {

        // Chế độ 2 vùng zone

        const z1H   = (+room.wallZ1H || 0) / 1000;

        const z2H   = Math.max(0, H - z1H);

        const sill  = (+room.wallSill || 900) / 1000;

        const wTop  = sill + wh;

        const z1Hmm = +room.wallZ1H || 0;

        const z2Hmm = Math.round(z2H * 1000);

        const rawZ1 = perim * z1H;

        const rawZ2 = perim * z2H;

        const doorInZ1 = nd * dw * Math.min(dh, z1H);

        const doorInZ2 = nd * dw * Math.max(0, dh - z1H);

        const winInZ1  = nw * ww * Math.max(0, Math.min(wTop, z1H) - Math.max(0, sill));

        const winInZ2  = nw * ww * Math.max(0, Math.min(wTop, H) - Math.max(sill, z1H));

        const finalZ1 = Math.max(0, rawZ1 - doorInZ1 - winInZ1);

        const finalZ2 = Math.max(0, rawZ2 - doorInZ2 - winInZ2);

        const mat1 = getMat('wall', room.wallMatZ1);

        const mat2 = getMat('wall', room.wallMatZ2);

        // Vùng 1

        const hasMat1 = mat1.id !== 'none';

        const price1  = hasMat1 ? (+room.wallPriceZ1 || 0) : 0;

        const qty1    = hasMat1 ? finalZ1 * (1 + mat1.waste) : finalZ1;

        if (finalZ1 > 0) items.push({

          surface: 'wallZ1',

          label:   hasMat1 ? `Tường Vùng 1 — ${mat1.label}` : `Tường Vùng 1 (cao ${fmtMM(z1Hmm)})`,

          unit: 'm²', qty: +qty1.toFixed(2),

          dai: perimM, rong: '', cao: z1Hmm,

          price: price1, total: qty1 * price1,

          formula: `CV(${fmtMM(perimM)}) × ${fmtMM(z1Hmm)} = ${fmt(rawZ1)} m² − cửa → ${fmt(finalZ1)} m²${hasMat1?` (+${(mat1.waste*100).toFixed(0)}% = ${fmt(qty1)} m²)`:''}`,

          note: hasMat1 ? `+${(mat1.waste*100).toFixed(0)}% hao hụt` : '',

        });

        // Vùng 2

        const hasMat2 = mat2.id !== 'none';

        const price2  = hasMat2 ? (+room.wallPriceZ2 || 0) : 0;

        const qty2    = hasMat2 ? finalZ2 * (1 + mat2.waste) : finalZ2;

        if (finalZ2 > 0) items.push({

          surface: 'wallZ2',

          label:   hasMat2 ? `Tường Vùng 2 — ${mat2.label}` : `Tường Vùng 2 (cao ${fmtMM(z2Hmm)})`,

          unit: 'm²', qty: +qty2.toFixed(2),

          dai: perimM, rong: '', cao: z2Hmm,

          price: price2, total: qty2 * price2,

          formula: `CV(${fmtMM(perimM)}) × ${fmtMM(z2Hmm)} = ${fmt(rawZ2)} m² − cửa sổ → ${fmt(finalZ2)} m²${hasMat2?` (+${(mat2.waste*100).toFixed(0)}% = ${fmt(qty2)} m²)`:''}`,

          note: hasMat2 ? `+${(mat2.waste*100).toFixed(0)}% hao hụt` : '',

        });

        rawWall = finalZ1 + finalZ2;

      }

    }

    // ══════════════════════════════════════════════

    // 3. LEN CHÂN TƯỜNG (thuộc nhóm tường — chu vi trừ cửa đi)

    // ══════════════════════════════════════════════

    if (D > 0 && R > 0) {

      const lenChanTuong = Math.max(0, perim - nd * dw);

      items.push({

        surface: 'perimeter',

        label:   'Len chân tường (chu vi trừ cửa đi)',

        unit:    'm',

        qty:     +lenChanTuong.toFixed(2),

        dai: Dmm, rong: Rmm, cao: '',

        price: 0, total: 0,

        formula: `${fmtMM(Dmm)}×2 + ${fmtMM(Rmm)}×2 = ${fmtMM(perimM)}mm${nd>0?` − ${nd} cửa đi(${fmtMM(+room.doorW||900)})`:''} ÷ 1.000 = ${fmt(lenChanTuong)} m`,

        note: '',

      });

    }

    // ══════════════════════════════════════════════

    // 4. DIỆN TÍCH CỬA ĐI (luôn hiển thị nếu có cửa)

    // ══════════════════════════════════════════════

    if (nd > 0 && da > 0) {

      const doorTotalArea = nd * da;

      items.push({

        surface: 'door',

        label:   'Diện tích cửa đi',

        unit:    'm²',

        qty:     +doorTotalArea.toFixed(2),

        dai:     '',

        rong:    +room.doorW || 900,

        cao:     +room.doorH || 2100,

        price: 0, total: 0,

        formula: `${nd} cửa × (${fmtMM(+room.doorW||900)} × ${fmtMM(+room.doorH||2100)}) = ${fmt(doorTotalArea)} m²`,

        note:    `${nd} cửa đi`,

      });

    }

    // ══════════════════════════════════════════════

    // 5. DIỆN TÍCH CỬA SỔ (luôn hiển thị nếu có)

    // ══════════════════════════════════════════════

    if (nw > 0 && wa > 0) {

      const winArea = nw * wa;

      items.push({

        surface: 'window',

        label:   'Diện tích cửa sổ',

        unit:    'm²',

        qty:     +winArea.toFixed(2),

        dai:     '',

        rong:    +room.windowW || 1200,

        cao:     +room.windowH || 1200,

        price: 0, total: 0,

        formula: `${nw} cửa sổ × (${fmtMM(+room.windowW||1200)} × ${fmtMM(+room.windowH||1200)}) = ${fmt(winArea)} m²`,

        note:    `${nw} cửa sổ — dùng tính rèm / vật liệu kính`,

      });

    }

    // ══════════════════════════════════════════════

    // 6. DIỆN TÍCH TRẦN (luôn hiển thị)

    // ══════════════════════════════════════════════

    if (D > 0 && R > 0) {

      const hasMat = cMat.id !== 'none';

      const price  = hasMat ? (+room.ceilPrice || 0) : 0;

      const qty    = hasMat ? rawCeil * (1 + cMat.waste) : rawCeil;

      items.push({

        surface: 'ceiling',

        label:   hasMat ? `Trần ${cMat.label}` : 'Diện tích trần',

        unit:    'm²',

        qty:     +qty.toFixed(2),

        dai: Dmm, rong: Rmm, cao: '',

        price, total: qty * price,

        formula: `${fmtMM(Dmm)} × ${fmtMM(Rmm)} = ${fmt(rawCeil)} m²${hasMat ? ` (+${(cMat.waste*100).toFixed(0)}% = ${fmt(qty)} m²)` : ''}`,

        note:    hasMat ? `+${(cMat.waste*100).toFixed(0)}% hao hụt` : '',

      });

    }

    // ══════════════════════════════════════════════

    // 7. CHU VI TRẦN

    // ══════════════════════════════════════════════

    if (D > 0 && R > 0) {

      items.push({

        surface: 'ceilPerim',

        label:   'Chu vi trần',

        unit:    'm',

        qty:     +perim.toFixed(2),

        dai: Dmm, rong: Rmm, cao: '',

        price: 0, total: 0,

        formula: `${fmtMM(Dmm)}×2 + ${fmtMM(Rmm)}×2 = ${fmtMM(perimM)}mm ÷ 1.000 = ${fmt(perim)} m`,

        note:    'Len trần / chỉ trần',

      });

    }

    // ── THIẾT BỊ ĐIỆN ────────────────────────────

    // ── THIẾT BỊ ĐIỆN TỰ ĐỘNG PHÂN TÍCH TỪ GHI CHÚ ────────────────────────────
    const parsedLights = parseElecNote(room.elecNoteLights || '');
    const parsedPanel  = parseElecNote(room.elecNotePanel || '');
    const parsedAc     = parseElecNote(room.elecNoteAc || '');
    const allParsedElec = [...parsedLights, ...parsedPanel, ...parsedAc];

    // Trích xuất số lượng cho việc tính toán dây điện tự động
    let eLightDl = 0, eLightSl = 0, eLightPanel = 0, eLightTuyp1200 = 0, eLightTuyp600 = 0, eLightLed = 0, eLightOther = 0;
    let eSw2 = 0, eSw1 = 0, eSwOther = 0;
    let eOutlet = 0, eCb1 = 0, eCb2 = 0, eCb3 = 0, ePanelBox = 0, eFan = 0;
    let eAcWall = 0, eAcCeil = 0, eAcCentral = 0, eAcOther = 0;

    allParsedElec.forEach(item => {
      const lbl = (item.label || '').toLowerCase();
      const norm = lbl.normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/\u0111/g, 'd').replace(/\u0110/g, 'd');
      const q = item.qty || 0;

      if (norm.includes('downlight') || norm.includes('downligh')) {
        eLightDl += q;
      } else if (norm.includes('spotlight') || norm.includes('sportlight')) {
        eLightSl += q;
      } else if (norm.includes('panel')) {
        eLightPanel += q;
      } else if (norm.includes('1200mm') || norm.includes('1200')) {
        eLightTuyp1200 += q;
      } else if (norm.includes('600mm') || norm.includes('600')) {
        eLightTuyp600 += q;
      } else if (norm.includes('tuyp')) {
        eLightOther += q;
      } else if (norm.includes('led')) {
        eLightLed += q;
      } else if (norm.includes('den') || norm.includes('light')) {
        eLightOther += q;
      } else if (norm.includes('o cam') || norm.includes('outlet')) {
        eOutlet += q;
      } else if (norm.includes('cong tac') || norm.includes('sw')) {
        if (norm.includes('2')) eSw2 += q;
        else if (norm.includes('1')) eSw1 += q;
        else eSwOther += q;
      } else if (norm.includes('cb 1') || norm.includes('cb tong')) {
        eCb1 += q;
      } else if (norm.includes('cb 2')) {
        eCb2 += q;
      } else if (norm.includes('cb 3')) {
        eCb3 += q;
      } else if (norm.includes('cb') || norm.includes('aptomat')) {
        eCb1 += q;
      } else if (norm.includes('tu dien') || norm.includes('panel box') || norm.includes('tu cb')) {
        ePanelBox += q;
      } else if (norm.includes('quat') || norm.includes('fan')) {
        eFan += q;
      } else if (norm.includes('treo tuong')) {
        eAcWall += q;
      } else if (norm.includes('am tran')) {
        eAcCeil += q;
      } else if (norm.includes('trung tam')) {
        eAcCentral += q;
      } else if (norm.includes('may lanh') || norm.includes('dieu hoa') || norm.includes('ac')) {
        eAcOther += q;
      }
    });

    const eLights = eLightDl + eLightSl + eLightPanel + eLightTuyp1200 + eLightTuyp600 + eLightLed + eLightOther;
    const eSw = eSw2 + eSw1 + eSwOther;
    const eCB20 = eCb1 + eCb2 + eCb3;
    const eAC = eAcWall + eAcCeil + eAcCentral + eAcOther;

    const hasElec = allParsedElec.length > 0;

    if (hasElec) {
      // Header section điện
      items.push({ surface: 'elecHeader', label: 'THIẾT BỊ ĐIỆN', unit: '', qty: 0, dai: '', rong: '', cao: '', price: 0, total: 0, formula: '', note: '' });

      // Thêm các thiết bị điện đã parse
      parsedLights.forEach(item => {
        items.push({
          surface: 'elec',
          photoCategory: 'den',
          label: item.label,
          unit: item.unit || 'bộ',
          qty: item.qty,
          dai: '', rong: '', cao: '',
          price: 0, total: 0,
          formula: `${item.qty} ${item.unit || 'bộ'}`,
          note: ''
        });
      });

      parsedPanel.forEach(item => {
        items.push({
          surface: 'elec',
          photoCategory: 'tudien',
          label: item.label,
          unit: item.unit || 'bộ',
          qty: item.qty,
          dai: '', rong: '', cao: '',
          price: 0, total: 0,
          formula: `${item.qty} ${item.unit || 'bộ'}`,
          note: ''
        });
      });

      parsedAc.forEach(item => {
        items.push({
          surface: 'elec',
          photoCategory: 'maylanh',
          label: item.label,
          unit: item.unit || 'bộ',
          qty: item.qty,
          dai: '', rong: '', cao: '',
          price: 0, total: 0,
          formula: `${item.qty} ${item.unit || 'bộ'}`,
          note: ''
        });
      });

      // Dây điện: tính mét → đổi ra cuộn 100m
      const m15 = perim * 2 + eLights * 5 + eSw * 3;
      const cuon15 = Math.ceil(m15 / 100);
      if (cuon15 > 0) items.push({
        surface: 'elec',
        label: 'Dây điện 1,5mm² Cadivi (đèn, công tắc)',
        unit: 'cuộn',
        qty: cuon15,
        dai:'',rong:'',cao:'', price:0,total:0,
        formula: `CV×2(${fmt(perim*2,1)}m) + đèn×5(${fmt(eLights*5,1)}m) + CT×3(${fmt(eSw*3,1)}m) = ${fmt(m15,1)}m → ${cuon15} cuộn`,
        note: '1 cuộn = 100m',
      });

      // Dây 2,5mm²: ổ cắm → perim×1.5 + 4m/ổ cắm
      const m25 = perim * 1.5 + eOutlet * 4;
      const cuon25 = Math.ceil(m25 / 100);
      if (cuon25 > 0) items.push({
        surface: 'elec',
        label: 'Dây điện 2,5mm² Cadivi (ổ cắm)',
        unit: 'cuộn',
        qty: cuon25,
        dai:'',rong:'',cao:'', price:0,total:0,
        formula: `CV×1,5(${fmt(perim*1.5,1)}m) + ổcắm×4(${fmt(eOutlet*4,1)}m) = ${fmt(m25,1)}m → ${cuon25} cuộn`,
        note: '1 cuộn = 100m',
      });

      // Dây 4,0mm²: máy lạnh + CB → (perim + 5m) × số thiết bị nặng
      const heavyLoad = eAC + eCB20;
      if (heavyLoad > 0) {
        const m40 = (perim + 5) * heavyLoad;
        const cuon40 = Math.ceil(m40 / 100);
        items.push({
          surface: 'elec',
          label: 'Dây điện 4,0mm² Cadivi (máy lạnh, CB)',
          unit: 'cuộn',
          qty: cuon40,
          dai:'',rong:'',cao:'', price:0,total:0,
          formula: `(CV+5m)×${heavyLoad} = ${fmt(m40,1)}m → ${cuon40} cuộn`,
          note: '1 cuộn = 100m',
        });
      }
      
      // Notice we do NOT close "if (hasElec) {" here! It will be closed by the original closing brace in the code.
// Vật tư phụ: 1 gói/phòng

      items.push({ surface: 'elec', label: 'Vật tư phụ điện (băng keo, đinh vít, co nối)', unit: 'gói', qty: 1, dai:'',rong:'',cao:'', price:0,total:0, formula:'1 gói/phòng', note:'' });

      // Mục nhắc nhở — luôn liệt kê, số lượng tự điền

      const eNep     = +room.elecNep     || 0;

      const eOngRuot = +room.elecOngRuot || 0;

      const eOngCung = +room.elecOngCung || 0;

      items.push({ 

        surface: 'elecManual', 

        label: 'Nẹp nhựa 3-4 cm', 

        unit: 'thanh',   

        qty: eNep,     

        dai:'',rong:'',cao:'', price:0,total:0, 

        formula: eNep ? `${eNep} thanh` : '', 

        note: eNep ? '1 thanh = 2m' : '← Tự điền' 

      });

      items.push({ 

        surface: 'elecManual', 

        label: 'Ống ruột gà phi 20 (luồn dây)', 

        unit: 'cuộn',   

        qty: eOngRuot, 

        dai:'',rong:'',cao:'', price:0,total:0, 

        formula: eOngRuot ? `${eOngRuot} cuộn` : '', 

        note: eOngRuot ? '1 cuộn = 50m' : '← Tự điền' 

      });

      items.push({ 

        surface: 'elecManual', 

        label: 'Ống cứng PVC phi 20 (conduit)',   

        unit: 'thanh',   

        qty: eOngCung, 

        dai:'',rong:'',cao:'', price:0,total:0, 

        formula: eOngCung ? `${eOngCung} thanh` : '', 

        note: eOngCung ? '1 thanh = 2,92m' : '← Tự điền' 

      });

    }

    // ── HẠNG MỤC THỦ CÔNG (do user thêm tay) ──

    (room.customItems || []).forEach(ci => {

      items.push({

        surface: 'custom',

        itemId:  ci.id,

        label:   ci.label || '(chưa đặt tên)',

        unit:    ci.unit  || '',

        qty:     +ci.qty  || 0,

        dai: '', rong: '', cao: '',

        price:   +ci.price || 0,

        total:   (+ci.qty || 0) * (+ci.price || 0),

        formula: ci.qty ? `${ci.qty} ${ci.unit}` : '',

        note:    ci.note || '',

      });

    });

    // ── GHI CHÚ → HẠNG MỤC (parser tự động) ──

    const noteItems = parseNoteItems(room);

    if (noteItems.length > 0) {

      items.push({ surface: 'noteHeader', label: 'CHI TIET TU GHI CHU', unit:'',qty:0,dai:'',rong:'',cao:'',price:0,total:0,formula:'',note:'' });

      noteItems.forEach(ni => {
        ni.photoCategory = 'overview';
        items.push(ni);
      });

    }

    // Parse noteWoodwork (Nội thất)
    if (room.noteWoodwork && room.noteWoodwork.trim()) {
      room.noteWoodwork.split('\n').map(l => l.trim()).filter(l => l).forEach(line => {
        const parsed = parseNoteDimensionLine(line);
        if (parsed.label) {
          items.push({
            surface: 'woodworkNote',
            label: parsed.label,
            unit: parsed.unit,
            qty: parsed.qty,
            dai: parsed.dai,
            rong: parsed.rong,
            cao: parsed.cao,
            price: 0,
            total: 0,
            formula: '',
            note: ''
          });
        }
      });
    }

    // Parse notePlumbing (Nước)
    if (room.notePlumbing && room.notePlumbing.trim()) {
      room.notePlumbing.split('\n').map(l => l.trim()).filter(l => l).forEach(line => {
        const parsed = parseNoteDimensionLine(line);
        if (parsed.label) {
          items.push({
            surface: 'plumbingNote',
            label: parsed.label,
            unit: parsed.unit,
            qty: parsed.qty,
            dai: parsed.dai,
            rong: parsed.rong,
            cao: parsed.cao,
            price: 0,
            total: 0,
            formula: '',
            note: ''
          });
        }
      });
    }

    // Parse noteWaterproof (Chống thấm)
    if (room.noteWaterproof && room.noteWaterproof.trim()) {
      room.noteWaterproof.split('\n').map(l => l.trim()).filter(l => l).forEach(line => {
        const parsed = parseNoteDimensionLine(line);
        if (parsed.label) {
          items.push({
            surface: 'waterproofNote',
            label: parsed.label,
            unit: parsed.unit,
            qty: parsed.qty,
            dai: parsed.dai,
            rong: parsed.rong,
            cao: parsed.cao,
            price: 0,
            total: 0,
            formula: '',
            note: ''
          });
        }
      });
    }

    // Gan _key on dinh cho moi item

    const _kc = {};

    items.forEach(it => {

      if (it.surface === 'custom') {

        it._key = 'ci:' + (it.itemId || it.id || '?');

      } else if (it.surface === 'elec' || it.surface === 'elecManual') {

        const slug = (it.label||'').replace(/[^a-zA-Z0-9]/g,'').substr(0,12);

        it._key = it.surface + '_' + slug;

      } else if (it.surface === 'noteItem') {

        _kc.ni = (_kc.ni||0)+1;

        it._key = 'ni_' + _kc.ni;

      } else {

        it._key = it.surface || 'x';

      }

    });

    // Apply thu tu da luu

    if (room.rowOrder && room.rowOrder.length) {

      items.sort((a,b) => {

        const ai = room.rowOrder.indexOf(a._key);

        const bi = room.rowOrder.indexOf(b._key);

        return (ai<0?99999:ai)-(bi<0?99999:bi);

      });

    }

    // Apply night work labor multiplier if isNightWork is enabled
    if (room.isNightWork) {
      const LABOR_KEYWORDS = [
        'nhân công', 'nhan cong', 'thi công', 'thi cong', 'lắp đặt', 'lap dat', 
        'tháo dỡ', 'thao do', 'đập phá', 'dap pha', 'di dời', 'di doi', 
        'vận chuyển', 'van chuyen', 'bốc xếp', 'boc xep', 'khoan cắt', 'khoan cat'
      ];
      const isLaborItem = (label) => {
        if (!label) return false;
        const normLabel = label.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/đ/g, 'd');
        return LABOR_KEYWORDS.some(kw => {
          const normKw = kw.normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/đ/g, 'd');
          return normLabel.includes(normKw);
        });
      };
      items.forEach(item => {
        if (isLaborItem(item.label)) {
          if (item.price) {
            item.price = item.price * 2;
            item.total = item.qty * item.price;
          }
          const currentNote = item.note || '';
          if (!currentNote.includes('Làm đêm')) {
            item.note = currentNote ? `${currentNote}; Làm đêm (x2)` : 'Làm đêm (x2)';
          }
        }
      });
    }

    return { rawFloor, rawWall, rawCeil, perim, items };

  },

  project(project) {

    let tFloor = 0, tWall = 0, tItems = 0;

    (project.rooms || []).forEach(r => {

      const c = this.room(r);

      tFloor += c.rawFloor;

      tWall  += c.rawWall;

      tItems += c.items.length;

    });

    return {

      rooms: (project.rooms || []).length,

      items: tItems,

      floor: tFloor,

      wall:  tWall,

    };

  },

  projectCost(project) {
    let grandSubtotal = 0;
    (project.rooms || []).forEach(r => {
      const calc = this.room(r);
      calc.items.forEach(item => {
        if (item.surface !== 'elecHeader' && item.surface !== 'noteHeader') {
          grandSubtotal += item.total || 0;
        }
      });
    });

    const ocVat = project.otherCosts || {};
    const totalFloorVat = (project.rooms || []).reduce((s, r) => s + (+r.D || 0) / 1000 * (+r.R || 0) / 1000, 0);
    const ocSubtotal = [
      { key: 'transport', autoQty: false, defaultQty: 1 },
      { key: 'debris', autoQty: true },
      { key: 'scaffold', autoQty: true },
      { key: 'design', autoQty: true },
      { key: 'supervision', autoQty: false, defaultQty: 1 },
    ].reduce((s, tmpl) => {
      const saved = ocVat[tmpl.key] || {};
      const qty = tmpl.autoQty ? totalFloorVat : +(saved.qty != null ? saved.qty : tmpl.defaultQty || 0);
      const price = +(saved.price || 0);
      return s + qty * price;
    }, 0);

    const totalBeforeVat = grandSubtotal + ocSubtotal;
    const vatRate = +(project.vatRate ?? 8) / 100;
    const vatAmt = Math.round(totalBeforeVat * vatRate);
    return totalBeforeVat + vatAmt;
  },

  projectSummary(project) {

    const summary = {};

    (project.rooms || []).forEach(room => {

      const calc = this.room(room);

      calc.items.forEach(item => {

        if (item.surface === 'elecHeader' || item.surface === 'noteHeader') return;

        const key = `${item.label.trim()}|||${item.unit.trim()}`;

        if (!summary[key]) {

          summary[key] = {

            label: item.label,

            unit: item.unit,

            qty: 0,

            price: item.price || 0,

            total: 0,

            rooms: [],

            notes: [],

            surface: item.surface

          };

        }

        summary[key].qty += item.qty || 0;

        summary[key].total += item.total || 0;

        if (!summary[key].price && item.price) {

          summary[key].price = item.price;

        }

        if (item.qty > 0) {

          summary[key].rooms.push(`${room.name} (${fmt(item.qty)} ${item.unit})`);

        }

        if (item.note && item.note.trim()) {

          const cleanNote = item.note.trim();

          if (!summary[key].notes.includes(cleanNote)) {

            summary[key].notes.push(cleanNote);

          }

        }

      });

    });

    return Object.values(summary).filter(item => item.qty > 0).map(item => {

      item.note = item.notes ? item.notes.join('; ') : '';

      return item;

    });

  },

};

