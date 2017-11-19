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
                category1 = self.get_category(
                    tup[0],
                    lang,
                    transcription_scheme
                )
                category2 = self.get_category(
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

    # for input phoneLst: [(phone,phone,int),(...),]
    # returns a list of bigram tuples.
    # ex: [('m0d','d1s'),('d1s','n1l'),('n1l','a0m')]
    def get_tag_ngrams(self, phone_list):
        tag_bigrams = []
        for i in range(1, len(phone_list) - 1):
            tupl = (phone_list[i - 1][2], phone_list[i][2])
            tag_bigrams.append(tupl)

        return tag_bigrams

    # ------------------------------------------------------
    # B Matrix functions below
    # ------------------------------------------------------

    # expands the tagset to have vowel/consonant
    # knowledge in place of boundary 1 or 0.
    # returns the adjusted phoneme list
    def expand_tags(self, phone_list, lang, transcription_scheme=[]):
        spot = ''
        spot1 = ''
        spot2 = ''

        for phoneme in phone_list:
            for tup in phoneme:
                tup[0] = self.get_category(
                    tup[0],
                    lang,
                    transcription_scheme
                )
                is_boundary = str(tup[2])
                tup[1] = self.get_category(
                    tup[1],
                    lang,
                    transcription_scheme
                )
                tag_string = tup[0] + is_boundary + tup[1]
                tup[2] = tag_string

        return phone_list

    # allBigramTups: [[(phone,phone,int),(...),],[...],]
    # creates a master lookup list for all unique bigrams trained on.
    # bigrams are inserted into the list as tuples:
    # [(phone,phone),(phone,phone)...]
    def get_ngram_lookup(self, all_ngram_tups):
        bigram_lookup = set()

        for phoneme in all_ngram_tups:
            for bigram in phoneme:
                bigram_lookup.add((bigram[0], bigram[1]))
        return list(bigram_lookup)

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
