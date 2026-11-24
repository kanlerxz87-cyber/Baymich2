# San Francisco Bay Area Michelin guide — research and decision plan

**Evidence status:** planning document only. No restaurant, hotel, price, schedule, award status, social account, or activity has been confirmed yet. Keep the published dataset empty until the checks below are completed from first-party sources. Never convert search snippets, third-party listings, memory, or geographic assumptions into verified facts.

## Executive summary

The repository started as a 10-byte README with no app, source list, dataset, or deployment configuration. The requested deliverable is a mobile-first, map-oriented decision guide that distinguishes restaurants currently holding Michelin stars from restaurants merely included in the Michelin Guide; identifies restaurant clusters; compares hotels by verified proximity/coverage; and shows current schedules, social/video links, direct booking/menu links, and transparent total-cost estimates for two adults.

The core decision risk is freshness and comparability: Michelin distinctions and restaurant schedules change, hotel locations alone do not establish how many venues are practically accessible, and a restaurant's menu price is not a two-person bill. Each row needs direct evidence and an as-of date. At present those facts are **unknown**, not zero. No recommendation/ranking should be published until the coverage radius, dates, transport mode, budget, and what counts as a meal total are decided or explicitly set as disclosed defaults.

## Required content model

For each restaurant, capture: venue name; address/city; Michelin Guide inclusion; current star count/status and Michelin page; official restaurant URL; first-party menu URL; official opening days/hours and exceptions; reservation URL; social/video URLs (only accounts linked by the venue or Michelin); meal price for two with currency, date, inclusions, and whether tax/tip/drinks are included; evidence URLs per field; last checked date; and review flags. Distinguish `Starred` (current one/two/three stars confirmed by Michelin), `Guide-listed, not starred` (Guide page with no current star designation), and `Unverified` (insufficient current official evidence). Never infer that lack of a star means not listed.

For hotels capture: official name/address; official lodging URL; nightly price and dates/occupancy/currency only when returned by the hotel's own booking channel; official amenities/transport details; geospatial coordinates only from an official hotel/map source; nearby in-scope Michelin restaurant count under a declared method; walk/transit distance and routing source; methodology timestamp; and every supporting link. A hotel ranking must not imply Michelin endorsement.

For activities capture: name, official operator URL, location, official hours/closures, official social/video links, and source timestamp. Avoid adding activities without verified first-party evidence.

## Ranking and mapping method (proposed; approval needed)

1. Define the Bay Area boundary (suggested: counties explicitly listed in the application; do not silently equate the region with a radius).
2. Assign clusters from verified coordinates and a declared rule (for example, connected groups within a chosen straight-line threshold); display the threshold and allow list/map views.
3. Count only restaurants whose Michelin status has a current Michelin Guide page; separately display the star-bearing subset. Do not use the count as a quality score.
4. Rank hotels only after selecting a travel date, party size, currency, transport mode, and access measure. Prefer transparent multi-factor output: number of verified Guide restaurants within chosen walk/transit time, starred subset, distance to nearest restaurant, and verifiable hotel total price. Show components rather than opaque composite scores.
5. If a composite score is later chosen, publish its weights, normalization, missing-data treatment, and sensitivity analysis. Keep hotels with missing booking prices visibly unpriced; do not rank by fabricated rates.

## Restaurant cost rule

Show a two-adult total (USD) only where an official menu or official reservation/checkout price supports the calculation. Record itemized arithmetic and assumptions. A tasting menu total may be `2 × published per-person menu price`; do not label it an all-in total unless official source confirms fees/tax. For à la carte, give an explicit order basket or a clearly labeled range derived from official menu prices. If drinks, tax, service charge, tip, or mandatory fees are not verifiable, state exclusions in the cell. Otherwise leave the value blank and flag `Cost unverified`—do not estimate from third parties.

## Official-source hierarchy and verification

- Michelin Guide official venue pages are authoritative for Guide inclusion and Michelin distinction; record the current designation and check date.
- Restaurant-owned/operated official websites are authoritative for address, menu, reservations, hours, closures, and linked social accounts. For a specific exception, use the restaurant's own dated notice.
- Hotel-owned official pages/booking engines are authoritative for hotel details and live rates. Rates require dates, occupancy, room type, taxes/fees treatment, and currency.
- Activity operator's own site is authoritative for schedules and access details.
- Official YouTube/Instagram/TikTok profile links are acceptable only when linked from an official venue/operator site or explicitly confirmed as its official account. User-generated clips can be optional inspiration, never evidence for factual values.
- Map routing and coordinates require a named mapping source; if a value has no first-party confirmation, label it unverified rather than imply official validation.

Every table row must carry a source link, and ideally every changeable field its own source. Use citation labels that say what the link supports. Save a check date and re-check volatile data before publication. A link working is not by itself proof that the claim is true.

## Questions that block a defensible recommendation

| Question | What is currently known | Missing information / decision needed | Safe handling until answered |
|---|---|---|---|
| What does “Bay Area” include? | User requests San Francisco Bay Area. | Counties, edge cities, and whether wine-country destinations are in scope. | State scope explicitly; do not silently expand. |
| What dates are relevant? | None supplied. | Visit dates, weekday/weekend, season. | Hours and hotel rates are date-sensitive; leave rates blank. |
| How many travelers and rooms? | Restaurant comparison asks for two adults. | Hotel guest/room count and length of stay. | Do not compare nightly hotel totals. |
| What price means “total” for dining? | Two adults requested. | Drinks, tax, service, tip, supplements, and dietary preferences. | Show sourced subtotal and exclusions; leave unknown components explicit. |
| Which Michelin status year? | Current status requested. | Preferred guide edition/as-of convention. | Check the current Michelin page and date it; do not rely on old awards. |
| How should hotels be ranked? | By amount of Michelin restaurants around them. | Radius vs walk/transit time, transport mode, count weighting, hotel budget. | Show counts and distances separately; no opaque rank. |
| Which activities qualify? | Activities requested alongside restaurants. | Interests, accessibility, family needs, indoor/outdoor. | Include only official, directly relevant Bay Area activities; mark scope. |
| What social links count? | YouTube/TikTok/Instagram requested. | Official venue account or any relevant creator coverage? | Prefer linked official profiles; separate clearly labeled creator content. |
| Accessibility and dietary constraints? | Not provided. | Mobility, allergies, dietary needs, language. | Do not make accessibility or suitability promises without official evidence. |
| What map base/routing is acceptable? | Map requested. | Provider/privacy preference and whether map tiles can load in Pages. | Use a documented provider and avoid sending personal data; provide table fallback. |
| How frequently should data refresh? | Not specified. | Update cadence and owner. | Display “last checked”; mark volatile facts for review. |

## Site improvements to consider (decision queue; not yet implemented)

| Suggestion | Decision value | Trade-off / question before choosing |
|---|---|---|
| Filters for current stars, Guide-listed, city, price evidence, and open day | Quickly narrows options | Need a stable city taxonomy and “open” date context. |
| Cluster map with list/table fallback | Reveals geographic concentration | Requires reliable coordinates, geocoding provenance, and map-provider choice. |
| Per-field citations and last-checked badges | Makes verification auditable | Adds visual density; use expandable evidence details on mobile. |
| Price calculator for two | Makes totals comparable | Need explicit basket and tax/tip policy; avoid misleading false precision. |
| Hotel comparison with walk/transit access | Supports lodging choice | Must choose dates, route mode, radius/time threshold, and price basis. |
| Saved itinerary/export | Helps plan a trip | Requires user-data storage/privacy decision; avoid account creation by default. |
| Data refresh checklist / stale-data alerts | Prevents outdated hours and award claims | Requires maintenance cadence and owner. |
| Accessibility and dietary fields | Supports real-world decisions | Publish only sourced, specific attributes; avoid broad guarantees. |
| Structured data validation and broken-link checks | Catches publishing defects | Automated checks cannot prove that source content remains accurate. |

## Irregularities / review flags

- Initial repository had no source data or site; every requested factual listing remains unverified.
- User requires official verification for every row while also requesting creator/social links. Unofficial creator material cannot substantiate restaurant facts; keep it separate from official social profiles.
- “Total price for two” is undefined for à la carte dining and may omit tax, tip, service charges, and drinks unless disclosed.
- Hotel prices cannot be comparable without dates, occupancy, room type, and taxes/fees rules.
- Michelin stars and restaurant hours are volatile; clearly date all checks and re-verify before trip use.

## Completion checklist

- [ ] Source inventory includes direct official links and as-of dates.
- [ ] Every published restaurant, hotel, and activity row has an official source link.
- [ ] Michelin category is checked on Michelin's own current page, not inferred.
- [ ] Hours and exceptions are checked against venue/operator official pages.
- [ ] Costs and hotel prices have reproducible calculations, dates, and exclusions; otherwise blank + flag.
- [ ] Social links are source-attributed and distinguished from third-party creator posts.
- [ ] Cluster and hotel ranking methods are explicit and reproducible.
- [ ] Mobile table usability, keyboard access, and list fallback are checked.
- [ ] Internal navigation and external links are validated; GitHub Pages build/deploy is tested.
- [ ] All unresolved claims appear on a “Flagged for review” page.
