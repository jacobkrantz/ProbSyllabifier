from SyllabParser import SyllabParser
import sys
import numpy as np

'''
fileName:       utils.py
Authors:        Jacob Krantz
Date Modified:  2/26/17

Common utilies needed for building matrices with a HMM
- initMatrix
- outputMatrix
- importMatrix
- getAllBigramTups
- getBoundLst
- getBoundCount
- getBoundBigrams
- getNumBounds
- getBigramLookup
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

            np.savetxt("./HMMFiles/MatrixA.txt",matrix, newline = '\n',header = "matrixA", fmt = '%.5f')
            print ("Matrix A outputted to: ./HMMFiles/MatrixA.txt")

        elif(which == "B"):

            np.savetxt("./HMMFiles/MatrixB.txt",matrix, newline = '\n',header = "matrixB", fmt = '%.5f')
            print ("Matrix B outputted to: ./HMMFiles/MatrixB.txt")

        else:
            print ("'" + which + "'' does not match any option.")


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
        sylParser = SyllabParser()

        return sylParser.makePhonemeLst()


    # generates the tag dictionary by iterating though the bigram tuples and
    # looking up what type of consonant or vowel each phone belongs to.
    # returns a dictionary of [tag]: [number of occurances]
    # also returns a lookup list for matrix indices.
    def getTagLookup(self, allBigramTups):
        spot = 0
        spot1 = 0
        spot2 = 0
        tagDict = {}
        tagLst = []

        for phoneme in allBigramTups:
            for tup in phoneme:

                spot = self.getCategory(tup[0])
                spot1 = str(tup[2])
                spot2 = self.getCategory(tup[1])
                tagString = spot + spot1 + spot2
                tagLst.append(tagString)
                if tagString in tagDict:
                    tagDict[tagString] += 1
                else:
                    tagDict[tagString] = 1
        print len(tagDict)
        return tagDict, set(tagLst) 


    # returns the category that the phone belongs to
    def getCategory(self, phone):
        cat = ""
        tagNames = self.getTagNames()
        phone = phone.upper()

        for category in tagNames:
            if phone in category:
                cat = category[0]
                return cat[0] # remove trailing unique ID
        print "not found in tagset."
        return ""


        # imports the tags from a specific file.
        # returns as a list of lists.
    def getTagNames(self):
        inFile = open("./HMMFiles/phoneCategories.txt",'r')
        tags = []

        for line in inFile:
            tmpLst = line.split(' ')
            tmpLst[len(tmpLst) - 1] = tmpLst[len(tmpLst) - 1].strip('\r\n')
            tags.append(tmpLst)

        return tags


    # phonemeLst is allBigramTups
    # returns a list of all
    def getBoundLst(self, phonemeLst):
        boundLst = []

        for phoneme in phonemeLst:
            for tup in phoneme:
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
    # returns a list of tuples containing boundary bigrams with v/c knowledge.
    # ex: [('m0d','d1s'),('s0n','n1l'),('la1','a0m')]
    def getTagBigrams(self, phoneme):
        TagBigrams = []
        tagLst = []

        for tup in phoneme:
            spot0 = self.getCategory(tup[0])
            spot2 = self.getCategory(tup[1])
            tagString = spot0 + str(tup[2]) + spot2
            tagLst.append(tagString)

        for i in range(1,len(tagLst) - 1):
            tupl = (tagLst[i - 1], tagLst[i])
            TagBigrams.append(tupl)

        return TagBigrams

    # ------------------------------------------------------
    # B Matrix functions below
    # ------------------------------------------------------

    # counts and returns the number of boundaries matching
    # the passed in integer within boundaryLst.
    def getNumBounds(self, boundaryLst, match):
        total = 0

        for bound in boundaryLst:
            if(bound == match):
                total += 1

        return total


    # allBigramTups: [[(phone,phone,int),(...),],[...],]
    # creates a master lookup list for all unique bigrams trained on.
    # bigrams are inserted into the list as tuples:
    # [(phone,phone),(phone,phone)...]
    def getBigramLookup(self, allBigramTups):
        bigramLookup = []

        for phoneme in allBigramTups:
            for bigram in phoneme:
                newTup = (bigram[0],bigram[1])
                if newTup not in bigramLookup:
                    bigramLookup.append(newTup)
        return bigramLookup


    # builds a dictionary containing bigram: P(bigram)
    # used for normalizing MatrixB
    def getBigramFreqDict(self, allBigramTups, numBigrams):
        bigramFreqDict = {}

        for phoneme in allBigramTups:
            for bigram in phoneme:

                newTup = (bigram[0],bigram[1])

                if(newTup not in bigramFreqDict):
                    bigramFreqDict[newTup] = 1
                else:
                    bigramFreqDict[newTup] += 1

        return self.__normBigramFreqDict(bigramFreqDict, numBigrams)


    # nornamlize the bigramFreqDict to (countBigram / countAllBigrams)
    def __normBigramFreqDict(self, bigramFreqDict, numBigrams):
        for bigram in bigramFreqDict:
            bigramFreqDict[bigram] = bigramFreqDict[bigram] / float(numBigrams)

        return bigramFreqDict

    # ------------------------------------------------------
    # File outputs for Viterbi
    # ------------------------------------------------------

    # outputs a list to a file. Entries separated by newline char
    def makeLookup(self, lookup, fileName):
        File = open(fileName,'w')
        for item in lookup:
            File.write(str(item))
            File.write('\n')
        File.close()


    # generates a dictionary of hiddenState: probability
    def makeHiddenProb(self, hiddenLst):
        hiddenProb = self.__makeHiddenProbHelper(hiddenLst)
        File = open("./HMMFiles/hiddenProb.txt",'w')

        for state in hiddenProb:

            File.write(str(state))
            File.write(' ')
            File.write(str(hiddenProb[state]))
            File.write('\n')

        File.close()


    #returns a dictionary of the probability of a hidden state
    #equation: hiddenProb = count(state) / count(all states)
    def __makeHiddenProbHelper(self, hiddenLst):
        hiddenProb = {}

        # insert counts int dict
        for state in hiddenLst:
            if state not in hiddenProb:
                hiddenProb[state] = 1
            else:
                hiddenProb[state] += 1

        # normalize counts to list length
        for state in hiddenProb:
            hiddenProb[state] = hiddenProb[state] / float(len(hiddenLst))

        return hiddenProb
