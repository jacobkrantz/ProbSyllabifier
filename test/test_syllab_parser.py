from utils import SyllabParser as sp
import unittest

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
        parseResult = self.sp.parseCelexTrainingSet(self.trainingSet)
        self.assertEqual(len(parseResult), 3)
        for parsedWord in parseResult:
            for bigram in parsedWord:
                self.assertEqual(len(bigram), 3)
                self.assertTrue(bigram[2] == 0 or bigram[2] == 1)

if __name__ == '__main__':
    unittest.main()
