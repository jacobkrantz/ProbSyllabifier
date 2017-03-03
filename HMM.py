from utils import Utils
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

    def __init__(self):
        self.utils = Utils()

        self.boundCount = 0
        self.allBigramTups = []
        self.boundFreqDict = {}
        self.boundLst = []
        self.boundBigrams = []
        self.allBigramTups = []

        self.numBigrams = 0
        self.numYesBounds = 0
        self.numNoBounds = 0
        self.bigramLookup = []

        self.__loadFiles('shared')


    # goes through process of creating MatrixA for an HMM.
    # MatrixA is the transition probability of going from one
    #     boundary to another.
    #
    # for both x and y, 0 is no boundary.
    # for both x and y, 1 is a boundary.
    #
    # Loads files necessary, builds matrix probabilities,
    #     outputs final matrix to a file "./HMM/MatrixA.txt"
    #     using numpy. Also returns MatrixA.
    def buildMatrixA(self):

        self.__loadFiles('A')
        matrixA = self.utils.initMatrix(2,2)

        for phoneme in self.allBigramTups:

            self.boundBigrams = self.utils.getBoundBigrams(phoneme)
            matrixA = self.__insertCountA(matrixA)

        matrixA = self.__normalizeA(matrixA)
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
        MatrixB = self.utils.initMatrix(self.numBigrams,2)

        MatrixB = self.__insertCountB(MatrixB)
        MatrixB = self.__normalizeB(MatrixB)

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
        self.utils.makeLookup([0,1], "./HMMFiles/hiddenLookup.txt")
        self.utils.makeHiddenProb(self.boundLst)


    # return an integer of the number of items that exist in the training set.
    def getTrainingSize(self):
        return len(self.allBigramTups)

    # ------------------------------------------------------
    # helper functions below
    # ------------------------------------------------------


    # loads values into necessary data structures for building the HMM
    # if mode == 'shared', loads data necessary for both matrices
    #       - allBigramTups
    # if mode == 'A', loads data necessary for A matrix
    #       - boundCount
    # if mode == 'B', loads data necessary for B matrix
    #       - boundLst
    #       - numYesBounds
    #       - numNoBounds
    #       - bigramLookup
    #       - numBigrams
    def __loadFiles(self, mode):
        if(mode == 'shared'):

            self.allBigramTups = self.utils.getAllBigramTups()

        elif(mode == 'A'):

            self.boundCount = self.utils.getBoundCount(self.allBigramTups)
            print("Files loaded for A matrix.")

        elif(mode == 'B'):

            self.boundLst = self.utils.getBoundLst(self.allBigramTups)
            self.numYesBounds = self.utils.getNumBounds(self.boundLst, 1)
            self.numNoBounds = self.utils.getNumBounds(self.boundLst, 0)
            self.bigramLookup = self.utils.getBigramLookup(self.allBigramTups)
            self.numBigrams = len(self.bigramLookup)
            print("Files loaded for B matrix.")

        else:
            print("Error: mode can be either 'A', 'B', or 'shared'.")
            sys.exit()

        # test to make sure boundary counts are done correctly
        assert(len(self.boundLst) == self.numNoBounds + self.numYesBounds)
        # test to make sure all items in lookup are unique
        assert(len(self.bigramLookup) == len(set(self.bigramLookup)))


    # inserts the count of a tag given the previous tag
    # populates matrixA with these values and return matrixA
    def __insertCountA(self, matrixA):

        for bigramTup in self.boundBigrams:
            if(bigramTup == (0,0)):
                matrixA[0,0] = matrixA[0,0] + 1

            elif(bigramTup == (0,1)):
                matrixA[0,1] = matrixA[0,1] + 1

            elif(bigramTup == (1,0)):
                matrixA[1,0] = matrixA[1,0] + 1

            elif(bigramTup == (1,1)):
                matrixA[1,1] = matrixA[1,1] + 1

        return matrixA


    # normalizes the counts in matrix A to be probabilities by
    # dividing each count by the total number of bigrams trained on.
    # probablilites inserted as floating point decimals. Returns matrixA.
    def __normalizeA(self, matrixA):
        totFloat = matrixA[0,0] + matrixA[0,1] + matrixA[1,0] + matrixA[1,1]
        totFloat = float(totFloat)

        matrixA[0,0] = matrixA[0,0] / totFloat
        matrixA[0,1] = matrixA[0,1] / totFloat
        matrixA[1,0] = matrixA[1,0] / totFloat
        matrixA[1,1] = matrixA[1,1] / totFloat

        return matrixA


    # inserts the count of a bigram given a boundary
    # populates matrixB with these values and return matrixB
    def __insertCountB(self, MatrixB):

        for phoneme in self.allBigramTups:
            for bigram in phoneme:

                tup = (bigram[0],bigram[1])
                i = self.bigramLookup.index(tup)

                if(bigram[2] == 0): # increment no boundary count
                    MatrixB[i, 0] = MatrixB[i, 0] + 1

                else: # increment yes boundary count
                    MatrixB[i, 1] = MatrixB[i, 1] + 1

        return MatrixB


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
