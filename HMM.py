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

        self.syllabDict = {}
        self.syllabLst = []
        self.sylBigramLst = []
        self.sylBigramFreqDict = {}
        self.sylFreqDict = {}
        self.syllabCount = 0


    # goes through process of creating MatrixA for an HMM.
    # MatrixA is the transition probability of going from one
    #     syllible to another.
    # Loads files necessary, builds matrix probabilities,
    #     outputs final matrix to a file "./HMM/MatrixA.txt"
    #     using numpy. Also returns MatrixA.
    def buildMatrixA(self, outFile):
        self.__loadFiles__('A')

        matrixA = self.utils.initMatrix(self.syllabCount)

        matrixA = self.__insertProbA__(matrixA)

        self.utils.outputMatrix(matrixA, "./HMM/MatrixA.txt")

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

        self.utils.outputMatrix(MatrixB, "./HMM/MatrixB.txt")

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

            self.syllabLst = self.utils.makeSylLst(self.syllabDict)
            self.sylBigramLst = self.utils.makeBigramLst(self.syllabDict)
            self.sylBigramFreqDict = self.utils.makesylFreqDict(self.sylBigramLst)
            self.sylFreqDict = self.utils.getSyllableFreq(self.syllabDict)
            self.syllabCount = len(self.syllabLst)

        elif(mode == 'B'):
            return

        else:
            print("Error: mode can be either 'A' or 'B'.")
            sys.exit()

        print("Success: loaded files for " + mode + " matrix.")
        return


    # computes probabilities of a tag given the previous tag
    # populates matrixB with these values as floating point decimals
    def __insertProbA__(self, matrixA):
        for entry in self.sylBigramFreqDict:
            iTag = entry[0]
            jTag = entry[1]

            count  = self.sylBigramFreqDict[entry]
            divisor = self.sylFreqDict[iTag]
            probability = count / float(divisor)

            iIndex = self.syllabLst.index(iTag) #finds index in matrix with tagLst
            jIndex = self.syllabLst.index(jTag)

            matrixA[iIndex,jIndex] = probability

        return matrixA
