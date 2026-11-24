# Shared task board

Session ID: `arena/0d35b38f-baymich2` (current Arena branch; work remains on the branch assigned by Arena).

| Task | Status | Owner | File scope |
|---|---|---|---|
| Site foundation, source-verification workflow, and initial research dataset | done | `arena/0d35b38f-baymich2` | `COORDINATION.md`, `README.md`, `index.html`, `styles.css`, `app.js`, `data/` |
| Final integration, full row-by-row source verification, and GitHub Pages publication | needs review | `arena/0d35b38f-baymich2` | `.github/workflows/pages.yml`, shared site/data outputs |

## Log

- 2026-11-24 — Claimed site foundation and research scope. Repo initially contained only the initial README; no coordination board or other claims were present. Work stayed on the active Arena branch.
- 2026-11-24 — Built mobile-responsive dashboard, search/filterable restaurant index, city-level cluster summary, hotel shortlist, decision questions, suggestions, and a flagged-review register. Added a GitHub Pages Actions workflow. The dashboard's row-level restaurant links point to the official MICHELIN restaurant profile pages; each row's 2026 star distinction was cross-checked against MICHELIN's official 2026 California starred list.
- 2026-11-24 — Checked the official MICHELIN Guide's 2026 selection article (published June 24, 2026) in full, including all star tiers and restaurant names/cities. It yielded 41 local/adjacent-region starred entries (7 three-star, 7 two-star, 27 one-star) for the stated working boundary. Checked representative individual profile pages for Acquerello, Commis, Enclos, Wolfsbane, hotel profiles for SingleThread Inn and Rosewood Sand Hill, and Acquerello's official menu/surcharge page. Source links are in the data and site.
- 2026-11-24 — Validation passed: JSON parsed; 41 unique restaurant records and 4 hotel records; 7/7/27 star counts; every restaurant has an official MICHELIN profile URL; every hotel has an official MICHELIN profile URL; `node --check app.js` passed; local HTTP server started on port 4173.

## Source record, verification and irregularities

- 2026 MICHELIN California star list: https://guide.michelin.com/en/article/michelin-guide-ceremony/guide-michelin-california — verified against the full official list; row-level links to each official MICHELIN Guide restaurant profile are stored in `data/restaurants.json`.
- Official MICHELIN 2026 California overview: https://www.michelin.com/en/publications/products-and-services/the-michelin-guide-california-2026
- Acquerello menu price and mandatory additions: https://www.acquerellosf.com/seasonal-tasting-menu — verified $295/person, 20% service charge, 4% benefits surcharge. Current two-person figure is $731.60 before tax and drinks; taxes have not been asserted.
- Official MICHELIN Key hotel profiles: SingleThread Inn https://guide.michelin.com/en/hotels-stays/napa-sonoma-valleys/singlethread-inn-13698 ; Auberge du Soleil https://guide.michelin.com/en/hotels-stays/napa-sonoma-valleys/auberge-du-soleil-auberge-collection-7246 ; Meadowood Napa Valley https://guide.michelin.com/en/hotels-stays/napa-sonoma-valleys/meadowood-napa-valley-8121 ; Rosewood Sand Hill https://guide.michelin.com/en/hotels-stays/silicon-valley/rosewood-sand-hill-11406.
- Deliberate blanks/flags: all but one restaurant's total for two; most restaurant hours and exception schedules; verified social/video profiles; full MICHELIN Selected and Bib Gourmand roster; activity listings; verified coordinates; hotel rates; and hotel dining-density ranking. These fields remain explicitly unverified or unranked. No hotel rank is presented because travel radius/mode and comprehensive geocoded restaurant data are missing.
- Publication irregularity: the GitHub Pages workflow is prepared, but this branch's successful build does not itself prove Pages is enabled or live. Confirm the Pages configuration/deployment after branch integration. See the site's Flagged for Review section.
