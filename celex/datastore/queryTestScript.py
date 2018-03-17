import time

from sqlQueryService import SQLQueryService

# this is just thrown together to
# 1) give an idea as to how to use it and
# 2) to ensure it works.

print "Running Query Test..."
qs = SQLQueryService("wordforms_db")


def pronunciation_test():
    print "Test fixture: getSinglePronunciation"
    print "'spaghetti' query:\t", qs.get_single_pronunciation("spaghetti")
    print "Bad query:\t", qs.get_single_pronunciation("asfdsgfh")
    print "Empty query:\t", qs.get_single_pronunciation(""), '\n'

    print "Test fixture: getManyPronunciations"
    print "Query:\t\t", qs.get_many_pronunciations(["words", "are", "neat"])
    print "Bad query:\t", qs.get_many_pronunciations(["asdfdgf", ""])
    print "Empty query:\t", qs.get_many_pronunciations([]), '\n'


def syllabification_test():
    print "Test fixture: getSingleSyllabification"
    print "'spaghetti' query:\t", qs.get_single_syllabification("spaghetti")
    print "Bad query:\t", qs.get_single_syllabification("asfdsgfh")
    print "Empty query:\t", qs.get_single_syllabification(""), '\n'

    print "Test fixture: getManySyllabifications"
    print "Query:\t\t", qs.get_many_syllabifications(
        ["Saturday", "is", "splendid"]
    )
    print "Bad query:\t", qs.get_many_syllabifications(["asdfdgf", ""])
    print "Empty query:\t", qs.get_many_syllabifications([]), '\n'


def word_queries_test():
    start_time = time.clock()
    word_subset = qs.get_word_subset(10000)
    second_set = qs.get_word_subset(10000, word_subset)
    time_delta = "{0:.2f}".format(time.clock() - start_time)
    print "Test fixture: word queries"
    print "Time to query two unique sets of 10000 words:", "%ss" % time_delta
    print "Total word count in 'words':", qs.getTotalWordCount(), '\n'
    print word_subset.pop()


pronunciation_test()
syllabification_test()
word_queries_test()
