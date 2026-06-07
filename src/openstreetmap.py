import logging
import threading
import time
import requests
from src.crawler_common import _APP_UA

# Nominatim usage policy: https://operations.osmfoundation.org/policies/nominatim/
_DEFAULT_RATE_LIMIT = 1.0

_HEADERS = {"User-Agent": f"{_APP_UA} Python-requests/2"}


class RateLimiter:
    def __init__(self, min_interval: float) -> None:
        self._min_interval = min_interval
        self._lock = threading.Lock()
        self._last_call = 0.0

    def acquire(self) -> None:
        with self._lock:
            elapsed = time.monotonic() - self._last_call
            wait = self._min_interval - elapsed
            if wait > 0:
                time.sleep(wait)
            self._last_call = time.monotonic()


def get_coordinates(
    location_name: str,
    rate_limiter: RateLimiter | None = None,
) -> tuple[float, float] | None:
    data = _get_data(location_name, rate_limiter)
    if data:
        return (float(data[0]["lat"]), float(data[0]["lon"]))
    return None


def _get_data(
    location_name: str,
    rate_limiter: RateLimiter | None,
) -> list | None:
    if rate_limiter is not None:
        rate_limiter.acquire()

    base_url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": location_name,
        "format": "json",
        "limit": 1,
    }

    try:
        response = requests.get(base_url, params=params, headers=_HEADERS)
        if response.status_code != 200:
            logging.warning(
                f"Received unexpected status code for '{location_name}'. "
                f"{response.status_code}: {response.text}"
            )
            return None

        data = response.json()
        if not data:
            logging.warning(f"No results found for '{location_name}'")
            return None
        return data

    except requests.RequestException as e:
        logging.warning(f"Error fetching data for '{location_name}': {e}")
        return None
