import sys
import numpy as np

'''
fileName:       utils.py
Authors:        Jacob Krantz
Date Modified:  2/14/17

Common utilies needed for building matrices with a HMM
- outputMatrix
- importMatrix
- makeBigramLst
- makeBigramDict
- makeSyllabDict
- importSyllabDict

'''


class Utils:

    # intialize a matrix using numpy with provided size
    # returns matrix
    def initMatrix(self,size):
        return np.zeros((size,size), dtype=np.float)


    # Given a matrix created with numpy, outputMatrix sends the matrix
    # to a txt file under the provided name.
    def outputMatrix(self, matrix, which):
        if(which == "A"):
            np.savetxt("./HMMFiles/MatrixA.txt",matrix, newline = '\n',header = "MatrixA", footer = "", fmt = '%.5f')
        else:
            np.savetxt("./HMMFiles/MatrixB.txt",matrix, newline = '\n',header = "MatrixB", footer = "", fmt = '%.5f')


    # given the name of a file, imports a matrix using the numpy tool.
    # prints error to console upon failure. 
    def importMatrix(self, fileName):
        try:
            matrix = np.loadtxt(fileName, dtype = 'float') 
        except:
            print(fileName +" does not exist or is corrupt.")
            sys.exit(0)
        return matrix


    # allBigramTups: [[(phone,phone,int),(...),],[...],] where int 
    # corresponds to the type of boundary. 
    # Returns number of unique boundary types.
    def getUniqueBoundCount(self, allBigramLst):
        typeLst = []

        for phoneme in allBigramLst:
            for tup in phoneme:
                if(tup[2] not in typeLst):
                    typeLst.append(tup[2])
            return len(typeLst)


    # phonemeLst: [(phone,phone,int)]
    # returns a list of all 
    def getBoundaryLst(self, phonemeLst):
        boundLst = []

        for tup in phonemeLst:
            boundLst.append(tup[2])

        return boundLst


    # allBigramTups: [[(phone,phone,int),(...),],[...],]
    # counts up every tuple in the list of lists. Returns this count
    def getBoundCount(self, allBigramTups):
        boundCount = 0
        
        for phoneme in allBigramTups:
            for tup in phoneme:
                boundCount += 1

        return boundCount

    # ------------------------------------------------------
    # helper functions below
    # ------------------------------------------------------

