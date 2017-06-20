from SQLiteClient import SQLiteClient
from contextlib import closing

class SQLQueryService(SQLiteClient):

    # returns "" if word is not in the database
    def getSinglePronunciation(self, word):
        SQL = """SELECT %s FROM pronunciations WHERE Word= ?""" % self._getAlphabetColumn("Phon")
        with closing(self.connection.cursor()) as cursor:
            cursor.execute(SQL, (word,))
            pronunciation = cursor.fetchone()
            return pronunciation[0] if pronunciation else ""

    # wordList: list of strings
    # returns dictionary of {word:pronunciation}
    # if the word does not exist in the database, entry is not returned
    def getManyPronunciations(self, wordList):
        wordsString = ', '.join(map(str, wordList))
        places = ','.join(['?'] * len(wordList))
        words = tuple(wordList)
        SQL = """SELECT Word, %s FROM pronunciations WHERE Word IN ({})""" % self._getAlphabetColumn("Phon")

        with closing(self.connection.cursor()) as cursor:
            cursor.execute(SQL.format(places), words)
            pronunciations = dict(cursor.fetchall())
            return { str(key):str(value) for key,value in pronunciations.items() }



    #----------------#
    #   "Private"    #
    #----------------#

    def _getAlphabetColumn(self, prefix):
        return prefix + self.config[self._databaseContext]["default_alphabet"]


if(__name__ == "__main__"):
    "Running Query Test..."
    qs = SQLQueryService("wordformsDB")
    print "Query on getManyPronunciations:", qs.getManyPronunciations(["words","are","neat"])
    print "Empty query on getManyPronunciations:", qs.getManyPronunciations([])

    print "Empty query on getSinglePronunciation:", qs.getSinglePronunciation("")
    print "'spaghetti' query on getSinglePronunciation:", qs.getSinglePronunciation("spaghetti")
