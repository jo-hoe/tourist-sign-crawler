import os
import random
import uuid

from src.sight import Sight, export_sights_to_csv
from test.integration.integration_test_tools import IntegrationTestWithTestDirectory


class TestIntegrationSights(IntegrationTestWithTestDirectory):

    def test_export_sights_to_csv(self):
        number_of_sights = 10
        sights = []
        for _ in range(number_of_sights):
            sight = Sight()
            sight.set_name(str(uuid.uuid4()))
            sight.set_highway("A 1")
            sight.set_wiki_link("https://de.wikipedia.org/wiki/")
            sight.set_location((round(random.uniform(0.0, 90.0), 6), round(random.uniform(0.0, 90.0), 6)))
            sight.signs_on_kilometer_on_highway
            for _ in range(3):
                sight.add_kilometer(round(random.uniform(0.0, 100.0), 1))
            sights.append(sight)

        expected_file_name = "test.csv"
        expected_file_path = os.path.join(self.test_directory, expected_file_name)

        export_sights_to_csv(sights=sights, filename=expected_file_path)

        self.assertTrue(os.path.exists(expected_file_path))
        self.assertGreater(os.stat(expected_file_path).st_size, 3)

