import unittest

from config import settings as config
from probSyllabifier import Utils

'''
testing exists for parseCelexTrainingSet() but not for makeNistPhonemeLst()
'''


class TestSyllabParser(unittest.TestCase):
    def setUp(self):
        self.utils = Utils()
        self.training_set = ["@-b2d", "dI-litIN", "pVI-sIN"]
        self.scheme = None

    def tearDown(self):
        self.utils = None
        self.training_set = None

    def test_load_scheme(self):
        self.scheme = self.utils.load_scheme(2)

        # ensure a transcription scheme was loaded
        self.assertIsNotNone(self.scheme)

        # ensure all phones are in transcription scheme
        gene_set = set(config["genetic_algorithm"]["gene_list"])
        trans_set = set()
        map(lambda c: trans_set.update(set(c)), self.scheme)
        trans_set.discard('<')
        trans_set.discard('>')
        self.assertEqual(gene_set, trans_set)

    def test_parse_celex_training_word(self):
        if self.scheme is None:
            self.test_load_scheme()

        parsed_lst = [
            self.utils.parse_celex_training_word(w, self.scheme)
            for w in self.training_set
        ]
        self.assertEqual(len(parsed_lst), len(self.training_set))
        for i in range(3):
            self.assertEqual(len(parsed_lst[i][0]), len(parsed_lst[i][1]))

if __name__ == '__main__':
    unittest.main()
