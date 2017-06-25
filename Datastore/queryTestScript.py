from SQLQueryService import SQLQueryService
import time
# this is just thrown together to
# 1) give an idea as to how to use it and
# 2) to ensure it works.

print "Running Query Test..."
qs = SQLQueryService("wordformsDB")

def pronunciationTest():
    print "Test fixture: getSinglePronunciation"
    print "'spaghetti' query:\t", qs.getSinglePronunciation("spaghetti")
    print "Bad query:\t", qs.getSinglePronunciation("asfdsgfh")
    print "Empty query:\t", qs.getSinglePronunciation(""), '\n'

    print "Test fixture: getManyPronunciations"
    print "Query:\t\t", qs.getManyPronunciations(["words","are","neat"])
    print "Bad query:\t", qs.getManyPronunciations(["asdfdgf",""])
    print "Empty query:\t", qs.getManyPronunciations([]), '\n'

def syllabificationTest():
    print "Test fixture: getSingleSyllabification"
    print "'spaghetti' query:\t", qs.getSingleSyllabification("spaghetti")
    print "Bad query:\t", qs.getSingleSyllabification("asfdsgfh")
    print "Empty query:\t", qs.getSingleSyllabification(""), '\n'

    print "Test fixture: getManySyllabifications"
    print "Query:\t\t", qs.getManySyllabifications(["Saturday","is","splendid"])
    print "Bad query:\t", qs.getManySyllabifications(["asdfdgf",""])
    print "Empty query:\t", qs.getManySyllabifications([]), '\n'

def wordQueriesTest():
    startTime = time.clock()
    wordSubSet = qs.getWordSubset(10000)
    secondSet = qs.getWordSubset(10000, wordSubSet)
    timeDelta = "{0:.2f}".format(time.clock() - startTime)
    print "Test fixture: word queries"
    print "Time to query two unique sets of 10000 words:", "%ss" %timeDelta
    print "Total word count in 'words':", qs.getTotalWordCount(), '\n'
    print wordSubSet.pop()


pronunciationTest()
syllabificationTest()
wordQueriesTest()
