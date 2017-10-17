from config import settings as config
from datastore import SQLQueryService
from probSyllabifier import ProbSyllabifier, HMM
from utils import AbstractSyllabRunner
import logging as log
import uuid

# transcriptionSchemes passed in will be modified to include
# static entries as specified in Celex.addStaticTags()
class Celex(AbstractSyllabRunner):

    def __init__(self):
        log.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', datefmt='%X', level=log.INFO)
        self.SQLQueryService = SQLQueryService()
        self._CSylResultsDict = dict()
        self._pronunciationsDict = dict()
        self._syllabifiedLst = []

    # Prompts user for training and testing sizes.
    # Loads sets, trains the HMM, and syllabifies Celex.
    def InputTrainHMM(self):
        trainingSize = int(input("enter number of words to train on: "))
        testingSize = int(input("enter number of words to test on: "))
        self.loadSets(trainingSize, testingSize)
        return self.trainHMM()

    # Populates testing and training sets.
    # Computes CELEX syllabification results.
    def loadSets(self, trainingSize, testingSize):
        log.info("Starting step: Building sets.")
        trainingSet = self._toASCII(self.SQLQueryService.getWordSubset(trainingSize))
        testingSet = self._toASCII(self.SQLQueryService.getWordSubset(testingSize, trainingSet))
        self._CSylResultsDict = self.SQLQueryService.getManySyllabifications(trainingSet)
        self._syllabifiedLst = self._CSylResultsDict.values()
        log.info("Finished step: Building sets.")
        log.info("Starting step: Syllabify CELEX")
        self._CSylResultsDict = self.SQLQueryService.getManySyllabifications(testingSet)
        self._pronunciationsDict = self.SQLQueryService.getManyPronunciations(testingSet)
        log.info("Finished step: Syllabify CELEX")

    def trainHMM(self, transcriptionScheme=[]):
        GUID = str(uuid.uuid1()) # set new GUID based on host machine and current time

        log.info("Starting step: Train HMM Model")
        self.hmm = HMM(2, self.addStaticTags(transcriptionScheme), self._syllabifiedLst) # lang hack: 2 is celex
        self.hmm.setGUID(GUID)
        self.hmm.buildMatrixA()
        self.hmm.buildMatrixB()
        self.hmm.makeViterbiFiles()
        log.info("Finished step: Train HMM Model")
        return GUID

    # thread-safe when DB results is false.
    def testHMM(self, transcriptionScheme=[], GUID=""):
        pSylResultsDict = self._syllabifyTesting(GUID, self.addStaticTags(transcriptionScheme))
        testResultsList = self._combineResults(pSylResultsDict)

        if(config["write_results_to_DB"]):
            self._fillResultsTable(testResultsList)

        self.hmm.clean()
        self._CSylResultsDict = dict()
        self._PSylResultsDict = dict()
        return self._compare(testResultsList)

    # Where Psyl is different than Csyl,
    # Returns: [{ Word, PSyllab, CSyllab, isSame },{...}]
    def getIncorrectResults(self):
        return self.SQLQueryService.getIncorrectResults()

    # returns string of syllabified observation
    def syllabify(self, observation):
        return self.ps.syllabify(observation, "CELEX")

    def syllabifyFile(self, fileIN, fileOUT):
        self.ps.syllabifyFile(fileIN, fileOUT, "CELEX")

    #----------------#
    #   "Private"    #
    #----------------#

    # builds dictionary of {testWord:syllabification}
    # for pSylResultsDict
    def _syllabifyTesting(self, GUID, transcriptionScheme=[]):
        log.info("Starting step: Syllabify ProbSyllabifier")
        self.ps = ProbSyllabifier(transcriptionScheme)
        self.ps.loadStructures(GUID)
        pSylResultsDict = {}
        for word, pronunciation in self._pronunciationsDict.iteritems():
            pSylResultsDict[word] = self.ps.syllabify(pronunciation, "CELEX")
        log.info("Finished step: Syllabify ProbSyllabifier")
        return pSylResultsDict

    # Queries result lines from the "workingresults" table
    # Returns: [{ Word, PSyllab, CSyllab, isSame },{...}]
    def _combineResults(self, PResultsDict):
        testResultsList = []
        for word,PSyllab in PResultsDict.iteritems():
            if not PSyllab:
                PSyllab = ""
            CSyllab = self._CSylResultsDict[word]
            isSame = int(CSyllab == PSyllab)
            testResultsLine = { "Word":word, "ProbSyl":PSyllab, "CSyl":CSyllab, "Same":isSame }
            testResultsList.append(testResultsLine)
        return testResultsList

    # given: [{ Word, PSyllab, CSyllab, isSame },{...}]
    # publishes results to "workingresults" table
    def _fillResultsTable(self, testResultsList):
        self.SQLQueryService.truncateTable("workingresults")
        for resultLine in testResultsList:
            self.SQLQueryService.insertIntoTable("workingresults", resultLine)

    def _compare(self, testResultsList):
        totalEntries = float(len(testResultsList))
        skippedSyllabCount = 0
        numSame = 0
        for entry in testResultsList:
            if(entry["Same"] == 1):
                numSame += 1
            elif(entry["ProbSyl"] == ""):
                skippedSyllabCount += 1
        percentSame = "{0:.2f}".format(100 * numSame / totalEntries)
        ignoredPercentSame = "{0:.2f}".format(100 * numSame / totalEntries - float(skippedSyllabCount))
        print "\n----------------------------------------"
        print "ProbSyllabifier is " + percentSame + "% similar to CELEX."
        print "Ignoring", skippedSyllabCount, "skips:", ignoredPercentSame, "%"
        print "----------------------------------------"
        return percentSame

    # add all static tags to the incoming transcriptionScheme.
    # current use: include start and end tags for a word ('<', '>')
    #   as its own category.
    def addStaticTags(self, transcriptionScheme):
        startAndEnd = ['<','>']
        if (startAndEnd not in transcriptionScheme) and (len(transcriptionScheme) > 0):
            transcriptionScheme.append(startAndEnd)
        return transcriptionScheme

    def _toASCII(self, wordLst):
        return map(lambda x: x[0].encode('utf-8'), wordLst)
