# Shared task board – Baymich2

Session ID: `arena-6a60274e` (branch `arena/6a60274e-baymich2`, base `1554148`).
Note: the session rules require all work on this single branch. The `session-<id>/<task>` branch scheme from the brief is therefore not used. Scopes below are kept non-overlapping by file instead (see Flagged F8).

Statuses: `unclaimed` · `in progress` · `done` · `needs review` (published on Flagged for Review, does not block).

| ID | Task | Status | Owner | Files in scope | Notes |
|---|---|---|---|---|---|
| T1 | Repo review + irregularities | done | arena-6a60274e | README.md, COORDINATION.md | Flagged F7, F8 |
| T2 | Bay Area Michelin starred list (status) | needs review | arena-6a60274e | docs/data/data.js (starred rows) | Status for 41 rows from official article. Selby's city conflict (F1) |
| T3 | Starred restaurant details (3★/2★ Bay Area) | needs review | arena-6a60274e | docs/data/data.js | 11 rows detailed. Hours partial for 4 (F4). Costs blank (F5) |
| T4 | Starred restaurant details (1★ Bay Area + wine country) | unclaimed | – | docs/data/data.js | Only status + Michelin URL present. Needs address, hours, price tier, website |
| T5 | Couple cost for 2 adults (exact, from official menu/booking pages) | unclaimed | – | docs/data/data.js (coupleCost) | Blank for all rows. Use exact prices only |
| T6 | Social links (YouTube / TikTok / IG) | unclaimed | – | docs/data/data.js (social) | Blank for all rows. Prefer the restaurant's own site links |
| T7 | Bib Gourmand + Recommended (Bay Area) | unclaimed | – | new data file (to add) | Official list not yet pulled |
| T8 | Hotels ranking by nearby Michelin restaurants | unclaimed | – | docs/hotels.html, new data file | Needs scope/radius decision (Questions) |
| T9 | Site (GitHub Pages) | done | arena-6a60274e | docs/** | Built, renders, pending publish step |
| T10 | Integration: merge, re-verify line by line, publish | unclaimed | – | docs/** (all) | Final step after T4–T8 |

## Log

### 2026-11-24 · arena-6a60274e
- Claimed and completed T1, T2, T3, T9 in one session. Claims are recorded here after the work was done, because the board did not exist before this session.
- Sources used (official unless marked):
  - Michelin Guide California 2026 official article (24 Jun 2026): https://guide.michelin.com/us/en/article/michelin-guide-ceremony/guide-michelin-california
  - Michelin SF listing: https://guide.michelin.com/us/en/california/san-francisco/restaurants
  - Michelin restaurant pages (one per detailed row), e.g. https://guide.michelin.com/us/en/california/san-francisco/restaurant/atelier-crenn
  - Eater SF (secondary, cross-check only): https://sf.eater.com/restaurant-news/212958/2026-michelin-star-winners-california-guide-san-francisco-bay-area
- Verification performed:
  - Full official article list read (3★ 10 · 2★ 13 · 1★ 60 = 83, matching the article's stated total of 83).
  - 11 Bay Area 3★/2★ Michelin pages read for address, cuisine, price tier, phone, website, hours.
  - Eater list used only for conflict checks.
- Irregularities: see Flagged for Review (F1–F9).
- Not done: T4–T8. Reason: each needs one official page per row, which is large. Left as unclaimed for the next session or the integration step.

## Handoff rules
- Pull and rebase before every push: `git pull --rebase origin arena/6a60274e-baymich2`.
- If a conflict happens, stop and log it here. Do not discard the other session's changes.
- A claim older than 60 minutes with no commits can be taken over (note the handoff here).

### 2026-11-24 · arena-6a60274e · publish
- GitHub Pages already exists for this repo, serving `main` at `/` (https://kanlerxz87-cyber.github.io/Baymich2/). The session token cannot change Pages settings (HTTP 403), so the dashboard is not live yet.
- Opened PR #1 (`arena/6a60274e-baymich2` → `main`): https://github.com/kanlerxz87-cyber/Baymich2/pull/1
- To publish: merge PR #1, then set Pages source to `main` / `/docs`. This is the T10 integration step.
