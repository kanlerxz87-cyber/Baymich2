# COORDINATION — Shared Task Board

Created by session `arena-ffcabdcb` on 2026-11-24 (created because the repo had no board).

**Branch note:** This session is bound to branch `arena/ffcabdcb-baymich2` (base `1554148`). Per the session rules, all work stays on this branch. The `session-<id>/<task>` naming in the coordination brief is not used, because switching or creating branches is not allowed for this session. Scopes below are kept non-overlapping by file path instead.

Statuses: `unclaimed` · `in progress` · `done` · `needs review` (published on the Flagged for Review page, does not block others).

## Task board

| # | Task | Status | Owner (session) | Files in scope | Notes |
|---|------|--------|-----------------|----------------|-------|
| T1 | Repo review (README, git state, board setup) | in progress | arena-ffcabdcb | `COORDINATION.md`, `README.md` | Repo contained only `README.md` at base commit. Irregularities logged below. |
| T2 | Michelin Bay Area starred restaurants — data + verification | in progress | arena-ffcabdcb | `data/michelin_starred_bay_area.json`, `data/SOURCES.md` | Source: official Michelin 2026 California article and official Michelin restaurant pages. |
| T3 | Site build (GitHub Pages, `docs/`) | in progress | arena-ffcabdcb | `docs/**` | Static site. Pages: landing dashboard, Michelin, Flagged for Review, Suggestions & Questions. |
| T4 | Hotel ranking by nearby Michelin restaurants | unclaimed | — | `data/hotels*` | Blocked: needs verified hotel + coordinate source. See Questions page. |
| T5 | Social links (YouTube / TikTok / Instagram) | unclaimed | — | `data/social*` | Blocked: no verified official source yet. Left blank by policy. |
| T6 | Bib Gourmand / Recommended list (Bay Area) | unclaimed | — | `data/bib*` | Not yet pulled from official Michelin list. |
| T7 | Integration / final verification / publish | unclaimed | — | all shared outputs | Reserved for final integration session. |

## Log

### 2026-11-24 · arena-ffcabdcb
- Claimed T1, T2, T3. Reviewed repo: only `README.md` (1 line), single commit `1554148`, no board, no site.
- Irregularity (T2): Eater SF's Bay Area article lists **Selby's** under *Redwood City*. The official Michelin California 2026 article lists it under **Atherton**. The official source is used; the discrepancy is flagged. Source: https://guide.michelin.com/us/en/article/michelin-guide-ceremony/guide-michelin-california ; https://sf.eater.com/restaurant-news/212958/2026-michelin-star-winners-california-guide-san-francisco-bay-area
- Irregularity (T2): Eater's Bay Area article reports Le Comptoir at Bar Crenn, O' by Claude Le Tohic and Shota lost stars. These restaurants are not in the official 2026 starred list; they are not shown as starred and are flagged for confirmation on the official Michelin site.
- Scope decision (T2): "Bay Area" is defined as the nine ABAG counties (Alameda, Contra Costa, Marin, Napa, San Francisco, San Mateo, Santa Clara, Solano, Sonoma). This is an assumption — see the Questions page.
- Process note: `[COORDINATION.md]` links in the brief point to `http://COORDINATION.md`; the file lives at repo root as `COORDINATION.md`.
