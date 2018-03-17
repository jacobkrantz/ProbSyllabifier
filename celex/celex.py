from __future__ import print_function

import logging as log

from config import settings as config
from datastore import SQLQueryService
from utils import AbstractSyllabRunner
from probSyllabifier import ProbSyllabifier as ps


# transcriptionSchemes passed in will be modified to include
# static entries as specified in Celex.addStaticTags()
class Celex(AbstractSyllabRunner):
    def __init__(self):
        log.getLogger('')
        self.SQLQueryService = SQLQueryService()
        self._c_syl_results_dict = dict()
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
        log.debug("Starting step: Building sets.")
        training_set = self._to_ascii(
            self.SQLQueryService.get_word_subset(training_size)
        )
        testing_set = self._to_ascii(
            self.SQLQueryService.get_word_subset(testing_size, training_set)
        )
        log.debug("Finished step: Building sets.")
        log.debug("Starting step: populate training structures")
        self._populate_training_structures(training_set, testing_set)
        log.debug("Finished step: populate training structures")

    def train_hmm(self, transcription_scheme=[]):
        """
        Trains a ProbSyllabifier model.
        Args:
            transcription_scheme (list<list<phone>>): optional. Defines a
                categorization for all phones. Defaults to file specified
                in `config.json`.
        Returns:
            ps_model (ProbSyllabifier): A fully trained model.
        """
        log.debug("Starting step: Train HMM Model")
        ps_model = ps(transcription_scheme)
        ps_model.train(self._syllabifiedLst)
        log.debug("Finished step: Train HMM Model")
        return ps_model

    def test_hmm(self, ps_model):
        """
        Runs the ProbSyllabifier on all testing examples.
        Thread-safe when DB results is false.
        Args:
            ps_model (ProbSyllabifier): A fully trained model.
        Returns:
            float: percent same formatted to two decimal places.
            list<tuple(p_syl_result, c_syl_result, same): entire test results
        """
        p_syl_results_dict = self._syllabify_testing(ps_model)
        test_results_list = self._combine_results(p_syl_results_dict)

        if config["write_results_to_DB"]:
            self._fill_results_table(test_results_list)

        self._c_syl_results_dict = dict()

        percent_same = self._compare(test_results_list)
        test_results_list = map(
            lambda r: (r["ProbSyl"], r["CSyl"], r["Same"]),
            test_results_list
        )
        return percent_same, test_results_list

    def cross_validate(self):
        """
        Using k-fold cross-validation, determine the predicted
        practical syllabification accuracy of the current system.
        Outputs each run to logs. Outputs final accuracy to logs.
        Returns:
            float: cross validated ProbSyllabifier accuracy
        """
        n_value = config["crossValidation"]["NValue"]
        k_value = config["crossValidation"]["KValue"]
        subset_size = n_value / k_value
        results_list = []

        validation_list = list(self._to_ascii(
            self.SQLQueryService.get_word_subset(n_value)
        ))
        for i in range(k_value):
            lower_bound = i * subset_size
            upper_bound = (i + 1) * subset_size
            testing_set = set(validation_list[lower_bound:upper_bound])
            training_set = set(validation_list) - set(testing_set)
            self._populate_training_structures(training_set, testing_set)
            accuracy, ignore = self.test_hmm(self.train_hmm())
            results_list.append(float(accuracy))

        accuracy = round(sum(results_list) / float(len(results_list)), 2)
        log.info("Cross-validated accuracy: " + str(accuracy) + "%")
        return accuracy

    def get_incorrect_results(self):
        """
        Gets the results set for incorrect syllabifications.
        Returns:
            [{ Word, PSyllab, CSyllab, isSame },{...}] for all
                    incorrect syllabifications (Psyl different than Csyl).
        """
        return self.SQLQueryService.get_incorrect_results()

    def syllabify(self, ps_model, observation):
        """
        Function call for single syllabification.
        Args:
            ps_model (ProbSyllabifier): A fully trained model.
            observation (string): sequence of phones to be syllabified.
        Returns:
            string: observation syllabified where '-'
                    represents syllable breaks.
        """
        return ps_model.syllabify(observation, "CELEX")

    def syllabify_file(self, file_in, file_out):
        """
        Not currently maintained (11/27)
        """
        raise NotImplementedError

    # ---------------- #
    #    "Private"     #
    # ---------------- #

    def _populate_training_structures(self, training_set, testing_set):
        """
        Loads self._c_syl_results_dict with syllabification results
        of the testing set. Loads self._syllabifiedLst with syllabified
        training words. Loads self._pronunciationsDict with prnunciations
        of the testing set.
        Args:
            training_set (set<string>) set for training HMM
            testing_set (set<string>) set reserved for testing HMM
        """
        self._c_syl_results_dict = (
            self.SQLQueryService.get_many_syllabifications(training_set)
        )
        self._syllabifiedLst = self._c_syl_results_dict.values()
        self._c_syl_results_dict = (
            self.SQLQueryService.get_many_syllabifications(testing_set)
        )
        self._pronunciationsDict = (
            self.SQLQueryService.get_many_pronunciations(testing_set)
        )

    def _syllabify_testing(self, ps_model):
        """
        Syllabifies the test set using ProbSyllabifier.
        Args:
            ps_model (ProbSyllabifier): A fully trained model.
        Returns:
            dictionary <test word, syllabification>
        """
        log.debug("Starting step: Syllabify ProbSyllabifier")
        p_syl_results_dict = {}
        for word, pronunciation in self._pronunciationsDict.iteritems():
            p_syl_results_dict[word] = ps_model.syllabify(pronunciation)

        log.debug("Finished step: Syllabify ProbSyllabifier")
        return p_syl_results_dict

    # Queries result lines from the "workingresults" table
    # Returns: [{ Word, PSyllab, CSyllab, isSame },{...}]
    def _combine_results(self, p_results_dict):
        test_results_list = []
        none_count = 0
        for word, p_syllab in p_results_dict.iteritems():
            if not p_syllab:
                p_syllab = ""
                none_count +=1
            else:
                c_syllab = self._c_syl_results_dict[word]

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
            100 * num_same / (total_entries - float(skipped_syllab_count))
        )

        log_message = ("ProbSyllabifier is "+ percent_same
            + "% similar to CELEX." + '\n')
        if(skipped_syllab_count > 0):
            log_message += ('\t' + "Ignoring " + str(skipped_syllab_count) +
                " skips: " + str(ignored_percent_same) + "%" + '\n')

        log.info(log_message)
        return float(percent_same)

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
