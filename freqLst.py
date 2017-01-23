'''
Takes in a file of all tokenized words
Adds word and # of occurrances to a dictionary
outputs top 1000 words and their probability 
Note: all top 1000 words must exist in CMU pronouncing dictionary
'''
import sys
from nltk.corpus import cmudict

def getWords():
    if(len(sys.argv) == 2 and sys.argv[1] == '-e'):
        fileName = './corpusFiles/editorial_words.txt'
    else:
        fileName = './corpusFiles/raw_words.txt'

    wordFile = open(fileName,'r')
    print("Extracting from: " + fileName)
    words = ""

    for line in wordFile:
        words = words + ' ' + line

    words = words.split()

    return words, fileName


def getWordCount(words):
    return len(words)


def createWordDict(words):
    wordDict = {}

    for word in words:
        if word in wordDict:
            wordDict[word] = wordDict[word] + 1
        else:
            wordDict[word] = 1

    return wordDict


def createFreqDict(wordDict, count):
    CMUDict = cmudict.dict()
    freqLst = []
    wordLst = []
    freqCount = 0

    while(freqCount < 1000):

        maxWord = max(wordDict, key=wordDict.get)
        unicodeWord = unicode(maxWord)

        try:

            CMUDict[unicodeWord]
            wordLst.append(maxWord)
            freqLst.append(wordDict[maxWord])
            del wordDict[maxWord]
            freqCount = freqCount + 1

        except:

            del wordDict[maxWord]            

    return wordLst, freqLst

def viewMost(w, f):
    for i in range(len(w)):
        sys.stdout.write(str(f[i]))
        sys.stdout.write(' ')
        sys.stdout.write(w[i])
        sys.stdout.write('\n')

def printLst(w,fileName):
    if('editorial' in fileName):
        outFile = './corpusFiles/freqEditWords.txt'
    else:
        outFile = './corpusFiles/freqWords.txt'

    txt = open(outFile,'w')
    for word in w:
        txt.write(word)
        txt.write(' ')

def main():
    words,fileName = getWords()

    count = getWordCount(words)

    wordDict = createWordDict(words)

    wordLst, freqLst = createFreqDict(wordDict,count)

    viewMost(wordLst, freqLst)

    print('\n' + "Number of words: " + str(len(wordLst)))

    printLst(wordLst,fileName)

main()
