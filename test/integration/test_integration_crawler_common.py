import unittest
from src.crawler_common import get_tree


class TestIntegrationCommonCrawler(unittest.TestCase):

    TEST_URL = "https://de.wikipedia.org/"

    def test_get_tree(self):
        output = get_tree(self.TEST_URL)

        self.assertIsNotNone(output)


    def test_get_tree_cache(self):
        '''
        test that returned is the same instance instead of just a similar object.
        '''
        output1 = get_tree(self.TEST_URL)
        output2 = get_tree(self.TEST_URL)

        self.assertEqual(output1, output2)

