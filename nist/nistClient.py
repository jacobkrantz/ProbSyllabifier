from nltk.corpus import cmudict
from subprocess import Popen, PIPE, STDOUT
import subprocess
import shlex
import re

'''
module for running the NIST Syllabifier
assumes tsylb2 file exists in directory '~/NIST/tsylb2-1.1/'
'''
class NISTClient:

    def __init__(self):
        self.CMUDict = cmudict.dict()
        self.outFile = ""
        self.inFile = ""

    ## uses NIST to find syllabification of a word in arpabet
    ## ArpString must have no stress
    ## returns list of syllabifications
    def syllabify(self, ArpString):
        syllabs = []
        try:
            ArpString = ArpString.lower()
            data      = self._runNIST(ArpString)
            syllabs   = self._parseNISTData(data, ArpString)

        except:
            print("Arpabet String Input Error.")

        return syllabs

    # given an input file, will syllabify all the words within.
    # Outputs as a syllabification dictionary to specified
    # output file. Parsing of this file shown in 'utils.py'.
    def syllabifyFile(self, inputFile, outputFile):
        wordLst = self.readWords(inputFile)
        arpabetDict = self.buildArpabet(wordLst)
        syllabDict = self._getSyllabDict(arpabetDict)
        self.printDictToFile(syllabDict, outputFile)

    ## ------------------------------
    ##            PRIVATE
    ## ------------------------------

    ## takes in a phonetic pronounciation and runs them through NIST
    ## returns the proper syllabification(s) in a list
    # Param 1: An arpabet string
    def _runNIST(self,ArpString):
        p = subprocess.Popen("cd ~/NIST/tsylb2-1.1/ && ./tsylb2 -n phon1ax.pcd", shell = True,stdin = PIPE,stdout = PIPE,stderr = PIPE, bufsize = 1)
        return p.communicate(input = ArpString + "\n")[0] # data = output

    ## takes in the raw output of NIST
    ## parses for pronounciations and returns all in a list
    # Param 1: ????
    # Param 2: ???
    def _parseNISTData(self, data, ArpString):
        pattern   = '\/.*?\/'
        pattern2 = '[^0-9]'
        error     = 'ERR'
        returnLst = []
        proLst    = []

        data = str(data)

        if(len(re.findall(error, data))):
            print("Error. No syllabification found for: " + ArpString)

        proLst = re.findall(pattern, data)
        proLst = proLst[1:]

        for item in proLst:
            tmp = item.strip('/# ')
            tmp = tmp.strip('#')
            newString = ""
            for i in range(len(tmp)):
                if(tmp[i] !='0' and tmp[i] != '1' and tmp[i] != '2' and tmp[i] !="'"):
                    newString += tmp[i]
            returnLst.append(newString)

        return returnLst

    ## needs textfile of words to exist in specified directory
    ## imports words from file as list of words.
    ## populates self.wordLst with file contents.
    ## throws IOError if file not found
    def readWords(self, inFile):
        with open(inFile,'r') as wordFile:
            words = ""
            for line in wordFile:
                words = words + ' ' + line
        return words.split()

    ## looks up each word in cmudict and adds the word and pronunciation
    ## to a dictionary. Values are in list format with unicode phonemes.
    ## Only takes the first pronounciation for CMU when multiple exist.
    def buildArpabet(self, wordLst):
        arpabetDict = {}
        for word in wordLst:
            unicodeWord = unicode(word)

            try:
                arpabetDict[word] = self.CMUDict[unicodeWord][0]
            except:
                print(unicodeWord + " not found in CMUDict")
                sys.exit()

        return arpabetDict

    def _getSyllabDict(self, arpabetDict):
        syllabDict = {}
        for key in arpabetDict:
            syllabif = self._getSyllabificationCMU(arpabetDict[key])
            syllabDict[key] = syllabif

        #need parser here to ensure that the syllabifier can handle it
        return syllabDict

    #For each word that is asked to be syllabified
    #it needs to go through a word to phone translation
    #This is what CMU is used for.
    def _getSyllabificationCMU(self, pronunciation):
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

        return self.syllabify(ArpString)

    ## dictionary format: word: [[syllab1],[syllab2]...]
    def printDictToFile(self, Dict, outFile):
        with open(outFile,'w') as outF:
            for entry in Dict:
                outF.write(str(entry))
                outF.write(" ")
                outF.write(str(Dict[entry][0]))
                outF.write("\n")

        print ("File successfully syllabified to: " + outFile)
