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

    def test_parse_celex_training_set(self):
        parse_result = self.sp.parse_celex_training_set(self.trainingSet)
        self.assertEqual(len(parse_result), 3)
        for parsed_word in parse_result:
            for bigram in parsed_word:
                self.assertEqual(len(bigram), 3)
                self.assertTrue(bigram[2] == 0 or bigram[2] == 1)


if __name__ == '__main__':
    unittest.main()
