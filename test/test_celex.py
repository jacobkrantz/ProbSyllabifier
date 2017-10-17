from celex import Celex
import unittest

class TestCelex(unittest.TestCase):

    def test_with_transcription(self):
        transciptionScheme = [
            ['b', 'h', 'z', 'm', '0', 'x', 'Z'],
            ['p', 'C', 'T', '_', 'v'],
            ['k'],
            ['d', 'n'],
            ['$', 'I', 'P', '2', '5', '~'],
            ['@', 'E', 'i', '1', 'u', '7', '8', 'U'],
            ['t', 'N'],
            ['c', 'H', '#', 'r', 'F'],
            ['D', 'j', 'Q', '3', '4', 'V', '9', '{'],
            ['S', 'R', 'l', '6'],
            ['q', 's'],
            ['J', 'w', 'g', 'f']
        ]
        c = Celex()
        c.loadSets(500,25)
        GUID = c.trainHMM(transciptionScheme)
        percentSame = c.testHMM(transciptionScheme, GUID)
        self.assertTrue(percentSame > 0.00)

    def test_without_transcription(self):
        c = Celex()
        c.loadSets(500,25)
        GUID = c.trainHMM([])
        percentSame = c.testHMM([], GUID)
        self.assertTrue(percentSame > 0.00)


if __name__ == '__main__':
    unittest.main()
