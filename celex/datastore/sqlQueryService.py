from sqliteClient import SQLiteClient
from contextlib import closing

class SQLQueryService(SQLiteClient):

    # returns "" if word is not in the database
    def getSinglePronunciation(self, word):
        self._checkPermissions("read_permissions")

        query = """
            SELECT %s
            FROM pronunciations
            WHERE Word = ?
            """ % self._getAlphabetColumn("Phon")

        with closing(self.connection.cursor()) as cursor:
            cursor.execute(query, (word,))
            pronunciation = cursor.fetchone()
            return pronunciation[0] if pronunciation else ""

    # wordList: list of strings
    # returns dictionary of {word:pronunciation}
    # if the word does not exist in the database, entry is not returned
    def getManyPronunciations(self, wordList):
        self._checkPermissions("read_permissions")

        wordsString = ', '.join(map(str, wordList))
        places = ','.join(['?'] * len(wordList))
        query = """
            SELECT
                Word,
                %s
            FROM pronunciations
            WHERE Word IN ({})
            """ % self._getAlphabetColumn("Phon")

        with closing(self.connection.cursor()) as cursor:
            cursor.execute(query.format(places), tuple(wordList))
            pronunciations = dict(cursor.fetchall())
            return { str(key):str(value) for key,value in pronunciations.items() }

    # returns "" if word is not in the database
    def getSingleSyllabification(self, word):
        self._checkPermissions("read_permissions")

        query = """
            SELECT %s
            FROM syllabifications
            WHERE Word = ?
            """ % self._getAlphabetColumn("PhonSyl")

        with closing(self.connection.cursor()) as cursor:
            cursor.execute(query, (word,))
            syllabification = cursor.fetchone()
            return syllabification[0] if syllabification else ""

    # wordList: list of strings
    # returns dictionary of {word:syllabification}
    # if the word does not exist in the database, entry is not returned
    def getManySyllabifications(self, wordList):
        self._checkPermissions("read_permissions")

        wordsString = ', '.join(map(str, wordList))
        places = ','.join(['?'] * len(wordList))
        query = """
            SELECT
                Word,
                %s
            FROM syllabifications
            WHERE Word IN ({})
            """ % self._getAlphabetColumn("PhonSyl")

        with closing(self.connection.cursor()) as cursor:
            cursor.execute(query.format(places), tuple(wordList))
            syllabifications = dict(cursor.fetchall())
            return { str(key):str(value) for key,value in syllabifications.items() }

    # returns total number of words in the 'words' table: integer
    def getTotalWordCount(self):
        self._checkPermissions("read_permissions")
        query = """
            SELECT Count(Word)
            FROM words
            """
        with closing(self.connection.cursor()) as cursor:
            cursor.execute(query)
            return cursor.fetchone()[0]

    def getIsSameSyllabificationCount(self):
        self._checkPermissions("read_permissions")
        query = """
            SELECT Count(Same)
            FROM workingresults
            """
        with closing(self.connection.cursor()) as cursor:
            cursor.execute(query)
            return cursor.fetchone()[0]

    # numberOfWords: integer
    # wordBlacklist: list of strings
    # returns set of words in ASCII encoding
    def getWordSubset(self, numberOfWords, wordBlacklist=set()):
        # this implementation makes me sad, but it works.
        self._checkPermissions("read_permissions")
        if numberOfWords + len(wordBlacklist) > self._getCountOfWordEntries:
            raise IndexException("numberOfWords exceeds potential entries in 'words' table")

        query = """
            SELECT Word
            FROM words
            ORDER BY Random()
            """
        with closing(self.connection.cursor()) as cursor:
            cursor.execute(query)
            allWordsSet = set(cursor.fetchall())
            wordSubSet = set()

            while len(wordSubSet) < numberOfWords:
                word = allWordsSet.pop()
                if word not in wordBlacklist:
                    wordSubSet.add(word)

        assert(len(wordSubSet.intersection(wordBlacklist)) == 0)
        return wordSubSet

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
