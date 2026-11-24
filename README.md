# Bay Michelin

A mobile-friendly, source-led planning dashboard for current MICHELIN-starred restaurants in the San Francisco Bay Area and adjacent North Bay wine country.

## Run locally

Because the dashboard loads JSON with `fetch`, serve this directory over HTTP (opening `index.html` directly as a `file://` URL will not work):

```sh
python3 -m http.server 8000
```

Then open `http://localhost:8000`.

## Current scope and verification

- Restaurant stars reflect the MICHELIN Guide’s **2026 California** selection, announced June 24, 2026. The official 2026 star-list source and individual MICHELIN profile are linked from every restaurant row. The table contains current starred restaurants only; being listed in the Guide without a Star is a separate status and is not represented as a star here.
- The official California-wide release reports 10 three-star, 13 two-star and 60 one-star restaurants. This working geography subset contains 7 three-star, 7 two-star and 27 one-star rows (41 total); these counts are checked by the local validator.
- The 41-entry roster covers current starred restaurants in San Francisco, Oakland, the Peninsula, Marin and North Bay / wine country. This is not a complete list of all MICHELIN Selected or Bib Gourmand establishments.
- Venue pricing, opening hours and social links are blank/marked unverified unless an official source was checked. Hotel rates require stay dates and are not asserted here.
- Hotel cards are a shortlist of MICHELIN Guide hotels with Keys, not a dining-density ranking. The site explicitly withholds a rank until geographic boundary, travel radius, travel mode and complete restaurant dataset are set.
- See the dedicated Open Questions, Suggestions and Flagged for Review sections before relying on the information for trip booking.

## Files

- `index.html` — single-page dashboard and category sections
- `styles.css` — responsive layout
- `app.js` — data filtering, cluster counts and rendering
- `data/restaurants.json`, `data/hotels.json` — structured records
- `COORDINATION.md` — shared work and verification log

## Local data check

Run `node scripts/validate-data.js` to check JSON structure, uniqueness, the 2026 local star-count snapshot, and required official MICHELIN source URLs. This static check is not a substitute for reopening the cited official pages; the source record and known gaps are in `COORDINATION.md` and the site’s Method & Sources / Flagged for Review sections.

## Deployment

GitHub Pages is enabled from the `main` branch root. The site is published at [`https://kanlerxz87-cyber.github.io/Baymich2/`](https://kanlerxz87-cyber.github.io/Baymich2/). The existing Pages deployment is branch-based; no additional deployment workflow is required.
