import sys
from nltk.corpus import cmudict

'''
Takes in a file of all tokenized words
Adds word and # of occurrances to a dictionary
outputs top 1000 words and their probability
Note: all top 1000 words must exist in CMU pronouncing dictionary
'''

class FrequentWords:

    def __init__(self):
        self.__inFile = ""
        self.__outFile = ""
        self.__numWords = 0
        self.__wordLst = []
        self.__freqLst = []

    # inFile = './corpusFiles/editorial_words.txt'
    # inFile = './corpusFiles/raw_words.txt'
    # param 1: inFile. file for raw word input
    # param 2: outFile. file to output the most frequent words.
    # param 3: numWords. Number of most frequent words to be outputted.
    def generateMostFreq(self, inFile, outFile, numWords):
        self.CMUDict = cmudict.dict()
        self.__inFile = inFile
        self.__outFile = outFile
        self.__numWords = numWords

        words = self.__getWords()

        wordDict = self.__createWordDict(words)

        self.__createFreqDict(wordDict,len(words))

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
        wordDict = {}

        for word in words:
            if word in wordDict:
                wordDict[word] = wordDict[word] + 1
            else:
                wordDict[word] = 1

        return wordDict


    def __createFreqDict(self, wordDict, count):
        freqCount = 0

        while(freqCount < self.__numWords):

            maxWord = max(wordDict, key=wordDict.get)
            unicodeWord = unicode(maxWord)

            try:

                self.CMUDict[unicodeWord]
                self.__wordLst.append(maxWord)
                self.__freqLst.append(wordDict[maxWord])
                del wordDict[maxWord]
                freqCount += 1

            except:
                del wordDict[maxWord]


    # outputs a list to a file. List entries are
    # separated by spaces
    def __printLst(self, w):
        txt = open(self.__outFile,'w')
        for word in w:
            txt.write(word)
            txt.write(' ')


if(__name__ == "__main__"):
    fw = FrequentWords()
    #inFile = raw_input("enter file in: ")
    #outFile = raw_input("enter file out: ")
    inFile = './corpusFiles/editorial_words.txt'
    outFile = './corpusFiles/FEWtst.txt'

    fw.generateMostFreq(inFile, outFile, 10)
    fw.viewMost()
