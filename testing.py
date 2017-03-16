from SyllabParser import SyllabParser

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


    # compares the syllabifications of compFile to those done by NIST.
    # Printed percentage is how accurate compFile is to NISTfile.
    # Both compFile and NISTfile must be in specific formats.
    def compare(self, NISTfile, compFile):

        nSyllabs = self.__importFile(NISTfile)
        cSyllabs = self.__importFile(compFile)

        percentSim = self.__runComparison(nSyllabs, cSyllabs)
        self.__outputResults(percentSim)


    # prints the differences between NIST and the compared file
    def viewDifferences(self):

        for i in range(1, len(self.__difLst), 2):
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
        #self.sParser.setFile(fileName)
        return self.sParser.makePhonemeLst(fileName)


    # assumes that the ordering of nSyllabs is the same as cSyllabs.
    # iterates through both datasets. For each that are the same, adds
    # to same count. Also counts total entries. Returns percent.
    def __runComparison(self, nSyllabs, cSyllabs):
        end = len(cSyllabs)
        sameCount = 0
        same = True
        nSylIndex = 0

        for i in range(0, end): # loop lines

            if(not self.__isSamePhoneme(nSyllabs[i],cSyllabs[i])):
                print nSyllabs[i]
                nSylIndex += 1

            for j in range(0,len(nSyllabs[i])): # loop bigrams

                if(nSyllabs[nSylIndex][j][2] != cSyllabs[i][j][2]):
                    same = False

            if(same):
                sameCount += 1
            else:
                same = True
                self.__difLst.append(nSyllabs[nSylIndex])
                self.__difLst.append(cSyllabs[i])

            nSylIndex += 1

        return (sameCount / float(end) * 100)


    # checks if both phonemes to be compared are the same. Loops through
    # checking each bigram contents.
    def __isSamePhoneme(self,nSyllab, cSyllab):
        if(len(nSyllab) != len(cSyllab)):
            return False

        for i in range(0, len(nSyllab)):

            if(nSyllab[0] != cSyllab[0]):
                return False
            elif(nSyllab[1] != cSyllab[1]):
                return False

        return True


    # prints the percentage to the commandline
    def __outputResults(self, percentSim):
        print("File is " + str(percentSim) + "% similar to NIST.")
