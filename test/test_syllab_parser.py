import unittest

from utils import SyllabParser as sp

'''
testing exists for parseCelexTrainingSet() but not for makeNistPhonemeLst()
'''


class TestSyllabParser(unittest.TestCase):
    def setUp(self):
        self.sp = sp()
        self.trainingSet = ["@-b2d", "dI-litIN", "pVI-sIN"]

    def tearDown(self):
        self.sp = None
        self.trainingSet = None

    def test_parse_celex_set_as_bigrams(self):
        parse_result = self.sp.parse_celex_set_as_bigrams(self.trainingSet)
        self.assertEqual(len(parse_result), 3)
        for parsed_word in parse_result:
            for bigram in parsed_word:
                self.assertEqual(len(bigram), 3)
                self.assertTrue(bigram[2] == 0 or bigram[2] == 1)

    def test_parse_celex_set_as_trigrams(self):
        parse_result = self.sp.parse_celex_set_as_trigrams(self.trainingSet)
        self.assertEqual(len(parse_result), 3)
        # TODO: expand this test.


if __name__ == '__main__':
    unittest.main()
