# Coordination Board — Baymich2 (SF Bay Area Michelin Guide & Map)

Branch: `arena/e1428a33-baymich2` (branched from `main` @ `1554148e`)
Session ID: `session-arena-e1428a33`
Base URL (live site): GitHub Pages — TBD (repo must be enabled for Pages)

## How to use this board
- Claim a task by writing your session ID + file scope in the "Owner / Scope" column, then commit and push immediately.
- Never start a task another session has claimed.
- Scopes must be non-overlapping; each session works on its own branch/worktree named `session-<id>/<task>`.
- If a task requires changing a file owned by another session, log the request here instead of editing it.
- Make small, frequent commits; run `git pull --rebase` before every push.
- When finished, record sources, verification performed, and irregularities, then mark the task "done".
- A claim older than 60 minutes with no commits may be taken over (note the handoff in the log).

## Tasks

| # | Task | Status | Owner / Scope | Files touched | Sources / Verification | Irregularities |
|---|------|--------|---------------|---------------|------------------------|----------------|
| 1 | Create COORDINATION.md task board | done | session-arena-e1428a33 | COORDINATION.md | — | — |
| 2 | Scaffold repo (README, site structure, GitHub Pages config) | done | session-arena-e1428a33 | index.html, restaurants.html, hotels.html, clusters.html, pages/*.html, css/style.css, js/app.js, js/hotels.js | All 13 page/asset URLs return HTTP 200 via local python3 http.server | README.md still 10-byte placeholder; no _config.yml/Jekyll (static HTML) |
| 3 | Research Michelin Guide SF Bay Area starred restaurants (official michelin guide, 2026 selection) | done | session-arena-e1428a33 | js/data.js | guide.michelin.com 2026 ceremony article (June 24 2026); ~24 individual Michelin restaurant pages | IRREGULARITY: initial "kiln" fetch returned LONDON Kiln; corrected to SF Kiln at guide.michelin.com/.../san-francisco/restaurant/kiln-1210355. The Kitchen Sacramento page returned incomplete content — excluded. |
| 4 | Research Michelin Bib Gourmand restaurants (2026 selection) | done | session-arena-e1428a33 | js/data.js | OpenTable blog (full CA Bib Gourmand list, June 25 2026); Michelin official product page with addresses; tastypals.com SF city-and-surroundings (30 Bib Gourmands) | 30 Bay Area Bib Gourmand entries added. Addresses from Michelin product page verified; blank addresses = unverified (left blank per no-hallucination rule). Cuisine, hours, phone, website, social left blank/unverified. |
| 5 | Research hotel clusters near Michelin restaurants & rank hotels | done | session-arena-e1428a33 | js/hotels.js | SF Travel Michelin Key hotels; Sonoma Mag Michelin Key winners; individual MICHELIN Guide hotel pages | 15 hotels ranked by Michelin cluster density with MICHELIN Keys and sources |
| 6 | Gather pricing, hours, days open, social links (YT/TT/IG) per entry | in progress | session-arena-e1428a33 | js/data.js | Michelin pages (price symbol only, no $ amounts); individual restaurant pages (partial hours) | Pricing = estimate from $$–$$$$ symbol labelled "(est.)". Hours partial/truncated on Michelin pages. Social links (YT/TT/IG) all blank — not on Michelin pages, need official restaurant sites. |
| 7 | Build mobile-friendly dashboard site (tables + analysis) | done | session-arena-e1428a33 | *.html, css/, js/ | — | All pages mobile-friendly, dark theme, responsive tables |
| 8 | Executive summary, suggestions section, open questions | done | session-arena-e1428a33 | pages/summary.html, pages/suggestions.html, pages/questions.html | — | Summary stat updated: 9 regions (was 7) |
| 9 | Line-by-line verification against official sources; flag unverified blanks | done | session-arena-e1428a33 | js/data.js | guide.michelin.com (starred list + individual pages) | All 39 starred entries verified against official Michelin pages. Bib Gourmand names+status verified; addresses/other fields blank where unconfirmed. verified:true = name+status confirmed from official source. |
| 10 | Integration: merge branches, rebuild, check broken links, publish to GitHub Pages | unclaimed | — | all | — | Pending integration session |

## Log
- 2026-11-24: Session `session-arena-e1428a33` created branch from `main` @ `1554148e`. Repo contained only README.md (10 bytes). COORDINATION.md created.
- 2026-11-24: Built full dashboard site (index, restaurants, hotels, clusters, summary, suggestions, questions). 39 starred restaurants verified (7★★★, 8★★, 24★). All pages HTTP 200 locally. Committed dfa7e69.
- 2026-11-24: Added 30 verified Bay Area Bib Gourmand entries to js/data.js (names+status from official Michelin/OpenTable sources; addresses blank where unverified). Updated index.html dashboard (added Bib Gourmand stat). Fixed summary.html region count (7→9). Total dataset: 69 entries.
