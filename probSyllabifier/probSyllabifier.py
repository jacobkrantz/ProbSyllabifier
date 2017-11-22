import logging as log

from config import settings as config
from utils import BigramHmmUtils, TrigramHmmUtils


class ProbSyllabifier:
    """
    Syllabifies a given sequence of phones using the Viterbi Algorithm.
    Provides an empty result when a foreign phone bigram is parsed.
    """

    def __init__(self, hmmbo):
        """ Unpack the HMMBO data object. """
        log.getLogger('')
        if(config["NGramValue"] == 2):
            self.utils = BigramHmmUtils()
        else:
            self.utils = TrigramHmmUtils()
        self.matrix_a = hmmbo.matrix_a
        self.matrix_b = hmmbo.matrix_b
        self.obs_lookup = hmmbo.observation_lookup
        self.hidden_lookup = hmmbo.hidden_lookup
        self.tran_scheme = hmmbo.transcription_scheme
        self.comparator = ""

    def syllabify_file(self, file_in, file_out, comparator="CELEX"):
        """
        Currently ignored (11/1/17).
        Needs big rework, but not used.
        """
        # self.comparator = comparator
        # self.s_tools = SyllabTools(self.comparator)
        # self.s_tools.in_file = file_in
        # self.s_tools.out_file = file_out
        # self.s_tools.readWords()
        # self.s_tools.buildArpabet()
        # syllab_dict = self.__syllabify_all()
        # self.__print_dict_to_file(syllab_dict)
        raise NotImplementedError("not in use")

    def syllabify(self, observation, comparator="CELEX"):
        """
        Generates the syllabification of a given word string.
        Args:
            observation (string): sequence of phones
            comparator (string): either "NIST" or default "CELEX"
        Returns:
            string: observation string with '-'
                            representing syllable boundaries.
        """
        self.comparator = comparator
        obs_lst = self.__make_obs_lst(observation)

        if len(obs_lst) < config["NGramValue"]:  # early return small obs
            return observation # assumption: no syllable boundaries

        transcribed_obs = self.__transcribe_phones(obs_lst)
        transcribed_obs = self.__convert_to_ngrams(transcribed_obs)
        obs_lst = self.__convert_to_ngrams(obs_lst)

        is_valid, problem_obs = self.__is_valid_obs(transcribed_obs)

        if not is_valid:
            bad_ngram = ""
            for i in range(config["NGramValue"]):
                bad_ngram += (problem_obs[i] + " ")
            log.debug("(%s) does not exist in training set.", bad_ngram)
            return ""

        matrix_v, matrix_p = self.__build_matrix_v(transcribed_obs)
        output_lst = self.__decode_matrix(matrix_v, matrix_p, transcribed_obs)
        return self.utils.make_final_str(obs_lst, output_lst)

    # ------------------------------------------------------
    # helper functions below
    # ------------------------------------------------------

    def __make_obs_lst(self, observation):
        """
        Converts string observation to a list of characters.
        Args:
            observation (string). Example: 'abc'
        Returns:
            list<char>. Example: ['<','a','b','c','>']
        """
        if self.comparator == "CELEX":
            return list(observation)

        obs_lst = ['<']
        for phone in observation.split(' '):
            if phone[0] in ['"', "'"]:  # remove ' or " at start.
                phone = phone[1:]
            if phone[-1] in ['"', "'"]:  # for removing from end.
                phone = phone[:-1]
            obs_lst.append(phone)
        obs_lst.append('>')
        return obs_lst

    def __transcribe_phones(self, obs_lst):
        """
        Replaces each character of obs_lst with its category.
        Args:
            list<char> list of phones
        Returns:
            list<char> with categories instead of phones
        """
        lang = 1 if(self.comparator == "NIST") else 2
        return list(map(
            lambda x: self.utils._get_category(x, lang, self.tran_scheme),
            obs_lst
        ))

    def __convert_to_ngrams(self, obs_lst):
        """
        Converts an observation list into corresponding n-grams.
        Args:
            obs_lst (list<char>): observation list
        Returns:
            list<(n-tuple)>
        """
        bigram_lst = []
        nValue = config["NGramValue"]
        for i in range((nValue - 1), len(obs_lst)):
            tup = tuple()
            for offset in range(nValue - 1, -1, -1):
                tup += (obs_lst[i - offset],)
            bigram_lst.append(tup)
        return bigram_lst

    def __is_valid_obs(self, obs_lst):
        """
        Checks if all elements of a list are contained in the training set.
        Args:
            obs_lst (list<char>): observation list
        Returns:
            boolean: True if observation is valid
            string: value in obs_lst not in training set.
        """
        try:
            for i in range(len(obs_lst)):
                problem_obs = obs_lst[i]
                self.obs_lookup.index(obs_lst[i])

        except ValueError:
            return False, problem_obs
        return True, ''

    # constructs Viterbi and backpointer matrices.
    # these are used for determining correct hidden state sequence
    #
    # ****note: for the B matrix, the algorithm was constructed to look at
    #       i and j backwards. Our matrixB is correct, but had to be flipped
    #       in reference here to be used "properly".
    def __build_matrix_v(self, obs_lst):
        i_max = len(self.hidden_lookup)
        j_max = len(obs_lst)

        # Viterbi matrix
        matrix_v = self.utils.init_matrix(i_max, j_max)
        # backpointer matrix
        matrix_p = self.utils.init_matrix(i_max, j_max, 'int,int')

        if j_max == 0:  # no bigrams, just one entry
            return matrix_v, matrix_p

        obs_index = self.obs_lookup.index(obs_lst[0])
        for i in range(i_max):  # initialization step
            matrix_v[i][0] = self.matrix_b[obs_index][i]  # flipped

        for j in range(1, j_max):  # iterative step
            obs_ngram = self.obs_lookup.index(obs_lst[j])
            for i in range(i_max):
                max_prob = 0
                i_back = 0
                j_back = 0

                matrix_b_multiplier = self.matrix_b[obs_ngram][i]
                if matrix_b_multiplier == 0.0:
                    continue

                for old_i in range(i_max):
                    cur_prob = (matrix_v[old_i][j - 1]
                                * self.matrix_a[old_i][i]
                                * matrix_b_multiplier)
                    if cur_prob > max_prob:
                        max_prob = cur_prob
                        i_back = old_i
                        j_back = j - 1

                matrix_v[i][j] = self.utils.format_insert(max_prob)
                matrix_p[i][j] = (i_back, j_back)

        return matrix_v, matrix_p

    # traces through the backpointer matrix P and catches
    # the most likely tag sequence as it iterates
    def __decode_matrix(self, matrix_v, matrix_p, obs_lst):
        rev_output = []

        j_max = len(obs_lst)
        max_final = 0
        i_final = 0

        # only grabs final max prob
        for i in range(len(self.hidden_lookup)):
            current_final = matrix_v[i][j_max - 1]
            if current_final > max_final:
                max_final = current_final
                i_final = i

        rev_output.append(self.hidden_lookup[i_final])
        i_cur = matrix_p[i_final][j_max - 1][0]
        j_cur = matrix_p[i_final][j_max - 1][1]

        for j in range(j_max - 2, -1, -1):
            rev_output.append(self.hidden_lookup[i_cur])
            i_cur_old = i_cur
            i_cur = matrix_p[i_cur][j_cur][0]
            j_cur = matrix_p[i_cur_old][j_cur][1]

        return rev_output[::-1]

    # given a list of phonemes, syllabifies all of them.
    # returns a list of syllabifications, with indices corresponding
    # to the inputted phoneme list.
    def __syllabify_all(self):
        syllab_dict = {}

        for key in self.s_tools.ArpabetDict:
            syllabif = self.__get_syllabification(
                self.s_tools.ArpabetDict[key]
            )
            syllab_dict[key] = syllabif

        return syllab_dict

    def __get_syllabification(self, pronunciation):
        arp_string = ""

        for phoneme in pronunciation:
            a_phoneme = phoneme.encode('ascii', 'ignore')

            if len(a_phoneme) == 2:
                if a_phoneme[1].isdigit():
                    a_phoneme = a_phoneme[:1]

            else:
                if len(a_phoneme) == 3:
                    if a_phoneme[2].isdigit():
                        a_phoneme = a_phoneme[:2]

            arp_string = arp_string + a_phoneme + " "

        # arp_string ready for syllabification
        final_syllab = self.syllabify(arp_string.lower().strip(" "))

        return final_syllab

    # prints the contents of a syllabification dictionary to a file.
    # Conforms to format of 'SyllabDict.txt' for future parsing.
    def __print_dict_to_file(self, syllab_dict):
        # print syllab_dict
        out_f = open(self.s_tools.outFile, 'w')

        for entry in syllab_dict:

            try:
                value_string = syllab_dict[entry].split(" ")
                out_f.write(str(entry))
                out_f.write(" ")
                out_f.write("[ ")

                for char in value_string:
                    if char == '|':
                        out_f.write("][")
                    else:
                        out_f.write(char)

                    out_f.write(" ")

                out_f.write("]")
                out_f.write('\n')

            except:
                pass
        out_f.close()
