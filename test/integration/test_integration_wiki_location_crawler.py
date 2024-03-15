import unittest

from src.wiki_location_crawler import get_location_from_wiki


class TestIntegrationWikiLocationCrawler(unittest.TestCase):

    TEST_URL = "https://de.wikipedia.org/wiki/G%C3%A4rten_der_Welt"

    def test_get_location_from_wiki(self):
        latitude, longitude = get_location_from_wiki(self.TEST_URL)

        self.assertAlmostEqual(latitude, 52.539444444444)
        self.assertAlmostEqual(longitude, 13.576666666667)

