import os
import unittest
from src.openstreetmap import get_coordinates


class TestIntegrationOpenStreetMap(unittest.TestCase):

    TEST_LOCATION = "Oldenburger Wallmuseum"

    def test_get_coordinates(self):
        if self.is_on_github_actions():
            self.skipTest("Skipping test on GitHub Actions")

        latitude, longitude = get_coordinates(self.TEST_LOCATION)

        self.assertAlmostEqual(latitude, 54.2976194)
        self.assertAlmostEqual(longitude, 10.8828391)


    def is_on_github_actions(self):
        if os.getenv("GITHUB_ACTIONS"):
            return True
        return False

