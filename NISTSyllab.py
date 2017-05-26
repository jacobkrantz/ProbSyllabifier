'''
fileName:       NISTSyllab.py
Authors:        Jacob Krantz
Date Modified:  3/14/17

- Mass syllabifier using espeak and
    NIST Sylabifier (needs to be the celex database)
- Program takes in file of words to be syllabified separated
    by spaces. Creates dictionary of word:syllabification.
    This is outputted as a text file with one dictionary
    entry per line.
- Output file: './HMMFiles/SyllabDict.txt'
'''
import sys
from nltk.corpus import cmudict
from NIST import NIST
from subprocess import check_output

class NISTSyllab:

    def __init__(self):
        self.NIST = NIST()
        #self.CMUDict = cmudict.dict()
        self.wordLst = []
        self.IPADict = {}
        self.outFile = ""
        self.inFile = ""

    # given an input file, will syllabify all the words within.
    # Outputs as a syllabification dictionary to specified
    # output file. Parsing of this file shown in 'utils.py'.
    def syllabifyFile(self, inputFile, outputFile):
        self.inFile = inputFile
        self.outFile = outputFile

        self.readWords()

        self.buildIPA()

        #this will need to be celex
        #syllabDict = self.__getSyllabDict()

        self.printDictToFile(self.IPADict)

        print ("File successfully syllabified to: " + self.outFile)
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


    ## looks up the IPA translation for each word
    ## to a dictionary. Values are in list format with unicode phonemes.
    #this will literally parse anything that it is given.
    #What did Celex use for the word to phone converter?
    def buildIPA(self):

        for word in self.wordLst:
            unicodeWord = unicode(word)
            print unicodeWord
            self.IPADict[word] = str(check_output(["espeak", "-q","--ipa",'-v','en-us',unicodeWord]))

            try:
                #self.IPADict[word] = self.CMUDict[unicodeWord][0]
                self.IPADict[word] = str(check_output(["espeak", "-q","--ipa",'-v','en-us',unicodeWord]))
                print check_output(["espeak", "-q","--ipa",'-v','en-us',unicodeWord]).decode('utf8')
            except:

                print(unicodeWord + " not found in CMUDict")
                sys.exit()


    def __getSyllabDict(self):
        syllabDict = {}

        for key in self.IPADict:

            syllabif = self.__getSyllabification(self.IPADict[key])
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
        print Dict
        for entry in Dict:

            outF.write(str(entry))
            outF.write(" ")
            outF.write(str(Dict[entry]))
            outF.write("\n")
            #print str(Dict[entry])

        outF.close()


if(__name__ == "__main__"):
    N = NISTSyllab()
    N.syllabifyFile("./corpusFiles/testIPA.txt","IPAoutput.txt")
