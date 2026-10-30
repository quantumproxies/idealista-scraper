"""Idealista Scraper: Idealista scraper for Python and the command line: homes for sale or rent in Spain, Italy and Portugal with price, price per m2, rooms, size, floor, price drops and listing agency, as JSON or CSV. Free and open source; sign in with your QuanticData account, no proxies or headless browser to run.

    from quanticdata_idealista_scraper import IdealistaScraper

    scraper = IdealistaScraper()   # saved login (`idealista-scraper login`) or QUANTICDATA_API_KEY
    run = scraper.search(...)   # Idealista listings for sale or rent in Spain, Italy or Portugal
"""

from typing import Any, Dict, Optional, Sequence, Union

from ._qd.client import Client, Run
from ._qd.errors import (APIError, AuthError, InsufficientCredit, InvalidInput, JobFailed, JobTimeout,
                         QuanticDataError, RateLimited)
from ._qd.output import write

__version__ = "0.1.0"
__all__ = ["IdealistaScraper", "Run", "write", "APIError", "AuthError", "InsufficientCredit", "InvalidInput",
           "JobFailed", "JobTimeout", "QuanticDataError", "RateLimited", "__version__"]


def _as_list(value: Any) -> Any:
    if value is None or isinstance(value, (list, tuple)):
        return list(value) if value is not None else None
    return [value]


class IdealistaScraper:
    """Idealista Scraper on the QuanticData Data API.

    Every method runs one collector and returns a :class:`Run`: iterate it for the
    rows (plain dicts, typed in ``types``), or save it with ``to_csv()``,
    ``to_json()``, ``to_jsonl()`` or ``to_dataframe()``.
    """

    def __init__(self, api_key: Optional[str] = None, *, timeout: float = 180.0) -> None:
        self.client = Client(api_key, user_agent="idealista-scraper/0.1.0 (+https://github.com/quantumproxies/idealista-scraper)", timeout=timeout)

    def search(
        self, location: str,
        *,
        operation: Optional[str] = None,
        site: Optional[str] = None,
        max_results: Optional[int] = None,
        wait: bool = True,
        timeout: float = 900.0,
    ) -> Run:
        """Property listings from Idealista Spain/Italy/Portugal — price, rooms, size, agency.

        Args:
            location: Idealista location slug as in the site's own search URLs, e.g. "madrid-madrid" or "barcelona-barcelona", or a full listing URL.
            operation: sale (default) or rent. One of: sale, rent.
            site: Country site: es (Spain, the default), it (Italy) or pt (Portugal). One of: es, it, pt.
            max_results: How many listings to deliver at most (1–100). You pay only for delivered listings.
            wait: False starts the run in the background and returns its id at once.
            timeout: seconds to wait for a background run before giving up.

        Returns up to 100 rows, one per listing: see ``types.IdealistaSearchRow``.
        """
        payload = {
            "location": location,
            "operation": operation,
            "site": site,
            "max_results": max_results,
        }
        return self.client.run_collector("idealista_search", payload, wait=wait, timeout=timeout)
