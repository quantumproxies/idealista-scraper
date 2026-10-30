"""Gross rental yield of a location from its Idealista sale and rent listings.

    python rental_yield.py madrid-madrid barcelona-barcelona --site es

For each location it reads the listings for sale and for rent, takes the
median price per square metre of each and computes the gross yield as
12 x median monthly rent per m2 / median sale price per m2. A first read of an
area for investors, before looking at single listings.
"""

import argparse
from statistics import median

from quanticdata_idealista_scraper import IdealistaScraper, write


def median_per_m2(listings):
    values = [l["price_value"] / l["size_m2"] for l in listings if l.get("price_value") and l.get("size_m2")]
    return (median(values), len(values)) if values else (None, 0)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("locations", nargs="+", help='Idealista location slugs, e.g. "madrid-madrid"')
    parser.add_argument("--site", default="es", choices=["es", "it", "pt"])
    parser.add_argument("--max-results", type=int, default=100, help="listings per search (max 100)")
    parser.add_argument("--out", default="rental_yield.csv")
    args = parser.parse_args()

    idealista = IdealistaScraper()
    rows = []
    for location in args.locations:
        sale, n_sale = median_per_m2(idealista.search(location, operation="sale", site=args.site,
                                                      max_results=args.max_results))
        rent, n_rent = median_per_m2(idealista.search(location, operation="rent", site=args.site,
                                                      max_results=args.max_results))
        gross = round(12 * rent / sale * 100, 2) if sale and rent else None
        rows.append({
            "location": location,
            "sale_listings": n_sale,
            "median_sale_per_m2": round(sale, 2) if sale else None,
            "rent_listings": n_rent,
            "median_rent_per_m2": round(rent, 2) if rent else None,
            "gross_yield_pct": gross,
        })
        print(f"{location}: sale {rows[-1]['median_sale_per_m2']}/m2, rent {rows[-1]['median_rent_per_m2']}/m2 "
              f"a month, gross yield {gross}%")

    write(rows, args.out)
    print(f"{len(rows)} locations written to {args.out}")


if __name__ == "__main__":
    main()
