
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
        if self._language == 'English':
            query = """
                    SELECT %s
                    FROM pronunciations
                    WHERE Word = ?
                    """ % self._get_alphabet_column("Phon")
        elif self._language == "Dutch":
            query = """
                    SELECT %s
                    FROM CleanDutch
                    WHERE Word = ?
                    """ % self._get_alphabet_column("Phon")
        elif self._language == "Italian":
            query = """
                    SELECT %s
                    FROM Italian
                    WHERE Word = ?
                    """ % self._get_alphabet_column("Phon")
        else:
            raise ValueError('illegal language parameter in config.json.')

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
        batch_size = 100
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
        if self._language == 'English':
            query = """
                    SELECT %s
                    FROM syllabifications
                    WHERE Word = ?
                    """ % self._get_alphabet_column("PhonSyl")
        elif self._language == "Dutch":
            query = """
                    SELECT %s
                    FROM CleanDutch
                    WHERE Word = ?
                    """ % self._get_alphabet_column("PhonSyl")
        elif self._language == "Italian":
            query = """
                    SELECT %s
                    FROM Italian
                    WHERE Word = ?
                    """ % self._get_alphabet_column("PhonSyl")
        else:
            raise ValueError('illegal language parameter in config.json.')

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
        batch_size = 100
        batch_lst = []
        many_syls = []
        for word in word_list:
            batch_lst.append(word)
            if len(batch_lst) >= batch_size:
                many_syls = dict(many_syls, **self._syllabify_batch(batch_lst))
                batch_lst = []
        return dict(many_syls, **self._syllabify_batch(batch_lst))

    def get_entry_count(self, table_name):
        """
        :param table_name: string
        :return: integer, total number of words in a given table
        """
        query = """
                SELECT COUNT(Word)
                FROM %s
                """ % self._scrub_parameter(table_name)

        with closing(self.connection.cursor()) as cursor:
            cursor.execute(query)
            return cursor.fetchone()[0]

    def get_is_same_syllabification_count(self, ignore_skipped=False):
        where_prob_syl_not_empty = 'AND ProbSyl != ""' if ignore_skipped else ""
        query = """
                SELECT COUNT(Word)
                FROM workingresults
                WHERE Same = 1 %s
                """ % where_prob_syl_not_empty

        with closing(self.connection.cursor()) as cursor:
            cursor.execute(query)
            return cursor.fetchone()[0]

    def get_skipped_prob_syl_count(self):
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
        if (number_of_words + len(word_blacklist)
                > self._get_count_of_word_entries()):
            raise ValueError(
                "numberOfWords exceeds potential entries in 'words' table"
            )

        if self._language == 'English':
            query = """
                    SELECT Word
                    FROM pronunciations
                    WHERE Word NOT LIKE '% %'
                    ORDER BY Random()
                    """
        elif self._language == 'Dutch':
            query = """
                    SELECT Word
                    FROM CleanDutch
                    WHERE Word NOT LIKE '% %'
                    ORDER BY Random()
                    """
        elif self._language == 'Italian':
            query = """
                    SELECT Word
                    FROM Italian
                    WHERE Word NOT LIKE '% %'
                    ORDER BY Random()
                    """
        else:
            raise ValueError('illegal language parameter in config.json.')

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
            if self._language == 'English':
                query = """
                        SELECT COUNT (*)
                        FROM pronunciations
                        WHERE Word NOT LIKE '% %'
                        """
            elif self._language == 'Dutch':
                query = """
                        SELECT COUNT (*)
                        FROM CleanDutch
                        WHERE Word NOT LIKE '% %'
                        """
            elif self._language == 'Italian':
                query = """
                        SELECT COUNT (*)
                        FROM Italian
                        WHERE Word NOT LIKE '% %'
                        """
            else:
                raise ValueError('illegal language parameter in config.json.')

            cursor.execute(query)
            return cursor.fetchone()[0]

    def _get_batch_pronunciations(self, word_list):
        if len(word_list) > 100:
            raise OverflowError("SQLite cannot handle large input size")

        places = ','.join(['?'] * len(word_list))
        if self._language == 'English':
            query = """
                    SELECT
                        Word,
                        %s
                    FROM pronunciations
                    WHERE Word IN ({})
                    """ % self._get_alphabet_column("Phon")
        elif self._language == 'Dutch':
            query = """
                    SELECT
                        Word,
                        %s
                    FROM CleanDutch
                    WHERE Word IN ({})
                    """ % self._get_alphabet_column("Phon")
        elif self._language == 'Italian':
            query = """
                    SELECT
                        Word,
                        %s
                    FROM Italian
                    WHERE Word IN ({})
                    """ % self._get_alphabet_column("Phon")
        else:
            raise ValueError('illegal language parameter in config.json.')

        with closing(self.connection.cursor()) as cursor:
            cursor.execute(query.format(places), tuple(word_list))
            pronunciations = dict(cursor.fetchall())
            return {str(key): str(value)
                    for key, value in pronunciations.items()}

    def _syllabify_batch(self, word_list):
        if len(word_list) > 100:
            raise OverflowError("SQLite cannot handle large input size")

        places = ','.join(['?'] * len(word_list))
        if self._language == 'English':
            query = """
                    SELECT
                        Word,
                        %s
                    FROM syllabifications
                    WHERE Word IN ({})
                    """ % self._get_alphabet_column("PhonSyl")
        elif self._language == 'Dutch':
            query = """
                    SELECT
                        Word,
                        %s
                    FROM CleanDutch
                    WHERE Word IN ({})
                    """ % self._get_alphabet_column("PhonSyl")
        elif self._language == 'Italian':
            query = """
                    SELECT
                        Word,
                        %s
                    FROM Italian
                    WHERE Word IN ({})
                    """ % self._get_alphabet_column("PhonSyl")
        else:
            raise ValueError('illegal language parameter in config.json.')

        with closing(self.connection.cursor()) as cursor:
            cursor.execute(query.format(places), tuple(word_list))
            syllabifications = dict(cursor.fetchall())
            return {str(key): str(value)
                    for key, value in syllabifications.items()}

    def _get_alphabet_column(self, prefix):
        return prefix + config[self._database_context]["default_alphabet"]
