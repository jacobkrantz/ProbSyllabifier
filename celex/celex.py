from __future__ import print_function

import logging as log

from config import settings as config
from datastore import SQLQueryService
from probSyllabifier import ProbSyllabifier, HMM
from utils import AbstractSyllabRunner


# transcriptionSchemes passed in will be modified to include
# static entries as specified in Celex.addStaticTags()
class Celex(AbstractSyllabRunner):
    def __init__(self):
        log.basicConfig(
            format='%(asctime)s %(levelname)s:%(message)s',
            datefmt='%X',
            level=log.INFO
        )
        self.SQLQueryService = SQLQueryService()
        self.__c_syl_results_dict = dict()
        self._pronunciationsDict = dict()
        self._syllabifiedLst = []

    # Prompts user for training and testing sizes.
    # Loads sets, trains the HMM, and syllabifies Celex.
    def input_train_hmm(self):
        training_size = int(input("enter number of words to train on: "))
        testing_size = int(input("enter number of words to test on: "))
        self.load_sets(training_size, testing_size)
        return self.train_hmm()

    # Populates testing and training sets.
    # Computes CELEX syllabification results.
    def load_sets(self, training_size, testing_size):
        log.info("Starting step: Building sets.")
        training_set = self._to_ascii(
            self.SQLQueryService.get_word_subset(training_size)
        )
        testing_set = self._to_ascii(
            self.SQLQueryService.get_word_subset(testing_size, training_set)
        )
        self.__c_syl_results_dict = (
            self.SQLQueryService.get_many_syllabifications(training_set)
        )
        self._syllabifiedLst = self.__c_syl_results_dict.values()
        log.info("Finished step: Building sets.")
        log.info("Starting step: Syllabify CELEX")
        self.__c_syl_results_dict = (
            self.SQLQueryService.get_many_syllabifications(testing_set)
        )
        self._pronunciationsDict = (
            self.SQLQueryService.get_many_pronunciations(testing_set)
        )
        log.info("Finished step: Syllabify CELEX")

    def train_hmm(self, transcription_scheme=[]):
        log.info("Starting step: Train HMM Model")
        self.hmm = HMM(
            2,  # lang hack: 2 is celex
            self.add_static_tags(transcription_scheme),
            self._syllabifiedLst
        )
        hmmbo = self.hmm.train()
        log.info("Finished step: Train HMM Model")
        return hmmbo

    # thread-safe when DB results is false.
    def test_hmm(self, hmmbo):
        p_syl_results_dict = self._syllabify_testing(hmmbo)
        test_results_list = self._combine_results(p_syl_results_dict)

        if config["write_results_to_DB"]:
            self._fill_results_table(test_results_list)

        self.__c_syl_results_dict = dict()
        self.__p_syl_results_dict = dict()
        return self._compare(test_results_list)

    # Where Psyl is different than Csyl,
    # Returns: [{ Word, PSyllab, CSyllab, isSame },{...}]
    def get_incorrect_results(self):
        return self.SQLQueryService.get_incorrect_results()

    # returns string of syllabified observation
    def syllabify(self, observation):
        return self.ps.syllabify(observation, "CELEX")

    def syllabify_file(self, file_in, file_out):
        self.ps.syllabify_file(file_in, file_out, "CELEX")

    # ---------------- #
    #    "Private"     #
    # ---------------- #

    # builds dictionary of {testWord:syllabification}
    # for pSylResultsDict
    def _syllabify_testing(self, hmmbo):
        log.info("Starting step: Syllabify ProbSyllabifier")
        self.ps = ProbSyllabifier(hmmbo)
        p_syl_results_dict = {}
        for word, pronunciation in self._pronunciationsDict.iteritems():
            p_syl_results_dict[word] = self.ps.syllabify(
                pronunciation,
                "CELEX"
            )
        log.info("Finished step: Syllabify ProbSyllabifier")
        return p_syl_results_dict

    # Queries result lines from the "workingresults" table
    # Returns: [{ Word, PSyllab, CSyllab, isSame },{...}]
    def _combine_results(self, p_results_dict):
        test_results_list = []
        for word, p_syllab in p_results_dict.iteritems():
            if not p_syllab:
                p_syllab = ""
            c_syllab = self.__c_syl_results_dict[word]
            is_same = int(c_syllab == p_syllab)
            test_results_line = {
                "Word": word,
                "ProbSyl": p_syllab,
                "CSyl": c_syllab,
                "Same": is_same
            }
            test_results_list.append(test_results_line)
        return test_results_list

    # given: [{ Word, PSyllab, CSyllab, isSame },{...}]
    # publishes results to "workingresults" table
    def _fill_results_table(self, test_results_list):
        self.SQLQueryService.truncate_table("workingresults")
        for result_line in test_results_list:
            self.SQLQueryService.insert_into_table(
                "workingresults",
                result_line
            )

    def _compare(self, test_results_list):
        total_entries = float(len(test_results_list))
        skipped_syllab_count = 0
        num_same = 0
        for entry in test_results_list:
            if entry["Same"] == 1:
                num_same += 1
            elif entry["ProbSyl"] == "":
                skipped_syllab_count += 1
        percent_same = "{0:.2f}".format(100 * num_same / total_entries)
        ignored_percent_same = "{0:.2f}".format(
            100 * num_same / total_entries - float(skipped_syllab_count)
        )
        print("\n----------------------------------------")
        print("ProbSyllabifier is " + percent_same + "% similar to CELEX.")
        print("Ignoring", skipped_syllab_count,
              "skips:", ignored_percent_same, "%")
        print("----------------------------------------")
        return percent_same

    # add all static tags to the incoming transcriptionScheme.
    # current use: include start and end tags for a word ('<', '>')
    #   as its own category.
    def add_static_tags(self, transcription_scheme):
        start_and_end = ['<', '>']
        if (start_and_end not in transcription_scheme
                and len(transcription_scheme) > 0):
            transcription_scheme.append(start_and_end)
        return transcription_scheme

    def _to_ascii(self, word_lst):
        return map(lambda x: x[0].encode('utf-8'), word_lst)
