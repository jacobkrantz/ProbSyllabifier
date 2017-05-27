from NISTSyllab import NISTSyllab
import numpy as np
import sys
from ast import literal_eval

'''
fileName:       ProbSyllabifier.py
Authors:        Jacob Krantz
Date Modified:  3/14/17

- Purpose: Syllabifies a given phoneme (or file of phonemes)
    - uses the Viterbi Algrithm
    - skips syllabification if a foreign phone bigram is parsed
- Functions:
    - syllabifyFile(fileIN, fileOUT)
    - syllabify(phonemeString)
'''

class ProbSyllabifier:

    # initializes all data structures necessary
    # to syllabify a phoneme or a file.
    def __init__(self):
        self.__matrixA = self.__loadMatrix('A')
        self.__matrixB = self.__loadMatrix('B')
        self.__exceptionLst = []
        self.__obsLookup = []
        self.__hiddenLookup = []
        self.__hiddenProb = {}
        self.__iMax = 0
        self.__jMax = 0

        self.__loadStructures()


    # given a file containing a dict of word: syllab,
    # syllabifies each and outputs the results into a new file under the
    # new file name.
    # param 1: phoneme file in
    # param 2: fileName for syllabification out
    def syllabifyFile(self, fileIN):
        self.sTools = NISTSyllab()
        self.sTools.inFile = fileIN
        self.sTools.outFile = "outputFile.txt"
        self.getExceptionLst # for reset

        self.sTools.readWords()
        self.sTools.buildIPA()
        syllabDict = self.__syllabifyAll()

        numSkips = len(self.getExceptionLst()) # resets the exception list
        print("Number of words skipped: " + str(numSkips))

        self.__printDictToFile(syllabDict)


    # given an observation string, generates the most likely hidden state.
    # what should this return?
    def syllabify(self, observation):
        obsLst = self.__makeObsLst(observation)
        if(not (len(obsLst) - 1)): # early return for single phone obs
            return obsLst[0]
        obsLst = self.__convertToBigrams(obsLst)

        isValid, problemObs = self.__isValidObs(obsLst)


        if(isValid):

            matrixV, matrixP = self.__buildMatrixV(obsLst)
            outputLst = self.__decodeMatrix(matrixV, matrixP, obsLst)
            finalStr = self.__makeFinalStr(obsLst, outputLst)

        else:

            badBigram = problemObs[0] +  " " + problemObs[1]
            #print("Error: '" + badBigram + "' does not exist in training set.")
            self.__exceptionLst.append(badBigram)
            return []

        return finalStr


    # returns a list containing all bigrams that were not present in the
    # training set. Also resets the exception list.
    def getExceptionLst(self):
        allExceptions = list(self.__exceptionLst)
        self.__exceptionLst= []

        return allExceptions


    # ------------------------------------------------------
    # helper functions below
    # ------------------------------------------------------


    # loads either MatrixA (if which == 'A') or MatrixB (if which == 'B')
    def __loadMatrix(self, which):
        if(which == 'A'):
            fileName = "./HMMFiles/MatrixA.txt"
        elif(which == 'B'):
            fileName = "./HMMFiles/MatrixB.txt"
        else:
            raise Exeption("__loadMatrix bad input")

        try:
            matrix = np.loadtxt(fileName, dtype = 'float')
        except:
            print(fileName +" does not exist or is corrupt.")
            sys.exit(0)
        return matrix


    # initializes the necessary data structures by loading them from files
    # within the /HMMFiles/ directory.
    def __loadStructures(self):
        self.__obsLookup = self.__loadLookup('./HMMFiles/obsLookup.txt')
        self.__obsLookup = self.__fixObsLookup()
        self.__hiddenLookup =self.__loadLookup('./HMMFiles/hiddenLookup.txt')
        self.hiddenProb = self.__loadDictFile('./HMMFiles/hiddenProb.txt')


    # given a fileName, loads the list that exists inside of it.
    # each line of the file corresponds to a list entry.
    def __loadLookup(self, fileName):
        lookup = []
        try:
            rawFile = open(fileName,'r')
            for line in rawFile:
                item = line.strip('\n')
                lookup.append(item)
        except IOError:
            print(fileName + " does not exist or is corrupt.")
            sys.exit(0)
        return lookup


    # converts the observation lookup data structure from strings to tuples
    def __fixObsLookup(self):
        tmpLst = []
        for obs in self.__obsLookup:
            tmpLst.append(literal_eval(obs))
        return tmpLst


    # given a filename, loads the dictionary that exists inside of it.
    # each line of the file contains the key followed by a space then the
    # value.
    def __loadDictFile(self, fileName):
        tagProb = {}
        try:
            tagFile = open(fileName,'r')
            for line in tagFile:
                newLine = line.split(' ')
                tagProb[newLine[0]] = float(newLine[1])
        except IOError:
            print(fileName + " does not exist or is corrupt.")
            sys.exit(0)
        return tagProb


    # given an observation string, appends each phone to a new
    # obersvation list. returns list.
    def __makeObsLst(self, observation):
        obsLst = []
        obs = observation.split(' ')

        for phone in obs:
            if phone[0] == '"':     # *****for removing ' or " at start.
                phone = phone[1:]
            elif phone[0] == "'":
                phone = phone[1:]
            if phone[-1] == '"':    # for removing from end.
                phone = phone[:-1]
            elif phone[-1] == "'":
                phone = phone[:-1]

            obsLst.append(phone)

        return obsLst


    # convert obsLst to its bigrams
    def __convertToBigrams(self,obsLst):
        bigramLst = []
        for i in range(1,len(obsLst)):
                tup = (obsLst[i - 1],obsLst[i])
                bigramLst.append(tup)
        return bigramLst


    # given an observation list, returns True if all observations exist in
    # the training set. Returns False and the problem observation as a string
    # otherwise.
    def __isValidObs(self, obsLst):
        try:
            for i in range(0,len(obsLst)):

                problemObs = obsLst[i]
                self.__obsLookup.index(obsLst[i])

        except ValueError:
            return False, problemObs
        return True, ''


    # constructs Viterbi and backpointer matrices.
    # these are used for determining correct hidden state sequence
    #
    # ****note: for the B matrix, the algorithm was constructed to look at
    #       i and j backwards. Our matrixB is correct, but had to be flipped
    #       in reference here to be used "properly".
    def __buildMatrixV(self, obsLst):
        self.__iMax = len(self.__hiddenLookup)
        self.__jMax = len(obsLst)
        matrixV = np.zeros((self.__iMax,self.__jMax), dtype=np.float) # Viterbi matrix
        matrixP = np.zeros((self.__iMax,self.__jMax), dtype='int,int') # backpointer matrix

        if(self.__jMax == 0): # no bigrams, just one phone
            return matrixV, matrixP

        for i in range(0,self.__iMax):                #initialization step
            obsIndex = self.__obsLookup.index(obsLst[0])
            matrixV[i,0] = self.__matrixB[obsIndex, i]#flipped

        for j in range(1,self.__jMax):                #iterative step
            obsBigram = self.__obsLookup.index(obsLst[j])
            for i in range(0,self.__iMax):
                curProb = 0
                maxProb = 0
                iBack = 0
                jBack = 0
                for oldI in range(0,self.__iMax):
                    Bword = self.__obsLookup[j]
                    curProb = matrixV[oldI,j-1] * self.__matrixA[oldI,i] * self.__matrixB[obsBigram, i]

                    if (curProb > maxProb):
                        maxProb = curProb
                        iBack = oldI
                        jBack = j - 1

                matrixV[i,j] = maxProb
                matrixP[i,j][0] = iBack
                matrixP[i,j][1] = jBack

        return matrixV, matrixP


    # traces through the backpointer matrix P and catches
    # the most likely tag sequence as it iterates
    def __decodeMatrix(self, matrixV, matrixP, obsLst):
            revOutput = []

            maxFinal = 0
            iFinal = 0

            for i in range(0,self.__iMax):         #only grabs final max prob
                currentFinal = matrixV[i,self.__jMax - 1]
                if(currentFinal > maxFinal):
                    maxFinal = currentFinal
                    iFinal = i

            revOutput.append(self.__hiddenLookup[iFinal])
            iCur = matrixP[iFinal,self.__jMax - 1][0]
            jCur = matrixP[iFinal,self.__jMax - 1][1]

            for j in range(self.__jMax-2,-1,-1):

                revOutput.append(self.__hiddenLookup[iCur])
                iCurOld = iCur
                iCur = matrixP[iCur,jCur][0]
                jCur = matrixP[iCurOld,jCur][1]

            return revOutput[::-1]


    # combines the hidden list with the observation list.
    # returns the final string, formed nicely.
    def __makeFinalStr(self, obsLst, outputLst):
        finalStr = ""
        isTruncated = False

        for i in range(0, len(obsLst)):

            isTruncated = (i == len(obsLst) - 1)
            finalStr += obsLst[i][0]
            if(outputLst[i][1] == '0' or isTruncated):
                finalStr += " "
            else:
                finalStr += " | "

        finalStr += obsLst[len(obsLst) - 1][1]
        return finalStr


    # given a list of phonemes, syllabifies all of them.
    # returns a list of syllabifications, with indices corresponding
    # to the inputted phoneme list.
    def __syllabifyAll(self):
        syllabDict = {}

        for key in self.sTools.ArpabetDict:

            syllabif = self.__getSyllabification(self.sTools.ArpabetDict[key])
            syllabDict[key] = syllabif

        return syllabDict


    def __getSyllabification(self, pronunciation):
        ArpString = ""

        for phoneme in pronunciation:
            aPhoneme = phoneme.encode('ascii','ignore')

            if(len(aPhoneme) == 2):
                if(aPhoneme[1].isdigit()):
                    aPhoneme = aPhoneme[:1]

            else:
                if(len(aPhoneme) == 3):
                    if(aPhoneme[2].isdigit()):
                        aPhoneme = aPhoneme[:2]

            ArpString = ArpString + aPhoneme + " "

        ## ArpString ready for syllabification
        finalSyllab = self.syllabify(ArpString.lower().strip(" "))

        return finalSyllab


    # prints the contents of a syllabification dictionary to a file.
    # Comforms to format of 'SyllabDict.txt' for future parsing.
    def __printDictToFile(self, syllabDict):
        #print syllabDict
        outF = open(self.sTools.outFile,'w')

        for entry in syllabDict:

            try:
                valueString = syllabDict[entry].split(" ")
                outF.write(str(entry))
                outF.write(" ")
                outF.write("[ ")

                for char in valueString:
                    if(char == '|'):
                        outF.write("][")
                    else:
                        outF.write(char)

                    outF.write(" ")

                outF.write("]")
                outF.write('\n')

            except:
                pass
