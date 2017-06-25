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
    def getAllBigramTups(self, lang):
        sylParser = SyllabParser()
        if lang == 1:
            return sylParser.makePhonemeLst()
        else:
            return


    # generates the tag dictionary by iterating though the bigram tuples and
    # looking up what type of consonant or vowel each phone belongs to.
    # returns a dictionary of [tag]: [number of occurances]
    # also returns a lookup list for matrix indices.
    def getTagLookup(self, allBigramTups,lang):
        spot = ''
        spot1 = ''
        spot2 = ''
        tagDict = {}
        tagLst = []

        for phoneme in allBigramTups:
            for tup in phoneme:

                spot = self.getCategory(tup[0],lang)
                spot1 = str(tup[2])
                spot2 = self.getCategory(tup[1],lang)
                tagString = spot + spot1 + spot2
                tagLst.append(tagString)
                if tagString in tagDict:
                    tagDict[tagString] += 1
                else:
                    tagDict[tagString] = 1

        return tagDict, list(set(tagLst))


    # returns the category that the phone belongs to
    def getCategory(self, phone,lang):
        cat = ""
        tagNames = self.getTagNames(lang)
        phone = phone.upper()

        for category in tagNames:
            if phone in category:
                cat = category[0]
                return cat[0] # remove trailing unique ID
        print "not found in tagset."
        return ""


        # imports the tags from a specific file.
        # returns as a list of lists.
    def getTagNames(self,lang):
        if(lang == 1):
            inFile = open("./HMMFiles/phoneCategoriesArp.txt",'r')
        else:
            inFile = open("./HMMFiles/phoneCategoriesDISC.txt",'r')
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

    #Puts the tagDict into a list
    #This is the label for each of the matrix spots
    def getTagLst(self,tagDict):
        tagLst = []
        for i in range(0,len(tagDict)):
            largest = max(tagDict, key=tagDict.get)
            tagLst.append(largest)
            del tagDict[largest]
        return tagLst

    # for input phoneme: [(phone,phone,int),(...),]
    # returns a list of bigram tuples.
    # ex: [('m0d','d1s'),('d1s','n1l'),('n1l','a0m')]
    def getTagBigrams(self, phoneme):
        TagBigrams = []

        for i in range(1,len(phoneme) - 1):
            tupl = (phoneme[i - 1][2], phoneme[i][2])
            TagBigrams.append(tupl)

        return TagBigrams


    # param: all tag bigrams, including duplicates.
    # creates a dictionary of [bigram]: [number of occurances]
    def buildTagBigramDict(self, tagBigrams):
        tagBigramDict = {}

        for bigramTup in tagBigrams:
            if bigramTup in tagBigramDict:
                tagBigramDict[bigramTup] +=1
            else:
                tagBigramDict[bigramTup] = 1

        return tagBigramDict

    # ------------------------------------------------------
    # B Matrix functions below
    # ------------------------------------------------------


    # expands the tagset to have vowel/consonant
    # knowledge in place of boundary 1 or 0.
    # returns the adjusted phoneme list
    def expandTags(self, phonemeLst,lang):
        spot = ''
        spot1 = ''
        spot2 = ''

        for phoneme in phonemeLst:
            for tup in phoneme:

                spot = self.getCategory(tup[0],lang)
                spot1 = str(tup[2])
                spot2 = self.getCategory(tup[1],lang)
                tagString = spot + spot1 + spot2
                tup[2] = tagString

        return phonemeLst


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
