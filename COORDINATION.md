# Shared task board

Session ID: `arena/0ee547c1-baymich2` (current Arena branch; work remains on the branch assigned by Arena).

| Task | Status | Owner | File scope |
|---|---|---|---|
| Site foundation, source-verification workflow, and initial research dataset | done | `arena/0ee547c1-baymich2` | `COORDINATION.md`, `README.md`, `index.html`, `styles.css`, `app.js`, `data/` |
| Final integration, full row-by-row source verification, and GitHub Pages publication | done | `arena/0ee547c1-baymich2` | shared site/data outputs |

## Log

- 2026-11-24 — Claimed site foundation and research scope. Repo initially contained only the initial README; no coordination board or other claims were present. Work stayed on the active Arena branch.
- 2026-11-24 — Built mobile-responsive dashboard, search/filterable restaurant index, city-level cluster summary, hotel shortlist, decision questions, suggestions, and a flagged-review register. The dashboard's row-level restaurant links point to the official MICHELIN restaurant profile pages; each row's 2026 star distinction was cross-checked against MICHELIN's official 2026 California starred list.
- 2026-11-24 — Checked the official MICHELIN Guide's 2026 selection article (published June 24, 2026) in full, including all star tiers and restaurant names/cities. It yielded 41 local/adjacent-region starred entries (7 three-star, 7 two-star, 27 one-star) for the stated working boundary.
- 2026-11-24 — **Final integration verification complete.** All 41 restaurant rows were verified row-by-row against their official MICHELIN Guide profile pages (`/ca/en/california/<city>/restaurant/<slug>`). Every profile resolves and confirms the star level, the `$$$$`/`$$$` price band, opening hours, and an official "Visit Website" link. All verified hours, price bands and venue URLs were written into `data/restaurants.json`.
- 2026-11-24 — **Hotel verification complete.** All four MICHELIN Key hotel profiles were verified against their official MICHELIN Guide hotel pages: SingleThread Inn (3 Keys), Auberge du Soleil (3 Keys), Meadowood Napa Valley (3 Keys), Rosewood Sand Hill (1 Key). Room counts and date-specific starting rates (22–23 Dec 2026 widget) were captured into `data/hotels.json`.
- 2026-11-24 — Validation passed: JSON parsed; 41 unique restaurant records and 4 hotel records; 7/7/27 star counts; all 41 restaurants carry official MICHELIN profile URLs, verified hours and verified official venue URLs; all 4 hotels carry official MICHELIN profile URLs; `node --check app.js` passed; local HTTP smoke test returned 200 for the index, CSS, JS, and both JSON files.
- 2026-11-24 — PR #3 merged to `main` (merge commit `65175a55f10ab8fde38242c9f0e96da07425c892`). GitHub Pages build/deploy run `45360018248` succeeded; public page verified with the live 41-row restaurant index at https://kanlerxz87-cyber.github.io/Baymich2/.

## Source record, verification and irregularities

- 2026 MICHELIN California star list: https://guide.michelin.com/en/article/michelin-guide-ceremony/guide-michelin-california — verified against the full official list; row-level links to each official MICHELIN Guide restaurant profile are stored in `data/restaurants.json`.
- Official MICHELIN 2026 California overview: https://www.michelin.com/en/publications/products-and-services/the-michelin-guide-california-2026
- **All 41 official MICHELIN restaurant profile pages** were fetched and verified (star level, price band, hours, "Visit Website" link). Verified profile URLs follow the stable pattern `https://guide.michelin.com/ca/en/california/<city>/restaurant/<slug>`. Mister Jiu's profile URL requires the percent-encoded apostrophe (`mister-jiu%E2%80%99s`); the plain `mister-jius` slug does not resolve.
- **All 4 official MICHELIN hotel profile pages** were fetched and verified (Key count, room count, rate widget). Verified hotel URLs follow `https://guide.michelin.com/ca/en/hotels-stays/<region>/<slug>-<id>`.
- Acquerello menu price and mandatory additions: https://www.acquerellosf.com/seasonal-tasting-menu — verified $295/person, 20% service charge, 4% benefits surcharge. Current two-person figure is $731.60 before tax and drinks; taxes have not been asserted.
- **Verified price bands:** `$$$$` applies to nearly all starred entries. Notable `$$$` exceptions among one-stars: Hilda and Jesse, Kin Khao, Mister Jiu's, State Bird Provisions, The Progress, The Village Pub.
- **Deliberate boundary-scope exclusions** (statewide 2026 list items outside the working Bay Area boundary, deliberately excluded and flagged for review): Carmel-by-the-Sea two-star Aubergine and one-star Chez Noir; Elk/Mendocino two-star Harbor House Inn; Sacramento one-star Localis and The Kitchen. These are recorded here so the exclusion is deliberate and auditable, not an omission.
- **Deliberate blanks/flags (remaining unverified):** all but one restaurant's total for two; most pair prices; holiday/temporary-closure exception schedules; verified social/video (YouTube/TikTok/Instagram) profiles; full MICHELIN Selected and Bib Gourmand roster; activity listings; verified coordinates; hotel dining-density ranking. These fields remain explicitly unverified or unranked. No hotel rank is presented because travel radius/mode and comprehensive geocoded restaurant data are missing.
- **Social-link note:** the social column stays blank/"Unverified" until a social profile is linked from an official venue source. Official restaurant homepages did not expose social handles in extracted content, so no social links were inferred or fabricated.
- Publication: GitHub Pages is live from the repository's `main` branch at `/` (public URL: https://kanlerxz87-cyber.github.io/Baymich2/). The existing branch-based Pages configuration was retained. An optional attempt to switch the repo to Actions-based deployment was rejected by GitHub permissions (HTTP 403); it was unnecessary because the existing Pages build succeeded.
- Review status is closed for the completed row-by-row verification. Open review items remaining are the explicitly flagged research gaps above (full Selected/Bib roster, social links, pair prices/exception schedules, activities, map coordinates, hotel density-ranking inputs).
