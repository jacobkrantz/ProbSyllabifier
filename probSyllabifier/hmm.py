from config import settings as config
from utils import BigramHmmUtils, TrigramHmmUtils
from HMMBO import HMMBO


class HMM:
    """ Trains a Hidden Markov Model with provided training data. """

    def __init__(self, lang, transcription_scheme, training_set=[]):
        """
        Args:
            lang (int): 1 for NIST, 2 for CELEX.
            transcription_scheme (list of sets of phones): should be
                '[]' if not used.
            training_set (list of strings): optional set of words to
                train from. Must be populated if lang = 2 (CELEX)
        """
        if(config["NGramValue"] == 2):
            self.utils = BigramHmmUtils()
        else:
            self.utils = TrigramHmmUtils()
        self.hmmbo = HMMBO()
        self.hmmbo.transcription_scheme = transcription_scheme
        self.all_ngram_tups = self._load_training_data(training_set)
        self.tag_dict = dict()
        self.b_freq_dict = dict()
        self.bigram_lookup = []
        self.tag_lookup = []
        self.tag_bigrams = []
        self._load_structures(lang, transcription_scheme)

    def train(self):
        """
        Trains all structures needed for the Hidden Markov Model.
        Fills out all attributes of the HMMBO accordingly.
        Returns:
            HMMBO: business object containing training information.
        """
        self.hmmbo.matrix_a = self._build_matrix_a()
        self.hmmbo.matrix_b = self.build_matrix_b()
        self.hmmbo.observation_lookup = self.bigram_lookup
        self.hmmbo.hidden_lookup = self.tag_lookup
        return self.hmmbo

    def get_training_size(self):
        """
        Returns:
            int: number of syllabified words in the training set.
        """
        return len(self.all_ngram_tups)

    # ------------------------------------------------------
    # helper functions below
    # ------------------------------------------------------

    def _build_matrix_a(self):
        """
        Goes through process of creating MatrixA for an HMM.
        MatrixA is the transition probability of going from one
             boundary to another.

        for both x and y, 0 is no boundary.
        for both x and y, 1 is a boundary.
        each entry is normalized by prior tag count.

        Returns:
            numpy matrix: matrix_a transition probabilities
        """
        tag_bigram_dict = self.utils.build_tag_bigram_dict(self.tag_bigrams)
        matrix_a = self.__insert_prob_a(tag_bigram_dict)
        return matrix_a

    def build_matrix_b(self):
        """
        Goes through the process of creating MatrixB for an HMM.
        For y direction, 0 is no boundary and 1 is a boundary.

        Returns:
            numpy matrix: matrix_b hidden state prior probabilities
        """
        matrix_b = self.utils.init_matrix(len(self.bigram_lookup),
                                          len(self.tag_lookup))
        matrix_b = self.__insert_count_b(matrix_b)
        matrix_b = self.normalize_naive_b(matrix_b)
        return matrix_b

    def _load_training_data(self, training_set):
        """
        Args:
            training_set(list of strings): set of words to train from.
            Can be empty.
        Returns:
            List of lists of tuples:
                [[(phone,phone,int),(...),],[...],] where int is 0 for
                no boundary 1 for yes boundary.
        """
        if len(training_set) == 0:  # from nist
            return self.utils.get_nist_bigram_tups()
        return self.utils.parse_celex_training_set(training_set)

    def _load_structures(self, lang, transcription_scheme):
        """ loads necessary data structures for building the HMM """
        self.tag_dict, self.tag_lookup = self.utils.get_tag_lookup(
            self.all_ngram_tups,
            lang,
            transcription_scheme
        )
        self.all_ngram_tups = self.utils.expand_tags(
            self.all_ngram_tups,
            lang,
            transcription_scheme
        )
        self.tag_bigrams = self.utils.get_tag_bigrams(self.all_ngram_tups)
        self.bigram_lookup, self.b_freq_dict = self.utils.get_bigram_lookup_and_freq_dict(self.all_ngram_tups)
        self._structures_did_load()

    def __insert_prob_a(self, tag_bigram_dict):
        """
        Inserts the count of a tag given the previous tag
        populates matrix_a with these values after normalizing the
        probabilities by the occurrence count of the prior tag (tagDict).
        Args:
            tag_bigram_dict (dictionary <(string,string), int>):
                bigram of tags with value being number of occurrences.
        Returns:
            numpy matrix: matrix_a
        """
        matrix_a = self.utils.init_matrix(
            len(self.tag_lookup),
            len(self.tag_lookup)
        )
        for entry in tag_bigram_dict:
            i_tag = entry[0]
            j_tag = entry[1]

            count = tag_bigram_dict[entry]  # Count of tag bigram occurrences
            divisor = self.tag_dict[i_tag]  # Count of the i_tags
            probability = count / float(divisor)  # normalizes the probability
            # use tag_lookup for matrix location
            i_index = self.tag_lookup.index(i_tag)
            j_index = self.tag_lookup.index(j_tag)

            # inserts prob into the matrix
            matrix_a[i_index][j_index] = probability

        return matrix_a

    def __insert_count_b(self, matrix_b):
        """
        Inserts the count of an ngram given a boundary.
        Populates matrix_b with these values.
        Args:
            matrix_b (2D-array)
        Returns:
            2D-array: matrixB
        """
        for phone_list in self.all_ngram_tups:
            for ngram in phone_list:
                tup = ()
                for i in range(config["NGramValue"]):
                    tup += (ngram[i],)
                row = self.bigram_lookup.index(tup)
                # current tag stored in lastspot of tuple
                col = self.tag_lookup.index(ngram[-1])
                matrix_b[row][col] = matrix_b[row][col] + 1
        return matrix_b

    def normalize_naive_b(self, matrix_b):
        """
        Normalization strategy: divide all MatrixB entries by the probability
        of the bigram occurring.
        Args:
            matrix_b (numpy matrix)
        Returns:
            numpy matrix: matrixB
        """
        for i, bigram in enumerate(self.bigram_lookup):
            bigram_prob = self.b_freq_dict[bigram]
            for j in range(len(self.tag_lookup)):  # loop through each tag
                matrix_b[i][j] = matrix_b[i][j] / float(bigram_prob)
        return matrix_b

    def _structures_did_load(self):
        """ Ensures all structures are loaded. Fail fast. """
        assert (len(self.tag_dict) != 0)
        assert (len(self.tag_lookup) != 0)
        assert (len(self.all_ngram_tups) != 0)
        assert (len(self.bigram_lookup) != 0)
        assert (len(self.b_freq_dict) != 0)
        assert (len(self.bigram_lookup) != 0)

        # All items in lookup must be unique
        assert (len(self.bigram_lookup) == len(set(self.bigram_lookup)))
