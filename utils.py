from SyllabParser import SyllabParser
import sys
import numpy as np

'''
fileName:       utils.py
Authors:        Jacob Krantz
Date Modified:  2/5/17

Common utilies needed for building matrices with a HMM
- outputMatrix
- importMatrix
- getAllBigramTups
- getUniqueBoundCount
- getBoundaryLst
- getBoundCount
- getBoundBigrams

'''


class Utils:

    # intialize a matrix using numpy with provided size: (X,Y)
    # returns matrix
    def initMatrix(self, X, Y):
        return np.zeros((X,Y), dtype=np.float)


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


    # uses SyllabParser to generate a list of lists.
    # allBigramTups: [[(phone,phone,int),(...),],[...],] where int
    # corresponds to the type of boundary.
    def getAllBigramTups(self):
        allBigramTups = []
        sylParser = SyllabParser()

        #allBigramTups = sylParser.parseSyllabs()

        return allBigramTups


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


    # for input phoneme: [(phone,phone,int),(...),]
    # returns a list of tuples containing boundary bigrams.
    # ex: [(0,0),(0,1),(1,0)]
    def getBoundBigrams(self, phoneme):
        boundBigrams = []
        boundLst = []

        for tup in phoneme:
            boundLst.append(tup[2])

        for i in range(1,len(boundLst) - 1):
            tupl = (boundLst[i - 1], boundLst[i])
            boundBigrams.append(tupl)

        return boundBigrams

    # ------------------------------------------------------
    # B Matrix functions below
    # ------------------------------------------------------

    # allBigramTups: [[(phone,phone,int),(...),],[...],]
    # returns the total number of unique bigrams.
    def getNumBigrams(self, allBigramTups):
        bigs = []

        for phoneme in allBigramTups:
            for tup in phoneme:

                bigram = (tup[0],tup[1])
                if bigram not in bigs:
                    bigs.append(bigram)

        return len(bigs)

    # counts and returns the number of boundaries matching
    # the passed in integer within boundaryLst.
    def getNumBounds(self, boundaryLst, match):
        total = 0

        for bound in boundaryLst:
            if(bound == match):
                total += 1

        return total


    # ------------------------------------------------------
    # helper functions below
    # ------------------------------------------------------
