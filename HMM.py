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
        matrixA = self.utils.initMatrix(self.bigramCount)

        for phoneme in self.AllBigramTups:

            self.boundBigrams = self.utils.getBoundBigrams(phoneme)
            matrixA = self.__insertCountA__(matrixA)

        matrixA = __normalizeA__(matrixA)
        self.utils.outputMatrix(matrixA, "A")

        return matrixA


    # goes through process of creating MatrixB for an HMM.
    # MatrixB is...
    # 
    # Loads files necessary, builds matrix probabilities,
    #     outputs final matrix to a file "./HMM/MatrixB.txt"
    #     using numpy. Also returns MatrixB. 
    def buildMatrixB(self):

        self.__loadFiles__('B')

        MatrixB = 0 # placeholder

        self.utils.outputMatrix(MatrixB, "B")

        return MatrixB



    # ------------------------------------------------------
    # helper functions below
    # ------------------------------------------------------


    # loads values into necessary data structures for building the HMM
    # if mode == 'A', loads data necessary for A matrix
    #       - syllabDict
    #       - syllabLst
    #       - sylBigramLst
    #       - bigramFreqDict
    #       - syllabFreqDict
    #       - syllabCount
    # if mode == 'B', loads data necessary for B matrix
    def __loadFiles__(self,mode):
        if(mode == 'A'):

            self.syllabDict = self.utils.importSyllabDict("HMMFiles/SyllabDict.txt")
            self.allBigramTups = self.utils.getAllBigramTups()
            self.uniqueBoundCount = self.utils.getUniqueBoundCount(self.AllBigramTups)
            self.boundaryLst = self.utils.getBoundaryLst(bigramTups)
            self.boundCount = self.utils.getBoundCount(self.allBigramTups)

        elif(mode == 'B'):
            return

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



