from celex import SQLQueryService as Service
import unittest

class TestSqlQueryService(unittest.TestCase):

    def setUp(self):
        self.service = Service()
        self.words = ["seventy", "onions", "hurt", "my", "eyes"]

    def tearDown(self):
        self.service = None
        self.words = None

    def test_get_single_pronunciation(self):
        self.assertEqual(self.service.get_single_pronunciation("mountainous"), "m6ntIn@s")
        self.assertEqual(self.service.get_single_pronunciation("word"), "w3d")
        self.assertEqual(self.service.get_single_pronunciation(""), "")

    def test_get_many_pronunciations(self):
        resultDict = self.service.get_many_pronunciations(self.words)
        self.assertIn("onions", resultDict)
        self.assertIn("eyes", resultDict)
        self.assertEqual(len(resultDict), 5)
        self.assertIsNotNone(resultDict["eyes"])

    def test_get_single_syllabification(self):
        self.assertEqual(self.service.get_single_syllabification("seventy"), "sE-vH-tI")

    def test_get_many_syllabifications(self):
        resultDict = self.service.get_many_syllabifications(self.words)
        self.assertIn("onions", resultDict)
        self.assertIn("eyes", resultDict)
        self.assertEqual(len(resultDict), 5)
        self.assertIsNotNone(resultDict["eyes"])
        self.assertEqual(resultDict["seventy"], "sE-vH-tI")

    def test_get_entry_count(self):
        self.assertTrue(self.service.get_entry_count("words") > 0)

    def test_get_word_subset(self):
        subset = self.service.get_word_subset(25)
        self.assertEqual(len(subset), 25)
        self.assertEqual(len(subset), len(set(subset)))

if __name__ == '__main__':
    unittest.main()
