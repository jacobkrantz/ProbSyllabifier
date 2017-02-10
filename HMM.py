from utils import Utils
import sys

'''
fileName:       HMM.py
Authors:        Jacob Krantz
Date Modified:  2/9/17

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
        self.syllabCount = 0
        self.matrixA




    # goes through process of creating MatrixA for an HMM.
    # MatrixA is the transition probability of going from one
    #     syllible to another.
    # Loads files necessary, builds matrix probabilities,
    #     outputs final matrix to a file "./HMM/MatrixA.txt"
    #     using numpy.
    def buildMatrixA(self):
        self.__loadFiles__('A')

        self.utils.outputMatrix(MatrixA, "./HMM/MatrixA.txt")
        return


    # goes through process of creating MatrixB for an HMM.
    # MatrixB is...
    # 
    # Loads files necessary, builds matrix probabilities,
    #     outputs final matrix to a file "./HMM/MatrixB.txt"
    #     using numpy.
    def buildMatrixB(self):
        self.__loadFiles__('B')

        self.utils.outputMatrix(MatrixB, "./HMM/MatrixB.txt")
        return 



    # ------------------------------------------------------
    # helper functions below
    # ------------------------------------------------------


    # loads values into necessary data structures for building the HMM
    # if mode == 'A', loads data necessary for A matrix
    #       - syllabDict
    #       - syllabLst
    #       - sylBigramLst
    #       - bigramFreqDict
    #       - syllabCount
    # if mode == 'B', loads data necessary for B matrix
    def __loadFiles__(self,mode):
        if(mode == 'A'):

            self.syllabDict = utils.importSyllabDict("HMMFiles/SyllabDict.txt")

            self.syllabLst = utils.makeSylLst(self.syllabDict)
            self.sylBigramLst = []
            self.sylBigramFreqDict = {}
            self.syllabCount = 0

        elif(mode == 'B'):
            return

        else:
            print("Error: mode can be either 'A' or 'B'.")
            sys.exit()

        print("Success: loaded files for " + mode + " matrix.")
        return
