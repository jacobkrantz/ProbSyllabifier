import unittest

from celex import Celex


class TestCelex(unittest.TestCase):
    def setUp(self):
        self.celex = Celex()
        self.celex.load_sets(500, 25)
        self.transciptionScheme = [
            ['b', 'h', 'z', 'm', '0', 'x', 'Z'],
            ['p', 'C', 'T', '_', 'v'],
            ['k'],
            ['d', 'n'],
            ['$', 'I', 'P', '2', '5', '~'],
            ['@', 'E', 'i', '1', 'u', '7', '8', 'U'],
            ['t', 'N'],
            ['H', '#', 'r', 'c', 'F'],
            ['D', 'j', 'Q', '3', '4', 'V', '9', '{'],
            ['S', 'R', 'l', '6'],
            ['q', 's'],
            ['J', 'w', 'g', 'f']
        ]

    def tearDown(self):
        self.celex = None
        self.transcriptionScheme = None

    def test_hmmbo(self):
        hmmbo = self.celex.train_hmm(self.transciptionScheme)
        self.assertGreater(len(hmmbo.observationLookup), 0)
        self.assertGreater(len(hmmbo.hiddenLookup), 0)
        self.assertGreater(len(hmmbo.transcriptionScheme), 0)
        self.assertIsNotNone(hmmbo.matrixA)
        self.assertIsNotNone(hmmbo.matrixB)

    def test_with_transcription(self):
        hmmbo = self.celex.train_hmm(self.transciptionScheme)
        percent_same = self.celex.test_hmm(hmmbo)
        self.assertTrue(percent_same > 0.00)

    def test_without_transcription(self):
        hmmbo = self.celex.train_hmm()
        percent_same = self.celex.test_hmm(hmmbo)
        self.assertTrue(percent_same > 0.00)


if __name__ == '__main__':
    unittest.main()
