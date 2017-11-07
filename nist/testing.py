"""
fileName:       testing.py
Authors:        Jacob Krantz
Date Modified:  3/14/17

Contains classes for testing the performance of Syllabifiers.
- CompareNIST
    * compare
    * viewDifferences
"""
from __future__ import print_function

from utils import SyllabParser


class CompareNIST:
    def __init__(self):
        self.s_parser = SyllabParser()
        self.__dif_lst = []
        self.__n_syllabs = []
        self.__c_syllabs = []

    def compare(self, nist_file, comp_file):
        """
        Compares the syllabifications of compFile to those done by NIST.
        Printed percentage is how accurate compFile is to NISTfile.
        Both compFile and NISTfile must be in specific formats.

        :param nist_file:
        :param comp_file:
        :return:
        """
        self.__n_syllabs = self.__import_file(nist_file)
        self.__c_syllabs = self.__import_file(comp_file)

        percent_sim = self.__run_comparison()
        self.__output_results(percent_sim)

    def view_differences(self):
        """
        Prints the differences between NIST and the compared file

        :return: None
        """
        for i in range(1, len(self.__dif_lst), 2):
            # This should also print the word; but this would require
            # the datatype to change from a list into a dictionary
            # or for two different lists to be present.
            print("Word: ")
            print("NIST: "),
            print(self.__dif_lst[i - 1])
            print("Prob: "),
            print(self.__dif_lst[i])
            print()

        self.__dif_lst = []

    # ------------------------------------------------------
    # Private functions below
    # ------------------------------------------------------

    def __import_file(self, file_name):
        """
        Imports a file that is formatted like 'SyllabDict.txt'.
        Parses file with SyllabParser and returns result (list of lists).

        :param file_name:
        :return:
        """
        return self.s_parser.make_nist_phoneme_lst(file_name)

    def __run_comparison(self):
        """
        Assumes that the ordering of nSyllabs is the same as cSyllabs.
        iterates through both datasets. For each that are the same,
        adds to same count. Also counts total entries.

        :return: float, percent
        """
        end = len(self.__c_syllabs)
        same_count = 0
        n_syl_index = 0
        same = True

        for i in range(end):  # loop lines

            n_syl_index = self.__is_same_phoneme(i, n_syl_index)

            for j in range(len(self.__c_syllabs[i])):  # loop bigrams

                if (self.__n_syllabs[n_syl_index][j][2]
                        != self.__c_syllabs[i][j][2]):
                    same = False

            if same:
                same_count += 1
            else:
                same = True
                self.__dif_lst.append(self.__n_syllabs[n_syl_index])
                self.__dif_lst.append(self.__c_syllabs[i])

            n_syl_index += 1

        return same_count / float(end) * 100

    def __is_same_phoneme(self, i, n_syl_index):
        """
        Checks if both phonemes to be compared are the same. Loops through
        checking each bigram contents. Continues until they are the same.
        returns the adjusted index for nSyllabs.

        :param i:
        :param n_syl_index:
        :return:
        """
        if len(self.__n_syllabs[n_syl_index]) != len(self.__c_syllabs[i]):
            return self.__is_same_phoneme(i, n_syl_index + 1)

        for j in range(len(self.__n_syllabs[n_syl_index])):

            d1 = (self.__n_syllabs[n_syl_index][j][0]
                  != self.__c_syllabs[i][j][0])
            d2 = (self.__n_syllabs[n_syl_index][j][1]
                  != self.__c_syllabs[i][j][1])

            if d1 or d2:
                return self.__is_same_phoneme(i, n_syl_index + 1)

        return n_syl_index  # the same

    def __output_results(self, percent_sim):
        """
        Prints the percentage to the commandline

        :param percent_sim:
        :return:
        """
        print("File is " + str(percent_sim) + "% similar to NIST.")
