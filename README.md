# Idealista listings API — examples

Property listings from Idealista Spain/Italy/Portugal — price, rooms, size, agency.

**Live page, full schema & pricing → [quanticdata.io/collectors/idealista-scraper-api/](https://quanticdata.io/collectors/idealista-scraper-api/)**

Reads Idealista search results (sale or rent) for a location and delivers one row per listing: title, listing URL, price with parsed value, price per m², rooms, size, the detail chips as shown, description, agency and thumbnail. Choose the site (idealista.com/.it/.pt) and pass the location as a slug ("madrid-madrid", "barcelona-barcelona") or paste a full listing URL to read exactly that search.

## Quick start (curl)

```bash
curl -X POST https://api.quanticdata.io/v1/scraper/collectors/idealista_search/run \
  -H "Authorization: Bearer $QD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"location": "madrid-madrid", "operation": "sale", "site": "es", "max_results": 30}'
```

## Python

See [`example.py`](example.py):

```bash
export QD_API_KEY=qd_live_...   # https://quanticdata.io/
python3 example.py
```

## Inputs

- `location` (string, required) — Idealista location slug ("madrid-madrid") or a full listing URL.
- `operation` (string) — sale (default) or rent.
- `site` (string) — Country site: es (default), it, pt.
- `max_results` (integer) — How many listings to deliver at most (1–100). You pay only for delivered listings.

## Output — one row per listing

| field | type | description |
|---|---|---|
| `rank` | integer | 1-based position. |
| `listing_id` | string | Idealista listing id. |
| `title` | string | Listing title (type + street/zone). |
| `url` | string | Listing URL. |
| `price` | string | Price as shown. |
| `price_value` | number | Parsed price. |
| `price_per_m2` | string | Price per m² as shown. |
| `rooms` | integer | Rooms. |
| `size_m2` | number | Size in m². |
| `details` | string[] | Detail chips as shown (floor, elevator…). |
| `description` | string | Listing description excerpt. |
| `agency` | string | Listing agency (null for private). |
…and 1 more fields — full schema on the [live page](https://quanticdata.io/collectors/idealista-scraper-api/).

## Pricing

**$0.001 per delivered listing** ($1 per 1,000). A run that delivers nothing costs nothing, and failed rows are never billed. The $2/month free allowance covers roughly 2,000 listings — no card required.

## Links

- This collector: https://quanticdata.io/collectors/idealista-scraper-api/
- All collectors: https://quanticdata.io/collectors/
- Docs: https://quanticdata.io/docs/
