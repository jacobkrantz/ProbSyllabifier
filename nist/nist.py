from __future__ import print_function

from nistClient import NISTClient
from testing import CompareNIST
from utils import AbstractSyllabRunner, FrequentWords as FW


class NIST(AbstractSyllabRunner):

    def __init__(self):
        self.nist_client = NISTClient()
        self.c_nist = CompareNIST()
        self._lang = 1  # 1 == NIST, needed for HMM. outdated.

    def train_hmm(self):
        self._build_sets()
        self._train_hmm()

    def test_hmm(self):
        self.ps = ProbSyllabifier()
        self.ps.loadStructures()
        test_in = "./corpusFiles/testSet.txt"
        test_out = "./HMMFiles/probSyllabs.txt"
        self.ps.syllabify_file(test_in, test_out, "NIST")

        nist_name = "./HMMFiles/NISTtest.txt"
        prob_name = "./HMMFiles/probSyllabs.txt"
        self.c_nist.compare(nist_name, prob_name)

        view_dif = raw_input("view differences (y): ")
        if view_dif == 'y':
            self.c_nist.view_differences()

    # returns string of syllabified observation
    def syllabify(self, observation):
        try:
            return self.ps.syllabify(observation)
        except:
            self.ps = ProbSyllabifier()
            return self.ps.syllabify(observation)

    def syllabify_file(self, file_in, file_out, comparator="NIST"):
        try:
            self.ps.syllabify_file(file_in, file_out, comparator)
        except:
            self.ps = ProbSyllabifier()
            self.ps.syllabify_file(file_in, file_out, comparator)

    # ---------------- #
    #    "Private"     #
    # ---------------- #

    def _build_sets(self):
        in_file = "./corpusFiles/brown_words.txt"  # /editorial_words.txt
        out_file = "./HMMFiles/SyllabDict.txt"
        freq_file = "./corpusFiles/freqWords.txt"

        in_test = "./corpusFiles/testSet.txt"
        out_test = "./HMMFiles/NISTtest.txt"

        print("current input file: " + in_file)
        print("current output file: " + out_file)

        user_in = raw_input("Press enter to continue, or 'c' to change: ")
        if user_in == 'c':
            in_file = raw_input("choose input file: ")
            out_file = raw_input("choose output file: ")

        self._generate_words(in_file, in_test)
        try:
            self.nist_client.syllabify_file(freq_file, out_file)
            self.nist_client.syllabify_file(in_test, out_test)

        except IOError as err:
            print(err)

    # build A and B matrices. Makes files to be used in the Viterbi
    # decoding algorithm.
    def _train_hmm(self):
        hmm = HMM(self._lang)

        hmm._build_matrix_a()  # "./HMMFiles/MatrixA.txt"
        hmm.build_matrix_b()  # "./HMMFiles/MatrixB.txt"
        hmm.makeViterbiFiles()
        print("Items in training set: " + str(hmm.get_training_size()))

    # builds word set files to be used in NIST syllabification
    def _generate_words(self, file_in, test_file_in):
        fw = FW()
        num_words = int(raw_input("Enter number of words to syllabify: "))
        num_test_words = int(raw_input("Enter number of words to test on: "))

        # pulling from entire corpus or editorials
        file_in = "./corpusFiles/brown_words.txt"  # /editorial_words.txt
        fw_out = "./corpusFiles/freqWords.txt"

        fw.generate_most_freq(file_in, fw_out, num_words)
        # testFileIn is outfile
        fw.generate_testing(file_in, test_file_in, num_test_words)
