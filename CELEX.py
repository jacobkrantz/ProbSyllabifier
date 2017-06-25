#from Datastore/SQLQueryService import SQLQueryService.SQLQueryService
from Datastore import SQLQueryService
from abstractSyllabRunner import AbstractSyllabRunner
from Datastore import SQLiteClient
#from ProbSyllabifier import ProbSyllabifier

# TODO assert against total word count in `buildSets`
# TODO figure out if it is worth training HMM off database or conform to files
# TODO implement compareResults
# TODO figure out python's crappy way of doing 'packages'

class Celex(AbstractSyllabRunner):

    def __init__(self):
        self.SQLQueryService = SQLQueryService(SQLiteClient)
        self._trainingSize = 0
        self._testingSize = 0
        self._trainingSet = set()
        self._testingSet = set()

    def trainHMM(self):
        buildSets()
        hmm = HMM(lang)

        hmm.buildMatrixA() # "./HMMFiles/MatrixA.txt"
        hmm.buildMatrixB() # "./HMMFiles/MatrixB.txt"
        hmm.makeViterbiFiles()

    def testHMM(self):
        PSylResultsDict, CSylResultsDict = self._syllabifyTesting()
        testResultsList = self._combineResults(PSylResultsDict, CSylResultsDict)
        self._fillResultsTable(testResultsList)

    # prints out general results comparison gathered from "workingresults" table
    def compareResults(self):
        pass

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
        ps = ProbSyllabifier()
        pronunciationsDict = getManyPronunciations(self._testingSet)
        CELEXSylDict = getManySyllabifications(self._testingSet)

        for wordKey in pronunciationsDict:
             pronunciation = pronunciationsDict[wordKey]
             ProbSylDict[wordKey] = ps.syllabify(pronunciation)
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
        truncateTable("workingresults")
        lambda resultLine: insertIntoTable("workingresults", resultLine), testResultsList

if(__name__ == "__main__"):
    c = Celex()
