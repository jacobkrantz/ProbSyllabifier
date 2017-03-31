'''
fileName:       NISTSyllab.py
Authors:        Jacob Krantz
Date Modified:  3/14/17

- Mass syllabifier using CMU Pronouncing Dictionary and
    NIST Sylabifier.
- Program takes in file of words to be syllabified separated
    by spaces. Creates dictionary of word:syllabification.
    This is outputted as a text file with one dictionary
    entry per line.
- Output file: './HMMFiles/SyllabDict.txt'
'''
import sys
from nltk.corpus import cmudict
from NIST import NIST

class NISTSyllab:

    def __init__(self):
        self.NIST = NIST()
        self.CMUDict = cmudict.dict()
        self.wordLst = []
        self.ArpabetDict = {}
        self.outFile = ""
        self.inFile = ""

    # given an input file, will syllabify all the words within.
    # Outputs as a syllabification dictionary to specified
    # output file. Parsing of this file shown in 'utils.py'.
    def syllabifyFile(self, inputFile, outputFile):
        self.inFile = inputFile
        self.outFile = outputFile

        self.readWords()

        self.buildArpabet()

        syllabDict = self.__getSyllabDict()

        self.printDictToFile(syllabDict)

        print "File successfully syllabified."
        self.__init__()


    # ------------------------------------------------------
    # Helper functions below
    # ------------------------------------------------------


    ## needs textfile of words to exist in specified directory
    ## imports words from file as list of words.
    ## populates self.wordLst with file contents.
    ## throws IOError if file not found
    def readWords(self):

        wordFile = open(self.inFile,'r')
        words = ""

        for line in wordFile:
            words = words + ' ' + line

        words = words.split()

        for i in words:
            self.wordLst.append(i)


    ## looks up each word in cmudict and adds the word and pronunciation
    ## to a dictionary. Values are in list format with unicode phonemes.
    ## Only takes the first pronounciation for CMU when multiple exist.
    def buildArpabet(self):

        for word in self.wordLst:
            unicodeWord = unicode(word)

            try:
                self.ArpabetDict[word] = self.CMUDict[unicodeWord][0]

            except:

                print(unicodeWord + " not found in CMUDict")
                sys.exit()


    def __getSyllabDict(self):
        syllabDict = {}

        for key in self.ArpabetDict:

            syllabif = self.__getSyllabification(self.ArpabetDict[key])
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

        ## ArpString ready for NIST
        finalSyllab = self.NIST.syllabify(ArpString)

        return finalSyllab


    ## dictionary format: word: [[syllab1],[syllab2]...]
    def printDictToFile(self, Dict):

        outF = open(self.outFile,'w')

        for entry in Dict:

            outF.write(str(entry))
            outF.write(" ")
            outF.write(str(Dict[entry][0]))
            outF.write("\n")

        outF.close()
