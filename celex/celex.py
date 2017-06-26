from probSyllabifier import ProbSyllabifier
from utils import AbstractSyllabRunner
from datastore import SQLQueryService
from datastore import SQLiteClient

# TODO assert against total word count in `buildSets`
# TODO figure out if it is worth training HMM off database or conform to files

class CELEX(AbstractSyllabRunner):

    def __init__(self):
        self.SQLQueryService = SQLQueryService()
        self.ps = ProbSyllabifier()
        self._trainingSize = 0
        self._testingSize = 0
        self._trainingSet = set()
        self._testingSet = set()

    def trainHMM(self):
        self._buildSets()
        hmm = HMM(lang)

        hmm.buildMatrixA() # "./HMMFiles/MatrixA.txt"
        hmm.buildMatrixB() # "./HMMFiles/MatrixB.txt"
        hmm.makeViterbiFiles()

    def testHMM(self):
        PSylResultsDict, CSylResultsDict = self._syllabifyTesting()
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

        self._trainingSet = getWordSubset(trainingSize)
        self._testingSet = getWordSubset(testingSize, self._trainingSet)

    # returns dictionary of {testWord:syllabification} for both ProbSyl and CELEX
    def _syllabifyTesting(self):
        pronunciationsDict = getManyPronunciations(self._testingSet)
        CELEXSylDict = getManySyllabifications(self._testingSet)

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
