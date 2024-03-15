import re
from xml.etree import ElementTree

from src.crawler_common import get_tree
from src.sight import Sight

WIKIPEDIA_BASE = "https://de.wikipedia.org/"
AUTOBAHN_WEBSITE_TEMPLATE = f"{WIKIPEDIA_BASE}wiki/Liste_der_Unterrichtungstafeln_in_Deutschland_an_den_Autobahnen_A_"

def get_sights() -> list[Sight]:
    result = []
    for i in range(9):
        website = f"{AUTOBAHN_WEBSITE_TEMPLATE}{i+1}xx"
        tree = get_tree(website)
        tables = _get_tables(tree)

        for highway, table in tables:
            result += _get_sights(highway, table)

    return result

def _get_tables(tree:ElementTree) -> list[tuple[str, ElementTree.Element]]:
    tables_xpath = "//table[@class='wikitable']"
    sections_sub_xpath = "/preceding-sibling::h2"
    results = []

    # strong assumption here that each table is has a section
    # and first section alines with 
    tables = tree.xpath(tables_xpath)
    sections = tree.xpath(tables_xpath + sections_sub_xpath)
    for i, table in enumerate(tables):
        highway = ""
        if sections[i].getchildren()[0].attrib.has_key("id"):
            highway = sections[i].getchildren()[0].attrib.get("id")
            highway = highway.replace("_", " ")

        results.append([highway, table])

    return results

def _get_text(element : ElementTree.Element) -> str:
    result = ""
    if element.text != None:
        result += f"{element.text.strip()} "
    if element.tail != None:
        result += f"{element.tail.strip()} "
    
    return result


def _get_name(name_table_tuple : ElementTree.Element) -> str:        
    sight_name = ""
    name_column_children = name_table_tuple.getchildren()
    if name_table_tuple.text != None:
        sight_name += f"{name_table_tuple.text.strip()} "

    if len(name_column_children) > 0:
        for name_element in name_column_children:
            sight_name += _get_text(name_element)
            for child in name_element.getchildren():
                sight_name += _get_text(child)

    sight_name = sight_name.strip()
    # remove consecutive whitespaces
    sight_name = re.sub(' +', ' ', sight_name)
    
    if sight_name != "":
        return sight_name
    else:
        return None


def _get_sights(highway : str, table : ElementTree.Element) -> list[Sight]:
    table_row_xpath = ".//td/parent::tr"
    rows = table.xpath(table_row_xpath)

    result = []
    last_sight = None
    for row in rows:    
        columns = row.getchildren()
        
        sight_name = ""
        sight_name = _get_name(columns[0])
        if sight_name != None:
            if last_sight != None:
                result.append(last_sight)
            last_sight = Sight()
            last_sight.set_name(sight_name)
            last_sight.set_highway(highway)
            
            name_column_children = columns[0].getchildren()
            for child in name_column_children:
                if child.attrib.has_key("href"):
                    last_sight.set_wiki_link(WIKIPEDIA_BASE + child.get("href"))
        
        kilometer_tuple = columns[1]
        if kilometer_tuple.text != None and last_sight != None:
            kilometer_string = kilometer_tuple.text.strip()
            # german websites have 'wrong' decimal point
            kilometer_string = kilometer_string.replace(',','.')
            if kilometer_string != "":
                last_sight.add_kilometer(float(kilometer_string))


    if last_sight != None and last_sight not in result:
        result.append(last_sight)

    return result