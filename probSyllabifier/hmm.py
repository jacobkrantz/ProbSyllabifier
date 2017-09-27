from utils import HMMUtils
import os

'''
fileName:       HMM.py
Authors:        Jacob Krantz
Date Modified:  9/17

- Builds A and B matrices of an HMM
- Functions:
    - buildMatrixA()
    - buildMatrixB()
    - makeViterbiFiles()
    - getTrainingSize()
'''
class HMM:

    # lang = 1 for NIST.
    # lang = 2 for CELEX. `trainingSet` must be populated for CELEX.
    # transcriptionScheme should be [] if not used.
    def __init__(self, lang, transcriptionScheme, trainingSet=[]):
        self.utils = HMMUtils()
        self.lang = lang
        self.allBigramTups = self._loadTrainingData(trainingSet)
        self.transcriptionScheme = transcriptionScheme
        self.boundFreqDict = {}
        self.tagDict       = {}
        self.bigramLookup  = []
        self.tagBigrams    = []
        self.tagLookup     = []
        self.boundCount    = 0
        self.numBigrams    = 0
        self.GUID          = ""
        self.__loadFiles()

    def setGUID(self, GUID):
        self.GUID = GUID

    # goes through process of creating MatrixA for an HMM.
    # MatrixA is the transition probability of going from one
    #     boundary to another.
    #
    # for both x and y, 0 is no boundary.
    # for both x and y, 1 is a boundary.
    # each entry is normalized by prior tag count.
    #
    # builds matrix probabilities,
    #     outputs final matrix to a file "./HMM/MatrixA.txt"
    #     using numpy. Also returns MatrixA.
    def buildMatrixA(self):
        for phoneme in self.allBigramTups:
            self.tagBigrams += self.utils.getTagBigrams(phoneme)

        tagBigramDict = self.utils.buildTagBigramDict(self.tagBigrams)
        matrixA = self.__insertProbA(tagBigramDict)
        self.utils.outputMatrix(matrixA, "MatrixA" + self.GUID, "A")

        return matrixA


    # goes through process of creating MatrixB for an HMM.
    # MatrixB is...
    #
    # for y direction, 0 is no boundary and 1 is a boundary
    #
    # builds matrix probabilities,
    #     outputs final matrix to a file "./HMM/MatrixB.txt"
    #     using numpy.
    def buildMatrixB(self):
        MatrixB = self.utils.initMatrix(self.numBigrams,len(self.tagLookup))
        MatrixB = self.__insertCountB(MatrixB)
        MatrixB = self.normalizeNaiveB(MatrixB)

        self.utils.outputMatrix(MatrixB, "MatrixB" + self.GUID, "B")


    # creates files that allow the Viterbi algorithm to use the matrices
    # created. Creates files:
    # - ./HMMFiles/obsLookup{GUID}.txt
    # - ./HMMFiles/hiddenLookup{GUID}.txt
    def makeViterbiFiles(self):
        obsLookupName = "./HMMFiles/obsLookup" + self.GUID + ".txt"
        hiddenLookupName = "./HMMFiles/hiddenLookup" + self.GUID + ".txt"
        try:
            self._filesDidLoad()
        except Exception as e:
            print "reload", e
            self.__loadFiles()
        finally:
            self.utils.makeLookup(self.bigramLookup, obsLookupName)
            self.utils.makeLookup(self.tagDict, hiddenLookupName)

    # return an integer of the number of items that exist in the training set.
    def getTrainingSize(self):
        return len(self.allBigramTups)

    # remove files containing the GUID
    def clean(self):
        if self.GUID == "":
            return

        source = "./HMMFiles/"
        for f in os.listdir(source):
            if self.GUID in f:
                os.remove(source + f)

    # ------------------------------------------------------
    # helper functions below
    # ------------------------------------------------------

    def _loadTrainingData(self, trainingSet):
        if len(trainingSet) == 0:   # from nist
            return self.utils.getNistBigramTups()
        return self.utils.parseCelexTrainingSet(trainingSet)


    # loads values into necessary data structures for building the HMM
    #       - allBigramTups
    #       - tagDict
    #       - tagLookup
    #       - bigramLookup
    #       - numBigrams
    #       - bigramFreqDict
    def __loadFiles(self):
        if len(self.tagDict) != 0:
            assert(False)
        self.tagDict, self.tagLookup = self.utils.getTagLookup(self.allBigramTups,self.lang, self.transcriptionScheme)
        self.allBigramTups = self.utils.expandTags(self.allBigramTups,self.lang,self.transcriptionScheme)
        #print self.allBigramTups
        self.bigramLookup = self.utils.getBigramLookup(self.allBigramTups)
        self.numBigrams = len(self.bigramLookup)
        self.bigramFreqDict = self.utils.getBigramFreqDict(self.allBigramTups, self.numBigrams)
        self._filesDidLoad()

    # inserts the count of a tag given the previous tag
    # populates matrixA with these values after normalizing the
    # probabilities by the occurance count of the prior tag (tagDict).
    # Param 1: a dictionary of bigrams as the key: value is the number of occuarances
    def __insertProbA(self, tagBigramDict):
        #makes a matrix as big as the the tagLookUp is. X = Y.
        xy = len(self.tagLookup)

        matrixA = self.utils.initMatrix(xy,xy)

        for entry in tagBigramDict:
            iTag = entry[0]
            jTag = entry[1]

            #the total count of times that the bigram of tags appears in the order
            count = tagBigramDict[entry]
            #This is the count of the iTag's that we need to normalize it.
            divisor = self.tagDict[iTag]
            #normalizes the probability
            probability = count / float(divisor)

            #these find the index of where they should be on matrixA
            #tagLookup cooresponds to the spot on the matrix
            iIndex = self.tagLookup.index(iTag)
            jIndex = self.tagLookup.index(jTag)

            #sets the value into the matrix
            matrixA[iIndex,jIndex] = probability

        return matrixA


    # inserts the count of a bigram given a boundary
    # populates matrixB with these values and return matrixB
    # Param 1: A matrix
    def __insertCountB(self, MatrixB):
        for phoneme in self.allBigramTups:
            for bigram in phoneme:
                tup = (bigram[0],bigram[1])
                i = self.bigramLookup.index(tup)

                # easy test for bigram occurance
                #if(tup == ('ae','l')):
                #    print bigram

                curTag = bigram[2]
                j = self.tagLookup.index(curTag)
                MatrixB[i, j] = MatrixB[i, j] + 1

        return MatrixB


    # normaliziation strategy: divide all MatrixB entries by the probability
    # of the bigram occurring.
    # Param 1: The matrix that is to be normalized
    def normalizeNaiveB(self, MatrixB):
        for i in range(0, self.numBigrams):     # loop through each phone bigram
            bigram = self.bigramLookup[i]
            bigramProb = self.bigramFreqDict[bigram]
            for j in range(0, len(self.tagLookup)):     # loop through each tag
                MatrixB[i,j] = MatrixB[i,j] / float(bigramProb)

        return MatrixB




    # called to ensure class structures are all loaded. Fail fast.
    def _filesDidLoad(self):
        assert(len(self.tagDict)        != 0)
        assert(len(self.tagLookup)      != 0)
        assert(len(self.allBigramTups)  != 0)
        assert(len(self.bigramLookup)   != 0)
        assert(len(self.bigramFreqDict) != 0)
        assert(self.numBigrams          != 0)

        # All items in lookup must be unique
        assert(len(self.bigramLookup) == len(set(self.bigramLookup)))
