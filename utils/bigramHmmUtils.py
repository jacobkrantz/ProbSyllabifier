from abstractHmmUtils import AbstractHmmUtils


class BigramHmmUtils(AbstractHmmUtils):
    """
    Common utilities needed for building matrices based on
    a bigram assumption.
    """

    # uses SyllabParser to generate a list of lists.
    # allBigramTups: [[(phone,phone,int),(...),],[...],] where int
    # corresponds to the type of boundary.
    def get_nist_bigram_tups(self):
        return self.syl_parser.make_nist_phoneme_lst()

    # uses SyllabParser to generate a list of lists.
    # allBigramTups: [[(phone,phone,int),(...),],[...],] where int
    # corresponds to the type of boundary.
    def parse_celex_training_set(self, training_set):
        return self.syl_parser.parse_celex_set_as_bigrams(training_set)

    # generates the tag dictionary by iterating though the bigram tuples and
    # looking up what type of consonant or vowel each phone belongs to.
    # returns a dictionary of [tag]: [number of occurrences]
    # also returns a lookup list for matrix indices.
    def get_tag_lookup(self, all_ngram_tups, lang, transcription_scheme=[]):
        category1 = ''
        category2 = ''
        tag_dict = {}
        tag_lookup = set()

        for phoneme in all_ngram_tups:
            for tup in phoneme:
                category1 = self._get_category(
                    tup[0],
                    lang,
                    transcription_scheme
                )
                category2 = self._get_category(
                    tup[1],
                    lang,
                    transcription_scheme
                )
                tag_string = category1 + str(tup[2]) + category2
                tag_lookup.add(tag_string)
                if tag_string in tag_dict:
                    tag_dict[tag_string] += 1
                else:
                    tag_dict[tag_string] = 1

        return tag_dict, list(tag_lookup)

    # ------------------------------------------------------
    # B Matrix functions below
    # ------------------------------------------------------

    # expands the tagset to have vowel/consonant
    # knowledge in place of boundary 1 or 0.
    # returns the adjusted phoneme list
    def expand_tags(self, all_ngram_tups, lang, transcription_scheme=[]):
        spot = ''
        spot1 = ''
        spot2 = ''

        for phone_list in all_ngram_tups:
            for tup in phone_list:
                tup[0] = self._get_category(
                    tup[0],
                    lang,
                    transcription_scheme
                )
                is_boundary = str(tup[2])
                tup[1] = self._get_category(
                    tup[1],
                    lang,
                    transcription_scheme
                )
                tag_string = tup[0] + is_boundary + tup[1]
                tup[2] = tag_string

        return all_ngram_tups

    # builds a dictionary containing bigram: P(bigram)
    # used for normalizing MatrixB
    def get_ngram_freq_dict(self, all_ngram_tups, num_ngrams):
        b_freq_dict = {}

        for phoneme in all_ngram_tups:
            for bigram in phoneme:
                new_tup = (bigram[0], bigram[1])
                if new_tup not in b_freq_dict:
                    b_freq_dict[new_tup] = 1
                else:
                    b_freq_dict[new_tup] += 1

        # normalize the b_freq_dict to (countBigram / countAllBigrams)
        return dict(map(lambda (k, v):
                        (k, v / float(num_ngrams)), b_freq_dict.iteritems()))

    def make_final_str(self, obs_lst, output_lst, comparator="CELEX"):
        """
        Synthesize the resulting syllabification.
        Args:
            obs_lst (list<ngram observation>)
            output_lst (list<tag>) result from Viterbi backtrace
        Returns:
            string of syllabified initial input.
        """
        final_str = ""
        for i in range(len(obs_lst)):
            is_truncated = (i == len(obs_lst) - 1)
            final_str += obs_lst[i][0]
            if output_lst[i][1] == '0' or is_truncated:
                if comparator == "NIST":
                    final_str += " "
            else:
                if comparator == "NIST":
                    final_str += " | "
                else:
                    final_str += "-"

        return final_str + obs_lst[len(obs_lst) - 1][1]
