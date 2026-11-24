#!/usr/bin/env python3
"""Build the static GitHub Pages site in docs/ from data/bay_area_michelin_2026.json.

Run:  python3 scripts/build_site.py
Every table row is generated from the JSON; blank verified fields render as 'Unverified'.
"""
import html
import json
import pathlib
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "data" / "bay_area_michelin_2026.json").read_text(encoding="utf-8"))
OUT = ROOT / "docs"
OUT.mkdir(exist_ok=True)
AS_OF = DATA["meta"]["as_of"]

NAV = [
    ("index.html", "Summary"),
    ("starred.html", "Michelin stars"),
    ("bib.html", "Bib Gourmand"),
    ("hotels.html", "Hotels"),
    ("analysis.html", "Analysis"),
    ("flagged.html", "Flagged"),
    ("questions.html", "Questions"),
    ("suggestions.html", "Suggestions"),
    ("sources.html", "Sources"),
]


def esc(v):
    return html.escape("" if v is None else str(v))


def cell(v, label, unverified_ok=True):
    """Render a cell; empty values are flagged as unverified (never inferred)."""
    if v is None or str(v).strip() == "":
        if unverified_ok:
            return f'<td data-label="{esc(label)}"><span class="unv">Unverified</span></td>'
        return f'<td data-label="{esc(label)}">—</td>'
    return f'<td data-label="{esc(label)}">{esc(v)}</td>'


def link(url, text):
    if not url:
        return '<span class="unv">Unverified</span>'
    return f'<a href="{esc(url)}" target="_blank" rel="noopener">{esc(text)}</a>'


def page(filename, title, body, description):
    parts = []
    for href, label in NAV:
        cls = ' class="on"' if href == filename else ""
        parts.append(f'<a href="{href}"{cls}>{label}</a>')
    nav_html = "".join(parts)
    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} · SF Bay Area Michelin Tracker</title>
<meta name="description" content="{esc(description)}">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<header class="top">
  <div class="brand"><a href="index.html">SF Bay Area Michelin Tracker</a></div>
  <nav class="nav">{nav_html}</nav>
</header>
<main class="wrap">
<h1>{esc(title)}</h1>
<p class="asof">Data as of {AS_OF} · Official-source verified fields only · blank = <span class="unv">Unverified</span></p>
{body}
</main>
<footer class="foot">
  <p>Not affiliated with MICHELIN. Star and Bib status from michelin.com and guide.michelin.com. Hours and prices change: confirm with the restaurant before you go.</p>
  <p><a href="https://github.com/kanlerxz87-cyber/Baymich2" target="_blank" rel="noopener">Repository</a> · <a href="sources.html">All sources</a></p>
</footer>
<script src="assets/app.js"></script>
</body>
</html>
"""
    (OUT / filename).write_text(doc, encoding="utf-8")


def search_box(table_id):
    return (
        f'<div class="tools"><input type="search" placeholder="Filter rows (name, city, cuisine…)" '
        f'data-filter="{table_id}" aria-label="Filter table"></div>'
    )


# ---------- derived numbers (computed from the verified JSON only) ----------
starred = DATA["starred"]
bibs = DATA["bib"]
news = DATA["news_only_not_yet_verified"]
lost = DATA["lost_stars_reported_not_verified"]
full_rows = [s for s in starred if s["verification"] == "full"]
partial_rows = [s for s in starred if s["verification"] == "partial"]
listing_rows = [s for s in starred if s["verification"] == "listing"]
star_by_city = Counter(s["city"] for s in starred)
bib_by_city = Counter(b["city"] for b in bibs)
dist_counts = Counter(s["distinction"].split(" (")[0] for s in starred)
new_2026_stars = [s["name"] for s in starred if "new in 2026" in s["distinction"]]

# ---------- index / summary ----------
summary_points = [
    f"<strong>{len(starred)}</strong> starred restaurants in the official Michelin San Francisco listing: "
    f"{dist_counts.get('3 MICHELIN Stars', 0)} three-star, {dist_counts.get('2 MICHELIN Stars', 0)} two-star, "
    f"{dist_counts.get('1 MICHELIN Star', 0)} one-star (Michelin SF listing, read 2026-11-24).",
    f"<strong>{len(bibs)}</strong> Bay Area Bib Gourmand restaurants on the official Michelin California 2026 list "
    f"(San Francisco {bib_by_city.get('San Francisco', 0)}, Oakland {bib_by_city.get('Oakland', 0)}).",
    "New 2026 stars in the SF group: " + ", ".join(new_2026_stars) + ". Enclos (Sonoma) and Californios (San Francisco) "
    "were promoted to three stars in June 2026.",
    "Michelin shows only a price tier ($–$$$$) for each restaurant. "
    "<strong>No dollar price for two has been verified yet</strong>, so the price column is blank on purpose.",
    f"Verification depth: {len(full_rows)} starred rows are complete (address, cuisine, tier, hours, website); "
    f"{len(partial_rows)} are partial; {len(listing_rows)} have only listing data (name, tier, cuisine).",
    f"{len(news)} additional Bay Area star claims come from press only and are held on the Flagged page until "
    "checked on michelin.com. One conflict (Selby's city) is open.",
    "Social links (TikTok, Instagram, YouTube) and hotel rankings are <strong>not yet verified</strong>. See Suggestions and Questions.",
]
index_body = f"""
<section class="kpis">
  <a class="kpi" href="starred.html"><b>{len(starred)}</b><span>Starred (SF group)</span></a>
  <a class="kpi" href="bib.html"><b>{len(bibs)}</b><span>Bib Gourmand (Bay Area)</span></a>
  <a class="kpi" href="starred.html#unverified"><b>{len(news)}</b><span>Press-only (unverified)</span></a>
  <a class="kpi" href="hotels.html"><b>0</b><span>Hotels ranked (pending)</span></a>
  <a class="kpi" href="questions.html"><b>{len(DATA['questions'])}</b><span>Open questions</span></a>
  <a class="kpi" href="suggestions.html"><b>{len(DATA['suggestions'])}</b><span>Suggestions to choose</span></a>
</section>
<section class="card">
  <h2>Executive summary</h2>
  <ul class="bullets">{''.join(f'<li>{p}</li>' for p in summary_points)}</ul>
  <p class="note">Plain-English summary: the official guide is clear about <em>which</em> restaurants have stars and Bibs. It does not give dollar prices, and it does not link social accounts. Those gaps are open, and the Questions page lists what is needed to close them.</p>
</section>
<section class="card">
  <h2>Where to go next</h2>
  <div class="grid3">
    <a class="tile" href="starred.html"><b>Michelin stars</b><span>Table of 29 starred restaurants with status, hours, address and source links.</span></a>
    <a class="tile" href="bib.html"><b>Bib Gourmand</b><span>43 Bay Area Bib restaurants with addresses and the official source.</span></a>
    <a class="tile" href="analysis.html"><b>Clusters &amp; analysis</b><span>Counts by city from verified rows, plus what the data can and cannot show.</span></a>
    <a class="tile" href="hotels.html"><b>Hotels</b><span>Status of the hotel ranking, candidate hotels, and the method we will use.</span></a>
    <a class="tile" href="flagged.html"><b>Flagged for review</b><span>Repo irregularities, press-only claims and source conflicts.</span></a>
    <a class="tile" href="suggestions.html"><b>Suggestions</b><span>Improvements for you to approve before anything changes.</span></a>
  </div>
</section>
"""
page("index.html", "Summary", index_body,
     "SF Bay Area MICHELIN starred and Bib Gourmand tracker, verified against michelin.com and guide.michelin.com.")

# ---------- starred ----------
rows = []
for s in starred:
    tier = s["michelin_price_tier"]
    rows.append(
        "<tr>"
        + f'<td data-label="Restaurant"><b>{esc(s["name"])}</b><div class="sub">{esc(s["city"])}</div></td>'
        + cell(s["distinction"], "Michelin status")
        + cell(s["cuisine"], "Cuisine")
        + cell(tier, "Michelin price tier")
        + cell(s["price_for_two_usd"], "Total for 2 adults (USD)")
        + cell(s["days_open"], "Days open")
        + cell(s["hours"], "Hours & exceptions")
        + cell(s["address"], "Address")
        + cell(s["social"], "TikTok / Instagram / YouTube")
        + f'<td data-label="Links">{link(s["michelin_url"], "Michelin")} · {link(s["website"], "Restaurant site")}</td>'
        + f'<td data-label="Verification"><span class="tag tag-{s["verification"]}">{esc(s["verification"])}</span></td>'
        + f'<td data-label="Source">{link(s["sources"][0], "Source")}</td>'
        + "</tr>"
    )
news_rows = []
for n in news:
    news_rows.append(
        "<tr>"
        + f'<td data-label="Restaurant"><b>{esc(n["name"])}</b><div class="sub">{esc(n["city"])}</div></td>'
        + cell(n["claimed"], "Claimed status")
        + f'<td data-label="Check status">{esc(n["status"])}</td>'
        + f'<td data-label="Source">{link(n["source"], "Official (michelin.com)" if "michelin.com" in n["source"] else "Press (not official)")}</td>'
        + "</tr>"
    )
starred_body = f"""
<p class="note">Michelin 'status' is taken from the official star listing pages. <b>Listed</b> means a Michelin entry without a star (not in this table). Total price for two and social links are blank until verified. Days and hours are as shown on each Michelin page; confirm before booking.</p>
<section class="card">
<h2>Starred restaurants · official SF listing</h2>
{search_box("t-starred")}
<div class="table-wrap"><table id="t-starred" class="data">
<thead><tr><th>Restaurant</th><th>Michelin status</th><th>Cuisine</th><th>Michelin price tier</th><th>Total for 2 adults (USD)</th><th>Days open</th><th>Hours &amp; exceptions</th><th>Address</th><th>TikTok / Instagram / YouTube</th><th>Links</th><th>Verification</th><th>Source</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table></div>
</section>
<section class="card" id="unverified">
<h2>Press-only claims (not yet on michelin.com) · held for review</h2>
<p class="note">These come from news articles, or from the official press release where stated. They are not rows in the main table until each Michelin page is checked.</p>
<div class="table-wrap"><table id="t-news" class="data">
<thead><tr><th>Restaurant</th><th>Claimed status</th><th>Check status</th><th>Source</th></tr></thead>
<tbody>{''.join(news_rows)}</tbody></table></div>
</section>
"""
page("starred.html", "Michelin stars", starred_body,
     "Starred restaurants in the San Francisco Bay Area, 2026 MICHELIN Guide, with status, hours and sources.")

# ---------- bibs ----------
brows = []
for b in bibs:
    brows.append(
        "<tr>"
        + f'<td data-label="Restaurant"><b>{esc(b["name"])}</b>{" <span class=tag>New 2026</span>" if b.get("new") else ""}</td>'
        + cell(b["city"], "City")
        + cell(b["address"], "Address")
        + '<td data-label="Michelin status">Bib Gourmand (official 2026)</td>'
        + cell("", "Total for 2 adults (USD)")
        + cell("", "Days open & hours")
        + cell("", "TikTok / Instagram / YouTube")
        + f'<td data-label="Source">{link("https://www.michelin.com/en/publications/products-and-services/the-michelin-guide-california-2026", "michelin.com 2026")}</td>'
        + "</tr>"
    )
bib_body = f"""
<p class="note">All {len(bibs)} Bay Area entries on the official Michelin California 2026 Bib list (cities in the Bay Area counties). Addresses are from the official list. Price, hours and social fields are still to be verified. Bibs outside the Bay Area (Santa Cruz, Carmel, Aptos, Seaside) are excluded.</p>
<section class="card">
{search_box("t-bib")}
<div class="table-wrap"><table id="t-bib" class="data">
<thead><tr><th>Restaurant</th><th>City</th><th>Address</th><th>Michelin status</th><th>Total for 2 adults (USD)</th><th>Days open &amp; hours</th><th>TikTok / Instagram / YouTube</th><th>Source</th></tr></thead>
<tbody>{''.join(brows)}</tbody></table></div>
</section>
"""
page("bib.html", "Bib Gourmand", bib_body, "Bay Area MICHELIN Bib Gourmand restaurants, 2026, from the official Michelin list.")

# ---------- hotels ----------
hrows = []
for h in DATA["hotels_michelin_listed_candidates"]:
    hrows.append(
        "<tr>"
        + f'<td data-label="Hotel"><b>{esc(h["name"])}</b></td>'
        + cell(h["area"], "Area")
        + '<td data-label="Michelin Keys / stars">Unverified</td>'
        + '<td data-label="Restaurants within radius">Unverified</td>'
        + '<td data-label="Rank">Not ranked</td>'
        + f'<td data-label="Source">{link(h["source"], "Michelin hotel page")}</td>'
        + "</tr>"
    )
hotels_body = f"""
<section class="card">
<h2>Status</h2>
<p><b>The hotel ranking is not built yet.</b> A ranking needs (1) an agreed radius and hotel pool (see Questions Q5), (2) verified official hotel addresses, and (3) coordinates for both hotels and restaurants. None of these is in the verified dataset yet, so no rank has been assigned. No hotel was given a rank or a count.</p>
<p>Method once approved: count verified Michelin starred + Bib restaurants within the chosen radius of each hotel's official address, and rank by that count. The rank column stays blank until the count is verified.</p>
</section>
<section class="card">
<h2>Michelin-listed hotels found on official pages (candidates, not ranked)</h2>
{search_box("t-hotels")}
<div class="table-wrap"><table id="t-hotels" class="data">
<thead><tr><th>Hotel</th><th>Area</th><th>Michelin Keys / stars</th><th>Restaurants within radius</th><th>Rank</th><th>Source</th></tr></thead>
<tbody>{''.join(hrows)}</tbody></table></div>
</section>
"""
page("hotels.html", "Hotels", hotels_body, "Hotel ranking status for the SF Bay Area Michelin tracker, with candidate hotels.")

# ---------- analysis ----------
city_rows = []
all_cities = sorted(set(star_by_city) | set(bib_by_city), key=lambda c: -(star_by_city.get(c, 0) * 2 + bib_by_city.get(c, 0)))
for c in all_cities:
    city_rows.append(
        f"<tr><td data-label='City'>{esc(c)}</td><td data-label='Starred (official listing)'>{star_by_city.get(c, 0)}</td>"
        f"<td data-label='Bib Gourmand'>{bib_by_city.get(c, 0)}</td>"
        f"<td data-label='Starred + Bib'>{star_by_city.get(c, 0) + bib_by_city.get(c, 0)}</td></tr>"
    )
analysis_body = f"""
<section class="kpis">
  <div class="kpi"><b>{len(full_rows)}</b><span>Starred rows fully verified</span></div>
  <div class="kpi"><b>{len(partial_rows)}</b><span>Partly verified</span></div>
  <div class="kpi"><b>{len(listing_rows)}</b><span>Listing-only (no hours)</span></div>
  <div class="kpi"><b>{len(news)}</b><span>Press-only claims</span></div>
</section>
<section class="card">
<h2>Counts by city (rows in this tracker)</h2>
<p class="note">Counts use only the official rows in this tracker. They are not a full count of the guide. The official SF listing shows 4 three-star, 7 two-star, 18 one-star, 30 Bib and 86 Selected in 'San Francisco and surroundings'. Our Bay Area Bib count (43) uses a wider geography.</p>
<div class="table-wrap"><table class="data"><thead><tr><th>City</th><th>Starred (official listing)</th><th>Bib Gourmand</th><th>Starred + Bib</th></tr></thead>
<tbody>{''.join(city_rows)}</tbody></table></div>
</section>
<section class="card">
<h2>What the clusters show (so far)</h2>
<ul class="bullets">
<li>San Francisco holds {star_by_city.get('San Francisco', 0)} of {len(starred)} starred rows and {bib_by_city.get('San Francisco', 0)} of {len(bibs)} Bibs in the verified set.</li>
<li>The official SF listing counts {DATA['counts_official']['sf_and_surroundings_listing']['three_star']} three-star, {DATA['counts_official']['sf_and_surroundings_listing']['two_star']} two-star and {DATA['counts_official']['sf_and_surroundings_listing']['one_star']} one-star restaurants. That matches our starred rows.</li>
<li>Oakland is the second cluster: {star_by_city.get('Oakland', 0)} starred and {bib_by_city.get('Oakland', 0)} Bibs.</li>
<li>Street-level clusters (e.g. the same block or district) need verified coordinates. Neighbourhood names are not used here because the official pages do not give them.</li>
</ul>
</section>
"""
page("analysis.html", "Analysis", analysis_body, "Counts and clusters of starred and Bib Gourmand restaurants in the SF Bay Area, verified rows only.")

# ---------- flagged ----------
irr_rows = "".join(
    f"<tr><td data-label='ID'>{esc(i['id'])}</td><td data-label='Area'>{esc(i['area'])}</td>"
    f"<td data-label='Irregularity'>{esc(i['item'])}</td><td data-label='Source'>{link(i.get('source'), 'Link') if i.get('source') else '—'}</td></tr>"
    for i in DATA["irregularities"]
)
lost_rows = "".join(
    f"<tr><td data-label='Restaurant'><b>{esc(l['name'])}</b><div class='sub'>{esc(l['city'])}</div></td>"
    f"<td data-label='Status'>{esc(l['status'])}</td></tr>"
    for l in lost
)
flagged_body = f"""
<p class="note">Items here are not final. A status of <b>needs review</b> means the item is published on this page and does not block other work.</p>
<section class="card"><h2>Irregularities &amp; source conflicts</h2>
<div class="table-wrap"><table class="data"><thead><tr><th>ID</th><th>Area</th><th>Irregularity</th><th>Source</th></tr></thead><tbody>{irr_rows}</tbody></table></div>
</section>
<section class="card"><h2>Reported lost stars (news only)</h2>
<div class="table-wrap"><table class="data"><thead><tr><th>Restaurant</th><th>Status</th></tr></thead><tbody>{lost_rows}</tbody></table></div>
</section>
<section class="card"><h2>Repo review summary</h2>
<p>The repository started with a one-line README. Full notes are in <code>REPO_REVIEW.md</code> in the repository root. Flagged for review: no license, no ignore file, branch-name mismatch with the brief, and no Pages configuration before this session.</p>
</section>
"""
page("flagged.html", "Flagged for review", flagged_body, "Irregularities, unverified claims and source conflicts in the SF Bay Area Michelin tracker.")

# ---------- questions ----------
qrows = "".join(
    f"<tr><td data-label='ID'>{esc(q['id'])}</td><td data-label='Question'>{esc(q['question'])}</td>"
    f"<td data-label='Why it matters'>{esc(q['why'])}</td><td data-label='Status'>{esc(q['status'])}</td></tr>"
    for q in DATA["questions"]
)
questions_body = f"""
<p class="note">Answers to these decide what can be verified and ranked. Reply with the ID and your answer (e.g. "Q1: Bay Area 9 counties").</p>
<section class="card"><div class="table-wrap"><table class="data"><thead><tr><th>ID</th><th>Question</th><th>Why it matters</th><th>Status</th></tr></thead><tbody>{qrows}</tbody></table></div></section>
"""
page("questions.html", "Questions to resolve", questions_body, "Open questions and missing information for the SF Bay Area Michelin tracker.")

# ---------- suggestions ----------
srows = "".join(
    f"<tr><td data-label='ID'>{esc(s['id'])}</td><td data-label='Suggestion'>{esc(s['title'])}</td>"
    f"<td data-label='Benefit'>{esc(s['benefit'])}</td><td data-label='Status'>{esc(s['status'])}</td></tr>"
    for s in DATA["suggestions"]
)
suggestions_body = f"""
<p class="note">Nothing on this list has been implemented. Reply with the IDs you want (e.g. "approve S1, S2, S4") and I will do only those.</p>
<section class="card"><div class="table-wrap"><table class="data"><thead><tr><th>ID</th><th>Suggestion</th><th>Benefit</th><th>Status</th></tr></thead><tbody>{srows}</tbody></table></div></section>
"""
page("suggestions.html", "Suggestions", suggestions_body, "Suggestions to improve the SF Bay Area Michelin tracker, for review before any change.")

# ---------- sources ----------
src = {}
def add(u, label):
    if u:
        src.setdefault(u, label)
add(DATA["meta"]["official_press_release"], "Michelin official press release, California 2026 (stars, Bib list, awards)")
add(DATA["meta"]["official_sf_listing_3_stars"], "Michelin SF 3-star listing")
add(DATA["meta"]["official_sf_listing_2_stars"], "Michelin SF 2-star listing")
add(DATA["meta"]["official_sf_listing_1_star"], "Michelin SF 1-star listing")
add("https://guide.michelin.com/us/en/california/san-francisco/restaurants", "Michelin SF listing (counts)")
for s in starred:
    add(s["michelin_url"], f"Michelin page: {s['name']}")
for h in DATA["hotels_michelin_listed_candidates"]:
    add(h["source"], f"Michelin hotel page: {h['name']}")
for n in news:
    add(n["source"], f"Press (not official): {n['name']}")
src_rows = "".join(
    f"<tr><td data-label='Source'>{esc(lbl)}</td><td data-label='Link'>{link(u, u)}</td></tr>" for u, lbl in src.items()
)
sources_body = f"""
<p class="note">Every link used in the tables. Official = michelin.com or guide.michelin.com. Press links are labelled and are not official.</p>
<section class="card"><div class="table-wrap"><table class="data"><thead><tr><th>Source</th><th>Link</th></tr></thead><tbody>{src_rows}</tbody></table></div></section>
"""
page("sources.html", "Sources", sources_body, "All sources for the SF Bay Area Michelin tracker.")

print(f"built {len(list(OUT.glob('*.html')))} pages in {OUT}")
