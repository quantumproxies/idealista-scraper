"""Row types of each command, for editors and type checkers (rows are plain dicts)."""

from typing import Any, Dict, List, Optional

try:  # Python 3.8+
    from typing import TypedDict
except ImportError:  # pragma: no cover
    from typing_extensions import TypedDict  # type: ignore


class IdealistaSearchRow(TypedDict, total=False):
    """One row of `idealista-scraper search` (idealista_search v1.1.1)."""

    rank: int
    """1-based position."""
    listing_id: Optional[str]
    """Idealista listing id."""
    title: str
    """Listing title (type + street/zone)."""
    url: Optional[str]
    """Listing URL."""
    price: Optional[str]
    """Price as shown."""
    price_value: Optional[float]
    """Parsed price."""
    price_per_m2: Optional[str]
    """Price per m² as shown."""
    rooms: Optional[int]
    """Rooms."""
    size_m2: Optional[float]
    """Size in m²."""
    details: List[str]
    """Detail chips as shown (floor, elevator…)."""
    description: Optional[str]
    """Listing description excerpt."""
    agency: Optional[str]
    """Listing agency (null for private)."""
    thumbnail: Optional[str]
    """First photo."""
    property_type: Optional[str]
    """Property type from the title, in the site language (Piso, Ático, Trilocale, Apartamento…)."""
    location: Optional[str]
    """Street, neighbourhood and city from the title."""
    price_per_m2_value: Optional[float]
    """Price per m² as a number: the figure the card prints, or price ÷ size when the card shows a price drop in its place."""
    previous_price: Optional[str]
    """Price before the latest reduction, as shown."""
    previous_price_value: Optional[float]
    """Numeric previous price."""
    price_drop_pct: Optional[float]
    """Reduction in percent, as the card states it."""
    floor: Optional[str]
    """Floor line as shown, e.g. "6ª planta exterior con ascensor"."""
    parking: Optional[str]
    """Parking line when the card has one, e.g. "Garaje incluido"."""
    photo_count: Optional[int]
    """Number of photos on the listing."""
    has_video: bool
    """True when the listing has a video."""
    has_3d_tour: bool
    """True when the listing has a 3D tour."""
    has_floor_plan: bool
    """True when the listing has a floor plan."""
    tags: Optional[List[str]]
    """Tags on the card, e.g. "Lujo", "Luminoso"."""
    is_professional: Optional[bool]
    """True when listed by an agency, false when listed by a private owner."""
    agency_url: Optional[str]
    """Agency page on Idealista."""
