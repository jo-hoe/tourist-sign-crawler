
import re
from src.crawler_common import get_tree


def get_location_from_wiki(wiki_link : str) -> tuple[float, float]:
    """
    Returns a tuple with [latitude, longitude]
    if the site does not have coordinates None is returned.
    """
    xpath_coordinates_link = "//span[@id='coordinates']/child::a[contains(@href,'geo')]"
    tree = get_tree(wiki_link)
    coordinates_link = tree.xpath(xpath_coordinates_link)

    if len(coordinates_link) < 1 or not coordinates_link[0].attrib.has_key("href"):
        return None

    # Link will be something like:
    #
    # https://geohack.toolforge.org/geohack.php?pagename=G%C3%A4rten_der_Welt
    # &language=de&params=52.539444444444_N_13.576666666667_E_dim:100_region:DE-BE_type:building'}
    geohack_link = coordinates_link[0].attrib.get("href")
    result = re.search(r"params=([0-9\\.]+)_N_([0-9\\.]+)_", geohack_link)
    if len(result.groups()) != 2:
        return None
    
    return (float(result.group(1)), float(result.group(2)))