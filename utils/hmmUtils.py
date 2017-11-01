from config import settings as config
from syllabParser import SyllabParser
import json
import numpy as np
import sys

class HMMUtils:
    """ Common utilities needed for building matrices with a HMM """

    def __init__(self):
        self.sylParser = SyllabParser()

    # intialize a matrix using numpy with provided size: (X,Y)
    # returns matrix
    def initMatrix(self, X, Y):
        return np.zeros((X,Y), dtype=np.float)

    # uses SyllabParser to generate a list of lists.
    # allBigramTups: [[(phone,phone,int),(...),],[...],] where int
    # corresponds to the type of boundary.
    def getNistBigramTups(self):
        return self.sylParser.makeNistPhonemeLst()

    # uses SyllabParser to generate a list of lists.
    # allBigramTups: [[(phone,phone,int),(...),],[...],] where int
    # corresponds to the type of boundary.
    def parseCelexTrainingSet(self, trainingSet):
        return self.sylParser.parseCelexTrainingSet(trainingSet)

    # generates the tag dictionary by iterating though the bigram tuples and
    # looking up what type of consonant or vowel each phone belongs to.
    # returns a dictionary of [tag]: [number of occurances]
    # also returns a lookup list for matrix indices.
    def getTagLookup(self, allBigramTups, lang, transciptionScheme=[]):
        category1 = ''
        category2 = ''
        tagDict = {}
        tagLookup = set()

        for phoneme in allBigramTups:
            for tup in phoneme:
                category1 = self.getCategory(tup[0], lang, transciptionScheme)
                category2 = self.getCategory(tup[1], lang, transciptionScheme)
                tagString = category1 + str(tup[2]) + category2
                tagLookup.add(tagString)
                if tagString in tagDict:
                    tagDict[tagString] += 1
                else:
                    tagDict[tagString] = 1

        return tagDict, list(tagLookup)

    # returns the category that the phone belongs to.
    # transciptionScheme is for CELEX used in GA
    def getCategory(self, phone,lang, transciptionScheme=[]):
        if transciptionScheme:
            for category in transciptionScheme:
                if phone in category:
                    # return an ascii character starting at 'a'
                    return chr(transciptionScheme.index(category) + 97)
            raise LookupError(phone + " not found in tagset.")

        cat = ""
        tagNames = self.getTagNames(lang)
        if lang == 1:
            phone = phone.upper()

        for category in tagNames:
            if phone in category:
                cat = category[0]
                return cat[0] # remove trailing unique ID
        raise LookupError(phone + " not found in tagset.")

    # imports the tags from a specific file.
    # returns as a list of lists.
    def getTagNames(self,lang):
        if(lang == 1):
            inFile = open(config["NistTranscriptionFile"], 'r')
        else:
            inFile = open(config["CelexTranscriptionFile"], 'r')

        tags = []
        for line in inFile:
            tmpLst = line.split(' ')
            tmpLst[len(tmpLst) - 1] = tmpLst[len(tmpLst) - 1].strip('\r\n')
            tags.append(tmpLst)

        return tags

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
    def expandTags(self, phonemeLst,lang, transciptionScheme=[]):
        spot = ''
        spot1 = ''
        spot2 = ''

        for phoneme in phonemeLst:
            for tup in phoneme:
                tup[0] = self.getCategory(tup[0],lang,transciptionScheme)
                isBoundary = str(tup[2])
                tup[1] = self.getCategory(tup[1],lang,transciptionScheme)
                tagString = tup[0] + isBoundary + tup[1]
                tup[2] = tagString

        return phonemeLst

    # allBigramTups: [[(phone,phone,int),(...),],[...],]
    # creates a master lookup list for all unique bigrams trained on.
    # bigrams are inserted into the list as tuples:
    # [(phone,phone),(phone,phone)...]
    def getBigramLookup(self, allBigramTups):
        bigramLookup = set()

        for phoneme in allBigramTups:
            for bigram in phoneme:
                bigramLookup.add((bigram[0],bigram[1]))
        return list(bigramLookup)

    # builds a dictionary containing bigram: P(bigram)
    # used for normalizing MatrixB
    def getBigramFreqDict(self, allBigramTups, numBigrams):
        bFreqDict = {}

        for phoneme in allBigramTups:
            for bigram in phoneme:
                newTup = (bigram[0],bigram[1])
                if(newTup not in bFreqDict):
                    bFreqDict[newTup] = 1
                else:
                    bFreqDict[newTup] += 1

        # nornamlize the bFreqDict to (countBigram / countAllBigrams)
        return dict(map(lambda (k,v): (k,v/float(numBigrams)),bFreqDict.iteritems()))
