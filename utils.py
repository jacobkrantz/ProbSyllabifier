import sys
import numpy as np

'''
Common utilies needed for building matrices with a HMM
- outputMatrix
- importMatrix
- makeBigramLst
- makeBigramDict
- makeSyllabDict
- importSyllabDict

#file i o
#structure analysis
#syllab?
#parse syllab dict
'''


class Utils:

    # Given a matrix created with numpy, outputMatrix sends the matrix
    # to a txt file under the provided name.
    def outputMatrix(self, matrix, fileName):
        np.savetxt("matrixA.txt",matrix, newline = '\n',header = fileName - ".txt", footer = "", fmt = '%.10f')


    # given the name of a file, imports a matrix using the numpy tool.
    # prints error to console upon failure. 
    def importMatrix(self, fileName):
        try:
            matrix = np.loadtxt(fileName, dtype = 'float') 
        except:
            print(fileName +" does not exist or is corrupt.")
            sys.exit(0)
        return matrix


    # given a list, returns a bigram list.
    # ex: in: [1,2,3,4] out: [(1,2),(2,3),(3,4)] 
    def makeBigramLst(self, lst):
        bigrams = []
        for i in range(0,len(lst) - 1):
            tup = (lst[i],lst[i+1])
            bigrams.append(tup)
        return bigrams


    # adds bigrams and their respective frequencies into a dictionary
    def makeBigramDict(bigramLst):
        bigramDict = {}
        for i in bigramLst:
            if i in bigramDict:
                bigramDict[i] += 1
            else:
                bigramDict[i] = 1
        return bigramDict


    # change this function when we know what our input looks like
    # currently converts dictionary keys into list. 
    # Added by greatest to least counts
    def makeSyllableLst(tagDict):
        tagLst = []

        for i in range(0,len(tagDict)):
            largest = max(tagDict, key=tagDict.get)
            tagLst.append(largest)
            del tagDict[largest]
        return tagLst

    # given a file name, imports as a dictionary.
    # input expected as:  word [syl][syl]...[syl]
    def importSyllabDict(self, fileName):
        syllabDict = {}

        try:

            sylFile = open(fileName, 'r')

            for line in sylFile:

                splitLine = line.strip('\n')
                splitLine = splitLine.split(' ',1)
                dictValue = self.__parseSyllabsIn__(str(splitLine[1]))

                syllabDict[splitLine[0]] = dictValue
    
        except:

            print (fileName+" does not exist or is not in proper form.")

        return syllabDict


    # -------------------------------------------------
    # helper functions below
    # -------------------------------------------------

    # helper for importSyllabDict.
    # parses the dict value beginning as a continuous string
    # ends as a list of syllable strings.
    # IMPORTANT: inserts start and end tags. 
    # ex: ["<s>","s er","t ah n","l iy","</s>"]
    def __parseSyllabsIn__(self, syllabString):
        fullSyllab = ["<s>"]

        splitLst = syllabString.split(']')

        for syllable in splitLst:

            fullSyllab.append(syllable.strip('[ '))
            
        fullSyllab = fullSyllab[0:-1]  # removes blank syllable
        fullSyllab.append("</s>")

        return fullSyllab

