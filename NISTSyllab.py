## Mass syllabifier using CMU Pronouncing Dictionary and 
##   NIST Sylabifier. 
## Program takes in file of words to be syllabified separated
##   by spaces. Creates dictionary of word:syllabification.
##   This is outputted as a text file with one dictionary
##   entry per line

import sys
from nltk.corpus import cmudict
import NIST


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


## looks up each word in cmudict and adds the word and pronunciation
## to a dictionary. Values are in list format with unicode phonemes
## only takes the first pronounciation for CMU when multiple exist
def getArpabet(wordLst):
    pronounceDict = {}
    CMUDict = cmudict.dict()

    for word in wordLst:
        unicodeWord = unicode(word) 

        try:
            pronounceDict[word] = CMUDict[unicodeWord][0]
            # print pronounceDict[word]

        except:

            print(unicodeWord + " not found in CMUDict")
            sys.exit()

    return pronounceDict


def getSyllabDict(ArpabetDict):
    syllabDict = {}

    for key in ArpabetDict:

        syllabification = getSyllabification(ArpabetDict[key])
        syllabDict[key] = syllabification
        # print(syllabDict[key])

    return syllabDict


def getSyllabification(pronunciation):
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

    ## ArpString ready for NIST
    finalSyllab = NIST.syllabify(ArpString)

    return finalSyllab


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

    printDictToFile(syllabDict)


main()
