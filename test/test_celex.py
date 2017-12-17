import unittest

from celex import Celex


class TestCelex(unittest.TestCase):
    def setUp(self):
        self.celex = Celex()
        self.celex.load_sets(500, 25)
        self.transcription_scheme = [
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
        hmmbo = self.celex.train_hmm(self.transcription_scheme)
        self.assertGreater(len(hmmbo.observation_lookup), 0)
        self.assertGreater(len(hmmbo.hidden_lookup), 0)
        self.assertGreater(len(hmmbo.transcription_scheme), 0)
        self.assertIsNotNone(hmmbo.matrix_a)
        self.assertIsNotNone(hmmbo.matrix_b)

    def test_with_transcription(self):
        hmmbo = self.celex.train_hmm(self.transcription_scheme)
        percent_same, test_results = self.celex.test_hmm(hmmbo)
        self.assertTrue(percent_same > 0.00)
        self.assertIsNotNone(test_results)

    def test_without_transcription(self):
        hmmbo = self.celex.train_hmm()
        percent_same, test_results = self.celex.test_hmm(hmmbo)
        self.assertTrue(percent_same > 0.00)
        self.assertIsNotNone(test_results)


if __name__ == '__main__':
    unittest.main()
