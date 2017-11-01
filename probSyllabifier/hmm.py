from utils import HMMUtils
from HMMBO import HMMBO

class HMM:
    """ Trains a Hidden Markov Model with provided training data. """

    def __init__(self, lang, transcriptionScheme, trainingSet=[]):
        """
        Args:
            lang (int): 1 for NIST, 2 for CELEX.
            transcriptionScheme (list of sets of phones):
                                        should be '[]' if not used.
            trainingSet (list of strings): optional set of words to train from.
                                        Must be populated if lang = 2 (CELEX)
        """
        self.utils = HMMUtils()
        self.HMMBO = HMMBO()
        self.HMMBO.transcriptionScheme = transcriptionScheme
        self.allBigramTups = self._loadTrainingData(trainingSet)
        self.tagDict       = {}
        self.bigramLookup  = []
        self.tagLookup     = []
        self._loadStructures(lang, transcriptionScheme)

    def train(self):
        """
        Trains all structures needed for the Hidden Markov Model.
        Fills out all attributes of the HMMBO accordingly.
        Returns:
            HMMBO: business object containing training information.
        """
        self.HMMBO.matrixA = self._buildMatrixA()
        self.HMMBO.matrixB = self.buildMatrixB()
        self.HMMBO.observationLookup = self.bigramLookup
        self.HMMBO.hiddenLookup = self.tagLookup
        return self.HMMBO

    def getTrainingSize(self):
        """
        Returns:
            int: number of syllabified words in the training set.
        """
        return len(self.allBigramTups)

    # ------------------------------------------------------
    # helper functions below
    # ------------------------------------------------------

    def _buildMatrixA(self):
        """
        Goes through process of creating MatrixA for an HMM.
        MatrixA is the transition probability of going from one
             boundary to another.

        for both x and y, 0 is no boundary.
        for both x and y, 1 is a boundary.
        each entry is normalized by prior tag count.

        Returns:
            numpy matrix: matrixA transition probabilities
        """
        tagBigrams = []
        for phoneme in self.allBigramTups:
            tagBigrams += self.utils.getTagBigrams(phoneme)

        tagBigramDict = self.utils.buildTagBigramDict(tagBigrams)
        matrixA = self.__insertProbA(tagBigramDict)
        return matrixA

    def buildMatrixB(self):
        """
        Goes through the process of creating MatrixB for an HMM.
        For y direction, 0 is no boundary and 1 is a boundary.

        Returns:
            numpy matrix: matrixB hidden state prior probabilities
        """
        matrixB = self.utils.initMatrix(len(self.bigramLookup),len(self.tagLookup))
        matrixB = self.__insertCountB(matrixB)
        matrixB = self.normalizeNaiveB(matrixB)
        return matrixB

    def _loadTrainingData(self, trainingSet):
        """
        Args:
            trainingSet(list of strings): set of words to train from. Can be empty.
        Returns:
            List of lists of tuples: [[(phone,phone,int),(...),],[...],] where
                            int is 0 for no boundary 1 for yes boundary.
        """
        if len(trainingSet) == 0:   # from nist
            return self.utils.getNistBigramTups()
        return self.utils.parseCelexTrainingSet(trainingSet)

    def _loadStructures(self, lang, transcriptionScheme):
        """ loads necessary data structures for building the HMM """
        self.tagDict, self.tagLookup = self.utils.getTagLookup(self.allBigramTups,lang, transcriptionScheme)
        self.allBigramTups = self.utils.expandTags(self.allBigramTups,lang,transcriptionScheme)
        self.bigramLookup = self.utils.getBigramLookup(self.allBigramTups)
        self.bigramFreqDict = self.utils.getBigramFreqDict(self.allBigramTups, len(self.bigramLookup))
        self._filesDidLoad()

    def __insertProbA(self, tagBigramDict):
        """
        Inserts the count of a tag given the previous tag
        populates matrixA with these values after normalizing the
        probabilities by the occurance count of the prior tag (tagDict).
        Args:
            tagBigramDict (dictionary <(string,string), int>): bigram of tags
                                with value being number of occurrances.
        Returns:
            numpy matrix: matrixA
        """
        matrixA = self.utils.initMatrix(len(self.tagLookup),len(self.tagLookup))
        for entry in tagBigramDict:
            iTag = entry[0]
            jTag = entry[1]

            count = tagBigramDict[entry]         # Count of tag bigram occurrances
            divisor = self.tagDict[iTag]         # Count of the iTags
            probability = count / float(divisor) # normalizes the probability
            iIndex = self.tagLookup.index(iTag)  # use tagLookup for matrix location
            jIndex = self.tagLookup.index(jTag)

            matrixA[iIndex,jIndex] = probability # inserts prob into the matrix

        return matrixA

    def __insertCountB(self, MatrixB):
        """
        Inserts the count of a bigram given a boundary.
        Populates matrixB with these values.
        Args:
            matrixB (numpy matrix)
        Returns:
            numpy matrix: matrixB
        """
        for phoneme in self.allBigramTups:
            for bigram in phoneme:
                tup = (bigram[0],bigram[1])
                i = self.bigramLookup.index(tup)
                j = self.tagLookup.index(bigram[2]) # current tag
                MatrixB[i, j] = MatrixB[i, j] + 1
        return MatrixB

    def normalizeNaiveB(self, MatrixB):
        """
        Normaliziation strategy: divide all MatrixB entries by the probability
        of the bigram occurring.
        Args:
            matrixB (numpy matrix)
        Returns:
            numpy matrix: matrixB
        """
        for i, bigram in enumerate(self.bigramLookup):
            bigramProb = self.bigramFreqDict[bigram]
            for j in range(0, len(self.tagLookup)):     # loop through each tag
                MatrixB[i,j] = MatrixB[i,j] / float(bigramProb)
        return MatrixB

    def _filesDidLoad(self):
        """ Ensures all structures are loaded. Fail fast. """
        assert(len(self.tagDict)        != 0)
        assert(len(self.tagLookup)      != 0)
        assert(len(self.allBigramTups)  != 0)
        assert(len(self.bigramLookup)   != 0)
        assert(len(self.bigramFreqDict) != 0)
        assert(len(self.bigramLookup)   != 0)

        # All items in lookup must be unique
        assert(len(self.bigramLookup) == len(set(self.bigramLookup)))
