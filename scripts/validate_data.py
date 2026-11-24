#!/usr/bin/env python3
"""Dependency-free checks for the published, source-linked dataset."""
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def load(name):
    return json.loads((ROOT / 'data' / name).read_text())

restaurants = load('restaurants.json')
hotels = load('hotels.json')
activities = load('activities.json')
sources = load('sources.json')
assert len(restaurants) == 49, f'Expected 41 Starred + 8 Bib examples, got {len(restaurants)}'
stars = [r for r in restaurants if r['stars']]
bibs = [r for r in restaurants if not r['stars']]
assert len(stars) == 41 and len(bibs) == 8
assert Counter(r['stars'] for r in stars) == {1: 27, 2: 7, 3: 7}
assert len({r['name'] for r in restaurants}) == len(restaurants), 'Duplicate restaurant names'
for r in restaurants:
    assert r['profile'].startswith('https://guide.michelin.com/'), r['name']
    assert r['annualSelectionSource'].startswith('https://guide.michelin.com/'), r['name']
    assert r['awardYear'] == 2026
    assert (r['stars'] > 0) == (r['guideStatus'] == 'Starred')
    if not r['stars']:
        assert r['note'].startswith('Curated non-star Bib Gourmand example'), r['name']
    if r['social']:
        assert r['social'].startswith(('https://www.instagram.com/', 'https://www.tiktok.com/', 'https://www.youtube.com/')), r['name']
assert len(hotels) == 5
for h in hotels:
    assert h['profile'].startswith('https://guide.michelin.com/')
    assert h['nearbyStarCount'] == len(h['guideNearbyStarred'])
assert len(activities) == 4
for a in activities:
    assert a['official'].startswith('https://')
    assert a['daysHours']
    if a['social']:
        assert a['social'].startswith('https://www.instagram.com/')
for s in sources:
    assert s['url'].startswith('https://')
    assert s['checked'] == '2026-11-24'

required_pages = ['index.html','restaurants.html','hotels.html','activities.html','decisions.html','review.html','sources.html']
for page in required_pages:
    assert (ROOT / page).is_file(), f'Missing page: {page}'

print('PASS: 49 restaurant records (41 Starred; 8 non-star Bib samples).')
print('PASS: Star counts: 7 Three-Star, 7 Two-Star, 27 One-Star.')
print('PASS: every restaurant, hotel, activity, and source row has a direct source URL.')
print('PASS: 5 hotel candidates, 4 activities, and 7 category pages present.')
print('NOTE: this validates local structure and stated totals, not live booking availability or page uptime.')
