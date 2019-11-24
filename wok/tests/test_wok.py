import unittest

from wok import wok


class TestWok(unittest.TestCase):
    def setUp(self):
        # print("setting up test")
        pass

    def test_run(self):
        # wok.run()
        self.assertTrue(True)

    @unittest.skip
    def test_skipped_test(self):
        self.assertTrue(False)

    @unittest.expectedFailure
    def test_failed_test(self):
        self.assertEqual(1, "2")

    def tearDown(self):
        # print("tearing down test")
        pass
