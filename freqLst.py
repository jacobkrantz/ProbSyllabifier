import sys
from nltk.corpus import cmudict

'''
fileName:       run.py
Authors:        Jacob Krantz
Date Modified:  3/11/17

Takes in a file of all tokenized words
Adds word and # of occurrances to a dictionary
outputs top 1000 words and their probability
Note: all top 1000 words must exist in CMU pronouncing dictionary
'''

class FrequentWords:

    def __init__(self):
        self.CMUDict = cmudict.dict()
        self.__inFile = ""
        self.__outFile = ""
        self.__numWords = 0
        self.__wordLst = []
        self.__freqLst = []
        self.wordDict = {}

    # inFile example = './corpusFiles/editorial_words.txt'
    # param 1: inFile. file for raw word input
    # param 2: outFile. file to output the most frequent words.
    # param 3: numWords. Number of most frequent words to be outputted.
    def generateMostFreq(self, inFile, outFile, numWords):
        self.__inFile = inFile
        self.__outFile = outFile
        self.__numWords = numWords

        words = self.__getWords()

        self.__createWordDict(words)

        self.__createFreqDict(len(words))

        self.__printLst(self.__wordLst)


    # builds a file of words to be tested on once the HMM is trained.
    # Uses most frequent words not already in training set.
    # testingOut: file output to hold generated words.
    # numTestWords: number of words to be in said file.
    # **Note: must be run after function 'generateMostFreq'
    def generateTesting(self, testingOut, numTestWords):
        if(numTestWords == 0):
            return
            
        self.__outFile = testingOut
        self.__numWords = numTestWords

        # current issue: same file output as generateMostFreq.
        self.__createFreqDict(len(self.wordDict))
        self.__printLst(self.__wordLst)


    # displays the most frequent words to the console with their
    # respective frequency counts. Prints total word count.
    def viewMost(self):
        for i in range(len(self.__wordLst)):
            sys.stdout.write(str(self.__freqLst[i]))
            sys.stdout.write(' ')
            sys.stdout.write(self.__wordLst[i])
            sys.stdout.write('\n')

        print('\n' + "Number of words: " + str(len(self.__wordLst)))

    ## ------------------------------
    ##            PRIVATE
    ## ------------------------------

    # imports the words contained in the inFile specified.
    # returns all words in split fashion.
    def __getWords(self):
        wordFile = open(self.__inFile,'r')
        print("Extracting from: " + self.__inFile)
        words = ""

        for line in wordFile:
            words = words + ' ' + line

        return words.split()


    # creates a dictionary of word: word count given a list of words.
    def __createWordDict(self, words):

        for word in words:
            if word in self.wordDict:
                self.wordDict[word] = self.wordDict[word] + 1
            else:
                self.wordDict[word] = 1


    def __createFreqDict(self, count):
        if(self.__numWords > count):
            print("Source too small. Cannot pull " + self.__numWords + " items.")
            return
        freqCount = 0

        while(freqCount < self.__numWords):

            maxWord = max(self.wordDict, key=self.wordDict.get)
            unicodeWord = unicode(maxWord)

            try:

                self.CMUDict[unicodeWord]
                self.__wordLst.append(maxWord)
                self.__freqLst.append(self.wordDict[maxWord])
                del self.wordDict[maxWord]
                freqCount += 1

            except:
                del self.wordDict[maxWord]


    # outputs a list to a file. List entries are
    # separated by spaces
    def __printLst(self, w):
        txt = open(self.__outFile,'w')
        for word in w:
            txt.write(word)
            txt.write(' ')


if(__name__ == "__main__"):
    fw = FrequentWords()
    inFile = './corpusFiles/editorial_words.txt'
    outFile = './corpusFiles/FEWtst.txt'

    fw.generateMostFreq(inFile, outFile, 10)
    fw.viewMost()
