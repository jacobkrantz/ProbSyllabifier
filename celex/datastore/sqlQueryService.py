from sqliteClient import SQLiteClient
from contextlib import closing

# does not currently support multithreading, even within batch functions.
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
        batchSize = 10
        batchLst = []
        manyPros = []
        for word in wordList:
            batchLst.append(word)
            if len(batchLst) >= batchSize:
                manyPros = dict(manyPros, **self._getBatchPronunciations(batchLst))
                batchLst = []
        return dict(manyPros, **self._getBatchPronunciations(batchLst))

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
        batchSize = 10
        batchLst = []
        manySyls = []
        for word in wordList:
            batchLst.append(word)
            if len(batchLst) >= batchSize:
                manySyls = dict(manySyls, **self._syllabifyBatch(batchLst)) # dict combination
                batchLst = []
        return dict(manySyls, **self._syllabifyBatch(batchLst))

    # returns total number of words in a given table: integer
    def getEntryCount(self, tableName):
        self._checkPermissions("read_permissions")
        query = """
            SELECT COUNT(Word)
            FROM %s
            """ % self._scrubParameter(tableName)
        with closing(self.connection.cursor()) as cursor:
            cursor.execute(query)
            return cursor.fetchone()[0]

    def getIsSameSyllabificationCount(self, ignoreSkipped=False):
        self._checkPermissions("read_permissions")
        whereProbSylNotEmpty = 'AND ProbSyl != ""' if ignoreSkipped else ""
        query = """
            SELECT COUNT(Word)
            FROM workingresults
            WHERE Same = 1
            """
        with closing(self.connection.cursor()) as cursor:
            cursor.execute(query)
            return cursor.fetchone()[0]

    def getSkippedProbSylCount(self):
        self._checkPermissions("read_permissions")
        query = """
            SELECT COUNT(Word)
            FROM workingresults
            WHERE Same = 0
                AND ProbSyl = ""
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
            WHERE Word NOT LIKE '% %'
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

    def _getCountOfWordEntries(self):
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("""
                SELECT COUNT (*)
                FROM words
                WHERE Word NOT LIKE '% %'
                """)
            return cursor.fetchone()[0]

    def _getBatchPronunciations(self, wordList):
        if len(wordList) > 100:
            raise OverflowError("SQLite cannot handle large input size")
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


    def _syllabifyBatch(self, wordList):
        if len(wordList) > 100:
            raise OverflowError("SQLite cannot handle large input size")
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

    def _getAlphabetColumn(self, prefix):
        return prefix + self.config[self._databaseContext]["default_alphabet"]


class IndexException(Exception):
    pass
