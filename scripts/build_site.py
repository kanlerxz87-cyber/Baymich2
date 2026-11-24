#!/usr/bin/env python3
"""Build the static GitHub Pages site in docs/ from the JSON data files.

Inputs : data/michelin_starred_bay_area.json, data/review.json
Outputs: docs/index.html, docs/michelin.html, docs/hotels.html,
         docs/flagged.html, docs/questions.html, docs/sources.html,
         docs/style.css, docs/.nojekyll
Standard library only. Re-run after any data change:
    python3 scripts/build_site.py
"""
import html
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
DOCS = ROOT / "docs"

michelin = json.loads((DATA / "michelin_starred_bay_area.json").read_text(encoding="utf-8"))
review = json.loads((DATA / "review.json").read_text(encoding="utf-8"))
META = michelin["meta"]
ROWS = michelin["restaurants"]


def e(value):
    return html.escape(str(value)) if value not in (None, "") else ""


def cell(value, flag_text="Not verified"):
    """Return the cell content, or a flagged 'unverified' marker if empty."""
    if value in (None, ""):
        return f'<span class="flag">{e(flag_text)}</span>'
    return e(value)


def link(url, label):
    if not url:
        return '<span class="flag">Not verified</span>'
    return f'<a href="{e(url)}" target="_blank" rel="noopener">{e(label)}</a>'


def page(title, active, body):
    nav = [
        ("index.html", "Dashboard"),
        ("michelin.html", "Michelin Stars"),
        ("hotels.html", "Hotels"),
        ("flagged.html", "Flagged for Review"),
        ("questions.html", "Questions & Suggestions"),
        ("sources.html", "Sources"),
    ]
    links = "".join(
        f'<a class="{"on" if href == active else ""}" href="{href}">{label}</a>' for href, label in nav
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)} · SF Bay Area Michelin Dashboard</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<header class="top">
  <div class="brand">SF Bay Area Michelin Dashboard</div>
  <nav>{links}</nav>
</header>
<main>
{body}
</main>
<footer>
  Every value links to an official source. Blank or “Not verified” means it could not be confirmed from an official source.
  Data as of {e(META["as_of"])}. Built from <code>data/</code> by <code>scripts/build_site.py</code>.
</footer>
</body>
</html>
"""


# ---------- counts ----------
total = len(ROWS)
by_star = {s: sum(1 for r in ROWS if r["stars"] == s) for s in (3, 2, 1)}
hours_full = sum(1 for r in ROWS if r["hours_status"] == "verified")
hours_partial = sum(1 for r in ROWS if r["hours_status"] == "partial")
hours_pending = sum(1 for r in ROWS if r["hours_status"] == "pending")
pages_pulled = sum(1 for r in ROWS if not r["detail_status"].startswith("pending"))
open_flags = [f for f in review["flagged"] if f["severity"] in ("high", "medium")]
open_questions = [q for q in review["questions"] if q["status"] == "open"]

# ---------- index ----------
index_body = f"""
<section class="hero">
  <h1>SF Bay Area Michelin Dashboard</h1>
  <p class="lede">A verified, organized view of the Michelin-starred restaurants in the Bay Area, with the questions that still need answers before any decisions are made.</p>
</section>

<section>
  <h2>Executive summary</h2>
  <ul class="summary">
    <li><b>{total} starred restaurants</b> in the Bay Area under the nine-county scope (assumption, see <a href="questions.html">Questions</a>). That is {total} of the 83 starred restaurants statewide in the official 2026 California selection.</li>
    <li><b>{by_star[3]} three-star</b>, <b>{by_star[2]} two-star</b>, <b>{by_star[1]} one-star</b>. Source: <a href="{e(META["star_source"]["url"])}" target="_blank" rel="noopener">official Michelin 2026 California article</a>.</li>
    <li><b>New 2026 stars in the Bay Area:</b> Californios and Enclos (3 stars), Naides, Troubadour, Wolfsbane (1 star each). Source: the same official article.</li>
    <li><b>Verification status:</b> star status is verified for all {total} rows. Official restaurant pages have been read for {pages_pulled} of {total}. Full listed hours are verified for {hours_full}, partial for {hours_partial}, and pending for {hours_pending}.</li>
    <li><b>Prices:</b> Michelin lists a price tier only. No couple-price dollar amount has been verified yet, so that column is blank for every row.</li>
    <li><b>Social links (YouTube, TikTok, Instagram):</b> none verified yet, so they are blank.</li>
    <li><b>Hotels and activities:</b> not built yet. They depend on decisions listed on the <a href="questions.html">Questions</a> page.</li>
    <li><b>Open items:</b> {len(open_flags)} medium/high flags on the <a href="flagged.html">Flagged for Review</a> page and {len(open_questions)} open questions.</li>
  </ul>
</section>

<section>
  <h2>Pages</h2>
  <div class="cards">
    <a class="card" href="michelin.html"><b>Michelin Stars</b><span>{total} starred Bay Area restaurants, by star level, with official links.</span></a>
    <a class="card" href="hotels.html"><b>Hotels</b><span>Ranking by nearby starred restaurants. Blocked until method and hotel data are approved.</span></a>
    <a class="card" href="flagged.html"><b>Flagged for Review</b><span>{len(review["flagged"])} irregularities and unverified items.</span></a>
    <a class="card" href="questions.html"><b>Questions & Suggestions</b><span>{len(review["questions"])} open questions and {len(review["suggestions"])} suggestions. Nothing is implemented until you choose.</span></a>
    <a class="card" href="sources.html"><b>Sources & Method</b><span>Every official source used, and how each value was checked.</span></a>
  </div>
</section>
"""

# ---------- michelin ----------
def star_section(stars):
    rows = [r for r in ROWS if r["stars"] == stars]
    label = {3: "Three MICHELIN Stars", 2: "Two MICHELIN Stars", 1: "One MICHELIN Star"}[stars]
    out = [f'<h2>{label} <span class="count">({len(rows)})</span></h2>',
           '<div class="table-wrap"><table class="data"><thead><tr>'
           '<th>Restaurant</th><th>Michelin status</th><th>City · County</th><th>Address</th>'
           '<th>Price tier</th><th>Days &amp; hours (Michelin listing)</th><th>Couple cost (2 adults)</th>'
           '<th>Video / social</th><th>Links</th></tr></thead><tbody>']
    for r in rows:
        hours = r["hours"] if r["hours"] else ""
        if r["hours_status"] == "partial":
            hours = f'{hours} <span class="flag">Partial</span>'
        elif r["hours_status"] == "pending":
            hours = '<span class="flag">Pending — not yet read from official page</span>'
        out.append(
            "<tr>"
            f'<td data-label="Restaurant"><b>{e(r["name"])}</b></td>'
            f'<td data-label="Michelin status">{e(r["michelin_status"])}</td>'
            f'<td data-label="City · County">{e(r["city"])} · {e(r["county"])}</td>'
            f'<td data-label="Address">{cell(r["address"], "Pending official page")}</td>'
            f'<td data-label="Price tier">{cell(r["price_tier"], "Pending official page")}</td>'
            f'<td data-label="Hours">{hours}</td>'
            f'<td data-label="Couple cost">{cell("", "Not verified — no official dollar figure found")}</td>'
            f'<td data-label="Video / social">{cell("", "Not verified")}</td>'
            f'<td data-label="Links">{link(r["michelin_url"], "Michelin page")}'
            f' · {link(r["official_website"], "Restaurant site")}</td>'
            "</tr>"
        )
    out.append("</tbody></table></div>")
    return "\n".join(out)


michelin_body = f"""
<section>
  <h1>Michelin Stars · SF Bay Area</h1>
  <p class="note">Star status is from the official 2026 Michelin California article. Address, price tier, and hours are from each official Michelin restaurant page. <b>Couple cost</b> and <b>social links</b> are blank because no verified official value exists yet. <b>Hours</b> are Michelin’s listed hours. Holiday exceptions are not captured. Confirm with the restaurant before you go.</p>
  <p class="note"><b>Legend:</b> “Not verified” or “Pending” means no official value has been confirmed yet. Those cells are intentionally blank.</p>
  <p class="note">Michelin shows only a price tier ($ to $$$$). No dollar amounts are shown.</p>
  <div class="kpis">
    <div><b>{total}</b><span>Starred</span></div>
    <div><b>{by_star[3]}</b><span>3-star</span></div>
    <div><b>{by_star[2]}</b><span>2-star</span></div>
    <div><b>{by_star[1]}</b><span>1-star</span></div>
  </div>
</section>
{star_section(3)}
{star_section(2)}
{star_section(1)}
<section>
  <h2>Listed but not starred (Bib Gourmand / Recommended)</h2>
  <p class="note">Not yet collected. Pending task T6 (see <a href="questions.html">Questions</a>, Q2).</p>
</section>
"""

# ---------- hotels ----------
hotels_body = """
<section>
  <h1>Hotels · ranked by nearby Michelin restaurants</h1>
  <p class="flag-banner"><b>Not built yet.</b> A verified ranking needs three decisions first: the radius and weights (Q5), the hotel scope (Q6), and an approved coordinate source. No hotel is ranked and no hotel row is filled in until those are verified.</p>
  <h2>Proposed method (for approval only)</h2>
  <ol>
    <li>Use the verified starred restaurant addresses from the Michelin page (see <a href="michelin.html">Michelin Stars</a>).</li>
    <li>For each hotel, count starred restaurants within an approved straight-line radius.</li>
    <li>Score: 3-star = 3, 2-star = 2, 1-star = 1 (weights to be approved).</li>
    <li>Rank by score, then by count. Show the verified source for each hotel.</li>
  </ol>
  <p>Decisions: <a href="questions.html">Questions Q5 and Q6</a>.</p>
</section>
"""

# ---------- flagged ----------
sev_order = {"high": 0, "medium": 1, "low": 2, "info": 3}
flag_rows = sorted(review["flagged"], key=lambda f: sev_order[f["severity"]])
flag_html = ['<div class="table-wrap"><table class="data"><thead><tr><th>ID</th><th>Severity</th><th>Item</th><th>Detail</th><th>Sources</th></tr></thead><tbody>']
for f in flag_rows:
    srcs = " · ".join(
        f'<a href="{e(s)}" target="_blank" rel="noopener">source {i+1}</a>' for i, s in enumerate(f["sources"])
    ) or '<span class="flag">None (not from a source)</span>'
    flag_html.append(
        f'<tr><td data-label="ID">{e(f["id"])}</td><td data-label="Severity"><span class="sev {e(f["severity"])}">{e(f["severity"])}</span></td>'
        f'<td data-label="Item"><b>{e(f["item"])}</b></td><td data-label="Detail">{e(f["detail"])}</td>'
        f'<td data-label="Sources">{srcs}</td></tr>'
    )
flag_html.append("</tbody></table></div>")
flagged_body = f"""
<section>
  <h1>Flagged for Review</h1>
  <p class="note">Irregularities and unverified items. Each one needs a human check against the linked source before any decision. Sorted by severity.</p>
  {"".join(flag_html)}
</section>
"""

# ---------- questions & suggestions ----------
q_html = ['<div class="table-wrap"><table class="data"><thead><tr><th>ID</th><th>Question / information needed</th><th>Why it matters</th><th>How to resolve</th><th>Status</th></tr></thead><tbody>']
for q in review["questions"]:
    q_html.append(
        f'<tr><td data-label="ID">{e(q["id"])}</td><td data-label="Question"><b>{e(q["question"])}</b></td>'
        f'<td data-label="Why">{e(q["why"])}</td><td data-label="How">{e(q["how_to_resolve"])}</td>'
        f'<td data-label="Status"><span class="sev info">{e(q["status"])}</span></td></tr>'
    )
q_html.append("</tbody></table></div>")
s_html = ['<div class="table-wrap"><table class="data"><thead><tr><th>ID</th><th>Suggestion</th><th>Benefit</th><th>Effort</th><th>Risk</th><th>Your choice</th></tr></thead><tbody>']
for s in review["suggestions"]:
    s_html.append(
        f'<tr><td data-label="ID">{e(s["id"])}</td><td data-label="Suggestion"><b>{e(s["title"])}</b></td>'
        f'<td data-label="Benefit">{e(s["benefit"])}</td><td data-label="Effort">{e(s["effort"])}</td>'
        f'<td data-label="Risk">{e(s["risk"])}</td><td data-label="Your choice">Pending — approve / reject / modify</td></tr>'
    )
s_html.append("</tbody></table></div>")
questions_body = f"""
<section>
  <h1>Questions &amp; Suggestions</h1>
  <p class="note">Nothing on this page is implemented until you choose. Answer the questions first. Then pick which suggestions to adopt.</p>
  <h2>Open questions</h2>
  {"".join(q_html)}
  <h2>Suggestions for site improvement</h2>
  {"".join(s_html)}
</section>
"""

# ---------- sources ----------
sources_body = f"""
<section>
  <h1>Sources &amp; Method</h1>
  <h2>Primary sources (official)</h2>
  <ul>
    <li><a href="{e(META["star_source"]["url"])}" target="_blank" rel="noopener">MICHELIN Guide — Every MICHELIN-Starred Restaurant in California for 2026</a> (published 24 June 2026). Used for star status and the 83-restaurant count.</li>
    <li>Official Michelin restaurant pages (guide.michelin.com/us/en/…). One link per row in the <a href="michelin.html">Michelin table</a>. Used for address, phone, restaurant website, price tier, and listed hours.</li>
  </ul>
  <h2>Secondary sources (cross-check only, not used as values)</h2>
  <ul>
    <li><a href="https://sf.eater.com/restaurant-news/212958/2026-michelin-star-winners-california-guide-san-francisco-bay-area" target="_blank" rel="noopener">Eater SF — 2026 Michelin Star Winners of the Bay Area</a>. Used to find conflicts (see <a href="flagged.html">Flagged</a>).</li>
  </ul>
  <h2>Method</h2>
  <ol>
    <li>Read the official article and copy star lists exactly.</li>
    <li>Open each official restaurant page and copy address, phone, website, price tier, and listed hours.</li>
    <li>If a value is missing from the official page, leave it blank and flag it. Nothing is inferred.</li>
    <li>Compare against secondary sources and flag any conflict.</li>
  </ol>
  <h2>Data files</h2>
  <ul>
    <li><code>data/michelin_starred_bay_area.json</code> — table data.</li>
    <li><code>data/review.json</code> — flags, questions, suggestions.</li>
    <li><code>COORDINATION.md</code> — shared task board and session log.</li>
  </ul>
</section>
"""

# ---------- write ----------
DOCS.mkdir(exist_ok=True)
(DOCS / ".nojekyll").write_text("", encoding="utf-8")
pages = {
    "index.html": page("Dashboard", "index.html", index_body),
    "michelin.html": page("Michelin Stars", "michelin.html", michelin_body),
    "hotels.html": page("Hotels", "hotels.html", hotels_body),
    "flagged.html": page("Flagged for Review", "flagged.html", flagged_body),
    "questions.html": page("Questions & Suggestions", "questions.html", questions_body),
    "sources.html": page("Sources", "sources.html", sources_body),
}
for name, content in pages.items():
    (DOCS / name).write_text(content, encoding="utf-8")
print(f"wrote {len(pages)} pages to {DOCS}")
