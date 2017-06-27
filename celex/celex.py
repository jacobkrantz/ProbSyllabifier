from datastore import SQLQueryService
from probSyllabifier import ProbSyllabifier, HMM
from utils import AbstractSyllabRunner

# TODO assert against total word count in `buildSets`
# TODO figure out if it is worth training HMM off database or conform to files

class CELEX(AbstractSyllabRunner):

    def __init__(self):
        self.SQLQueryService = SQLQueryService("wordformsDB")
        self.ps = ProbSyllabifier()
        self._trainingSize = 0
        self._testingSize = 0
        self._trainingSet = set()
        self._testingSet = set()
        self._CSylResultsDict = dict()

    def trainHMM(self):
        self._buildSets()
        self._CSylResultsDict = self.SQLQueryService.getManySyllabifications(self._trainingSet)
        syllabifiedList = self._CSylResultsDict.values()
        hmm = HMM(2, syllabifiedList) # lang hack: 2 is celex
        self._trainingSet = set() # clear memory

        hmm.buildMatrixA() # "./HMMFiles/MatrixA.txt"
        hmm.buildMatrixB() # "./HMMFiles/MatrixB.txt"
        hmm.makeViterbiFiles()

    def testHMM(self):
        PSylResultsDict = self._syllabifyTesting()
        testResultsList = self._combineResults(PSylResultsDict, CSylResultsDict)
        self._fillResultsTable(testResultsList)
        self._compareResults()

    # returns string of syllabified observation
    def syllabify(self, observation):
        return self.ps.syllabify(observation)

    def syllabifyFile(self, fileIN, fileOUT, comparator):
        self.ps.syllabifyFile(fileIN, fileOUT, comparator)

    #----------------#
    #   "Private"    #
    #----------------#

    def _buildSets(self):
        trainingSize = int(input("enter number of words to train on:"))
        testingSize = int(input("enter number of words to test on:"))

        self._trainingSet = self._toASCII(self.SQLQueryService.getWordSubset(trainingSize))
        self._testingSet = self._toASCII(self.SQLQueryService.getWordSubset(testingSize, self._trainingSet))

    # returns dictionary of {testWord:syllabification} for both ProbSyl and CELEX
    def _syllabifyTesting(self):
        if len(self._CSylResultsDict) == 0:
            self._CSylResultsDict = getManySyllabifications(self._testingSet)
        pronunciationsDict = getManyPronunciations(self._testingSet)

        for wordKey in pronunciationsDict:
             pronunciation = pronunciationsDict[wordKey]
             ProbSylDict[wordKey] = self.ps.syllabify(pronunciation)
        return ProbSylDict, CELEXSylDict

    # returns a list of dictionaries containing
    # definitions for the "workingresults" table
    def _combineResults(self, PResultsDict, CResultsDict):
        testResultsList = []
        for word,PSyllab in PResultsDict.iteritems():
            CSyllab = CResultsDict[word]
            isSame = (CSyllab == PSyllab)
            testResultsLine = { "Word":word, "ProbSyl":PSyllab, "CSyl":CSyllab, "Same":isSame }
            testResultsList.append(testResultsLine)
        return testResultsList

    def _fillResultsTable(self, testResultsList):
        self.SQLQueryService.truncateTable("workingresults")
        lambda resultLine: self.SQLQueryService.insertIntoTable("workingresults", resultLine), testResultsList

    # prints out general results comparison from "workingresults" table
    def _compareResults(self):
        wordCount = self.SQLQueryService.getTotalWordCount()
        sameSyllabCount = self.SQLQueryService.getIsSameSyllabificationCount()
        percentSame = "{0:.2f}".format(sameSyllabCount / float(wordCount))
        print "ProbSyllabifier is " + percentSame + "similar to CELEX."

    def _toASCII(self, wordLst):
        return map(lambda x: x[0].encode('utf-8'), wordLst)
