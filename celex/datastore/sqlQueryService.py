from contextlib import closing

from config import settings as config
from sqliteClient import SQLiteClient


class SQLQueryService(SQLiteClient):
    """ Does not support multithreading, even within batch functions """

    def get_single_pronunciation(self, word):
        """
        :param word: string
        :return: string, "" if word is not in the database
        """
        self._check_permissions("read_permissions")

        query = """
            SELECT %s
            FROM pronunciations
            WHERE Word = ?
            """ % self._get_alphabet_column("Phon")

        with closing(self.connection.cursor()) as cursor:
            cursor.execute(query, (word,))
            pronunciation = cursor.fetchone()
            return pronunciation[0] if pronunciation else ""

    def get_many_pronunciations(self, word_list):
        """
        :param word_list: list of strings
        :return: dict of {word: pronunciation}
            if the word does not exist in the database, entry is not
            returned
        """
        self._check_permissions("read_permissions")
        batch_size = 10
        batch_lst = []
        many_pros = []
        for word in word_list:
            batch_lst.append(word)
            if len(batch_lst) >= batch_size:
                many_pros = dict(many_pros,
                                 **self._get_batch_pronunciations(batch_lst))
                batch_lst = []
        return dict(many_pros, **self._get_batch_pronunciations(batch_lst))

    def get_single_syllabification(self, word):
        """
        :param word: string
        :return: string, "" if word is not in the database
        """
        self._check_permissions("read_permissions")

        query = """
            SELECT %s
            FROM syllabifications
            WHERE Word = ?
            """ % self._get_alphabet_column("PhonSyl")

        with closing(self.connection.cursor()) as cursor:
            cursor.execute(query, (word,))
            syllabification = cursor.fetchone()
            return syllabification[0] if syllabification else ""

    def get_many_syllabifications(self, word_list):
        """
        :param word_list: list of strings
        :return: dict of {word: syllabification}
            if the word does not exist in the database, entry is not
            returned
        """
        self._check_permissions("read_permissions")
        batch_size = 10
        batch_lst = []
        many_syls = []
        for word in word_list:
            batch_lst.append(word)
            if len(batch_lst) >= batch_size:
                # dict combination
                many_syls = dict(many_syls, **self._syllabify_batch(batch_lst))
                batch_lst = []
        return dict(many_syls, **self._syllabify_batch(batch_lst))

    def get_entry_count(self, table_name):
        """
        :param table_name: string
        :return: integer, total number of words in a given table
        """
        self._check_permissions("read_permissions")
        query = """
            SELECT COUNT(Word)
            FROM %s
            """ % self._scrub_parameter(table_name)
        with closing(self.connection.cursor()) as cursor:
            cursor.execute(query)
            return cursor.fetchone()[0]

    def get_is_same_syllabification_count(self, ignore_skipped=False):
        self._check_permissions("read_permissions")
        if ignore_skipped:
            where_prob_syl_not_empty = 'AND ProbSyl != ""'
        else:
            where_prob_syl_not_empty = ""
        query = """
            SELECT COUNT(Word)
            FROM workingresults
            WHERE Same = 1
            """
        with closing(self.connection.cursor()) as cursor:
            cursor.execute(query)
            return cursor.fetchone()[0]

    def get_skipped_prob_syl_count(self):
        self._check_permissions("read_permissions")
        query = """
            SELECT COUNT(Word)
            FROM workingresults
            WHERE Same = 0
                AND ProbSyl = ""
            """
        with closing(self.connection.cursor()) as cursor:
            cursor.execute(query)
            return cursor.fetchone()[0]

    def get_incorrect_results(self):
        """
        :return: all columns for an incorrect syllabification.
            selects all rows that are incorrect.
            returns a unicode 4-tuple (word, probSyl, celexSylab, isSame)
        """
        self._check_permissions("read_permissions")
        query = """
            SELECT *
            FROM workingresults
            WHERE Same = 0
            """
        with closing(self.connection.cursor()) as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    def get_word_subset(self, number_of_words, word_blacklist=set()):
        """
        :param number_of_words: integer
        :param word_blacklist: list of strings
        :return: set of words in ASCII encoding
        """
        # this implementation makes me sad, but it works.
        self._check_permissions("read_permissions")
        if (number_of_words + len(word_blacklist)
                > self._get_count_of_word_entries):
            raise IndexException(
                "numberOfWords exceeds potential entries in 'words' table"
            )

        query = """
            SELECT Word
            FROM pronunciations
            WHERE Word NOT LIKE '% %'
            ORDER BY Random()
            """
        with closing(self.connection.cursor()) as cursor:
            cursor.execute(query)
            all_words_set = set(cursor.fetchall())
            word_sub_set = set()

            while len(word_sub_set) < number_of_words:
                word = all_words_set.pop()
                if word not in word_blacklist:
                    word_sub_set.add(word)

        assert (len(word_sub_set.intersection(word_blacklist)) == 0)
        return word_sub_set

    # ---------------- #
    #    "Private"     #
    # ---------------- #

    def _get_count_of_word_entries(self):
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("""
                SELECT COUNT (*)
                FROM pronunciations
                WHERE Word NOT LIKE '% %'
                """)
            return cursor.fetchone()[0]

    def _get_batch_pronunciations(self, word_list):
        if len(word_list) > 100:
            raise OverflowError("SQLite cannot handle large input size")
        words_string = ', '.join(map(str, word_list))
        places = ','.join(['?'] * len(word_list))
        query = """
            SELECT
                Word,
                %s
            FROM pronunciations
            WHERE Word IN ({})
            """ % self._get_alphabet_column("Phon")

        with closing(self.connection.cursor()) as cursor:
            cursor.execute(query.format(places), tuple(word_list))
            pronunciations = dict(cursor.fetchall())
            return {str(key): str(value)
                    for key, value in pronunciations.items()}

    def _syllabify_batch(self, word_list):
        if len(word_list) > 100:
            raise OverflowError("SQLite cannot handle large input size")
        words_string = ', '.join(map(str, word_list))
        places = ','.join(['?'] * len(word_list))
        query = """
            SELECT
                Word,
                %s
            FROM syllabifications
            WHERE Word IN ({})
            """ % self._get_alphabet_column("PhonSyl")

        with closing(self.connection.cursor()) as cursor:
            cursor.execute(query.format(places), tuple(word_list))
            syllabifications = dict(cursor.fetchall())
            return {str(key): str(value)
                    for key, value in syllabifications.items()}

    def _get_alphabet_column(self, prefix):
        return prefix + config[self._databaseContext]["default_alphabet"]


class IndexException(Exception):
    pass
