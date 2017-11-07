from __future__ import print_function

import re
import subprocess
import sys
from subprocess import PIPE

from nltk.corpus import cmudict

'''
module for running the NIST Syllabifier
assumes tsylb2 file exists in directory '~/NIST/tsylb2-1.1/'
'''


class NISTClient:
    def __init__(self):
        self.cmu_dict = cmudict.dict()
        self.out_file = ""
        self.in_file = ""

    def syllabify(self, arp_string):
        """
        Uses NIST to find syllabification of a word in arpabet
        ArpString must have no stress

        :param arp_string:
        :return: list of syllabifications
        """
        syllabs = []
        try:
            arp_string = arp_string.lower()
            data = self._run_nist(arp_string)
            syllabs = self._parse_nist_data(data, arp_string)

        except:
            print("Arpabet String Input Error.")

        return syllabs

    def syllabify_file(self, input_file, output_file):
        """
        Given an input file, will syllabify all the words within.
        Outputs as a syllabification dictionary to specified
        output file. Parsing of this file shown in 'utils.py'.

        :param input_file:
        :param output_file:
        :return:
        """
        word_lst = self.read_words(input_file)
        arpabet_dict = self.build_arpabet(word_lst)
        syllab_dict = self._get_syllab_dict(arpabet_dict)
        self.print_dict_to_file(syllab_dict, output_file)

    # ------------------------------
    #            PRIVATE
    # ------------------------------

    def _run_nist(self, arp_string):
        """
        Takes in a phonetic pronunciation and runs them through NIST

        :param arp_string: arpabet string
        :return: proper syllabification(s) in a list
        """
        p = subprocess.Popen(
            "cd ~/NIST/tsylb2-1.1/ && ./tsylb2 -n phon1ax.pcd",
            shell=True,
            stdin=PIPE,
            stdout=PIPE,
            stderr=PIPE,
            bufsize=1
        )
        return p.communicate(input=arp_string + "\n")[0]  # data = output

    def _parse_nist_data(self, data, arp_string):
        """
        Takes in the raw output of NIST, parses for pronunciations and
        returns all in a list

        :param data:
        :param arp_string:
        :return: list of all pronunciations
        """
        pattern = '\/.*?\/'
        pattern2 = '[^0-9]'
        error = 'ERR'
        return_lst = []
        pro_lst = []

        data = str(data)

        if len(re.findall(error, data)):
            print("Error. No syllabification found for: " + arp_string)

        pro_lst = re.findall(pattern, data)
        pro_lst = pro_lst[1:]

        for item in pro_lst:
            tmp = item.strip('/# ')
            tmp = tmp.strip('#')
            new_string = ""
            for i in range(len(tmp)):
                if (tmp[i] != '0' and tmp[i] != '1'
                        and tmp[i] != '2' and tmp[i] != "'"):
                    new_string += tmp[i]
            return_lst.append(new_string)

        return return_lst

    def read_words(self, in_file):
        """
        Needs textfile of words to exist in specified directory,
        imports words from file as list of words.

        :param in_file: textfile of words
        :raises IOError, if file not found
        :return: list of words
        """
        with open(in_file, 'r') as wordFile:
            words = ""
            for line in wordFile:
                words = words + ' ' + line
        return words.split()

    def build_arpabet(self, word_lst):
        """
        Looks up each word in cmudict and adds the word and
        pronunciation to a dictionary. Values are in list format with
        unicode phonemes.
        Only takes the first pronunciation for CMU when multiple exist.

        :param word_lst:
        :return:
        """
        arpabet_dict = {}
        for word in word_lst:
            unicode_word = unicode(word)

            try:
                arpabet_dict[word] = self.cmu_dict[unicode_word][0]
            except:
                print(unicode_word + " not found in CMUDict")
                sys.exit()

        return arpabet_dict

    def _get_syllab_dict(self, arpabet_dict):
        """
        :param arpabet_dict:
        :return:
        """
        syllab_dict = {}
        for key in arpabet_dict:
            syllabif = self._get_syllabification_cmu(arpabet_dict[key])
            syllab_dict[key] = syllabif

        # need parser here to ensure that the syllabifier can handle it
        return syllab_dict

    def _get_syllabification_cmu(self, pronunciation):
        """
        For each word that is asked to be syllabified, it needs to go
        through a word to phone translation. This is what CMU is used
        for.

        :param pronunciation:
        :return:
        """
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

        return self.syllabify(arp_string)

    def print_dict_to_file(self, dict_, out_file):
        """
        dictionary format: word: [[syllab1],[syllab2]...]

        :param dict_:
        :param out_file:
        :return:
        """
        with open(out_file, 'w') as out_f:
            for entry in dict_:
                out_f.write(str(entry))
                out_f.write(" ")
                out_f.write(str(dict_[entry][0]))
                out_f.write("\n")

        print("File successfully syllabified to: " + out_file)
