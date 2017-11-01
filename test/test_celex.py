from celex import Celex
import unittest

class TestCelex(unittest.TestCase):

    def setUp(self):
        self.celex = Celex()
        self.celex.loadSets(500,25)
        self.transciptionScheme = [
            ['b','h','z','m','0','x','Z'],
            ['p','C','T','_','v'],
            ['k'],
            ['d','n'],
            ['$','I','P','2','5','~'],
            ['@','E','i','1','u','7','8','U'],
            ['t','N'],
            ['H','#','r','c','F'],
            ['D','j','Q','3','4','V','9','{'],
            ['S','R','l','6'],
            ['q','s'],
            ['J','w','g','f']
        ]

    def tearDown(self):
        self.celex = None
        self.transcriptionScheme = None

    def test_hmmbo(self):
        HMMBO = self.celex.trainHMM(self.transciptionScheme)
        self.assertGreater(len(HMMBO.observationLookup), 0)
        self.assertGreater(len(HMMBO.hiddenLookup), 0)
        self.assertGreater(len(HMMBO.transcriptionScheme), 0)
        self.assertIsNotNone(HMMBO.matrixA)
        self.assertIsNotNone(HMMBO.matrixB)

    def test_with_transcription(self):
        HMMBO = self.celex.trainHMM(self.transciptionScheme)
        percentSame = self.celex.testHMM(HMMBO)
        self.assertTrue(percentSame > 0.00)

    def test_without_transcription(self):
        HMMBO = self.celex.trainHMM()
        percentSame = self.celex.testHMM(HMMBO)
        self.assertTrue(percentSame > 0.00)


if __name__ == '__main__':
    unittest.main()
