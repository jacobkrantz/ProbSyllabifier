from datastore import SQLQueryService
from probSyllabifier import ProbSyllabifier, HMM
from utils import AbstractSyllabRunner
import logging as log

class CELEX(AbstractSyllabRunner):

    def __init__(self):
        log.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', datefmt='%X', level=log.INFO)
        self.SQLQueryService = SQLQueryService("wordformsDB")
        self._trainingSet = set()
        self._testingSet = set()
        self._CSylResultsDict = dict()
        self._PSylResultsDict = dict()
        self.GUID = "1000"

    def InputTrainHMM(self):
        trainingSize = int(input("enter number of words to train on: "))
        testingSize = int(input("enter number of words to test on: "))
        self.trainHMM(trainingSize, testingSize)

    def trainHMM(self, trainingSize, testingSize, transciptionScheme=[]):
        # set new GUID for training run
        self.GUID = str(int(self.GUID) + 1)

        log.info("Starting step: Building sets.")
        syllabifiedLst = self._buildSets(trainingSize, testingSize)
        log.info("Finished step: Building sets.")

        log.info("Starting step: Initialize training structures")
        self.hmm = HMM(2, transciptionScheme, syllabifiedLst) # lang hack: 2 is celex
        self._trainingSet = set()     # clear set from memory
        log.info("Finished step: Initialize training structures")

        log.info("Starting step: Train HMM Model")
        self.hmm.setGUID(self.GUID)
        self.hmm.buildMatrixA()
        self.hmm.buildMatrixB()
        self.hmm.makeViterbiFiles()
        log.info("Finished step: Train HMM Model")

    def testHMM(self, transciptionScheme=[]):
        self._syllabifyTesting(transciptionScheme)
        testResultsList = self._combineResults(self._PSylResultsDict, self._CSylResultsDict)
        self._fillResultsTable(testResultsList)
        percentAccuracy = self._compareResults()
        self._CSylResultsDict = dict()
        self._PSylResultsDict = dict()
        self.hmm.clean()
        return percentAccuracy

    # returns string of syllabified observation
    def syllabify(self, observation):
        return self.ps.syllabify(observation, "CELEX")

    def syllabifyFile(self, fileIN, fileOUT):
        self.ps.syllabifyFile(fileIN, fileOUT, "CELEX")

    #----------------#
    #   "Private"    #
    #----------------#

    # Populates testing and training sets.
    # Computes CELEX syllabification results.
    # Returns the phonetic syllabifications in a set.
    def _buildSets(self, trainingSize, testingSize):
        self._trainingSet = self._toASCII(self.SQLQueryService.getWordSubset(trainingSize))
        self._testingSet = self._toASCII(self.SQLQueryService.getWordSubset(testingSize, self._trainingSet))
        self._CSylResultsDict = self.SQLQueryService.getManySyllabifications(self._trainingSet)
        return self._CSylResultsDict.values()

    # builds dictionary of {testWord:syllabification}
    # for self._PSylResultsDict and self._CSylResultsDict
    def _syllabifyTesting(self,transciptionScheme=[]):
        log.info("Starting step: Syllabify CELEX")
        self._CSylResultsDict = self.SQLQueryService.getManySyllabifications(self._testingSet)
        log.info("Finished step: Syllabify CELEX")

        pronunciationsDict = self.SQLQueryService.getManyPronunciations(self._testingSet)

        log.info("Starting step: Syllabify ProbSyllabifier")
        self.ps = ProbSyllabifier(transciptionScheme)
        self.ps.loadStructures(self.GUID)
        for word, pronunciation in pronunciationsDict.iteritems():
            self._PSylResultsDict[word] = self.ps.syllabify(pronunciation, "CELEX")
        log.info("Finished step: Syllabify ProbSyllabifier")

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
    # returns percent accuracy.
    def _compareResults(self):
        wordCount = self.SQLQueryService.getEntryCount("workingresults")
        sameSyllabCount = self.SQLQueryService.getIsSameSyllabificationCount()
        skippedSyllabCount = self.SQLQueryService.getSkippedProbSylCount()
        percentSame = "{0:.2f}".format(100 * sameSyllabCount / float(wordCount))
        ignoredPercentSame = "{0:.2f}".format(100 * sameSyllabCount / float(wordCount - skippedSyllabCount))

        print "\n----------------------------------------"
        print "ProbSyllabifier is " + percentSame + "% similar to CELEX."
        print "Ignoring",skippedSyllabCount,"skips:",ignoredPercentSame,"%"
        print "To view results, query the 'workingresults' table in 'wordformsDB'."
        print "----------------------------------------"
        return percentSame

    def _toASCII(self, wordLst):
        return map(lambda x: x[0].encode('utf-8'), wordLst)
