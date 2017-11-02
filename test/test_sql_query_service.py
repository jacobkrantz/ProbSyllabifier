import unittest

from celex import SQLQueryService as Service


class TestSqlQueryService(unittest.TestCase):
    def setUp(self):
        self.service = Service()
        self.words = ["seventy", "onions", "hurt", "my", "eyes"]

    def tearDown(self):
        self.service = None
        self.words = None

    def test_get_single_pronunciation(self):
        self.assertEqual(self.service.get_single_pronunciation("mountainous"),
                         "m6ntIn@s")
        self.assertEqual(self.service.get_single_pronunciation("word"), "w3d")
        self.assertEqual(self.service.get_single_pronunciation(""), "")

    def test_get_many_pronunciations(self):
        result_dict = self.service.get_many_pronunciations(self.words)
        self.assertIn("onions", result_dict)
        self.assertIn("eyes", result_dict)
        self.assertEqual(len(result_dict), 5)
        self.assertIsNotNone(result_dict["eyes"])

    def test_get_single_syllabification(self):
        self.assertEqual(self.service.get_single_syllabification("seventy"),
                         "sE-vH-tI")

    def test_get_many_syllabifications(self):
        result_dict = self.service.get_many_syllabifications(self.words)
        self.assertIn("onions", result_dict)
        self.assertIn("eyes", result_dict)
        self.assertEqual(len(result_dict), 5)
        self.assertIsNotNone(result_dict["eyes"])
        self.assertEqual(result_dict["seventy"], "sE-vH-tI")

    def test_get_entry_count(self):
        self.assertTrue(self.service.get_entry_count("words") > 0)

    def test_get_word_subset(self):
        subset = self.service.get_word_subset(25)
        self.assertEqual(len(subset), 25)
        self.assertEqual(len(subset), len(set(subset)))


if __name__ == '__main__':
    unittest.main()
