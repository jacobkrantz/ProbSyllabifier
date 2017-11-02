import sys
from subprocess import check_output

from nltk.corpus import cmudict

'''
fileName:       syllabInfo.py
Authors:        Jacob Krantz
Date Modified:  3/14/17

- Mass syllabifier using CMU Pronouncing Dictionary and
    NIST Sylabifier for Arpabet
- Mass database from CELEX for IPA
- Program takes in file of words to be syllabified separated
    by spaces. Creates dictionary of word:syllabification.
    This is outputted as a text file with one dictionary
    entry per line.
- Output file: 'HMMFiles/SyllabDict.txt'
'''


class SyllabTools:
    def __init__(self, comparator):
        self.cmu_dict = cmudict.dict()
        self.word_lst = []
        self.arpabet_dict = {}
        self.ipa_dict = {}
        self.out_file = ""
        self.in_file = ""
        self.comparator = comparator

    # needs textfile of words to exist in specified directory
    # imports words from file as list of words.
    # populates self.wordLst with file contents.
    # throws IOError if file not found
    def read_words(self):

        word_file = open(self.in_file, 'r')
        words = ""
        for line in word_file:
            words = words + ' ' + line

        self.word_lst += words.split()

    # looks up each word in cmudict and adds the word and pronunciation
    # to a dictionary. Values are in list format with unicode phonemes.
    # Only takes the first pronunciation for CMU when multiple exist.
    def build_arpabet(self):

        for word in self.word_lst:
            unicode_word = unicode(word)

            try:
                self.arpabet_dict[word] = self.cmu_dict[unicode_word][0]

            except:

                print(unicode_word + " not found in CMUDict")
                sys.exit()

    '''
    NOTE*********************
    This converts words into IPA
    str(check_output(["espeak", "-q","--ipa",'-v','en-us',unicodeWord]))
    Not sure how the celex database is going to want this information
    so I'm going to leave this here until there is time to do more
    work on the database. Could have to translate a set of phones
    into a certain format to get this; we're not sure.
    '''

    # looks up the IPA translation for each word
    # to a dictionary. Values are in list format with unicode phonemes.
    # this will literally parse anything that it is given.
    # What did Celex use for the word to phone converter?
    def build_ipa(self):

        for word in self.word_lst:
            unicode_word = word
            try:
                # self.IPADict[word] = self.CMUDict[unicode_word][0]
                self.ipa_dict[word] = str(check_output([
                    "espeak",
                    "-q",
                    "--ipa",
                    '-v',
                    'en-us',
                    unicode_word
                ]))
                # print(check_output([
                #     "espeak",
                #     "-q",
                #     "--ipa",
                #     '-v',
                #     'en-us',
                #     unicode_word
                # ]).decode('utf8'))
            except:

                print(unicode_word + " not found in IPA")
                sys.exit()

    def __get_syllab_dict(self):
        syllab_dict = {}
        if self.comparator == "NIST":
            for key in self.arpabet_dict:
                syllabif = self.__get_syllabification_cmu(
                    self.arpabet_dict[key]
                )
                syllab_dict[key] = syllabif
        else:
            '''
            for key in self.IPADict:
                print key, self.IPADict[key]
                syllabif = self.__getSyllabificationIPA(self.IPADict[key])
                syllab_dict[key] = syllabif
            '''
            for key in self.word_lst:
                syllabif = self.__get_syllabification_ipa(self.ipa_dict[key])
                syllab_dict[key] = syllabif

                # Will need some sort of parser here to ensure that the
                # syllabifier can handle it

        return syllab_dict

    # this is where the celex phonetic string will come in
    # Function will need to go into the celex database to
    # find the words syllabification
    def __get_syllabification_ipa(self, pronunciation):
        return "IA"

    # For each word that is asked to be syllabified
    # it needs to go through a word to phone translation
    # This is what CMU is used for.
    def __get_syllabification_cmu(self, pronunciation):
        arp_string = ""

        for phoneme in pronunciation:
            a_phoneme = phoneme.encode('ascii', 'ignore')

            if len(a_phoneme) == 2:
                if a_phoneme[1].isdigit():
                    a_phoneme = a_phoneme[:1]

            else:
                if len(a_phoneme) == 3 and a_phoneme[2].isdigit():
                    a_phoneme = a_phoneme[:2]

            arp_string = arp_string + a_phoneme + " "

        # arp_string ready for NIST
        final_syllab = self.NISTClient.syllabify(arp_string)
        return final_syllab

    # dictionary format: word: [[syllab1],[syllab2]...]
    def print_dict_to_file(self, dict_):

        with open(self.out_file, 'w') as out_f:
            for entry in dict_:
                out_f.write(str(entry))
                out_f.write(" ")
                out_f.write(str(dict_[entry][0]))
                out_f.write("\n")
