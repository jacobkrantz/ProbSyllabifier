from abc import ABCMeta, abstractmethod
from copy import deepcopy

from config import settings as config
from syllabParser import SyllabParser


class AbstractHmmUtils(object):
    """
    Common utilities needed for building matrices with the HMM.
    Abstract Base Class that holds function definitions for all
    ngram related cases.
    """

    __metaclass__ = ABCMeta

    def __init__(self):
        self.syl_parser = SyllabParser()

    def init_matrix(self, rows, columns, data_type="float"):
        """
        Initialize a matrix using numpy with provided size: (X,Y)
        Args:
            rows (int)
            columns (int)
            data_type (string) must be either 'float' or 'int' to be numpy type.
                else it will be exact specified value. Defaults to 'float'.
        Return:
            the zero matrix of proper size and type
        """
        if(data_type == 'int'):
            item = 0
        elif(data_type == 'float'):
            item = 0.0
        elif(data_type == 'int,int'):
            item = (0,0)

        matrix = []
        row = []
        for i in range(0,columns):
            row.append(item)
        for j in range(0,rows):
            matrix.append(deepcopy(row))
        return matrix

    def get_category(self, phone, lang, transcription_scheme=[]):
        """
        Looks up the category that a phone belongs to.
        TODO: refactor both get_category and get_tag_names
        Args:
            phone (character)
            lang (int):  1 if using NIST, else CELEX.
            transcription_scheme (list): if empty, load transcription from file.
        Returns:
            character: unique name of category that the phone belongs to.
        """
        if transcription_scheme:
            for category in transcription_scheme:
                if phone in category:
                    # return an ascii character starting at 'a'
                    return chr(transcription_scheme.index(category) + 97)
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
            in_file = "NistTranscriptionFile"
        else:
            in_file = "CelexTranscriptionFile"

        with open(config["CelexTranscriptionFile"], 'r') as file:
            tags = []
            for line in file:
                tmp_lst = line.split(' ')
                tmp_lst[len(tmp_lst) - 1] = tmp_lst[len(tmp_lst) - 1].strip('\r\n')
                tags.append(tmp_lst)

        return tags

    def build_tag_ngram_dict(self, tag_ngrams):
        """
        Builds a dictionary of [ngram]:[number of occurrances]
        Args:
            tag_ngrams: for bigrams: form is
                [('m0d','d1s'),('d1s','n1l'),('n1l','a0m')]
        Returns:
            dict <tuple:int>: tag_ngram_dict
        """
        tag_ngram_dict = dict()

        for ngram_tup in tag_ngrams:
            if ngram_tup in tag_ngram_dict:
                tag_ngram_dict[ngram_tup] += 1
            else:
                tag_ngram_dict[ngram_tup] = 1

        return tag_ngram_dict

    @abstractmethod
    def get_nist_bigram_tups(self):
        pass

    @abstractmethod
    def parse_celex_training_set(self, training_set):
        pass

    @abstractmethod
    def get_tag_lookup(all_ngram_tups, lang, transcription_scheme=[]):
        pass

    @abstractmethod
    def get_tag_ngrams(self, phone_list):
        pass

    @abstractmethod
    def expand_tags(self, phoneme_lst, lang, transcription_scheme=[]):
        pass

    @abstractmethod
    def get_ngram_lookup(self, all_ngram_tups):
        pass

    @abstractmethod
    def get_ngram_freq_dict(self, all_ngram_tups, num_ngrams):
        pass
