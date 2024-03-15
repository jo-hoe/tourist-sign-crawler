
from functools import cache
from urllib.request import urlopen
from xml.etree import ElementTree
from lxml import etree


@cache
def get_tree(url:str) -> ElementTree:
    response = urlopen(url)
    htmlparser = etree.HTMLParser()
    return etree.parse(response, htmlparser)