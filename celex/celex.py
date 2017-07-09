from datastore import SQLQueryService
from probSyllabifier import ProbSyllabifier, HMM
from utils import AbstractSyllabRunner

# TODO assert against total word count in `buildSets`

class CELEX(AbstractSyllabRunner):

    def __init__(self):
        self.SQLQueryService = SQLQueryService("wordformsDB")
        self.ps = ProbSyllabifier()
        self._trainingSet = set()
        self._testingSet = set()
        self._CSylResultsDict = dict()
        self._PSylResultsDict = dict()

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
        self._syllabifyTesting()
        testResultsList = self._combineResults(self._PSylResultsDict, self._CSylResultsDict)
        self._fillResultsTable(testResultsList)
        self._compareResults()
        self._CSylResultsDict = dict()
        self._PSylResultsDict = dict()

    # returns string of syllabified observation
    def syllabify(self, observation):
        return self.ps.syllabify(observation, "CELEX")

    def syllabifyFile(self, fileIN, fileOUT):
        self.ps.syllabifyFile(fileIN, fileOUT, "CELEX")

    #----------------#
    #   "Private"    #
    #----------------#

    def _buildSets(self):
        trainingSize = int(input("enter number of words to train on: "))
        testingSize = int(input("enter number of words to test on: "))

        self._trainingSet = self._toASCII(self.SQLQueryService.getWordSubset(trainingSize))
        self._testingSet = self._toASCII(self.SQLQueryService.getWordSubset(testingSize, self._trainingSet))

    # builds dictionary of {testWord:syllabification}
    # for self._PSylResultsDict and self._CSylResultsDict
    def _syllabifyTesting(self):
        self._CSylResultsDict = self.SQLQueryService.getManySyllabifications(self._testingSet)
        pronunciationsDict = self.SQLQueryService.getManyPronunciations(self._testingSet)

        for word, pronunciation in pronunciationsDict.iteritems():
             self._PSylResultsDict[word] = self.ps.syllabify(pronunciation, "CELEX")

    # returns a list of dictionaries containing
    # definitions for the "workingresults" table
    def _combineResults(self, PResultsDict, CResultsDict):
        testResultsList = []
        for word,PSyllab in PResultsDict.iteritems():
            if not PSyllab:
                PSyllab = ""
            CSyllab = CResultsDict[word]
            isSame = int(CSyllab == PSyllab)
            testResultsLine = { "Word":word, "ProbSyl":PSyllab, "CSyl":CSyllab, "Same":isSame }
            testResultsList.append(testResultsLine)
        return testResultsList

    def _fillResultsTable(self, testResultsList):
        self.SQLQueryService.truncateTable("workingresults")
        for resultLine in testResultsList:
            self.SQLQueryService.insertIntoTable("workingresults", resultLine)

    # prints out general results comparison from "workingresults" table
    def _compareResults(self):
        wordCount = self.SQLQueryService.getEntryCount("workingresults")
        sameSyllabCount = self.SQLQueryService.getIsSameSyllabificationCount()
        percentSame = "{0:.2f}".format(100 * sameSyllabCount / float(wordCount))
        print "ProbSyllabifier is " + percentSame + "% similar to CELEX."
        print "To view results, query the 'workingresults' table in 'wordformsDB'."

    def _toASCII(self, wordLst):
        return map(lambda x: x[0].encode('utf-8'), wordLst)
