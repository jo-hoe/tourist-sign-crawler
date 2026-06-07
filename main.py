import argparse
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from src import sight_crawler
from src.openstreetmap import RateLimiter, _DEFAULT_RATE_LIMIT, get_coordinates
from src.sight import Sight, export_sights_to_csv
from src.wiki_location_crawler import get_location_from_wiki


def _set_location_for_item(item: Sight, rate_limiter: RateLimiter | None) -> None:
    if item.wiki_link is not None:
        location = get_location_from_wiki(item.wiki_link)
        if location is not None:
            item.set_location(location)
            return

    location = get_coordinates(
        item.name.replace("Historischer Stadtkern", "").strip(),
        rate_limiter=rate_limiter,
    )
    item.set_location(location)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Crawl tourist signs from German Autobahn Wikipedia pages."
    )
    parser.add_argument(
        "--no-rate-limit",
        "-n",
        action="store_true",
        help="Disable the 1 req/s rate limit for Nominatim (e.g. for self-hosted instances).",
    )
    return parser.parse_args()


def main(args: argparse.Namespace) -> None:
    rate_limiter = None if args.no_rate_limit else RateLimiter(_DEFAULT_RATE_LIMIT)

    items = sight_crawler.get_sights()

    worker = partial(_set_location_for_item, rate_limiter=rate_limiter)
    with ThreadPoolExecutor(max_workers=8) as executor:
        executor.map(worker, items)

    export_sights_to_csv(items, "unterrichtungstafeln.csv")


if __name__ == "__main__":
    main(_parse_args())
