# Coordination Board — Baymich2 (SF Bay Area Michelin Guide & Map)

Branch: `arena/e1428a33-baymich2` (branched from `main` @ `1554148e`)
Session ID: `session-arena-e1428a33`
Base URL (live site): GitHub Pages — TBD (repo must be enabled for Pages)

## How to use this board
- Claim a task by writing your session ID + file scope in the "Owner / Scope" column, then commit and push immediately.
- Never start a task another session has claimed.
- Scopes must be non-overlapping; each session works on its own branch/worktree named `session-<id>/<task>`.
- If a task requires changing a file owned by another session, log the request here instead of editing it.
- Make small, frequent commits; run `git pull --rebase` before every push.
- When finished, record sources, verification performed, and irregularities, then mark the task "done".
- A claim older than 60 minutes with no commits may be taken over (note the handoff in the log).

## Tasks

| # | Task | Status | Owner / Scope | Files touched | Sources / Verification | Irregularities |
|---|------|--------|---------------|---------------|------------------------|----------------|
| 1 | Create COORDINATION.md task board | done | session-arena-e1428a33 | COORDINATION.md | — | — |
| 2 | Scaffold repo (README, site structure, GitHub Pages config) | in progress | session-arena-e1428a33 | README.md, index.html, assets/, _config.yml (if Jekyll) | — | — |
| 3 | Research Michelin Guide SF Bay Area starred restaurants (official michelin guide) | unclaimed | — | data/restaurants.md | guide.michelin.com | — |
| 4 | Research Michelin recommended (Bib Gourmand / selected) restaurants | unclaimed | — | data/restaurants.md | guide.michelin.com | — |
| 5 | Research hotel clusters near Michelin restaurants & rank hotels | unclaimed | — | data/hotels.md | official hotel sites | — |
| 6 | Gather pricing, hours, days open, social links (YT/TT/IG) per entry | unclaimed | — | data/restaurants.md | official site + social | — |
| 7 | Build mobile-friendly dashboard site (tables + analysis) | unclaimed | — | *.html, css/, js/ | — | — |
| 8 | Executive summary, suggestions section, open questions | unclaimed | — | pages/summary.md, pages/suggestions.md, pages/questions.md | — | — |
| 9 | Line-by-line verification against official sources; flag unverified blanks | unclaimed | — | data/*.md | official sources | — |
| 10 | Integration: merge branches, rebuild, check broken links, publish to GitHub Pages | unclaimed | — | all | — | — |

## Log
- 2026-11-24: Session `session-arena-e1428a33` created branch from `main` @ `1554148e`. Repo contained only README.md (10 bytes). COORDINATION.md created.
