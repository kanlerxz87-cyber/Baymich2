# Repo review — kanlerxz87-cyber/Baymich2

Reviewed: 2026-11-24 · Branch: `arena/ea4cb30e-baymich2` · Base: `main` @ `1554148`

## What is in the repo (checked with git)

| Item | Finding | How checked |
|---|---|---|
| Commits | 1 (`Initial commit`, 1554148) before this session | `git log` |
| Tracked files | `README.md` only (contents: `# Baymich2`) | `git ls-files`, `cat README.md` |
| License | None | no LICENSE file |
| .gitignore | None | no file |
| CI / tests | None | no workflow directory |
| GitHub Pages | Not configured before this session | repo has no `docs/` or `gh-pages` |
| Remote | `origin` = https://github.com/kanlerxz87-cyber/Baymich2.git | `git remote -v` |
| Other branches | `main` only (plus this session's branch) | `git branch -a` |

## Irregularities (also on the site's Flagged page)

1. **Almost empty repo.** Only a title line. There is no data, code or docs until this session.
2. **Branch naming.** The brief asks for `session-<id>/<task>` branches. This session is fixed to `arena/ea4cb30e-baymich2`, so that name was used.
3. **Escaped text in the brief.** Parts of the brief appear as HTML entities (`&amp;amp;lt;id&amp;amp;gt;`). Read as `session-<id>/<task>`.
4. **No COORDINATION.md existed.** Created at the root and claimed T1–T5 on this branch.
5. **No license.** Public content is copyright by default. Ask before reuse beyond this repo.

## Source irregularities found while building the data

- Official Michelin press release spells Troubadour's city as "Headlsburg". Recorded as Healdsburg. Source: https://www.michelin.com/en/publications/products-and-services/the-michelin-guide-california-2026
- Selby's city conflicts in press: SF Chronicle says Redwood City, Press Democrat says Atherton. Open. Sources: https://www.sfchronicle.com/food/restaurants/article/2026-michelin-stars-of-bay-area-22317064.php and https://www.pressdemocrat.com/2026/06/24/michelin-stars-2026-which-california-restaurants-won-which-lost/
- Michelin's "San Francisco and surroundings" listing includes Oakland, San Anselmo and San Mateo, but not Napa, Sonoma or most of the Peninsula/South Bay. Scope must be chosen. Source: https://guide.michelin.com/us/en/california/san-francisco/restaurants
- Four Bay Area stars reported lost (news only). Not in Michelin's press release. Flagged.

## Verification method used

- Star status and counts: official Michelin star-filtered listing pages (3-, 2- and 1-star) for San Francisco.
- Bib Gourmand list and special awards: official michelin.com California 2026 press release.
- Address, cuisine, price tier, website and hours: each restaurant's official Michelin page (`guide.michelin.com/.../restaurant/<slug>`).
- Not yet verified: dollar prices for two, social links, hotel counts. These are blank on the site and listed as questions and suggestions.

## Limits

This session cannot reach the restaurants' own sites or social platforms. Only the hosts listed for this sandbox are reachable, and the fetch tool was used for the Michelin and press pages.
