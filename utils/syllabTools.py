from nltk.corpus import cmudict
from subprocess import check_output
import sys

'''
fileName:       syllabInfo.py
Authors:        Jacob Krantz
Date Modified:  3/14/17

- Mass syllabifier using CMU Pronouncing Dictionary and
    NIST Sylabifier for Arpabet
- Mass database from CELEX for IPA
- Program takes in file of words to be syllabified separated
    by spaces. Creates dictionary of word:syllabification.
    This is outputted as a text file with one dictionary
    entry per line.
- Output file: 'HMMFiles/SyllabDict.txt'
'''
class SyllabTools:

    def __init__(self,comparator):
        self.CMUDict = cmudict.dict()
        self.wordLst = []
        self.ArpabetDict = {}
        self.IPADict = {}
        self.outFile = ""
        self.inFile = ""
        self.comparator = comparator

    ## needs textfile of words to exist in specified directory
    ## imports words from file as list of words.
    ## populates self.wordLst with file contents.
    ## throws IOError if file not found
    def readWords(self):

        wordFile = open(self.inFile,'r')
        words = ""
        for line in wordFile:
            words = words + ' ' + line

        self.wordLst += words.split()


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

    '''
    NOTE*********************
    This converts words into IPA
    str(check_output(["espeak", "-q","--ipa",'-v','en-us',unicodeWord]))
    Not sure how the celex database is going to want this information
    so I'm going to leave this here until there is time to do more
    work on the database. Could have to translate a set of phones
    into a certain format to get this; we're not sure.
    '''
    ## looks up the IPA translation for each word
    ## to a dictionary. Values are in list format with unicode phonemes.
    #this will literally parse anything that it is given.
    #What did Celex use for the word to phone converter?
    def buildIPA(self):

        for word in self.wordLst:
            unicodeWord = word
            try:
                #self.IPADict[word] = self.CMUDict[unicodeWord][0]
                self.IPADict[word] = str(check_output(["espeak", "-q","--ipa",'-v','en-us',unicodeWord]))
                #print check_output(["espeak", "-q","--ipa",'-v','en-us',unicodeWord]).decode('utf8')
            except:

                print(unicodeWord + " not found in IPA")
                sys.exit()


    def __getSyllabDict(self):
        syllabDict = {}
        if(self.comparator == "NIST"):
            for key in self.ArpabetDict:

                syllabif = self.__getSyllabificationCMU(self.ArpabetDict[key])
                syllabDict[key] = syllabif
        else:
            '''
            for key in self.IPADict:
                print key, self.IPADict[key]
                syllabif = self.__getSyllabificationIPA(self.IPADict[key])
                syllabDict[key] = syllabif
            '''
            for key in self.wordLst:
                syllabif = self.__getSyllabificationIPA(self.IPADict[key])
                syllabDict[key] = syllabif

            #Will need some sort of parser here to ensure that the
            #syllabifier can handle it

        return syllabDict

    #this is where the celex phonetic string will come in
    #Function will need to go into the celex database to
    #find the words syllabification
    def __getSyllabificationIPA(self,pronunciation):
        return "IA"



    #For each word that is asked to be syllabified
    #it needs to go through a word to phone translation
    #This is what CMU is used for.
    def __getSyllabificationCMU(self, pronunciation):
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
        finalSyllab = self.NISTClient.syllabify(ArpString)
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
