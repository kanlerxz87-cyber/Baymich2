# Bay Michelin

A mobile-friendly, source-led planning dashboard for current MICHELIN-starred restaurants in the San Francisco Bay Area and adjacent North Bay wine country.

## Run locally

Because the dashboard loads JSON with `fetch`, serve this directory over HTTP (opening `index.html` directly as a `file://` URL will not work):

```sh
python3 -m http.server 8000
```

Then open `http://localhost:8000`.

## Current scope and verification

- Restaurant stars reflect the MICHELIN Guide’s **2026 California** selection, announced June 24, 2026. The source is linked in every restaurant row and in the Method & Sources section.
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

## Deployment

A GitHub Actions workflow publishes the static root to GitHub Pages on pushes to `main` and on manual dispatch. Repository Pages must be configured to use **GitHub Actions** as the build/deploy source. The workflow does not claim a site is live until a Pages deployment succeeds.
