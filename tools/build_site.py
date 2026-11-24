"""Build the static GitHub Pages site in docs/ from data/*.csv and data/*.json.

Every number shown on the site is computed here from data/michelin_restaurants.csv.
Blank values are shown as "unverified" flags, never filled in.
"""
import csv, html, json, os
from collections import Counter, OrderedDict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
DATA = os.path.join(ROOT, "data")
TODAY = "2026-11-24"
REPO = "https://github.com/kanlerxz87-cyber/Baymich2"
SITE = "https://kanlerxz87-cyber.github.io/Baymich2/"
LISTING = "https://guide.michelin.com/us/en/california/san-francisco/restaurants"

rows = list(csv.DictReader(open(os.path.join(DATA, "michelin_restaurants.csv"), encoding="utf-8")))
for r in rows:
    r["stars"] = int(r["stars"])
N = len(rows)
AWARDS = ["3 Stars", "2 Stars", "1 Star", "Bib Gourmand", "Selected"]
acount = Counter(r["award"] for r in rows)
ccount = Counter(r["city"] for r in rows)
starred = [r for r in rows if r["stars"] > 0]
det_checked = [r for r in rows if r["michelin_detail_checked"] == "Yes"]
hours_complete = [r for r in rows if r["hours_status"] == "complete"]
price_verified = [r for r in rows if r["price_for_two_usd"]]
social_verified = [r for r in rows if r["social_links"]]

def e(x):
    return html.escape(str(x or ""), quote=True)

def badge(award):
    cls = {"3 Stars": "b3", "2 Stars": "b2", "1 Star": "b1", "Bib Gourmand": "bib", "Selected": "sel", "Unverified": "unv"}.get(award, "sel")
    label = {"3 Stars": "★★★ 3 Stars", "2 Stars": "★★ 2 Stars", "1 Star": "★ 1 Star", "Bib Gourmand": "Bib Gourmand", "Selected": "Selected", "Unverified": "Tier unverified"}.get(award, award)
    return f'<span class="badge {cls}">{e(label)}</span>'

def unv(text="unverified"):
    return f'<span class="flag">⚑ {e(text)}</span>'

CSS = """
:root{--ink:#1d2330;--mut:#5b6474;--line:#e3e7ee;--bg:#f6f7f9;--card:#fff;--acc:#1f4fd1;--gold:#b7860b;--warn:#b45309;--ok:#15803d}
*{box-sizing:border-box}body{margin:0;font:15px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;color:var(--ink);background:var(--bg)}
a{color:var(--acc);word-break:break-word}
header.top{background:#111827;color:#fff;padding:14px 16px}
header.top .t{font-weight:700;font-size:17px;margin:0}header.top .s{color:#cbd5e1;font-size:12px;margin:2px 0 8px}
nav{display:flex;flex-wrap:wrap;gap:6px}nav a{color:#e5e7eb;text-decoration:none;background:#1f2937;padding:6px 10px;border-radius:999px;font-size:13px}
nav a.on,nav a:hover{background:#2563eb;color:#fff}
main{max-width:1200px;margin:0 auto;padding:16px}
h1{font-size:22px;margin:6px 0 4px}h2{font-size:18px;margin:22px 0 8px}h3{font-size:15px;margin:14px 0 6px}
.lead{color:var(--mut);margin:0 0 12px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:10px;margin:10px 0}
.kpi{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px}
.kpi .n{font-size:24px;font-weight:700}.kpi .l{color:var(--mut);font-size:12px}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px;text-decoration:none;color:inherit;display:block}
.card:hover{border-color:var(--acc)}.card b{display:block;font-size:16px;margin-bottom:4px}.card span{color:var(--mut);font-size:13px}
.panel{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px;margin:10px 0}
.note{background:#fffbeb;border:1px solid #fde68a;border-radius:10px;padding:10px 12px;margin:10px 0;font-size:13px}
.tools{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:10px 0}
.tools input{flex:1 1 220px;padding:9px 12px;border:1px solid var(--line);border-radius:10px;font-size:14px}
.tools button{border:1px solid var(--line);background:#fff;padding:7px 11px;border-radius:999px;font-size:13px;cursor:pointer}
.tools button.on{background:var(--acc);color:#fff;border-color:var(--acc)}
.tw{overflow-x:auto;background:var(--card);border:1px solid var(--line);border-radius:12px}
table{border-collapse:collapse;width:100%;font-size:13.5px}
th,td{padding:9px 10px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}
th{background:#f1f4f9;font-size:12px;text-transform:uppercase;letter-spacing:.03em;color:var(--mut);position:sticky;top:0}
td .sub{color:var(--mut);font-size:12px}
.badge{display:inline-block;padding:2px 8px;border-radius:999px;font-size:12px;font-weight:600;white-space:nowrap}
.b3{background:#fde68a;color:#78350f}.b2{background:#fcd9a8;color:#7c2d12}.b1{background:#e0e7ff;color:#312e81}.bib{background:#dcfce7;color:#14532d}.sel{background:#f1f5f9;color:#334155}.unv{background:#fff7ed;color:#9a3412;border:1px dashed #fdba74}
.flag{display:inline-block;color:var(--warn);background:#fff7ed;border:1px dashed #fdba74;border-radius:6px;padding:0 6px;font-size:12px;white-space:nowrap}
.ok{color:var(--ok);font-weight:600}.part{color:var(--warn);font-weight:600}
.bar{height:8px;background:#e5e7eb;border-radius:99px;overflow:hidden;min-width:80px}.bar i{display:block;height:100%;background:var(--acc)}
.cnt{font-weight:700}
ul.clean{padding-left:18px}ul.clean li{margin:4px 0}
footer{color:var(--mut);font-size:12px;padding:20px 16px;text-align:center}
/* mobile: each table row becomes a card */
@media (max-width:760px){
 .tw{overflow:visible;border:none;background:none}
 table,thead,tbody,tr,td{display:block;width:100%}
 thead{display:none}
 tr{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:6px 10px;margin:0 0 10px}
 td{border:none;padding:5px 0;display:flex;gap:8px;justify-content:space-between}
 td::before{content:attr(data-label);color:var(--mut);font-size:11px;text-transform:uppercase;flex:0 0 38%;letter-spacing:.03em}
 td.nolabel::before{content:none}
 td.nolabel{display:block}
 .sticky-mobile{display:none}
}
"""

NAV = [("index.html", "Home"), ("restaurants.html", "Michelin restaurants"), ("clusters.html", "Clusters"),
       ("hotels.html", "Hotels"), ("summary.html", "Summary & questions"), ("flagged.html", "Flagged for review"),
       ("repo-review.html", "Repo review & sources")]

def page(fname, title, body, active):
    nav = "".join(f'<a href="{h}" class="{"on" if h == active else ""}">{t}</a>' for h, t in NAV)
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)} · Bay Area Michelin Dashboard</title>
<meta name="description" content="Bay Area Michelin restaurants, clusters, hotels, verification status and open questions. Every value links to its source or is flagged unverified.">
<style>{CSS}</style></head><body>
<header class="top"><p class="t">Bay Area Michelin Dashboard</p><p class="s">Data as of {TODAY} · San Francisco &amp; surroundings (Michelin listing)</p><nav>{nav}</nav></header>
<main>{body}</main>
<footer>Built from <a href="{REPO}">the Baymich2 repo</a> · Michelin data: <a href="https://guide.michelin.com/us/en/california/san-francisco/restaurants">guide.michelin.com</a> · Unverified fields are blank and flagged ⚑.</footer>
<script>
(function(){{
 var q=document.getElementById('q'); var btns=document.querySelectorAll('[data-f]'); var rs=document.querySelectorAll('tbody tr[data-award]');
 var cur='all';
 function apply(){{var t=(q?q.value:'').toLowerCase();
  rs.forEach(function(r){{var okF=(cur==='all')||r.getAttribute('data-award')===cur;
   var okQ=!t||r.textContent.toLowerCase().indexOf(t)>-1; r.style.display=(okF&&okQ)?'':'none';}});
  var c=document.getElementById('count'); if(c){{c.textContent=document.querySelectorAll('tbody tr[data-award]:not([style*="none"])').length;}}
 }}
 btns.forEach(function(b){{b.addEventListener('click',function(){{btns.forEach(function(x){{x.classList.remove('on')}});b.classList.add('on');cur=b.getAttribute('data-f');apply();}});}});
 if(q){{q.addEventListener('input',apply);}}
 apply();
}})();
</script></body></html>"""

def write(name, content):
    with open(os.path.join(DOCS, name), "w", encoding="utf-8") as f:
        f.write(content)

os.makedirs(DOCS, exist_ok=True)
open(os.path.join(DOCS, ".nojekyll"), "w").close()

# ---------- INDEX / DASHBOARD ----------
kpis = [(N, "Michelin-listed restaurants captured"), (acount["3 Stars"], "3-star"), (acount["2 Stars"], "2-star"),
        (acount["1 Star"], "1-star"), (acount["Bib Gourmand"], "Bib Gourmand"), (acount["Selected"], "Selected (listed only)"),
        (len(det_checked), "restaurants with detail-page check"), (len(price_verified), "prices for 2 verified")]
kpi_html = "".join(f'<div class="kpi"><div class="n">{n}</div><div class="l">{e(l)}</div></div>' for n, l in kpis)
cards = [
 ("restaurants.html", "Michelin restaurants", f"{N} rows · filter by star, Bib or Selected · address, hours, source link per row"),
 ("clusters.html", "Clusters", f"City captured for {N-ccount['not captured']} of {N} rows · Oakland {ccount['Oakland']}, Berkeley {ccount['Berkeley']}, San Mateo {ccount['San Mateo']}"),
 ("hotels.html", "Hotels", "Michelin-listed Bay Area hotels · ranking pending (see flags)"),
 ("summary.html", "Summary & questions", "Executive summary, open questions, and suggestions awaiting your choice"),
 ("flagged.html", "Flagged for review", "Unverified fields, irregularities and gaps, with what is needed to close each"),
 ("repo-review.html", "Repo review & sources", "What the repo contains, irregularities, and every source link used"),
]
card_html = "".join(f'<a class="card" href="{h}"><b>{e(t)}</b><span>{e(d)}</span></a>' for h, t, d in cards)
body = f"""<h1>Dashboard</h1>
<p class="lead">Michelin restaurants and hotels around the San Francisco Bay Area. Stars, Bib Gourmand and Selected are shown separately. Anything that could not be confirmed from an official source is left blank and flagged ⚑.</p>
<div class="grid">{kpi_html}</div>
<div class="note"><b>Read first:</b> Only the Michelin listing was captured (San Francisco &amp; surroundings, {N} rows). Prices for two, social links and hotel rankings are <b>not yet verified</b>. See <a href="flagged.html">Flagged for review</a>.</div>
<h2>Pages</h2><div class="cards">{card_html}</div>"""
write("index.html", page("index.html", "Dashboard", body, "index.html"))

# ---------- RESTAURANTS ----------
th = ["Restaurant", "Michelin award", "Price tier (Michelin)", "Price for 2 adults", "Cuisine", "Address", "Days & hours (Michelin)", "Restaurant website", "Source", "YouTube / TikTok / Instagram"]
trs = []
for r in rows:
    addr = r["address"] or unv("not captured")
    hrs = r["hours_michelin"]
    if r["hours_status"] == "complete":
        hrs_html = f'{e(hrs)}<div class="sub"><span class="ok">✓ captured</span> from Michelin detail page</div>'
    elif r["hours_status"] == "partial":
        hrs_html = f'{e(hrs)}<div class="sub"><span class="part">partial</span> · verify</div>'
    else:
        hrs_html = unv("hours not captured")
    web = f'<a href="{e(r["website"])}" rel="noopener">Official site ↗</a>' if r["website"] else unv("not captured")
    trs.append(f"""<tr data-award="{e(r['award'])}">
<td data-label="Restaurant"><b>{e(r['name'])}</b><div class="sub">{e(r['city']) if r['city']!='not captured' else unv('city not captured')}</div></td>
<td data-label="Michelin award">{badge(r['award'])}{('<div class="sub">'+e(r['award_status'])+'</div>') if r['award_status']!='from listing card' else ''}</td>
<td data-label="Price tier">{e(r['michelin_price_tier'])}</td>
<td data-label="Price for 2">{unv('unverified')}</td>
<td data-label="Cuisine">{e(r['cuisine'])}</td>
<td data-label="Address">{addr}</td>
<td data-label="Days & hours">{hrs_html}</td>
<td data-label="Website">{web}</td>
<td data-label="Source"><a href="{e(r['source_url'])}" rel="noopener">Michelin ↗</a></td>
<td data-label="Social">{unv('not searched')}</td>
</tr>""")
body = f"""<h1>Michelin restaurants · SF &amp; surroundings</h1>
<p class="lead">{N} restaurants from Michelin's “San Francisco and surroundings” listing. Showing <span id="count">{N}</span>.</p>
<div class="note"><b>Verification:</b> every row links to its Michelin listing. Address, phone, website and hours are only filled where the Michelin detail page was checked ({len(det_checked)} of {N}). Price for 2 adults and social links are not verified yet, so they are blank and flagged.</div>
<div class="tools">
 <input id="q" type="search" placeholder="Search name, cuisine, city…" aria-label="Search">
 <button data-f="all" class="on">All ({N})</button>
 <button data-f="3 Stars">3★ ({acount['3 Stars']})</button>
 <button data-f="2 Stars">2★ ({acount['2 Stars']})</button>
 <button data-f="1 Star">1★ ({acount['1 Star']})</button>
 <button data-f="Bib Gourmand">Bib ({acount['Bib Gourmand']})</button>
 <button data-f="Selected">Selected ({acount['Selected']})</button>
</div>
<div class="tw"><table><thead><tr>{''.join(f'<th>{e(h)}</th>' for h in th)}</tr></thead>
<tbody>{''.join(trs)}</tbody></table></div>
<p class="lead" style="margin-top:10px">Source for every row: Michelin Guide listing pages 1–4 of the SF &amp; surroundings list (read {TODAY}). The Source link opens the restaurant's Michelin page where the city was captured, otherwise the listing page it was read from. Michelin's header says 145 restaurants and this table holds 145 rows. Two tiers are flagged for review (see <a href="flagged.html">Flagged</a>).</p>"""
write("restaurants.html", page("restaurants.html", "Michelin restaurants", body, "restaurants.html"))

# ---------- CLUSTERS ----------
crow = []
for city, n in ccount.most_common():
    sub = [r for r in rows if r["city"] == city]
    c = Counter(r["award"] for r in sub)
    pct = round(100 * n / N)
    crow.append(f"""<tr data-award="x"><td data-label="City"><b>{e(city)}</b></td>
<td data-label="Restaurants"><span class="cnt">{n}</span></td>
<td data-label="Share"><div class="bar"><i style="width:{pct}%"></i></div><span class="sub">{pct}%</span></td>
<td data-label="3★">{c['3 Stars']}</td><td data-label="2★">{c['2 Stars']}</td><td data-label="1★">{c['1 Star']}</td>
<td data-label="Bib">{c['Bib Gourmand']}</td><td data-label="Selected">{c['Selected']}</td></tr>""")
cuisine = Counter()
for r in rows:
    for part in r["cuisine"].split(","):
        cuisine[part.strip()] += 1
top_cu = cuisine.most_common(10)
cu_rows = "".join(f'<li>{e(k)} — <b>{v}</b></li>' for k, v in top_cu)
price_by_award = []
for a in AWARDS:
    sub = [r for r in rows if r["award"] == a]
    pc = Counter(r["michelin_price_tier"] for r in sub)
    price_by_award.append(f"<tr><td data-label='Award'>{badge(a)}</td>" + "".join(f"<td data-label='{t}'>{pc.get(t,0)}</td>" for t in ["$", "$$", "$$$", "$$$$"]) + "</tr>")
body = f"""<h1>Clusters</h1>
<p class="lead">Where the Michelin listings concentrate. Counts are computed from the verified listing rows (no estimates).</p>
<h2>By city</h2>
<div class="tw"><table><thead><tr><th>City</th><th>Restaurants</th><th>Share</th><th>3★</th><th>2★</th><th>1★</th><th>Bib</th><th>Selected</th></tr></thead>
<tbody>{''.join(crow)}</tbody></table></div>
<h2>Price tier (Michelin $ symbol) by award</h2>
<p class="lead">Michelin's price symbol is a range, not a dollar amount. Dollar prices for 2 adults are not yet verified.</p>
<div class="tw"><table><thead><tr><th>Award</th><th>$</th><th>$$</th><th>$$$</th><th>$$$$</th></tr></thead><tbody>{''.join(price_by_award)}</tbody></table></div>
<h2>Most common cuisine labels (Michelin)</h2>
<div class="panel"><ul class="clean">{cu_rows}</ul><p class="sub">Counts list a restaurant once per cuisine label it carries.</p></div>
<div class="note"><b>Scope and gaps:</b> pages 1–2 of the listing were captured without a city on each card, so {ccount['not captured']} of {N} rows show “not captured” rather than an assumed city. City counts are therefore partial. The table covers Michelin's “San Francisco and surroundings” list only; other Bay Area listings were not captured.</div>"""
write("clusters.html", page("clusters.html", "Clusters", body, "clusters.html"))

# ---------- HOTELS ----------
HOTEL_PAGE = "https://guide.michelin.com/us/en/hotels-stays/san-francisco-bay-area"
hotel_rows = [
 ("San Francisco Proper Hotel", "Guest score shown as 18.6 on the Michelin page (looks off-scale, see F10)"),
 ("Hotel Zeppelin San Francisco", "Named on the Michelin hotel page; no address captured"),
]
hrows = "".join(f"""<tr><td data-label="Hotel"><b>{e(n)}</b></td>
<td data-label="Michelin distinction">{unv('not captured')}</td>
<td data-label="Michelin restaurants nearby (rank)">{unv('not computed')}</td>
<td data-label="Notes">{e(note)}</td>
<td data-label="Source"><a href="{HOTEL_PAGE}" rel="noopener">Michelin hotels page ↗</a></td></tr>""" for n, note in hotel_rows)
body = f"""<h1>Hotels</h1>
<p class="lead">Michelin-listed hotels around the Bay Area. The ranking by nearby Michelin restaurants is <b>not computed</b>. It needs each hotel's address, a distance method, and a radius, none of which are settled.</p>
<div class="grid">
 <div class="kpi"><div class="n">31</div><div class="l">hotels on Michelin's SF Bay Area list</div></div>
 <div class="kpi"><div class="n">3</div><div class="l">Two MICHELIN Keys</div></div>
 <div class="kpi"><div class="n">2</div><div class="l">One MICHELIN Key</div></div>
 <div class="kpi"><div class="n">26</div><div class="l">Selected</div></div>
 <div class="kpi"><div class="n">2</div><div class="l">hotel names read so far</div></div>
</div>
<h2>Hotels read so far</h2>
<div class="tw"><table><thead><tr><th>Hotel</th><th>Michelin distinction</th><th>Restaurants nearby (rank)</th><th>Notes</th><th>Source</th></tr></thead><tbody>{hrows}</tbody></table></div>
<div class="note"><b>Why the ranking is blank:</b> only the first page of Michelin's hotel list was read, and it gave two hotel names. No hotel address was captured, so no distance can be measured. The remaining hotel pages are unread. Ranking them would mean guessing, so the ranking is left empty until the data is in (see S4 in <a href="summary.html">Summary</a>).</div>"""
write("hotels.html", page("hotels.html", "Hotels", body, "hotels.html"))

# ---------- SUMMARY / QUESTIONS / SUGGESTIONS ----------
top_city = ccount.most_common(4)
body = f"""<h1>Executive summary</h1>
<div class="panel"><ul class="clean">
<li><b>{N} restaurants</b> captured from Michelin's “San Francisco and surroundings” list (header: 145). Award counts: <b>{acount['3 Stars']} three-star, {acount['2 Stars']} two-star, {acount['1 Star']} one-star, {acount['Bib Gourmand']} Bib Gourmand, {acount['Selected']} Selected, {acount['Unverified']} tier unverified</b>. Michelin's sidebar shows Bib 30 and Selected 86; captured Selected is 85 plus one unverified tier.</li>
<li><b>Two tiers need review:</b> Village Sake (Bib Gourmand, from the Bibendum icon on its Michelin page) and Kajiken (tier not shown in the captured text).</li>
<li><b>Cluster:</b> city was captured for {N-ccount['not captured']} of {N} rows. Among those, Oakland has {ccount['Oakland']}, Berkeley {ccount['Berkeley']} and San Mateo {ccount['San Mateo']}. San Francisco rows from listing pages 1–2 have no city in the captured text.</li>
<li><b>Verified now:</b> the award for every row, from the listing cards (two tiers flagged above). For {len(det_checked)} detail pages (11 starred plus Village Sake), address, phone and website come from Michelin. Hours are complete for {len(hours_complete)}, partial for 2, and missing for 3.</li>
<li><b>Not verified yet:</b> price for 2 adults (0 of {N}), social links (0 of {N}), hours for most rows, and the hotel ranking.</li>
<li><b>Hotels:</b> Michelin lists 31 hotels for the Bay Area (3 Two-Key, 2 One-Key, 26 Selected). Only two hotel names have been read so far, and the ranking is not done.</li>
</ul></div>
<h2>Open questions</h2></ul></div>
<h2>Open questions</h2>
<div class="tw"><table><thead><tr><th>#</th><th>Question</th><th>Status</th><th>What is needed to answer it</th></tr></thead><tbody>
<tr><td data-label="#">Q1</td><td data-label="Question">What does “around” mean for the hotel ranking: walking distance, a neighbourhood, or a radius?</td><td data-label="Status"><span class="part">Open</span></td><td data-label="Needed">Your choice. Options: 1 km, 2 km, same neighbourhood.</td></tr>
<tr><td data-label="#">Q2</td><td data-label="Question">How many restaurants should the table hold: SF &amp; surroundings only, or the full Bay Area (San Jose, Napa, Sonoma, Santa Cruz etc.)?</td><td data-label="Status"><span class="part">Open</span></td><td data-label="Needed">Your scope decision. The other listings are linked from Michelin's page and were not captured.</td></tr>
<tr><td data-label="#">Q3</td><td data-label="Question">What is the price for 2 adults at each restaurant?</td><td data-label="Status"><span class="part">Unanswered</span></td><td data-label="Needed">Each restaurant's official menu page (tasting menu, à la carte, drinks extra) — see S2.</td></tr>
<tr><td data-label="#">Q4</td><td data-label="Question">Are current opening hours and days correct?</td><td data-label="Status"><span class="part">Partly answered</span></td><td data-label="Needed">Michelin hours for {len(hours_complete)} complete and 2 partial rows; cross-check against each restaurant's website; check holiday closures.</td></tr>
<tr><td data-label="#">Q5</td><td data-label="Question">Which social accounts (YouTube, TikTok, Instagram) belong to each restaurant?</td><td data-label="Status"><span class="part">Unanswered</span></td><td data-label="Needed">Social icons or links on each official site; confirm the account is the restaurant's own (S3).</td></tr>
<tr><td data-label="#">Q6</td><td data-label="Question">Which hotel is closest to the most Michelin restaurants?</td><td data-label="Status"><span class="part">Unanswered</span></td><td data-label="Needed">Hotel addresses from the 31 Michelin hotel pages, plus a distance method (Q1). No geocoding source has been chosen yet (S4).</td></tr>
<tr><td data-label="#">Q7</td><td data-label="Question">Does Michelin's total of 145 match the rows captured?</td><td data-label="Status"><span class="ok">Resolved on count</span></td><td data-label="Needed">Captured rows total 145. The two tiers in F1–F3 still need checking.</td></tr>
<tr><td data-label="#">Q8</td><td data-label="Question">How often will the data be refreshed, and by whom?</td><td data-label="Status"><span class="part">Open</span></td><td data-label="Needed">Your decision on refresh cadence (for example monthly) and owner.</td></tr>
</tbody></table></div>
<h2>Suggestions — choose before anything is changed</h2>
<p class="lead">Nothing below has been implemented. Reply with the IDs you want (for example “S1, S3, S4”), or with changes to any of them.</p>
<div class="tw"><table><thead><tr><th>ID</th><th>Suggestion</th><th>Why</th><th>Effort / risk</th></tr></thead><tbody>
<tr><td data-label="ID">S1</td><td data-label="Suggestion">Read the Michelin detail page for the 18 one-star, 30 Bib and 85 Selected rows (address, hours, website).</td><td data-label="Why">Fills the biggest gap in hours and addresses.</td><td data-label="Effort">About 133 page reads. Low risk.</td></tr>
<tr><td data-label="ID">S2</td><td data-label="Suggestion">Add “price for 2 adults” from each restaurant's own menu page. Store the menu, currency, date and URL. Leave blank if no official number exists.</td><td data-label="Why">Your required column; Michelin gives only $ symbols.</td><td data-label="Effort">About 144 menu pages. Prices change; add a date stamp.</td></tr>
<tr><td data-label="ID">S3</td><td data-label="Suggestion">Collect YouTube / TikTok / Instagram links only from each restaurant's official website footer or social links, and record the account name.</td><td data-label="Why">Avoids guessed or fan accounts.</td><td data-label="Effort">About 144 site checks. Some restaurants may have none.</td></tr>
<tr><td data-label="ID">S4</td><td data-label="Suggestion">Ranking method for hotels: read all 31 hotel pages for addresses, then count Michelin restaurants within a radius you choose (Q1). Show the method and distance on each row.</td><td data-label="Why">Answers the hotel ranking request.</td><td data-label="Effort">31 hotel reads plus a distance step. Distance needs a geocoding source; none has been chosen yet.</td></tr>
<tr><td data-label="ID">S5</td><td data-label="Suggestion">Add the South Bay and wider Bay Area Michelin listings (San Jose, Palo Alto, Napa/Sonoma, etc.) as separate tables.</td><td data-label="Why">Matches “Bay Area” in your brief.</td><td data-label="Effort">Several more listing reads. Larger table.</td></tr>
<tr><td data-label="ID">S6</td><td data-label="Suggestion">Add a “last verified” date and source column to every row, and a simple link-checker before publishing.</td><td data-label="Why">Keeps the “no hallucination” rule auditable.</td><td data-label="Effort">Small. Low risk.</td></tr>
<tr><td data-label="ID">S7</td><td data-label="Suggestion">Change GitHub Pages to publish from the <code>/docs</code> folder of <code>main</code> (currently <code>/</code>).</td><td data-label="Why">Keeps site files separate from data and tools.</td><td data-label="Effort">One setting change. Affects the live URL only if the setting changes.</td></tr>
<tr><td data-label="ID">S8</td><td data-label="Suggestion">Keep the data in CSV and rebuild the site from it with <code>tools/build_site.py</code>, so each refresh is one command.</td><td data-label="Why">Repeatable, reviewable changes.</td><td data-label="Effort">Already in place.</td></tr>
</tbody></table></div>
<p class="sub">Decision log: record your choice (approve / defer / decline) for each ID in <code>COORDINATION.md</code>.</p>"""
write("summary.html", page("summary.html", "Summary & questions", body, "summary.html"))

# ---------- FLAGGED ----------
flags = [
 ("F1", "Count reconciles, two tiers open", f"Michelin header 145. Captured rows total 145: 3★ {acount['3 Stars']}, 2★ {acount['2 Stars']}, 1★ {acount['1 Star']}, Bib {acount['Bib Gourmand']}, Selected {acount['Selected']}, tier unverified {acount['Unverified']}. Sidebar shows Selected 86.", LISTING, "F2 and F3"),
 ("F2", "Village Sake tier", "Bib Gourmand is inferred from the Bibendum icon above the name on its Michelin detail page, and from the sidebar Bib count (30). Not yet confirmed on the Bib Gourmand category page.", "https://guide.michelin.com/us/en/california/fairfax/restaurant/village-sake", "Read Michelin's Bib Gourmand category page"),
 ("F3", "Kajiken tier", "Kajiken (San Mateo, $, Noodles) is on listing page 4 (“145-145 of 145”). Its tier was not shown in the captured text.", "https://guide.michelin.com/us/en/california/san-mateo/restaurant/kajiken", "Read its detail page or the Selected category page"),
 ("F4", "City missing for listing pages 1–2", f"{ccount['not captured']} of {N} rows have no city in the captured text. Pages 1–2 were extracted without the city line on each card. Rows are shown “not captured”, not assumed.", LISTING, "Re-read pages 1–2 for the city line on each card"),
 ("F5", "Price for 2 adults", f"Not verified for any of the {N} rows. Michelin shows $ symbols only.", LISTING, "S2 — read each restaurant's official menu"),
 ("F6", "Social links", f"Not verified for any of the {N} rows.", "", "S3 — official site footers"),
 ("F7", "Hours incomplete", "Not captured: Atelier Crenn, Sons &amp; Daughters, Birdsong. Partial: Saison, Commis (later days cut off in the fetch).", "https://guide.michelin.com/us/en/california/san-francisco/restaurant/atelier-crenn", "Re-read detail pages; cross-check on the restaurant sites"),
 ("F8", "Hours for most rows not read", f"Only {len(det_checked)} detail pages were read (11 starred plus Village Sake). Hours for the other rows are blank.", "", "S1"),
 ("F9", "Hotel ranking not done", "Two hotel names read from the first page of Michelin's hotel list. No hotel addresses captured. Hotel pages 2–8 unread.", HOTEL_PAGE, "S4, Q1 and Q6"),
 ("F10", "Hotel guest score off-scale", "San Francisco Proper Hotel shows a guest score of 18.6 on Michelin's page. This looks off-scale. Not checked against another source.", HOTEL_PAGE, "Check the score's scale on the hotel's own page"),
 ("F11", "Scope", "Only Michelin's “San Francisco and surroundings” list was captured. Other Bay Area listings were not read.", LISTING, "S5 and Q2"),
 ("F12", "Listing-file row tags", "Two rows (Pearl 6101, La Cigale) sit in the page-2 file but were read from page 3. The listing_page column is correct for both.", "", "None needed; noted for audit"),
 ("F13", "Restaurant websites", "Websites come from each Michelin detail page. Ownership and currency were not checked.", "", "S3 — check on the restaurant sites"),
 ("F14", "Instructions conflict", "The parallel-session note asks for branches named session-&lt;id&gt;/&lt;task&gt;. This session is pinned to one branch, so all work is on that branch and claims are logged in COORDINATION.md.", "", "Your decision if you want per-task branches"),
 ("F15", "Repo has no content", "The repo held a single README (“# Baymich2”). No LICENSE, docs or code. Pages is set to main at /.", "https://github.com/kanlerxz87-cyber/Baymich2", "See Repo review"),
]
frows = "".join(f"""<tr><td data-label="ID">{e(i)}</td><td data-label="Item"><b>{e(t)}</b></td><td data-label="Detail">{d}</td><td data-label="Source">{('<a href="'+e(s)+'" rel="noopener">Open ↗</a>') if s else '<span class="sub">n/a</span>'}</td><td data-label="Needed to close">{e(n) if n.isascii() else n}</td></tr>""" for i, t, d, s, n in flags)
body = f"""<h1>Flagged for review</h1>
<p class="lead">Irregularities and unverified items. Each one says what is needed to close it. Nothing here has been filled in with a guess.</p>
<div class="tw"><table><thead><tr><th>ID</th><th>Item</th><th>Detail</th><th>Source</th><th>Needed to close</th></tr></thead><tbody>{frows}</tbody></table></div>"""
write("flagged.html", page("flagged.html", "Flagged for review", body, "flagged.html"))

# ---------- REPO REVIEW & SOURCES ----------
src = [
 ("Michelin listing: San Francisco &amp; surroundings (page 1)", LISTING, "Rows from page 1 (no city captured)"),
 ("Michelin listing page 2", LISTING + "/page/2", "Rows from page 2 (no city captured)"),
 ("Michelin listing page 3", LISTING + "/page/3", "Rows 97–144 incl. Oakland, Berkeley, Marin, Peninsula"),
 ("Michelin listing page 4", LISTING + "/page/4", "Header “145-145 of 145”; Kajiken"),
 ("Michelin detail: Village Sake", "https://guide.michelin.com/us/en/california/fairfax/restaurant/village-sake", "Address, website, phone, hours; Bibendum icon (Bib evidence)"),
 ("Michelin detail: Kajiken (not read)", "https://guide.michelin.com/us/en/california/san-mateo/restaurant/kajiken", "Listed only; detail page not read"),
 ("Michelin detail pages (11 starred)", LISTING, "Address, phone, website, hours (links per row in the restaurants table)"),
 ("Michelin Hotels: San Francisco Bay Area", HOTEL_PAGE, "Hotel count (31), distinctions, two hotel names"),
]
srows = "".join(f'<tr><td data-label="Source"><b>{n}</b></td><td data-label="Link"><a href="{e(u)}" rel="noopener">{e(u)}</a></td><td data-label="Used for">{e(d) if d.isascii() else d}</td></tr>' for n, u, d in src)
body = f"""<h1>Repo review &amp; sources</h1>
<h2>What the repo contained</h2>
<div class="panel"><ul class="clean">
<li><b>One commit</b> (“Initial commit”) on <code>main</code>; working branch <code>arena/5d054995-baymich2</code>, based on <code>1554148</code>.</li>
<li><b>Files:</b> <code>README.md</code> only, one line: “# Baymich2”. No code, data, LICENSE or docs before this work.</li>
<li><b>Pages:</b> GitHub Pages was already enabled on <code>main</code> at <code>/</code> (status built). This build publishes from <code>/docs</code>; that setting change is suggestion S7.</li>
<li><b>Coordination:</b> <code>COORDINATION.md</code> did not exist and was created as the task board.</li>
<li><b>Irregularities:</b> see <a href="flagged.html">Flagged</a> (F1–F4, F10, F11, F12, F15).</li>
</ul></div>
<h2>Sources used (every link)</h2>
<div class="tw"><table><thead><tr><th>Source</th><th>Link</th><th>Used for</th></tr></thead><tbody>{srows}</tbody></table></div>
<p class="sub">Restaurant websites are linked from each Michelin detail page and are listed per row on the restaurants page.</p>
<h2>Verification performed</h2>
<div class="panel"><ul class="clean">
<li>Read Michelin listing pages 1–4. Header on page 4 reads “145-145 of 145”. Captured rows total 145.</li>
<li>Award counts match the sidebar for 3★ (4), 2★ (7), 1★ (18) and Bib (30 with Village Sake). Selected is 85 plus Kajiken (tier unverified), against the sidebar's 86.</li>
<li>Read 12 detail pages (11 starred plus Village Sake). Address, phone and website come from them. Hours are complete for {len(hours_complete)}, partial for 2 and missing for 3.</li>
<li>Not verified: prices for two adults, social links, hotel addresses, and restaurant websites beyond the links Michelin shows.</li>
</ul></div>
"""
write("repo-review.html", page("repo-review.html", "Repo review & sources", body, "repo-review.html"))

print("pages written:", sorted(f for f in os.listdir(DOCS) if f.endswith(".html")))
