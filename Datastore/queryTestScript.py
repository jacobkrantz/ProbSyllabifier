from SQLQueryService import SQLQueryService
# this is just thrown together to
# 1) give an idea as to how to use it and
# 2) to ensure it works.

print "Running Query Test..."
qs = SQLQueryService("wordformsDB")

print "Test fixture: 'getSinglePronunciation'"
print "'spaghetti' query:\t", qs.getSinglePronunciation("spaghetti")
print "Bad query:\t", qs.getSinglePronunciation("asfdsgfh")
print "Empty query:\t", qs.getSinglePronunciation("")

print "\nTest fixture on 'getManyPronunciations'"
print "Query:\t\t", qs.getManyPronunciations(["words","are","neat"])
print "Bad query:\t", qs.getManyPronunciations(["asdfdgf",""])
print "Empty query:\t", qs.getManyPronunciations([])

print "\nTest fixture: 'getSingleSyllabification'"
print "'spaghetti' query:\t", qs.getSingleSyllabification("spaghetti")
print "Bad query:\t", qs.getSingleSyllabification("asfdsgfh")
print "Empty query:\t", qs.getSingleSyllabification("")

print "\nTest fixture on 'getManySyllabifications'"
print "Query:\t\t", qs.getManySyllabifications(["Saturday","is","splendid"])
print "Bad query:\t", qs.getManySyllabifications(["asdfdgf",""])
print "Empty query:\t", qs.getManySyllabifications([])
