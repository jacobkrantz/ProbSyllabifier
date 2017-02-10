from utils import Utils
import sys

'''
*****Hidden Markov Model Matrix Builder*****
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

        self.syllableLst = []
        self.sylBigramLst = []
        self.sylBigramDict = {}
        self.matrixA




    # goes through process of creating MatrixA for any HMM
    # Loads files necessary, builds matrix probabilities,
    #     outputs final matrix to a file "./HMM/MatrixA.txt"
    #     using numpy
    def buildMatrixA(self):
        self.__loadFiles__('A')

        self.utils.outputMatrix(MatrixA, "./HMM/MatrixA.txt")
        return


    def buildMatrixB(self):
        self.__loadFiles__('B')

        self.utils.outputMatrix(MatrixB, "./HMM/MatrixB.txt")
        return 



    # ------------------------------------------------------
    # helper functions below
    # ------------------------------------------------------


    # loads values into necessary data structures for building the HMM
    # if mode == 'A', loads data necessary for A matrix
    # if mode == 'B', loads data necessary for B matrix
    def __loadFiles__(self,mode):
        if(mode == 'A'):
        self.syllabDict = utils.importSyllabDict("HMMFiles/SyllabDict.txt")

        elif(mode == 'B'):
            return

        else:
            print("Error: mode can be either 'A' or 'B'.")
            sys.exit()

        print("Success: loaded files for " + mode + " matrix.")
        return
