"""Merge Michelin listing extracts + verified detail pages into data/michelin_restaurants.csv.

Row source: Michelin listing pages (guide.michelin.com/us/en/california/san-francisco/restaurants[/page/N]).
Detail fields (address, website, phone, hours) come only from Michelin detail pages captured in
data/michelin_detail_verified.json. Anything not captured stays blank and is flagged.
City is taken from the listing (p3 extract) or from a captured detail address. It is NOT assumed.
"""
import csv, json, os
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
LISTING = "https://guide.michelin.com/us/en/california/san-francisco/restaurants"

NAME_FIX = {"Mister Jiu's": "Mister Jiu’s", "Azalina's": "Azalina’s"}

def read_tsv(name, page_default_city):
    out = []
    with open(os.path.join(DATA, name), encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            r["city"] = r.get("city") or page_default_city
            out.append(r)
    return out

rows = []
rows += read_tsv("michelin_p1_raw.tsv", "")   # no city column captured for p1
rows += read_tsv("michelin_p2_raw.tsv", "")   # no city column captured for p2
rows += read_tsv("michelin_p3_raw.tsv", "")   # city column captured
rows += read_tsv("michelin_p4_raw.tsv", "")   # city column captured

seen, uniq = set(), []
for r in rows:
    if r["url_slug"] in seen:
        continue
    seen.add(r["url_slug"]); uniq.append(r)

detail = json.load(open(os.path.join(DATA, "michelin_detail_verified.json"), encoding="utf-8"))

out = []
for r in uniq:
    slug = r["url_slug"]
    name = NAME_FIX.get(r["name"], r["name"])
    d = detail.get(slug, {})
    award_raw = r["award"].strip()
    status = "from listing card"
    if "award_override" in d:
        award_raw, status = d["award_override"]
    stars = {"3 Stars": 3, "2 Stars": 2, "1 Star": 1}.get(award_raw, 0)
    if award_raw == "Unverified":
        status = "unverified – tier not shown in the captured listing text"
    city = d.get("city") or r["city"]
    if city:
        listing_url = f"https://guide.michelin.com/us/en/california/{city.lower().replace(' ', '-')}/restaurant/{slug}"
    else:
        listing_url = f"{LISTING}/page/{r['listing_page']}"
    out.append({
        "name": name,
        "award": award_raw,
        "award_status": status,
        "stars": stars,
        "bib_gourmand": "Yes" if award_raw == "Bib Gourmand" else "No",
        "michelin_price_tier": r["price_level"],
        "cuisine": r["cuisine"],
        "city": city or "not captured",
        "address": d.get("address", ""),
        "website": d.get("website", ""),
        "phone": d.get("phone", ""),
        "booking": d.get("booking", ""),
        "hours_michelin": d.get("hours", ""),
        "hours_status": d.get("hours_status", "not checked"),
        "price_for_two_usd": "",
        "price_status": "unverified – not captured",
        "social_links": "",
        "social_status": "unverified – not searched",
        "source_url": listing_url,
        "michelin_detail_checked": "Yes" if d else "No",
        "listing_page": r["listing_page"],
    })

order = {"3 Stars": 0, "2 Stars": 1, "1 Star": 2, "Bib Gourmand": 3, "Selected": 4, "Unverified": 5}
out.sort(key=lambda x: (order.get(x["award"], 9), x["name"].lower()))
with open(os.path.join(DATA, "michelin_restaurants.csv"), "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)

print("rows", len(out))
print(dict(Counter(x["award"] for x in out)))
print("city known", sum(1 for x in out if x["city"] != "not captured"), "| detail checked", sum(1 for x in out if x["michelin_detail_checked"] == "Yes"))
print(dict(Counter(x["city"] for x in out)))
