from datastore import SQLQueryService
from probSyllabifier import ProbSyllabifier, HMM
from utils import AbstractSyllabRunner
import logging as log
import json
import uuid

class CELEX(AbstractSyllabRunner):

    def __init__(self):
        log.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', datefmt='%X', level=log.INFO)
        self.SQLQueryService = SQLQueryService("wordformsDB")
        self._testingSet = set()
        self._CSylResultsDict = dict()
        self._PSylResultsDict = dict()
        with open('config.json') as json_data_file:
            self.config = json.load(json_data_file)

    # returns GUID for trained HMMFiles
    def InputTrainHMM(self):
        trainingSize = int(input("enter number of words to train on: "))
        testingSize = int(input("enter number of words to test on: "))
        return self.trainHMM(trainingSize, testingSize)

    # returns GUID for trained HMMFiles
    def trainHMM(self, trainingSize, testingSize, transciptionScheme=[]):
        # set new GUID based on host machine and current time
        GUID = str(uuid.uuid1())

        log.info("Starting step: Building sets.")
        syllabifiedLst = self._buildSets(trainingSize, testingSize)
        log.info("Finished step: Building sets.")

        log.info("Starting step: Initialize training structures")
        self.hmm = HMM(2, transciptionScheme, syllabifiedLst) # lang hack: 2 is celex
        log.info("Finished step: Initialize training structures")

        log.info("Starting step: Train HMM Model")
        self.hmm.setGUID(GUID)
        self.hmm.buildMatrixA()
        self.hmm.buildMatrixB()
        self.hmm.makeViterbiFiles()
        log.info("Finished step: Train HMM Model")
        return GUID

    def testHMM(self, transciptionScheme=[], GUID=""):
        self._syllabifyTesting(transciptionScheme, GUID)
        testResultsList = self._combineResults(self._PSylResultsDict, self._CSylResultsDict)

        self._CSylResultsDict = dict()
        self._PSylResultsDict = dict()
        self.hmm.clean()

        if(self.config["write_results_to_DB"]):
            self._fillResultsTable(testResultsList)
            return self._compareResults()
        return self._compareInMemory(testResultsList)

    # returns string of syllabified observation
    def syllabify(self, observation, GUID=""):
        self.ps.loadStructures(GUID)
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
        trainingSet = self._toASCII(self.SQLQueryService.getWordSubset(trainingSize))
        self._testingSet = self._toASCII(self.SQLQueryService.getWordSubset(testingSize, trainingSet))
        self._CSylResultsDict = self.SQLQueryService.getManySyllabifications(trainingSet)
        return self._CSylResultsDict.values()

    # builds dictionary of {testWord:syllabification}
    # for self._PSylResultsDict and self._CSylResultsDict
    def _syllabifyTesting(self,transciptionScheme=[], GUID=""):
        log.info("Starting step: Syllabify CELEX")
        self._CSylResultsDict = self.SQLQueryService.getManySyllabifications(self._testingSet)
        log.info("Finished step: Syllabify CELEX")

        pronunciationsDict = self.SQLQueryService.getManyPronunciations(self._testingSet)

        log.info("Starting step: Syllabify ProbSyllabifier")
        self.ps = ProbSyllabifier(transciptionScheme)
        self.ps.loadStructures(GUID)
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

    def _compareInMemory(self, testResultsList):
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

    def _toASCII(self, wordLst):
        return map(lambda x: x[0].encode('utf-8'), wordLst)
