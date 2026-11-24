# SF Bay Area Michelin Guide

An evidence-first, mobile-friendly planning dashboard for Michelin Guide dining, hotel clusters, activities, and open decision questions in the San Francisco Bay Area.

## Browse

- `index.html` — executive summary and restaurant clusters
- `restaurants.html` — 2026 Starred restaurants plus a separate, non-exhaustive Bib Gourmand sample
- `hotels.html` — a constrained hotel shortlist and its provisional ranking method
- `activities.html` — activity hours, exceptions, verified links, and two-person price where officially posted
- `decisions.html` — assumptions, questions, known answers, and improvement suggestions
- `review.html` — incomplete and unverified fields
- `sources.html` — source register and verification method

## Run locally

The site is static and dependency-free. From the repository root, run:

```sh
python3 -m http.server 8000 --bind 0.0.0.0
```

Then open `http://localhost:8000`. GitHub Pages deployment is configured in `.github/workflows/pages.yml`.

## Data policy

The 2026 MICHELIN Guide California annual list (revealed June 24, 2026) is the master source for current Star levels. The working geography is a nine-county Bay Area planning boundary. The current data records 41 Starred entries in that boundary, based on the official annual list. Eight Bib Gourmand examples are shown separately and are **not** an exhaustive list of non-star Guide selections. Empty price, hours, and social fields mean “not confirmed from an official source,” not free/closed/nonexistent. No distances, travel times, hotel rates, or all-in restaurant checks are invented.

Hotel ordering is a provisional evidence proxy: it counts the Starred venues named in each selected MICHELIN hotel profile's “Restaurants near the hotel” list. It is not a uniform radius or true density ranking. See `review.html` and `decisions.html` before relying on it.

Source notes and verification limitations are recorded in [COORDINATION.md](COORDINATION.md) and `data/sources.json`.
