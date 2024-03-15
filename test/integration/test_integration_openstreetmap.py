import unittest
from src.crawler_common import get_tree
from src.openstreetmap import get_coordinates


class TestIntegrationOpenStreetMap(unittest.TestCase):

    TEST_LOCATION = "Oldenburger Wallmuseum"

    def test_get_coordinates(self):
        latitude, longitude = get_coordinates(self.TEST_LOCATION)

        self.assertAlmostEqual(latitude, 54.2976194)
        self.assertAlmostEqual(longitude, 10.8828391)

