import re
from xml.etree import ElementTree

from src.crawler_common import get_tree
from src.sight import Sight

WIKIPEDIA_BASE = "https://de.wikipedia.org"
AUTOBAHN_WEBSITE_TEMPLATE = f"{WIKIPEDIA_BASE}/wiki/Liste_der_Unterrichtungstafeln_in_Deutschland_an_den_Autobahnen_A_"


def get_sights() -> list[Sight]:
    result = []
    for i in range(9):
        website = f"{AUTOBAHN_WEBSITE_TEMPLATE}{i+1}xx"
        tree = get_tree(website)
        tables = _get_tables(tree)

        for highway, table in tables:
            result += _get_sights(highway, table)

    return result


def _get_tables(tree: ElementTree) -> list[tuple[str, ElementTree.Element]]:
    # Wikipedia now wraps each section in a <section> element with an <h2 id="...">
    tables = tree.xpath("//table[@class='wikitable']")
    results = []
    for table in tables:
        section = table.getparent()
        h2s = section.xpath(".//h2[@id]") if section is not None else []
        highway = h2s[0].get("id").replace("_", " ") if h2s else ""
        results.append((highway, table))
    return results


def _get_text(element: ElementTree.Element) -> str:
    result = ""
    if element.text is not None:
        result += f"{element.text.strip()} "
    if element.tail is not None:
        result += f"{element.tail.strip()} "
    return result


def _get_name(name_column: ElementTree.Element) -> str | None:
    sight_name = ""
    if name_column.text is not None:
        sight_name += f"{name_column.text.strip()} "

    for child in name_column:
        sight_name += _get_text(child)
        for grandchild in child:
            sight_name += _get_text(grandchild)

    sight_name = re.sub(r" +", " ", sight_name.strip())
    return sight_name if sight_name else None


def _extract_wiki_link(name_column: ElementTree.Element) -> str | None:
    for child in name_column:
        href = child.get("href")
        if href is not None:
            # href may be protocol-relative (//de.wikipedia.org/...) or root-relative (/wiki/...)
            if href.startswith("//"):
                return f"https:{href}"
            if href.startswith("/"):
                return f"{WIKIPEDIA_BASE}{href}"
    return None


def _get_sights(highway: str, table: ElementTree.Element) -> list[Sight]:
    rows = table.xpath(".//td/parent::tr")

    result = []
    last_sight = None
    for row in rows:
        columns = list(row)

        sight_name = _get_name(columns[0])
        if sight_name is not None:
            if last_sight is not None:
                result.append(last_sight)
            last_sight = Sight()
            last_sight.set_name(sight_name)
            last_sight.set_highway(highway)
            wiki_link = _extract_wiki_link(columns[0])
            if wiki_link is not None:
                last_sight.set_wiki_link(wiki_link)

        kilometer_column = columns[1]
        if kilometer_column.text is not None and last_sight is not None:
            kilometer_string = kilometer_column.text.strip().replace(",", ".")
            if kilometer_string:
                try:
                    last_sight.add_kilometer(float(kilometer_string))
                except ValueError:
                    pass

    if last_sight is not None and last_sight not in result:
        result.append(last_sight)

    return result
