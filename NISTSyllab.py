## Mass syllabifier using CMU Pronouncing Dictionary and 
##   NIST Sylabifier. 
## Program takes in file of words to be syllabified separated
##   by spaces. Creates dictionary of word:syllabification.
##   This is outputted as a text file with one dictionary
##   entry per line

import sys
import re
from nltk.corpus import cmudict


## needs textfile of words to exist in specified directory
## imports words from file as list of words
def getWords(wordLst):

    if(len(sys.argv) == 2):
        fileName = sys.argv[1]
    else:
        print("Error. No word file provided.")
        sys.exit()

    wordFile = open(fileName,'r') 

    words = ""
    for line in wordFile:
        words = words + ' ' + line
    words = words.split()

    for i in words:
        wordLst.append(i)

    return wordLst

## looks up each word in cmudict and adds the word and pronounciation
## to a dictionary. Values are in list format to allow for 
## Multiple pronounciations.
def getArpabet(wordLst):
    pronounceDict = {}
    CMUDict = cmudict.dict()

    for word in wordLst:
        unicodeWord = unicode(word) 

        try:

            pronounceDict[word] = CMUDict[unicodeWord]

        except:

            print(unicodeWord + " not found in CMUDict")
            sys.exit()

    return pronounceDict


def getSyllabDict(ArpabetDict):
    syllabDict = {}

    for key in ArpabetDict:

        syllabDict[key] = []

        for pronounciation in ArpabetDict[key]:

            syllabification = getSyllabification(pronounciation)
            syllabDict[key].append(syllabification)
            
        #print(syllabDict[key])
    return syllabDict


def getSyllabification(pronounciation):
    ArpString = ""

    for phone in pronounciation:
        aPhone = phone.encode('ascii','ignore')

        if(len(aPhone) == 2):
            if(aPhone[1].isdigit()):
                aPhone = aPhone[:1]
                
        else:
            if(len(aPhone) == 3):
                if(aPhone[2].isdigit()):
                    aPhone = aPhone[:2]

        ArpString = ArpString + aPhone.lower() + " "

    ## ArpString ready for NIST

    return ArpString



## dictionary format: word: [[syllab1],[syllab2]...]
## this function not passing. Need actual dictionary format to proceed.
def printDictToFile(Dict):
    outFile = open("./corpusFiles/topSyllabDict.txt",'w')

    for entry in Dict:

        #print(Dict[entry])
        outFile.write(str(entry))
        outFile.write(" ")
        NumOfSyllabs = len(Dict[entry])

        for i in range(0,NumOfSyllabs):

            print(str(Dict[entry][i]))
            outFile.write(" ")
            outFile.write(str(Dict[entry][i]))

        outFile.write("\n")

    outFile.close()
    return


def main():
    wordLst = []

    wordLst = getWords(wordLst)
    
    ArpabetDict = getArpabet(wordLst)

    syllabDict = getSyllabDict(ArpabetDict)

    # printDictToFile(syllabDict)


main()
