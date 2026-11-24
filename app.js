// Shared renderer for all pages. Reads JSON from ./data/ (relative paths work on GitHub Pages subpaths).
const D = 'data/';
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const unv = (t='Unverified') => `<span class="unv">${esc(t)}</span>`;
const val = (v, t) => (v && String(v).trim()) ? esc(v) : unv(t);
const lnk = (url, text) => url ? `<a href="${esc(url)}" rel="noopener">${esc(text || 'Source')}</a>` : unv('No source');
const sev = s => `<span class="badge ${esc(s)}">${esc(s)}</span>`;
async function getJSON(f){ const r = await fetch(D + f, {cache:'no-store'}); if(!r.ok) throw new Error(f + ' ' + r.status); return r.json(); }

function socialCell(r){
  const s = r.social || {}; const parts = [];
  if (s.youtube) parts.push(lnk(s.youtube,'YouTube')); if (s.tiktok) parts.push(lnk(s.tiktok,'TikTok')); if (s.instagram) parts.push(lnk(s.instagram,'Instagram'));
  return parts.length ? parts.join(' · ') : unv('Unverified');
}
function hoursCell(r){
  const d = r.openDays && r.openDays !== 'UNVERIFIED' ? r.openDays : null;
  const h = r.hours && !r.hours.startsWith('Profile lists') ? r.hours : null;
  let out = '';
  if (d) out += `<div>${esc(d)}</div>`;
  if (h) out += `<div>${esc(h)}</div>`;
  if (r.hoursStatus === 'flagged') out += `<div class="flagtxt">⚠ ${esc(r.hours)} — unverified (F1)</div>`;
  if (!out) out = unv();
  return out;
}
function costCell(r){
  if (r.costForTwo) return `<div>${esc(r.costForTwo)}</div>` + (r.costStatus==='estimate' ? `<div class="note">Estimate (F9)</div>` : '');
  return unv();
}
function flagsFor(r){
  const f = [];
  if (r.hoursStatus === 'flagged') f.push('F1');
  if (r.verification && r.verification.startsWith('Not re-verified')) f.push('F10');
  if (r.name.startsWith('Acquerello')) f.push('F9');
  if (r.category==='Bib Gourmand') f.push('');
  return f.filter(Boolean).join(', ') || '—';
}
function restaurantRow(r){
  const star = r.category==='Starred' ? `<span class="badge star">${r.stars}★ currently</span>` : `<span class="badge bib">Bib Gourmand</span>`;
  return `<tr>
    <td data-label="Restaurant"><strong>${esc(r.name)}</strong><div class="note">${esc(r.city)} · ${esc(r.region)}</div></td>
    <td data-label="Status">${star}<div class="note">${esc(r.guideStatus)}</div></td>
    <td data-label="Price tier">${val(r.priceTier)}</td>
    <td data-label="Cost for two">${costCell(r)}</td>
    <td data-label="Open days / hours">${hoursCell(r)}</td>
    <td data-label="Address">${val(r.address)}</td>
    <td data-label="Official links"><div>${lnk(r.michelinUrl,'MICHELIN profile/listing')}</div>${r.website?`<div>${lnk(r.website,'Website')}</div>`:''}</td>
    <td data-label="Social">${socialCell(r)}</td>
    <td data-label="Verification"><div class="note">${esc(r.verification)}</div><div class="note">Flags: ${esc(flagsFor(r))}</div></td>
  </tr>`;
}

async function pageRestaurants(){
  const rows = await getJSON('restaurants.json');
  const state = {cat:'all', region:'all', q:''};
  const regions = [...new Set(rows.map(r=>r.region))].sort();
  document.getElementById('region').innerHTML = `<option value="all">All regions</option>` + regions.map(x=>`<option>${esc(x)}</option>`).join('');
  const draw = () => {
    const q = state.q.toLowerCase();
    const list = rows.filter(r => (state.cat==='all' || (state.cat==='starred'? r.category==='Starred' : r.category==='Bib Gourmand'))
      && (state.region==='all' || r.region===state.region)
      && (!q || (r.name+' '+r.city+' '+(r.cuisine||'')).toLowerCase().includes(q)));
    document.getElementById('rows').innerHTML = list.map(restaurantRow).join('');
    document.getElementById('count').textContent = `${list.length} of ${rows.length} rows shown · starred ${rows.filter(r=>r.category==='Starred').length} · Bib Gourmand ${rows.filter(r=>r.category==='Bib Gourmand').length}`;
  };
  document.querySelectorAll('[data-cat]').forEach(b => b.addEventListener('click', () => {
    state.cat = b.dataset.cat; document.querySelectorAll('[data-cat]').forEach(x=>x.setAttribute('aria-pressed', x===b)); draw(); }));
  document.getElementById('region').addEventListener('change', e => { state.region = e.target.value; draw(); });
  document.getElementById('q').addEventListener('input', e => { state.q = e.target.value; draw(); });
  draw();
}

async function pageHome(){
  const rows = await getJSON('restaurants.json');
  const flags = await getJSON('flags.json');
  const c = (f) => rows.filter(f).length;
  document.getElementById('kpis').innerHTML = [
    ['Starred rows (dataset)', c(r=>r.category==='Starred')],
    ['3★ / 2★ / 1★', `${c(r=>r.stars===3)} / ${c(r=>r.stars===2)} / ${c(r=>r.stars===1)}`],
    ['Bib Gourmand (SF & surroundings)', c(r=>r.category==='Bib Gourmand')],
    ['Open flags', flags.length],
  ].map(([k,v])=>`<div class="kpi"><b>${esc(v)}</b><span>${esc(k)}</span></div>`).join('');
  const regs = [...new Set(rows.map(r=>r.region))].sort();
  document.getElementById('clusters').innerHTML = regs.map(g => {
    const s = rows.filter(r=>r.region===g && r.category==='Starred').length;
    const b = rows.filter(r=>r.region===g && r.category==='Bib Gourmand').length;
    return `<tr><td data-label="Region">${esc(g)}</td><td data-label="Starred">${s}</td><td data-label="Bib Gourmand">${b}</td></tr>`;
  }).join('');
}

async function pageHotels(){
  const h = await getJSON('hotels.json');
  document.getElementById('status').textContent = h.status;
  document.getElementById('hstats').innerHTML = Object.entries(h.stats).map(([k,v])=>`<div class="kpi"><b>${esc(v)}</b><span>${esc(k)}</span></div>`).join('');
  document.getElementById('rows').innerHTML = h.hotels.map(x => `<tr>
    <td data-label="Hotel"><strong>${esc(x.name)}</strong>${x.note?`<div class="note">${esc(x.note)}</div>`:''}</td>
    <td data-label="Area">${esc(x.area)}</td>
    <td data-label="MICHELIN Keys">${x.keys}</td>
    <td data-label="Nearby MICHELIN restaurants">${unv('Not computed')}</td>
    <td data-label="Rank">${unv('Withheld')}</td>
    <td data-label="Official links">${lnk(x.url||x.listing, x.url?'Hotel page':'Key listing')}${x.url?` · ${lnk(x.listing,'Key listing')}`:''}</td>
  </tr>`).join('');
}

async function pageActivities(){
  const a = await getJSON('activities.json');
  document.getElementById('status').textContent = a.status;
  document.getElementById('rows').innerHTML = a.activities.map(x => `<tr>
    <td data-label="Activity"><strong>${esc(x.name)}</strong><div class="note">${esc(x.area||'')}</div></td>
    <td data-label="Open days">${val(x.openDays)}</td>
    <td data-label="Hours">${val(x.hours)}</td>
    <td data-label="Exceptions">${val(x.exceptions,'Unverified')}</td>
    <td data-label="Cost for two adults">${unv(x.costNote || 'Unverified')}</td>
    <td data-label="Phone">${val(x.phone)}</td>
    <td data-label="Social">${socialCell(x)}</td>
    <td data-label="Official links">${(x.sourceLinks||[]).length ? x.sourceLinks.map((u,i)=>lnk(u,'Source '+(i+1))).join(' · ') : unv('No source')}</td>
    <td data-label="Verification"><div class="note">${esc(x.verification)}</div></td>
  </tr>`).join('');
}

async function pageReview(){
  const flags = await getJSON('flags.json');
  const src = await getJSON('sources.json');
  document.getElementById('flags').innerHTML = flags.map(f => `<tr>
    <td data-label="ID">${esc(f.id)}</td><td data-label="Severity">${sev(f.severity)}</td>
    <td data-label="Item"><strong>${esc(f.item)}</strong><div class="note">${esc(f.type)}</div></td>
    <td data-label="Detail">${esc(f.detail)}</td>
    <td data-label="Action">${esc(f.action)}</td>
    <td data-label="Links">${f.links.map((u,i)=>lnk(u,'Link '+(i+1))).join(' · ')}</td></tr>`).join('');
  document.getElementById('sources').innerHTML = src.map(s => `<tr>
    <td data-label="ID">${esc(s.id)}</td><td data-label="Source">${esc(s.title)}</td><td data-label="Used for">${esc(s.used)}</td>
    <td data-label="Link">${lnk(s.url,'Open')}</td></tr>`).join('');
}

const PAGES = {restaurants: pageRestaurants, home: pageHome, hotels: pageHotels, activities: pageActivities, review: pageReview};
const page = document.body.dataset.page;
if (PAGES[page]) PAGES[page]().catch(err => {
  const m = document.getElementById('error'); if (m) { m.hidden = false; m.textContent = 'Could not load data: ' + err.message; }
});
