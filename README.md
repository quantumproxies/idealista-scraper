# Idealista Scraper

[![ci](https://github.com/quantumproxies/idealista-scraper/actions/workflows/ci.yml/badge.svg)](https://github.com/quantumproxies/idealista-scraper/actions/workflows/ci.yml) ![python](https://img.shields.io/badge/python-3.9%2B-blue) ![license](https://img.shields.io/badge/license-MIT-green) ![dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)

Scrape Idealista from Python or the command line: homes for sale or for rent in Spain, Italy and Portugal, with price, price per square metre, rooms, size, floor, parking, the previous price and the size of a reduction, photo and tour counts and the listing agency, as JSON or CSV. The code is free and open source (MIT). It runs on the QuanticData Data API, so there are no proxies to rotate and no headless browser to keep alive: sign in once and run a command.

```bash
pip install git+https://github.com/quantumproxies/idealista-scraper
idealista-scraper login
idealista-scraper search madrid-madrid --operation sale --site es --max-results 100 -o madrid.csv
```

`login` opens the QuanticData sign-in page in your browser. New accounts get $2 of free usage every month, no card required: [create one](https://app.quanticdata.io/register?utm_source=github&utm_medium=readme&utm_campaign=idealista-scraper).

## What it scrapes

| Command | Input | Returns | Per run |
|---|---|---|---|
| `idealista-scraper search` | location slug or listing URL | Price, rooms, size, agency, 28 fields per row ([fields and price](https://quanticdata.io/collectors/idealista-scraper-api/?utm_source=github&utm_medium=readme&utm_campaign=idealista-scraper)) | up to 100 |

`--site` picks the country: `es` (Spain, the default), `it` (Italy) or `pt` (Portugal); `--operation` is `sale` (the default) or `rent`. A location is the slug Idealista uses in its own search URLs, e.g. `madrid-madrid` or `barcelona-barcelona`. Labels such as the property type, the floor line and the detail chips come back in the site's language (Piso, Ático, Trilocale, Apartamento...).

## Sample output

A real row from `idealista-scraper search madrid-madrid --operation sale --site es --max-results 3` (2026-10-23):

```json
{
  "url": "https://www.idealista.com/inmueble/112832492/",
  "rank": 3,
  "tags": null,
  "floor": "3ª planta exterior con ascensor",
  "price": "1.040.000€",
  "rooms": 3,
  "title": "Piso en Calle de Preciados, Sol, Madrid",
  "agency": "Gilmar Centro",
  "details": [
    "3 hab.",
    "105 m²",
    "3ª planta exterior con ascensor"
  ],
  "parking": null,
  "size_m2": 105,
  "location": "Calle de Preciados, Sol, Madrid",
  "has_video": true,
  "thumbnail": "https://img4.idealista.com/blur/591_420_mq/0/id.pro.es.image.master/6a/c0/53/1484380109.jpg",
  "agency_url": "https://www.idealista.com/pro/gilmar-centro/",
  "listing_id": "112832492",
  "description": "GILMAR Consulting Inmobiliario pone a su disposición exclusiva vivienda en el corazón de Madrid. Ubicado en el emblemático barrio de Sol, este impresionante piso destaca por su elegancia, luminosidad y ubicación privilegiada...",
  "has_3d_tour": true,
  "photo_count": 40,
  "price_value": 1040000,
  "price_per_m2": "9.905 €/m²",
  "property_type": "Piso",
  "has_floor_plan": true,
  "previous_price": null,
  "price_drop_pct": null,
  "is_professional": true,
  "price_per_m2_value": 9905,
  "previous_price_value": null
}
```

## Python

```python
from quanticdata_idealista_scraper import IdealistaScraper

idealista = IdealistaScraper()  # saved login, or QUANTICDATA_API_KEY

madrid = idealista.search("madrid-madrid", operation="sale", site="es", max_results=100)
for l in madrid:
    print(l["listing_id"], l["property_type"], l["price_value"], l["size_m2"], l["price_per_m2_value"], l["agency"])
madrid.to_csv("madrid.csv")

rents = idealista.search("barcelona-barcelona", operation="rent", max_results=100)
cuts = [l for l in rents if l["price_drop_pct"]]
print(len(cuts), "rentals with a price reduction")
```

Each call returns a `Run`: iterate it for the rows (plain dicts), take `len()`, or save it with `to_csv()`, `to_json()`, `to_jsonl()` or `to_dataframe()` (pandas). Errors are specific: `InsufficientCredit`, `RateLimited`, `InvalidInput`, `JobFailed`, `AuthError`.

## Examples

- **Price per square metre**: Summarise one or more locations by property type: listing count, median price, median size and median price per square metre, for sale or for rent. See [`examples/price_per_m2.py`](examples/price_per_m2.py).
- **Gross rental yield**: Run the same location for sale and for rent and compare the median price per square metre of each, for a first read of the gross yield of an area. See [`examples/rental_yield.py`](examples/rental_yield.py).
- **Price reductions**: List the homes of an area whose price was cut, with the previous price and the reduction in percent, biggest cut first. See [`examples/price_drops.py`](examples/price_drops.py).

## Command line

Results print as a table; `-o file.csv`, `-o file.json` or `-o file.jsonl` writes a file. List inputs take `a b c`, `a,b,c`, `@file.txt` (one per line) or `-` (stdin). `--no-wait` starts a long run in the background and prints its id; `idealista-scraper run <id> -o out.csv` collects it later.

### `idealista-scraper search`

Property listings from Idealista Spain/Italy/Portugal — price, rooms, size, agency.

```
idealista-scraper search LOCATION [options]
```

| Option | Type | Default | Description |
|---|---|---|---|
| `LOCATION` | string |  | Idealista location slug as in the site's own search URLs, e.g. "madrid-madrid" or "barcelona-barcelona", or a full listing URL. |
| `--operation` | sale / rent | `sale` | sale (default) or rent. |
| `--site` | es / it / pt | `es` | Country site: es (Spain, the default), it (Italy) or pt (Portugal). |
| `--max-results` | integer | `30` | How many listings to deliver at most (1–100). You pay only for delivered listings. |

## Output fields

<details><summary><code>idealista-scraper search</code>: 28 fields</summary>

| Field | Type | Description |
|---|---|---|
| `rank` | integer | 1-based position. |
| `listing_id` | string or null | Idealista listing id. |
| `title` | string | Listing title (type + street/zone). |
| `url` | string or null | Listing URL. |
| `price` | string or null | Price as shown. |
| `price_value` | number or null | Parsed price. |
| `price_per_m2` | string or null | Price per m² as shown. |
| `rooms` | integer or null | Rooms. |
| `size_m2` | number or null | Size in m². |
| `details` | string[] | Detail chips as shown (floor, elevator…). |
| `description` | string or null | Listing description excerpt. |
| `agency` | string or null | Listing agency (null for private). |
| `thumbnail` | string or null | First photo. |
| `property_type` | string or null | Property type from the title, in the site language (Piso, Ático, Trilocale, Apartamento…). |
| `location` | string or null | Street, neighbourhood and city from the title. |
| `price_per_m2_value` | number or null | Price per m² as a number: the figure the card prints, or price ÷ size when the card shows a price drop in its place. |
| `previous_price` | string or null | Price before the latest reduction, as shown. |
| `previous_price_value` | number or null | Numeric previous price. |
| `price_drop_pct` | number or null | Reduction in percent, as the card states it. |
| `floor` | string or null | Floor line as shown, e.g. "6ª planta exterior con ascensor". |
| `parking` | string or null | Parking line when the card has one, e.g. "Garaje incluido". |
| `photo_count` | integer or null | Number of photos on the listing. |
| `has_video` | boolean | True when the listing has a video. |
| `has_3d_tour` | boolean | True when the listing has a 3D tour. |
| `has_floor_plan` | boolean | True when the listing has a floor plan. |
| `tags` | string[] or null | Tags on the card, e.g. "Lujo", "Luminoso". |
| `is_professional` | boolean or null | True when listed by an agency, false when listed by a private owner. |
| `agency_url` | string or null | Agency page on Idealista. |

</details>

## Sign-in and API keys

- `idealista-scraper login` signs you in with OAuth 2.1 and PKCE in the browser. The token is stored in `~/.config/quanticdata/credentials.json` (readable only by you) and refreshed automatically. One login serves every QuanticData tool on the machine.
- No browser on the machine (SSH, Docker, Colab): run `idealista-scraper login --no-browser`, open the link anywhere, then paste back the address the browser ends on.
- Scripts and CI: set `QUANTICDATA_API_KEY` to a key from the dashboard, or store one with `idealista-scraper login --api-key`.
- `idealista-scraper logout` revokes the token. The connection is listed under API keys in the dashboard as "API · QuanticData CLI"; deleting that key disconnects every machine that uses it.

## Pricing

The code is free and MIT-licensed. Runs are billed to your QuanticData account per delivered row, at the price shown on each collector page linked above; $2 of usage is free every month and failed runs are never billed. Plans with higher limits: [pricing](https://quanticdata.io/pricing/?utm_source=github&utm_medium=readme&utm_campaign=idealista-scraper).

## Other ways to call it

The same data over plain HTTP:

```bash
curl -X POST https://api.quanticdata.io/v1/scraper/collectors/idealista_search/run \
  -H "Authorization: Bearer $QUANTICDATA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"input": {"location": "madrid-madrid", "operation": "sale", "site": "es", "max_results": 3}}'
```

- [API reference](https://quanticdata.io/docs/?utm_source=github&utm_medium=readme&utm_campaign=idealista-scraper) with Python, Node, PHP and curl examples.
- [MCP server](https://quanticdata.io/mcp-server/?utm_source=github&utm_medium=readme&utm_campaign=idealista-scraper) to give Claude, Cursor or any MCP client the same tools.
- [n8n node](https://github.com/quantumproxies/n8n-nodes-quanticdata) for no-code workflows.

## FAQ

**Is this Idealista scraper free?**

The code is free and MIT-licensed. Scraping runs on your QuanticData account: $2 of usage is free every month with no card, then you pay per delivered row at the price shown on each collector page. Failed runs are never billed.

**Do I need proxies or a headless browser?**

No. You send a location slug and get rows back; the requests run on QuanticData's side. It reads public search results only; you are responsible for respecting Idealista's terms and the data-protection rules that apply to how you use the data.

**Which countries and listings does it cover?**

Spain, Italy and Portugal, chosen with --site es, it or pt, and homes for sale or for rent, chosen with --operation. is_professional tells listings by an agency from listings by a private owner.

**How many listings can one run return?**

Up to 100 listings per run; ask for fewer with --max-results and you pay only for what is delivered.

**Can I export to CSV or Excel?**

Add -o listings.csv (or .json, .jsonl). Lists such as the detail chips and tags are joined with '; ', so the CSV opens cleanly in Excel or Google Sheets.

**Can I run it on a schedule?**

Yes. Set QUANTICDATA_API_KEY in the environment and call the CLI or examples/price_drops.py from cron, GitHub Actions or any scheduler.

## Related scrapers

- [Zillow Scraper](https://github.com/quantumproxies/zillow-scraper): Zillow scraper for Python and the command line.
- [Redfin Scraper](https://github.com/quantumproxies/redfin-scraper): Redfin scraper for Python and the command line.
- [Airbnb Scraper](https://github.com/quantumproxies/airbnb-scraper): Airbnb scraper for Python and the command line.

## License

MIT. Built and maintained by [QuanticData](https://quanticdata.io/?utm_source=github&utm_medium=readme&utm_campaign=idealista-scraper).
