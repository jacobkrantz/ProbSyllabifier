from utils import SyllabParser

'''
fileName:       testing.py
Authors:        Jacob Krantz
Date Modified:  3/14/17

Contains classes for testing the perfomance of Sylabifiers.
- CompareNIST
    * compare
    * viewDifferences
'''
class CompareNIST:

    def __init__(self):
        self.sParser = SyllabParser()
        self.__difLst = []
        self.__nSyllabs  = []
        self.__cSyllabs = []

    # compares the syllabifications of compFile to those done by NIST.
    # Printed percentage is how accurate compFile is to NISTfile.
    # Both compFile and NISTfile must be in specific formats.
    def compare(self, NISTfile, compFile):
        self.__nSyllabs = self.__importFile(NISTfile)
        self.__cSyllabs = self.__importFile(compFile)

        percentSim = self.__runComparison()
        self.__outputResults(percentSim)


    # prints the differences between NIST and the compared file
    def viewDifferences(self):
        for i in range(1, len(self.__difLst), 2):
            #This should also print the word; but this would require
            #the datatype to change from a list into a dictionary
            #or for two different lists to be present.
            print "Word: "
            print("NIST: "),
            print(self.__difLst[i-1])
            print("Prob: "),
            print(self.__difLst[i])
            print

        self.__difLst = []


    # ------------------------------------------------------
    # Private functions below
    # ------------------------------------------------------

    # Imports a file that is formatted like 'SyllabDict.txt'.
    # Parses file with SyllabParser and returns result (list of lists).
    def __importFile(self, fileName):
        return self.sParser.makePhonemeLst(fileName)

    # assumes that the ordering of nSyllabs is the same as cSyllabs.
    # iterates through both datasets. For each that are the same, adds
    # to same count. Also counts total entries. Returns percent.
    def __runComparison(self):
        end = len(self.__cSyllabs)
        sameCount = 0
        nSylIndex = 0
        same = True

        for i in range(0, end): # loop lines

            nSylIndex = self.__isSamePhoneme(i, nSylIndex)

            for j in range(0,len(self.__cSyllabs[i])): # loop bigrams

                if(self.__nSyllabs[nSylIndex][j][2] != self.__cSyllabs[i][j][2]):
                    same = False

            if(same):
                sameCount += 1
            else:
                same = True
                self.__difLst.append(self.__nSyllabs[nSylIndex])
                self.__difLst.append(self.__cSyllabs[i])

            nSylIndex += 1

        return (sameCount / float(end) * 100)

    # checks if both phonemes to be compared are the same. Loops through
    # checking each bigram contents. Continues until they are the same.
    # returns the adjusted index for nSyllabs.
    def __isSamePhoneme(self, i, nSylIndex):
        if(len(self.__nSyllabs[nSylIndex]) != len(self.__cSyllabs[i])):
            return self.__isSamePhoneme(i, nSylIndex + 1)

        for j in range(0, len(self.__nSyllabs[nSylIndex])):

            d1 = (self.__nSyllabs[nSylIndex][j][0] != self.__cSyllabs[i][j][0])
            d2 = (self.__nSyllabs[nSylIndex][j][1] != self.__cSyllabs[i][j][1])

            if(d1 or d2):
                return self.__isSamePhoneme(i, nSylIndex + 1)

        return nSylIndex # the same

    # prints the percentage to the commandline
    def __outputResults(self, percentSim):
        print("File is " + str(percentSim) + "% similar to NIST.")
