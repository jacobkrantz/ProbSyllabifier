import unittest

from probSyllabifier import Utils

'''
testing exists for parseCelexTrainingSet() but not for makeNistPhonemeLst()
'''


class TestSyllabParser(unittest.TestCase):
    def setUp(self):
        self.utils = Utils()
        self.trainingSet = ["@-b2d", "dI-litIN", "pVI-sIN"]

    def tearDown(self):
        self.utils = None
        self.trainingSet = None

    def test_parse_celex_set(self):
        # TODO: rewrite test for new parser. Create more tests surrounding this.

        # parse_result = self.sp.parse_celex_set_as_bigrams(self.trainingSet)
        # self.assertEqual(len(parse_result), 3)
        # for parsed_word in parse_result:
        #     for bigram in parsed_word:
        #         self.assertEqual(len(bigram), 3)
        #         self.assertTrue(bigram[2] == 0 or bigram[2] == 1)
        pass

if __name__ == '__main__':
    unittest.main()
