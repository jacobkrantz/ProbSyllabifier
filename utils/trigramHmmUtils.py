from syllabParser import SyllabParser
from abstractHmmUtils import AbstractHmmUtils


class TrigramHmmUtils(AbstractHmmUtils):
    """
    Common utilities needed for building matrices based on
    a trigram assumption.
    """

    def get_nist_bigram_tups(self):
        return self.syl_parser.make_nist_phoneme_lst()

    def parse_celex_training_set(self, training_set):
        return self.syl_parser.parse_celex_set_as_trigrams(training_set)

    def get_tag_lookup(all_ngram_tups, lang, transcription_scheme=[]):
        pass

    def get_tag_ngrams(self, phone_list):
        pass

    def expand_tags(self, phoneme_lst, lang, transcription_scheme=[]):
        pass

    def get_ngram_lookup(self, all_ngram_tups):
        pass

    def get_ngram_freq_dict(self, all_ngram_tups, num_ngrams):
        pass
