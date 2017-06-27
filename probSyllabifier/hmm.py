from utils import HMMUtils
import numpy as np
import sys

'''
fileName:       HMM.py
Authors:        Jacob Krantz
Date Modified:  3/3/17

- Builds A and B matrices of an HMM
- Necessary files:
    - ./HMM/SyllabDict.txt  *contains dict of [word]:syllabification
    - ./utils.py            *utilities for training HMM
    - ./SyllabParser.py     *parses the syllabification dictionary file
- Functions:
    - buildMatrixA()
    - buildMatrixB()
    - makeViterbiFiles()
    - getTrainingSize()
'''
class HMM:

    #takes in 1 for Arpabet and 2 for IPA
    def __init__(self,lang, trainingSet=[]):
        self.utils = HMMUtils()
        self.lang = lang
        self.allBigramTups = self._loadTrainingData(trainingSet)
        self.boundCount = 0
        self.boundFreqDict = {}
        self.boundLst = []
        self.tagBigrams = []

        self.numBigrams = 0
        self.numYesBounds = 0
        self.numNoBounds = 0
        self.bigramLookup = []
        self.tagDict = {}
        self.tagLookup = []

        self.__loadFiles('shared')


    # goes through process of creating MatrixA for an HMM.
    # MatrixA is the transition probability of going from one
    #     boundary to another.
    #
    # for both x and y, 0 is no boundary.
    # for both x and y, 1 is a boundary.
    # each entry is normalized by prior tag count.
    #
    # Loads files necessary, builds matrix probabilities,
    #     outputs final matrix to a file "./HMM/MatrixA.txt"
    #     using numpy. Also returns MatrixA.
    def buildMatrixA(self):

        self.__loadFiles('A')

        for phoneme in self.allBigramTups:
            self.tagBigrams += self.utils.getTagBigrams(phoneme)

        tagBigramDict = self.utils.buildTagBigramDict(self.tagBigrams)
        matrixA = self.__insertProbA(tagBigramDict)

        self.utils.outputMatrix(matrixA, "A")

        return matrixA


    # goes through process of creating MatrixB for an HMM.
    # MatrixB is...
    #
    # for y direction, 0 is no boundary and 1 is a boundary
    #
    # Loads files necessary, builds matrix probabilities,
    #     outputs final matrix to a file "./HMM/MatrixB.txt"
    #     using numpy. Also returns MatrixB.
    def buildMatrixB(self):

        self.__loadFiles('B')
        MatrixB = self.utils.initMatrix(self.numBigrams,len(self.tagLookup))

        MatrixB = self.__insertCountB(MatrixB)
        MatrixB = self.normalizeNaiveB(MatrixB)
        #MatrixB = self.__normalizeB(MatrixB)

        self.utils.outputMatrix(MatrixB, "B")

        return MatrixB


    # creates files that allow the Viterbi algorithm to use the matrices
    # created. Creates files:
    # - ./HMMFiles/obsLookup.txt
    # - ./HMMFiles/hiddenLookup.txt
    # - ./HMMFiles/hiddenProb.txt
    def makeViterbiFiles(self):

        if(len(self.boundLst) == 0):
            self.__loadFiles('B')
        elif(len(self.bigramLookup) == 0):
            self.__loadFiles('B')

        self.utils.makeLookup(self.bigramLookup,"./HMMFiles/obsLookup.txt")
        self.utils.makeLookup(self.tagDict, "./HMMFiles/hiddenLookup.txt")
        self.utils.makeHiddenProb(self.boundLst)


    # return an integer of the number of items that exist in the training set.
    def getTrainingSize(self):
        return len(self.allBigramTups)

    # ------------------------------------------------------
    # helper functions below
    # ------------------------------------------------------

    def _loadTrainingData(self, trainingSet):
        if len(trainingSet) == 0:   # from nist
            return self.utils.getNistBigramTups()
        return self.utils.parseCelexTrainingSet(trainingSet)



    # loads values into necessary data structures for building the HMM
    # if mode == 'shared', loads data necessary for both matrices
    #       - allBigramTups
    #       - tagDict
    #       - tagLookup
    # if mode == 'A', loads data necessary for A matrix
    #       - boundCount
    # if mode == 'B', loads data necessary for B matrix
    #       - boundLst
    #       - numYesBounds
    #       - numNoBounds
    #       - bigramLookup
    #       - numBigrams
    #       - bigramFreqDict
    def __loadFiles(self, mode):
        if(mode == 'shared'):
            self.tagDict, self.tagLookup = self.utils.getTagLookup(self.allBigramTups,self.lang)
            self.allBigramTups = self.utils.expandTags(self.allBigramTups,self.lang)

        elif(mode == 'A'):
            self.boundCount = self.utils.getBoundCount(self.allBigramTups)
            print("Files loaded for A matrix.")

        elif(mode == 'B'):
            self.bigramLookup = self.utils.getBigramLookup(self.allBigramTups)
            self.numBigrams = len(self.bigramLookup)
            self.bigramFreqDict = self.utils.getBigramFreqDict(self.allBigramTups, self.numBigrams)
            print("Files loaded for B matrix.")

        else:
            print("Error: mode can be either 'A', 'B', or 'shared'.")
            sys.exit()

        # test to make sure boundary counts are done correctly
        assert(len(self.boundLst) == self.numNoBounds + self.numYesBounds)
        # test to make sure all items in lookup are unique
        assert(len(self.bigramLookup) == len(set(self.bigramLookup)))


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

    '''
    # normalizes the counts in matrix A to be probabilities by
    # dividing each count by the total number of boundaries trained on.
    # probablilites inserted as floating point decimals. Returns matrixB.
    def __normalizeB(self, MatrixB):

        for i in range(0,self.numBigrams):
            assert(MatrixB[i,0] + MatrixB[i,1] != 0)

            # normalize yes and no bounds separately
            MatrixB[i, 0] = MatrixB[i, 0] / float(self.numNoBounds)
            MatrixB[i, 1] = MatrixB[i, 1] / float(self.numYesBounds)

        return MatrixB
    '''

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


if(__name__ == "__main__"):
    # train whole machine
    H = HMM()
    H.buildMatrixA()
    H.buildMatrixB()
    H.makeViterbiFiles()
