"""Median price and price per square metre on Idealista, by location and property type.

    python price_per_m2.py madrid-madrid barcelona-barcelona --operation sale --site es

Pulls the listings of one or more locations and summarises them by property
type (Piso, Ático...): how many listings, median price, median size
and median price per square metre. Use --operation rent for monthly rents.
Listings without a price or a size are left out of the medians.
"""

import argparse
from collections import defaultdict
from statistics import median

from quanticdata_idealista_scraper import IdealistaScraper, write


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("locations", nargs="+", help='Idealista location slugs, e.g. "madrid-madrid"')
    parser.add_argument("--operation", default="sale", choices=["sale", "rent"])
    parser.add_argument("--site", default="es", choices=["es", "it", "pt"])
    parser.add_argument("--max-results", type=int, default=100, help="listings per location (max 100)")
    parser.add_argument("--out", default="price_per_m2.csv")
    args = parser.parse_args()

    idealista = IdealistaScraper()
    groups = defaultdict(list)
    for location in args.locations:
        run = idealista.search(location, operation=args.operation, site=args.site, max_results=args.max_results)
        for listing in run:
            if listing.get("price_value") and listing.get("size_m2"):
                groups[(location, listing.get("property_type") or "other")].append(listing)

    summary = []
    for (location, kind), listings in sorted(groups.items()):
        summary.append({
            "location": location,
            "operation": args.operation,
            "property_type": kind,
            "listings": len(listings),
            "median_price": round(median(l["price_value"] for l in listings)),
            "median_size_m2": round(median(l["size_m2"] for l in listings)),
            "median_price_per_m2": round(median(l["price_value"] / l["size_m2"] for l in listings), 2),
        })

    for s in summary:
        print(f"{s['location']:<24} {s['property_type']:<14} {s['listings']:>4} listings  "
              f"{s['median_price']:>10,}  {s['median_price_per_m2']:>9,.2f}/m2")
    write(summary, args.out)
    print(f"{len(summary)} groups written to {args.out}")


if __name__ == "__main__":
    main()
