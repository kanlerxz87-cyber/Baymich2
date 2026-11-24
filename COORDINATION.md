# Coordination board

Session ID: `ee58963c` (Arena branch `arena/ee58963c-baymich2`). At task start, the repository contained only a one-line README and no board, source code, or competing claims. The current Arena branch is the only branch used for this session.

| Task | Status | Owner | File scope |
|---|---|---|---|
| Initial source-grounded site, research log, and project structure | needs review | ee58963c | `COORDINATION.md`, `README.md`, `index.html`, `restaurants.html`, `hotels.html`, `activities.html`, `decisions.html`, `review.html`, `sources.html`, `assets/**`, `data/**`, `docs/**`, `scripts/**`, `.github/workflows/**` |

## Claim log
- 2026-11-24 — Claimed after checking the board (which did not exist) and confirming the repository contained only README. The claim commit was pushed to `arena/ee58963c-baymich2`. An initial pull attempt failed because that remote branch did not yet exist; rebasing on `origin/main` succeeded and the current branch was pushed. No other session claim was present.

## Completion, sources, and verification
- 2026-11-24 — Added a static, responsive, source-linked dashboard with an overview, restaurant directory, hotel cluster shortlist, activities, decision questions/suggestions, review register, and source register.
- Star source: official MICHELIN Guide California 2026 full Star list, announced June 24, 2026: https://guide.michelin.com/us/en/article/michelin-guide-ceremony/guide-michelin-california
- Local restaurant source: official MICHELIN Guide San Francisco & surroundings starred directory and each individual profile: https://guide.michelin.com/us/en/california/san-francisco/restaurants/all-starred
- Bib example sources: official individual profiles (e.g. A16 https://guide.michelin.com/us/en/california/san-francisco/restaurant/a16; Outerlands https://guide.michelin.com/us/en/california/san-francisco/restaurant/outerlands; MAMA Oakland https://guide.michelin.com/us/en/california/oakland/restaurant/mama-oakland). The eight examples are explicitly not represented as exhaustive.
- Hotel examples and related nearby-restaurant extracts: official MICHELIN profiles for SingleThread Inn https://guide.michelin.com/us/en/hotels-stays/napa-sonoma-valleys/singlethread-inn-13698, Hotel Healdsburg https://guide.michelin.com/us/en/hotels-stays/napa-sonoma-valleys/hotel-healdsburg-45, Auberge du Soleil https://guide.michelin.com/us/en/hotels-stays/napa-sonoma-valleys/auberge-du-soleil-auberge-collection-7246, The Battery https://guide.michelin.com/us/en/hotels-stays/san-francisco-bay-area/the-battery-san-francisco-8661, and San Francisco Proper Hotel https://guide.michelin.com/us/en/hotels-stays/san-francisco-bay-area/san-francisco-proper-hotel-8978. Ranking counts only the starred names shown in those profiles; it is not a radius/distance ranking.
- Official restaurant pricing source checked: Benu information page https://www.benusf.com/info states $425/person plus a 22% service charge and dinner Wednesday–Saturday. The site reports $1,037 as the mathematically derived two-person menu-plus-mandatory-service subtotal; it explicitly excludes sales tax and beverages and is not labeled an all-in check.
- Activity sources checked: SFMOMA https://www.sfmoma.org/visit/ ; National Park Service Alcatraz hours https://www.nps.gov/alca/planyourvisit/hours.htm ; Gardens of Golden Gate Park hours/admissions and official Instagram links https://gggp.org/visit/admissions-hours/ .
- Verification performed: official page fetches for the 2026 Michelin annual article (all list chunks), San Francisco directory and profiles, selected hotel pages, Benu official pricing, current SFMOMA hours/ticket price, NPS Alcatraz hours, and Gardens hours/socials. Local automated checks passed via `python3 scripts/validate_data.py`; JSON parsed with `python3 -m json.tool`; local HTTP smoke checks returned 200 for the landing page, data JSON, app script, and hotel page.
- Dataset verification asserts 41 current 2026 Starred entries in the stated nine-county Bay Area footprint (7 three-star, 7 two-star, 27 one-star), plus 8 Bib Gourmand examples. Every restaurant, hotel, activity, and source record contains an HTTPS source URL.

## Flagged review items (published on `review.html`)
- Full all-in restaurant totals for two adults are not confirmed; Benu's published figure is only a pre-tax, no-beverage subtotal. Other total fields remain blank.
- Current days/hours/holiday exceptions and restaurant social links were not individually verified for most restaurant rows; blank fields are intentional. No social handles were guessed.
- Five hotel candidate rate fields are blank because no stay dates/occupancy were supplied. Hotel counts are MICHELIN “nearby restaurants” list matches, not a complete catchment. No trip-time or distance claims are made.
- The 8 Bib Gourmand listings are a transparent sample, not a comprehensive transcription; non-star Recommended/Selected and Green Star inventories are not yet complete.
- Venue hours, menus, prices, reservation availability, accessibility, temporary closure, dietary, hotel rate, and commute facts are volatile or trip-specific and should be checked directly before a booking.

Status is `needs review` because the above material fields and coverage gaps are explicitly published in the Flagged for Review page. No value has been called verified unless checked against its linked official source.
