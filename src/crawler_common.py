
from functools import cache
from urllib.request import urlopen, Request
from xml.etree import ElementTree
from lxml import etree

# User-Agent policy: https://foundation.wikimedia.org/wiki/Policy:Wikimedia_Foundation_User-Agent_Policy
_APP_UA = "tourist-sign-crawler/1.0 (https://github.com/jo-hoe/tourist-sign-crawler; bot)"

_HEADERS = {"User-Agent": f"{_APP_UA} Python-urllib/3"}


@cache
def get_tree(url:str) -> ElementTree:
    response = urlopen(Request(url, headers=_HEADERS))
    htmlparser = etree.HTMLParser()
    return etree.parse(response, htmlparser)