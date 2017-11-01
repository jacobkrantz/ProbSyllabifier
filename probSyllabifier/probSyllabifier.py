from utils import SyllabTools, HMMUtils
import numpy as np
import logging as log

class ProbSyllabifier:
    """
    Syllabifies a given sequence of phones using the Viterbi Algorithm.
    Provides an empty result when a foreign phone bigram is parsed.
    """

    def __init__(self, HMMBO):
        """ Unpack the HMMBO data object. """
        log.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', datefmt='%X', level=log.INFO)
        self.hmmUtils     = HMMUtils()
        self.matrixA      = HMMBO.matrixA
        self.matrixB      = HMMBO.matrixB
        self.obsLookup    = HMMBO.observationLookup
        self.hiddenLookup = HMMBO.hiddenLookup
        self.tranScheme   = HMMBO.transcriptionScheme
        self.comparator   = ""

    def syllabifyFile(self, fileIN, fileOUT, comparator="CELEX"):
        """
        Currently ignored (11/1/17).
        Needs big rework, but not used.
        """
        # self.comparator = comparator
        # self.sTools = SyllabTools(self.comparator)
        # self.sTools.inFile = fileIN
        # self.sTools.outFile = fileOUT
        # self.sTools.readWords()
        # self.sTools.buildArpabet()
        # syllabDict = self.__syllabifyAll()
        # self.__printDictToFile(syllabDict)
        raise NotImplementedError("not in use")

    def syllabify(self, observation, comparator="CELEX"):
        """
        Generates the most likely hidden state.
        Args:
            observation (string): sequence of phones
            comparator (string): either "NIST" or default "CELEX"
        """
        self.comparator = comparator
        obsLst = self.__makeObsLst(observation)

        if len(obsLst) == 1: # early return for single phone obs
            return obsLst[0]

        transcribedObs = self.__transcribePhones(obsLst)
        transcribedObs = self.__convertToBigrams(transcribedObs)
        obsLst = self.__convertToBigrams(obsLst)

        isValid, problemObs = self.__isValidObs(transcribedObs)

        if(not isValid):
            badBigram = problemObs[0] +  " " + problemObs[1]
            log.warning("(%s) does not exist in training set.", badBigram)
            return []

        matrixV, matrixP = self.__buildMatrixV(transcribedObs)
        outputLst = self.__decodeMatrix(matrixV, matrixP, transcribedObs)
        return self.__makeFinalStr(obsLst, outputLst)

    # ------------------------------------------------------
    # helper functions below
    # ------------------------------------------------------

    # given an observation string, appends each phone to a new
    # obersvation list. returns list.
    def __makeObsLst(self, observation):
        if self.comparator == "CELEX":
            return list(observation)

        obsLst = ['<']
        for phone in observation.split(' '):
            if phone[0] in ['"',"'"]:     # remove ' or " at start.
                phone = phone[1:]
            if phone[-1] in ['"',"'"]:    # for removing from end.
                phone = phone[:-1]
            obsLst.append(phone)
        obsLst.append('>')
        return obsLst


    def __transcribePhones(self, obsLst):
        if self.comparator == "NIST":
            lang = 1
        else:
            lang = 2
        return list(map(lambda x:self.hmmUtils.getCategory(x, lang, self.tranScheme), obsLst))

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
                self.obsLookup.index(obsLst[i])

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
        iMax = len(self.hiddenLookup)
        jMax = len(obsLst)
        matrixV = np.zeros((iMax,jMax), dtype=np.float) # Viterbi matrix
        matrixP = np.zeros((iMax,jMax), dtype='int,int') # backpointer matrix

        if(jMax == 0): # no bigrams, just one phone
            return matrixV, matrixP

        for i in range(0,iMax):                #initialization step
            obsIndex = self.obsLookup.index(obsLst[0])
            matrixV[i,0] = self.matrixB[obsIndex, i]#flipped

        for j in range(1,jMax):                #iterative step
            obsBigram = self.obsLookup.index(obsLst[j])
            for i in range(0,iMax):
                curProb = 0
                maxProb = 0
                iBack = 0
                jBack = 0
                for oldI in range(0,iMax):
                    Bword = self.obsLookup[j]
                    curProb = matrixV[oldI,j-1] * self.matrixA[oldI,i] * self.matrixB[obsBigram, i]

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

            jMax = len(obsLst)
            maxFinal = 0
            iFinal = 0

            for i in range(0,len(self.hiddenLookup)):         #only grabs final max prob
                currentFinal = matrixV[i,jMax - 1]
                if(currentFinal > maxFinal):
                    maxFinal = currentFinal
                    iFinal = i

            revOutput.append(self.hiddenLookup[iFinal])
            iCur = matrixP[iFinal,jMax - 1][0]
            jCur = matrixP[iFinal,jMax - 1][1]

            for j in range(jMax-2,-1,-1):

                revOutput.append(self.hiddenLookup[iCur])
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
                if self.comparator == "NIST":
                    finalStr += " "
            else:
                if self.comparator == "NIST":
                    finalStr += " | "
                else:
                    finalStr += "-"

        return finalStr + obsLst[len(obsLst) - 1][1]


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
