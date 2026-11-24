# SF Bay Area MICHELIN Guide dashboard

A mobile-friendly, source-led dashboard for MICHELIN-starred and Bib Gourmand restaurants, MICHELIN Key hotels, and activities in the San Francisco Bay Area (with Napa/Sonoma rows kept separate; see Review).

Pages:

- `index.html` — overview, executive summary, region counts
- `restaurants.html` — starred and Bib Gourmand table with filters
- `hotels.html` — MICHELIN Key hotels; nearby-restaurant ranking withheld
- `activities.html` — NPS and other official activity pages
- `review.html` — flags, decisions needed, suggestions, sources, method

Data lives in `data/` as JSON (`restaurants.json`, `hotels.json`, `activities.json`, `flags.json`, `sources.json`). Every value has a source link; blanks mean no official value was found.

## Run locally

The pages load JSON with `fetch`, so serve the folder over HTTP (opening `index.html` as a `file://` URL will not work):

```sh
python3 -m http.server 8000
```

Then open http://localhost:8000/.

## Deployment

GitHub Pages serves the repository root from `main`: https://kanlerxz87-cyber.github.io/Baymich2/

## Notes

- Data was checked against official MICHELIN, NPS and venue pages on 24 Nov 2026. See `review.html` for the full list.
- Flags (F1–F17) and open questions are on `review.html`.
- Not affiliated with MICHELIN or the National Park Service.
