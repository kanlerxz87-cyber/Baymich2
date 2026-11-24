# COORDINATION — Shared Task Board

Repo: `kanlerxz87-cyber/Baymich2` · Live site (GitHub Pages, served from `main` `/`): https://kanlerxz87-cyber.github.io/Baymich2/

Status values: `unclaimed` · `in progress` · `done` · `needs review`
A `needs review` item is published on the **Flagged for Review** page and does not block anything.

Branch note: this session is pinned to branch `arena/5d054995-baymich2` (base `1554148e6cb3a83cac084a7dd38f863d3f3060e0`). The session-branch naming scheme (`session-<id>/<task>`) is not used here, because the session must stay on its single assigned branch. Scopes below are kept non-overlapping by file.

## Session log

| Session | Claimed | Tasks |
|---|---|---|
| `arena/5d054995-baymich2` | 2026-11-24 | All tasks below (single-session run; no other session is active on this branch) |

## Task board

| ID | Task | Status | Owner | Files in scope |
|---|---|---|---|---|
| T1 | Repo review + irregularities | needs review | arena/5d054995-baymich2 | `README.md`, `COORDINATION.md` (log section only) |
| T2 | Michelin restaurant data (SF Bay Area, stars vs. Bib/Selected) | needs review | arena/5d054995-baymich2 | `data/michelin_restaurants.csv` |
| T3 | Hotel ranking by nearby Michelin restaurants | needs review | arena/5d054995-baymich2 | `data/hotels.csv` |
| T4 | Social links (YouTube / TikTok / Instagram) + hours/pricing | needs review | arena/5d054995-baymich2 | `data/social_links.csv`, `data/pricing_hours.csv` |
| T5 | Analysis, executive summary, questions, suggestions | needs review | arena/5d054995-baymich2 | `docs/analysis/*.md` |
| T6 | Static site (landing + category subpages) | needs review | arena/5d054995-baymich2 | `docs/**` (site files only) |
| T7 | Integration: rebuild, link check, publish to Pages | unclaimed | — | `docs/**`, `COORDINATION.md` |

## Task log (sources, verification, irregularities)

_Each finished task records its sources, verification performed, and irregularities here._

### T1 — Repo review
- Sources: repo files and `gh api repos/kanlerxz87-cyber/Baymich2/pages` (legacy build, `main` `/`).
- Verified: one commit; only `README.md`; Pages on `main` `/`.
- Irregularities: F15 (no content), F14 (branch naming instruction vs. pinned branch), Pages publishes from `/` (suggestion S7).

### T2 — Michelin restaurants (`data/michelin_restaurants.csv`, 145 rows)
- Sources: Michelin listing pages 1–4 (`guide.michelin.com/us/en/california/san-francisco/restaurants[/page/N]`); detail pages for 11 starred restaurants and Village Sake.
- Verified: award counts 3★ 4, 2★ 7, 1★ 18, Bib 30, Selected 85, tier unverified 1 (= 145, header 145). Sidebar: Selected 86.
- Needs review: Village Sake (Bib inferred from Bibendum icon; F2), Kajiken (tier not shown; F3).
- Irregularities: city missing for 88 rows from listing pages 1–2 (F4); pagination ranges; two p2-file rows tagged page 3 (F12).
- Not captured: price for 2 adults (F5), hours for most rows (F7, F8), social links (F6).

### T3 — Hotels (`data/hotels.csv` not created)
- Sources: Michelin hotels page `hotels-stays/san-francisco-bay-area` chunk 0.
- Verified: 31 hotels listed; 3 Two Keys, 2 One Key, 26 Selected. Two hotel names read.
- Not done: addresses, distance method, ranking (F9, F10). Hotel pages 2–8 unread.

### T4 — Social links and hours/pricing (`data/social_links.csv`, `data/pricing_hours.csv` not created)
- Not done. Price for 2 adults and social links are unverified for all rows (F5, F6).

### T5 — Analysis (`docs/analysis/*.md` not created)
- Summary, open questions and suggestions live in `docs/summary.html` (built from the data). Nothing implemented; awaiting review.

### T6 — Site (`docs/**`)
- Built by `tools/build_site.py` from `data/` only. 7 pages: index, restaurants, clusters, hotels, summary, flagged, repo-review.
- Not live: Pages serves `main` `/`, so `docs/` is not published until the branch merges and Pages is set to `/docs` (S7).

### T7 — Integration
- Unclaimed. Not started.

## Flagged for Review

- T1 F14, F15 (instructions conflict; repo has no content)
- T2 F2 (Village Sake tier), F3 (Kajiken tier), F4 (city missing for 88 rows), F5–F8 (price, social, hours not captured)
- T3 F9, F10 (hotel ranking not done; guest score 18.6 looks off-scale)
- T2 F11, F12, F13 (scope, row tags, websites)

## Requests to other sessions

- **Merge conflict logged (2026-11-24, T7 owner to resolve).** `origin/main` moved to `c7849d2` after this branch was cut from `1554148`. Session `arena/0d35b38f-baymich2` merged a site to `main`: root `index.html`, `styles.css`, `data/restaurants.json`, `data/hotels.json`, and its own `COORDINATION.md`. Overlaps with this branch: `COORDINATION.md` (both edited) and `data/` (`michelin_restaurants.csv` here vs `restaurants.json` there). This branch has NOT been rebased or merged onto `main`. The live Pages site (`main` `/`) is the other session's site, not `docs/` from this branch.
- Request to T7 integration owner: choose one restaurant dataset and one `COORDINATION.md`, and decide whether `docs/` (this branch) or root `index.html` (`main`) becomes the Pages source. Compare row counts (this branch: 145) against the other session's `restaurants.json` before merging.
