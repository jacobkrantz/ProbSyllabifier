import numpy as np

from config import settings as config
from syllabParser import SyllabParser


class HMMUtils:
    """ Common utilities needed for building matrices with a HMM """

    def __init__(self):
        self.syl_parser = SyllabParser()

    # initialize a matrix using numpy with provided size: (X,Y)
    # returns matrix
    def init_matrix(self, x, y):
        return np.zeros((x, y), dtype=np.float)

    # uses SyllabParser to generate a list of lists.
    # allBigramTups: [[(phone,phone,int),(...),],[...],] where int
    # corresponds to the type of boundary.
    def get_nist_bigram_tups(self):
        return self.syl_parser.make_nist_phoneme_lst()

    # uses SyllabParser to generate a list of lists.
    # allBigramTups: [[(phone,phone,int),(...),],[...],] where int
    # corresponds to the type of boundary.
    def parse_celex_training_set(self, training_set):
        return self.syl_parser.parse_celex_training_set(training_set)

    # generates the tag dictionary by iterating though the bigram tuples and
    # looking up what type of consonant or vowel each phone belongs to.
    # returns a dictionary of [tag]: [number of occurrences]
    # also returns a lookup list for matrix indices.
    def get_tag_lookup(self, all_bigram_tups, lang, transciption_scheme=[]):
        category1 = ''
        category2 = ''
        tag_dict = {}
        tag_lookup = set()

        for phoneme in all_bigram_tups:
            for tup in phoneme:
                category1 = self.get_category(
                    tup[0],
                    lang,
                    transciption_scheme
                )
                category2 = self.get_category(
                    tup[1],
                    lang,
                    transciption_scheme
                )
                tag_string = category1 + str(tup[2]) + category2
                tag_lookup.add(tag_string)
                if tag_string in tag_dict:
                    tag_dict[tag_string] += 1
                else:
                    tag_dict[tag_string] = 1

        return tag_dict, list(tag_lookup)

    # returns the category that the phone belongs to.
    # transciptionScheme is for CELEX used in GA
    def get_category(self, phone, lang, transciption_scheme=[]):
        if transciption_scheme:
            for category in transciption_scheme:
                if phone in category:
                    # return an ascii character starting at 'a'
                    return chr(transciption_scheme.index(category) + 97)
            raise LookupError(phone + " not found in tagset.")

        cat = ""
        tag_names = self.get_tag_names(lang)
        if lang == 1:
            phone = phone.upper()

        for category in tag_names:
            if phone in category:
                cat = category[0]
                return cat[0]  # remove trailing unique ID
        raise LookupError(phone + " not found in tagset.")

    # imports the tags from a specific file.
    # returns as a list of lists.
    def get_tag_names(self, lang):
        if lang == 1:
            in_file = open(config["NistTranscriptionFile"], 'r')
        else:
            in_file = open(config["CelexTranscriptionFile"], 'r')

        tags = []
        for line in in_file:
            tmp_lst = line.split(' ')
            tmp_lst[len(tmp_lst) - 1] = tmp_lst[len(tmp_lst) - 1].strip('\r\n')
            tags.append(tmp_lst)

        return tags

    # for input phoneme: [(phone,phone,int),(...),]
    # returns a list of bigram tuples.
    # ex: [('m0d','d1s'),('d1s','n1l'),('n1l','a0m')]
    def get_tag_bigrams(self, phoneme):
        tag_bigrams = []
        for i in range(1, len(phoneme) - 1):
            tupl = (phoneme[i - 1][2], phoneme[i][2])
            tag_bigrams.append(tupl)

        return tag_bigrams

    # param: all tag bigrams, including duplicates.
    # creates a dictionary of [bigram]: [number of occurrences]
    def build_tag_bigram_dict(self, tag_bigrams):
        tag_bigram_dict = {}

        for bigram_tup in tag_bigrams:
            if bigram_tup in tag_bigram_dict:
                tag_bigram_dict[bigram_tup] += 1
            else:
                tag_bigram_dict[bigram_tup] = 1

        return tag_bigram_dict

    # ------------------------------------------------------
    # B Matrix functions below
    # ------------------------------------------------------

    # expands the tagset to have vowel/consonant
    # knowledge in place of boundary 1 or 0.
    # returns the adjusted phoneme list
    def expand_tags(self, phoneme_lst, lang, transciption_scheme=[]):
        spot = ''
        spot1 = ''
        spot2 = ''

        for phoneme in phoneme_lst:
            for tup in phoneme:
                tup[0] = self.get_category(tup[0], lang, transciption_scheme)
                is_boundary = str(tup[2])
                tup[1] = self.get_category(tup[1], lang, transciption_scheme)
                tag_string = tup[0] + is_boundary + tup[1]
                tup[2] = tag_string

        return phoneme_lst

    # allBigramTups: [[(phone,phone,int),(...),],[...],]
    # creates a master lookup list for all unique bigrams trained on.
    # bigrams are inserted into the list as tuples:
    # [(phone,phone),(phone,phone)...]
    def get_bigram_lookup(self, all_bigram_tups):
        bigram_lookup = set()

        for phoneme in all_bigram_tups:
            for bigram in phoneme:
                bigram_lookup.add((bigram[0], bigram[1]))
        return list(bigram_lookup)

    # builds a dictionary containing bigram: P(bigram)
    # used for normalizing MatrixB
    def get_bigram_freq_dict(self, all_bigram_tups, num_bigrams):
        b_freq_dict = {}

        for phoneme in all_bigram_tups:
            for bigram in phoneme:
                new_tup = (bigram[0], bigram[1])
                if new_tup not in b_freq_dict:
                    b_freq_dict[new_tup] = 1
                else:
                    b_freq_dict[new_tup] += 1

        # normalize the b_freq_dict to (countBigram / countAllBigrams)
        return dict(map(lambda (k, v):
                        (k, v / float(num_bigrams)), b_freq_dict.iteritems()))
