# Baymich2 — Michelin SF Bay Area Guide

Mobile-friendly GitHub Pages site of Michelin-rated restaurants in the San Francisco Bay Area, verified line-by-line against the official [MICHELIN Guide](https://guide.michelin.com/us/en/california/san-francisco/restaurants).

## What's included
- **index.html** — landing page with dashboard stats and category navigation
- **restaurants.html** — category tables (3★ / 2★ / 1★ / listed-no-star) with search + city filters
- **hotels.html** — hotels ranked by nearby Michelin stars (candidate set, unverified)
- **executive-summary.html** — key details at a glance
- **suggestions.html** — options to review before implementing
- **questions.html** — open questions, missing information, how to resolve
- **sources.html** — official source links and per-row verification trail
- **data/restaurants.json** — 29 starred restaurants (4×3★, 7×2★, 18×1★), fully sourced; plus 22 listed-no-star (page-1 subset) flagged unverified
- **data/hotels.json** — candidate hotel set ranked by nearby starred restaurants
- **assets/style.css, assets/app.js** — mobile-first styles + client-side table rendering

## Verification policy
- Every table row links to its official MICHELIN Guide detail page.
- Values not confirmed from an official source are left blank and flagged unverified. Nothing was inferred.
- MICHELIN does not publish dollar totals for 2 adults → blank/unverified.
- No official YouTube/TikTok links found → blank/unverified.

## Status
- Starred restaurants (29): complete and verified.
- Listed-only (116): page-1 subset (22) enumerated, unverified.
- Hotels: candidate set, unverified neighbourhood proxy.
- Site: static HTML, ready for GitHub Pages.

## Publish
Enable GitHub Pages in repo settings (source: `gh-pages` branch or `main`/`docs`, depending on setup). This branch is `arena/3a52860e-baymich2`.
