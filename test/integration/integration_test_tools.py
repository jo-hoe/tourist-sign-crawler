
import os
import shutil
import tempfile
import unittest
import uuid


class IntegrationTestWithTestDirectory(unittest.TestCase):

    def setUp(self):
        working_dir = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))
        os.makedirs(working_dir)
        self.test_directory = working_dir

    def tearDown(self):
        if os.path.exists(self.test_directory):
            shutil.rmtree(self.test_directory)   