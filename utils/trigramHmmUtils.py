from syllabParser import SyllabParser
from abstractHmmUtils import AbstractHmmUtils


class TrigramHmmUtils(AbstractHmmUtils):
    """
    Common utilities needed for building matrices based on
    a trigram assumption.
    """

    def get_nist_bigram_tups(self):
        return self.syl_parser.make_nist_phone_list()

    def parse_celex_training_set(self, training_set):
        return self.syl_parser.parse_celex_set_as_trigrams(training_set)

    def get_tag_lookup(self, all_ngram_tups, lang, transcription_scheme=[]):
        """
        Generates a tag dictionary by iterating through each trigram and
        performing category lookups on each phone.
        Args:
            all_ngram_tups: entire parsed training set.
        Returns:
            dict[tag]:[number of occurrences]
            list<string> list holding all unique tags from all_ngram_tups
        """
        tag_dict = dict()
        tag_lookup = set()

        for phone_list in all_ngram_tups:
            for tup in phone_list:
                tag = ""
                for i in range(3):
                    tag += self._get_category(
                        tup[i],
                        lang,
                        transcription_scheme
                    )
                tag += (str(tup[3]) + str(tup[4]))
                tag_lookup.add(tag)
                if tag in tag_dict:
                    tag_dict[tag] += 1
                else:
                    tag_dict[tag] = 1

        return tag_dict, list(tag_lookup)

    def expand_tags(self, all_ngram_tups, lang, transcription_scheme=[]):
        """
        Expand the tags to have categorical knowledge.
        Args:
            all_ngram_tups [[(phone,phone,phone,int,int),(...),],[...],]
            lang (int): 1 for NIST, 2 for CELEX.
            transcription_scheme list<list<string>>
        Returns:
            all_ngram_tups [[(phone,phone,phone,int,tag),(...),],[...],]
                where tag = str(phone,phone,phone,int,int)
        """
        for i, phone_list in enumerate(all_ngram_tups):
            for j, trigram in enumerate(phone_list):
                trigram = list(trigram)
                for tag_index in range(3):
                    trigram[tag_index] = self._get_category(
                        trigram[tag_index],
                        lang,
                        transcription_scheme
                    )
                tag = ""
                for h in range(4):
                    tag += str(trigram[h])
                trigram[4] = (tag + str(trigram[4]))
                all_ngram_tups[i][j] = trigram

        return all_ngram_tups
