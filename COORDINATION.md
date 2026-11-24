# Shared task board

Session ID: `arena/0d35b38f-baymich2` (current Arena branch; work remains on the branch assigned by Arena).

| Task | Status | Owner | File scope |
|---|---|---|---|
| Site foundation, source-verification workflow, and initial research dataset | done | `arena/0d35b38f-baymich2` | `COORDINATION.md`, `README.md`, `index.html`, `styles.css`, `app.js`, `data/` |
| Final integration, full row-by-row source verification, and GitHub Pages publication | needs review | `arena/0d35b38f-baymich2` | shared site/data outputs |
| Restaurant profile verification pass 1 (address, phone, venue website, hours from official MICHELIN profiles) | in progress | `arena/e3632548-baymich2` (session e3632548) | `data/restaurants.json`, `app.js` (address line only), `COORDINATION.md` |

## Log

- 2026-11-24 — Claimed site foundation and research scope. Repo initially contained only the initial README; no coordination board or other claims were present. Work stayed on the active Arena branch.
- 2026-11-24 — Built mobile-responsive dashboard, search/filterable restaurant index, city-level cluster summary, hotel shortlist, decision questions, suggestions, and a flagged-review register. The dashboard's row-level restaurant links point to the official MICHELIN restaurant profile pages; each row's 2026 star distinction was cross-checked against MICHELIN's official 2026 California starred list.
- 2026-11-24 — Checked the official MICHELIN Guide's 2026 selection article (published June 24, 2026) in full, including all star tiers and restaurant names/cities. It yielded 41 local/adjacent-region starred entries (7 three-star, 7 two-star, 27 one-star) for the stated working boundary. Checked representative individual profile pages for Acquerello, Commis, Enclos, Wolfsbane, hotel profiles for SingleThread Inn and Rosewood Sand Hill, and Acquerello's official menu/surcharge page. Source links are in the data and site.
- 2026-11-24 — Validation passed: JSON parsed; 41 unique restaurant records and 4 hotel records; 7/7/27 star counts; every restaurant has an official MICHELIN profile URL; every hotel has an official MICHELIN profile URL; `node --check app.js` passed; local HTTP smoke test returned 200 for the index, CSS, JS, and both JSON files.
- 2026-11-24 — PR #3 merged to `main` (merge commit `65175a55f10ab8fde38242c9f0e96da07425c892`). GitHub Pages build/deploy run `45360018248` succeeded; public page verified with the live 41-row restaurant index at https://kanlerxz87-cyber.github.io/Baymich2/.

- 2026-11-24 — Session e3632548 (branch `arena/e3632548-baymich2`) claimed restaurant profile verification pass 1. Repo review: branch matched `main` at c7849d2 (PR #4) and the working tree was clean. Protocol note: this board prescribes `session-<id>/<task>` branches, but Arena assigns one branch per session, so this session works on its assigned branch only and touches only the files in its claimed scope.
- 2026-11-24 — Read 9 official MICHELIN profile pages in full (Atelier Crenn, Benu, Californios, Quince, SingleThread, The French Laundry, Birdsong, Kiln, Lazy Bear). Added address, phone, official venue website and hours for the 6 whose hours were visible in the profile. Hours were not in the captured part of the profile for SingleThread, The French Laundry and Kiln, so they remain blank.

## Irregularities flagged for review (session e3632548)

- Repo log says PR #3 merged at 65175a5 and the Pages build ran at 45360018248. These hashes are not in the current branch history, which shows only the PR #4 merge (c7849d2); confirm on GitHub before relying on either.
- The Michelin article states 83 starred restaurants statewide for 2026. The dataset holds 41 Bay Area and adjacent entries, a boundary set by the previous session rather than by Michelin.
- Michelin's profile URLs are in `/ca/en/` and `/us/en/` forms. Both load the same profile; the us/en URL is used for Atelier Crenn, which redirected.
- Acquerello's $731.60 figure reconciles to 2 × $295 × 1.24 (20% service plus 4% surcharge on the menu base). Tax and beverages excluded.
- Many hours, prices, social links and all activities remain unverified (see the Flagged for Review page).

## Source record, verification and irregularities

- 2026 MICHELIN California star list: https://guide.michelin.com/en/article/michelin-guide-ceremony/guide-michelin-california — verified against the full official list; row-level links to each official MICHELIN Guide restaurant profile are stored in `data/restaurants.json`.
- Official MICHELIN 2026 California overview: https://www.michelin.com/en/publications/products-and-services/the-michelin-guide-california-2026
- Acquerello menu price and mandatory additions: https://www.acquerellosf.com/seasonal-tasting-menu — verified $295/person, 20% service charge, 4% benefits surcharge. Current two-person figure is $731.60 before tax and drinks; taxes have not been asserted.
- Official MICHELIN Key hotel profiles: SingleThread Inn https://guide.michelin.com/en/hotels-stays/napa-sonoma-valleys/singlethread-inn-13698 ; Auberge du Soleil https://guide.michelin.com/en/hotels-stays/napa-sonoma-valleys/auberge-du-soleil-auberge-collection-7246 ; Meadowood Napa Valley https://guide.michelin.com/en/hotels-stays/napa-sonoma-valleys/meadowood-napa-valley-8121 ; Rosewood Sand Hill https://guide.michelin.com/en/hotels-stays/silicon-valley/rosewood-sand-hill-11406.
- Deliberate blanks/flags: all but one restaurant's total for two; most restaurant hours and exception schedules; verified social/video profiles; full MICHELIN Selected and Bib Gourmand roster; activity listings; verified coordinates; hotel rates; and hotel dining-density ranking. These fields remain explicitly unverified or unranked. No hotel rank is presented because travel radius/mode and comprehensive geocoded restaurant data are missing.
- Publication: GitHub Pages is live from the repository's `main` branch at `/` (public URL: https://kanlerxz87-cyber.github.io/Baymich2/). The existing branch-based Pages configuration was retained. An optional attempt to switch the repo to Actions-based deployment was rejected by GitHub permissions (HTTP 403); it was unnecessary because the existing Pages build succeeded.
- Review status remains open for the explicitly flagged research gaps above (full Selected/Bib roster, social links, prices/hours, activities, map coordinates, hotel rates and density-ranking inputs).
