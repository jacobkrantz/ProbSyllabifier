from probSyllabifier import HMM, ProbSyllabifier
from nistClient import NISTClient
from testing import CompareNIST
from utils import AbstractSyllabRunner, FrequentWords as FW

class NIST(AbstractSyllabRunner):

    def __init__(self):
        self.NISTClient = NISTClient()
        self.cNIST = CompareNIST()
        self._lang = 1 # 1 == NIST, needed for HMM. outdated.

    def trainHMM(self):
        self._buildSets()
        self._trainHMM()

    def testHMM(self):
        self.ps = ProbSyllabifier()
        testIN = "./corpusFiles/testSet.txt"
        testOUT = "./HMMFiles/probSyllabs.txt"
        self.ps.syllabifyFile(testIN, testOUT,"NIST")

        NISTname = "./HMMFiles/NISTtest.txt"
        probName = "./HMMFiles/probSyllabs.txt"
        self.cNIST.compare(NISTname, probName)

        viewDif = raw_input("view differences (y): ")
        if(viewDif == 'y'):
            self.cNIST.viewDifferences()

    # returns string of syllabified observation
    def syllabify(self, observation):
        try:
            return self.ps.syllabify(observation)
        except:
            self.ps = ProbSyllabifier()
            return self.ps.syllabify(observation)

    def syllabifyFile(self, fileIN, fileOUT, comparator="NIST"):
        try:
            self.ps.syllabifyFile(fileIN, fileOUT, comparator)
        except:
            self.ps = ProbSyllabifier()
            self.ps.syllabifyFile(fileIN, fileOUT, comparator)

    #----------------#
    #   "Private"    #
    #----------------#

    def _buildSets(self):
        inFile = "./corpusFiles/brown_words.txt" #/editorial_words.txt
        outFile = "./HMMFiles/SyllabDict.txt"
        freqFile = "./corpusFiles/freqWords.txt"

        inTest = "./corpusFiles/testSet.txt"
        outTest = "./HMMFiles/NISTtest.txt"

        print ("current input file: " + inFile)
        print ("current output file: " + outFile)

        user_in = raw_input("Press enter to continue, or 'c' to change: ")
        if(user_in == 'c'):
            inFile = raw_input("choose input file: ")
            outFIle = raw_input("choose output file: ")

        self._generateWords(inFile, inTest)
        try:
            self.NISTClient.syllabifyFile(freqFile,outFile)
            self.NISTClient.syllabifyFile(inTest,outTest)

        except IOError as err:
            print err

    # build A and B matrices. Makes files to be used in the Viterbi
    # decoding algorithm.
    def _trainHMM(self):
        hmm = HMM(self._lang)

        hmm.buildMatrixA() # "./HMMFiles/MatrixA.txt"
        hmm.buildMatrixB() # "./HMMFiles/MatrixB.txt"
        hmm.makeViterbiFiles()
        print("Items in training set: " + str(hmm.getTrainingSize()))

    # builds word set files to be used in NIST syllabification
    def _generateWords(self, fileIn, testFileIn):
        fw = FW()
        numWords = int(raw_input("Enter number of words to syllabify: "))
        numTestWords = int(raw_input("Enter number of words to test on: "))

        # pulling from entire corpus or editorials
        fileIn = "./corpusFiles/brown_words.txt" #/editorial_words.txt
        fwOut = "./corpusFiles/freqWords.txt"

        fw.generateMostFreq(fileIn, fwOut, numWords)
        fw.generateTesting(fileIn, testFileIn, numTestWords) # testFileIn is outfile
