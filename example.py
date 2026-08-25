"""Minimal Idealista listings API call — one typed row per listing.

Docs & schema: https://quanticdata.io/collectors/idealista-scraper-api/
"""
import json
import os

import requests

API = "https://api.quanticdata.io/v1/scraper/collectors/idealista_search/run"
KEY = os.environ["QD_API_KEY"]  # https://quanticdata.io/

payload = {
        "location": "madrid-madrid",
        "operation": "sale",
        "site": "es",
        "max_results": 30
    }

r = requests.post(
    API,
    headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
    json=payload,
    timeout=180,
)
r.raise_for_status()
data = r.json()["payload"]

for row in data["results"]:
    print(row.get("listing_id"), row.get("title"), row.get("url"))
print(f"{len(data['results'])} listings, cost ${data['cost']}")
