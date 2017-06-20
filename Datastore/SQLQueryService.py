from SQLiteClient import SQLiteClient
from contextlib import closing

# TODO: implement getWordSubset to support testing and training set construction

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
        columnName = self._getAlphabetColumn("Phon")
        SQL = """SELECT Word, %s FROM pronunciations WHERE Word IN ({})""" % columnName

        with closing(self.connection.cursor()) as cursor:
            cursor.execute(SQL.format(places), words)
            pronunciations = dict(cursor.fetchall())
            return { str(key):str(value) for key,value in pronunciations.items() }

    # returns "" if word is not in the database
    def getSingleSyllabification(self, word):
        SQL = """SELECT %s FROM syllabifications WHERE Word= ?""" % self._getAlphabetColumn("PhonSyl")
        with closing(self.connection.cursor()) as cursor:
            cursor.execute(SQL, (word,))
            syllabification = cursor.fetchone()
            return syllabification[0] if syllabification else ""

    # wordList: list of strings
    # returns dictionary of {word:syllabification}
    # if the word does not exist in the database, entry is not returned
    def getManySyllabifications(self, wordList):
        wordsString = ', '.join(map(str, wordList))
        places = ','.join(['?'] * len(wordList))
        words = tuple(wordList)
        columnName = self._getAlphabetColumn("PhonSyl")
        SQL = """SELECT Word, %s FROM syllabifications WHERE Word IN ({})""" % columnName

        with closing(self.connection.cursor()) as cursor:
            cursor.execute(SQL.format(places), words)
            syllabifications = dict(cursor.fetchall())
            return { str(key):str(value) for key,value in syllabifications.items() }

    # numberOfWords: integer
    # wordBlacklist: list of strings
    #
    def getWordSubset(self, numberOfWords, wordBlacklist=[]):
        if numberOfWords + len(wordBlacklist) > self._getCountOfWordEntries:
            raise IndexException("numberOfWords exceeds potential entries in 'words' table")
        pass

    #----------------#
    #   "Private"    #
    #----------------#

    def _getAlphabetColumn(self, prefix):
        return prefix + self.config[self._databaseContext]["default_alphabet"]


    def _getCountOfWordEntries(self):
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("SELECT COUNT (*) FROM words")
            return cursor.fetchone()[0]


class IndexException(Exception):
    pass
