"""Idealista listings whose price was reduced, biggest cut first.

    python price_drops.py madrid-madrid --operation sale --site es --min-drop 5

Reads up to 100 listings per location and keeps the ones that show a price
reduction of at least --min-drop percent, with the current and previous price,
size, price per square metre and agency. Run it on a schedule to catch new
reductions in an area you follow.
"""

import argparse

from quanticdata_idealista_scraper import IdealistaScraper, write

FIELDS = ["location_slug", "listing_id", "title", "property_type", "price_value", "previous_price_value",
          "price_drop_pct", "size_m2", "rooms", "price_per_m2_value", "agency", "is_professional", "url"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("locations", nargs="+", help='Idealista location slugs, e.g. "madrid-madrid"')
    parser.add_argument("--operation", default="sale", choices=["sale", "rent"])
    parser.add_argument("--site", default="es", choices=["es", "it", "pt"])
    parser.add_argument("--min-drop", type=float, default=5.0, help="smallest reduction in percent")
    parser.add_argument("--out", default="price_drops.csv")
    args = parser.parse_args()

    idealista = IdealistaScraper()
    drops = []
    for location in args.locations:
        run = idealista.search(location, operation=args.operation, site=args.site, max_results=100)
        cut = [l for l in run if (l.get("price_drop_pct") or 0) >= args.min_drop]
        drops.extend({"location_slug": location, **l} for l in cut)
        print(f"{location}: {len(cut)} of {len(run)} listings reduced by {args.min_drop:g}% or more")

    drops.sort(key=lambda l: -l["price_drop_pct"])
    write([{k: l.get(k) for k in FIELDS} for l in drops], args.out)
    print(f"{len(drops)} listings written to {args.out}")


if __name__ == "__main__":
    main()
