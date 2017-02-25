from utils import Utils
import sys


'''
fileName:       HMM.py
Authors:        Jacob Krantz
Date Modified:  2/14/17

- Builds A and B matrices of an HMM
- Necessary files:
    - ./HMM/SyllabDict.txt      *contains dict of [word]:syllabification
    -
- Functions:
    - buildMatrixA()
    - buildMatrixB()
'''
class HMM:

    def __init__(self):
        self.utils = Utils()

        self.uniqueBoundCount = 2
        self.boundCount = 0
        self.allBigramTups = []
        self.boundFreqDict = {}
        self.boundLst = []
        self.boundBigrams = [] # how to update this for each entry?

        self.numBigrams = 0
        self.numYesBounds = 0
        self.numNoBounds = 0



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
    def buildMatrixA(self, outFile):

        self.__loadFiles__('A')
        matrixA = self.utils.initMatrix(self.bigramCount, self.bigramCount)

        for phoneme in self.AllBigramTups:

            self.boundBigrams = self.utils.getBoundBigrams(phoneme)
            matrixA = self.__insertCountA__(matrixA)

        matrixA = __normalizeA__(matrixA)
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

        self.__loadFiles__('B')
        MatrixB = self.utils.initMatrix(self.numBigrams,2)

        MatrixB = self.__insertCountB__(MatrixB)
        MatrixB = self.__normalizeB__(Matrix)

        self.utils.outputMatrix(MatrixB, "B")

        return MatrixB



    # ------------------------------------------------------
    # helper functions below
    # ------------------------------------------------------


    # loads values into necessary data structures for building the HMM
    #       - allBigramTups
    #       - uniqueBoundCount
    #       - boundaryLst
    # if mode == 'A', loads data necessary for A matrix
    #       - boundCount
    # if mode == 'B', loads data necessary for B matrix
    #       - numBigrams
    def __loadFiles__(self,mode):

        self.allBigramTups = self.utils.getAllBigramTups()
        self.uniqueBoundCount = self.utils.getUniqueBoundCount(self.AllBigramTups)
        self.boundaryLst = self.utils.getBoundaryLst(bigramTups)

        if(mode == 'A'):

            self.boundCount = self.utils.getBoundCount(self.allBigramTups)

        elif(mode == 'B'):

            self.numBigrams = self.utils.getNumBigrams(self.allBigramTups)
            self.numYesBounds = self.utils.getNumBounds(self.boundaryLst, 1)
            self.numNoBounds = self.utils.getNumBounds(self.boundaryLst, 0)


        else:
            print("Error: mode can be either 'A' or 'B'.")
            sys.exit()

        print("Success: loaded files for " + mode + " matrix.")
        return


    # inserts the count of a tag given the previous tag
    # populates matrixA with these values and return matrixA
    def __insertCountA__(self, matrixA):

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
    def __normalizeA__(self, matrixA):
        totFloat = float(self.boundCount)

        matrixA[0,0] = matrixA[0,0] / totFloat
        matrixA[0,1] = matrixA[0,1] / totFloat
        matrixA[1,0] = matrixA[1,0] / totFloat
        matrixA[1,1] = matrixA[1,1] / totFloat

        return matrixA


    # inserts the count of a boundary given a bigram
    # populates matrixA with these values and return matrixB
    def __insertCountB__(self, MatrixB):
        return


    # normalizes the counts in matrix A to be probabilities by
    # dividing each count by the total number of boundaries trained on.
    # probablilites inserted as floating point decimals. Returns matrixB.
    def __normalizeB__(self, MatrixB):
        # normalize yes and no bounds separately
        return
