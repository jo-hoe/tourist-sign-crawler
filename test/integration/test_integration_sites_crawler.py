import unittest
from src import sight_crawler
from src.crawler_common import get_tree


class TestIntegrationSightCrawler(unittest.TestCase):


    def test_get_tables(self):
        expected_number_of_highways = 12
        website = f"{sight_crawler.AUTOBAHN_WEBSITE_TEMPLATE}1xx"
        output = sight_crawler._get_tables(get_tree(website))

        self.assertEqual(len(output), expected_number_of_highways, "unexpected number of highways found")


    def test_get_sights(self):
        items = sight_crawler.get_sights()

        self.assertGreater(len(items), 1500)
        self.assertLess(len(items), 15000)
        foundAtLeastOneWikiLink = False
        foundAtLeastOneEntryWithKilometer = False
        
        for item in items:
            self.assertTrue(item.name, f"did not find name in {item.__dict__}")
            self.assertFalse("None" in item.name, f"name contained 'None' {item.__dict__}")
            self.assertFalse(item.name.endswith("-"), f"name ended with '-' {item.__dict__}")
            self.assertFalse("  " in item.name, f"name contained multiple whitespaces {item.__dict__}")
            self.assertTrue(item.highway, f"did not find highway in {item.__dict__}")

            if item.wiki_link != None and item.wiki_link != "":
                foundAtLeastOneWikiLink = True 
            if len(item.signs_on_kilometer_on_highway) > 0:
                foundAtLeastOneEntryWithKilometer = True
        self.assertTrue(foundAtLeastOneWikiLink, "found no wiki links")
        self.assertTrue(foundAtLeastOneEntryWithKilometer, "found kilometer entries")