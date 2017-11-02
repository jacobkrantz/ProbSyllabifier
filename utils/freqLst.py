from __future__ import print_function

import sys

from nltk.corpus import cmudict

'''
fileName:       run.py
Authors:        Jacob Krantz
Date Modified:  3/11/17

Takes in a file of all tokenized words
Adds word and # of occurrences to a dictionary
outputs top 1000 words and their probability
Note: all top 1000 words must exist in CMU pronouncing dictionary
'''


class FrequentWords:
    def __init__(self):
        self.cmu_dict = cmudict.dict()
        self.__in_file = ""
        self.__out_file = ""
        self.__num_words = 0
        self.__word_lst = []
        self.__freq_lst = []
        self.word_dict = {}

    # inFile example = './corpusFiles/editorial_words.txt'
    # param 1: inFile. file for raw word input
    # param 2: outFile. file to output the most frequent words.
    # param 3: numWords. Number of most frequent words to be outputted.
    def generate_most_freq(self, in_file, out_file, num_words):
        self.__in_file = in_file
        self.__out_file = out_file
        self.__num_words = num_words

        words = self.__get_words()

        self.__create_word_dict(words)
        # this is the ordered way
        # self.__createFreqDict(len(words))

        # unordered way
        # however, because this is in a dictionary this is
        # only partially random. The dictionary has an unordered system
        # that is the same every single time
        self.__create_pass_dict(len(words))

        self.__print_lst(self.__word_lst)

    # would create a dictionary with trully random words in it
    # Param1: a list of all the words in the file
    def create_random_dict(self, words):
        pass

    # builds a file of words to be tested on once the HMM is trained.
    # Uses most frequent words not already in training set.
    # testingOut: file output to hold generated words.
    # numTestWords: number of words to be in said file.
    # **Note: must be run after function 'generateMostFreq'
    def generate_testing(self, testing_in, testing_out, num_test_words):
        self.__in_file = testing_in
        if num_test_words == 0:
            return

        self.__out_file = testing_out
        self.__num_words = num_test_words
        self.__word_lst = []
        self.__freq_lst = []

        # current issue: same file output as generateMostFreq.
        self.__create_freq_dict(len(self.word_dict))
        self.__print_lst(self.__word_lst)

    # displays the most frequent words to the console with their
    # respective frequency counts. Prints total word count.
    def view_most(self):
        for i in range(len(self.__word_lst)):
            sys.stdout.write(str(self.__freq_lst[i]))
            sys.stdout.write(' ')
            sys.stdout.write(self.__word_lst[i])
            sys.stdout.write('\n')

        print('\n' + "Number of words: " + str(len(self.__word_lst)))

    # ------------------------------
    #            PRIVATE
    # ------------------------------

    # imports the words contained in the inFile specified.
    # returns all words in split fashion.
    def __get_words(self):
        word_file = open(self.__in_file, 'r')
        print("Extracting from: " + self.__in_file)
        words = ""

        for line in word_file:
            words = words + ' ' + line

        return words.split()

    # creates a dictionary of word: word count given a list of words.
    # Param1: a List of words
    def __create_word_dict(self, words):

        for word in words:
            if word in self.word_dict:
                self.word_dict[word] = self.word_dict[word] + 1
            else:
                self.word_dict[word] = 1

    # creates a list of words to be syllabifier
    # Param1: the number of words to be chosen
    def __create_freq_dict(self, count):
        if self.__num_words > count:
            print("Source too small. Cannot pull "
                  + self.__num_words + " items.")
            return
        freq_count = 0

        while freq_count < self.__num_words:

            max_word = max(self.word_dict, key=self.word_dict.get)
            unicode_word = unicode(max_word)

            try:

                self.cmu_dict[unicode_word]
                self.__word_lst.append(max_word)
                self.__freq_lst.append(self.word_dict[max_word])
                del self.word_dict[max_word]
                freq_count += 1

            except:
                del self.word_dict[max_word]

    # Grabs random words to put into the dictionary
    # Will be used to train the HMM
    # Param1: the number of words ot be used
    def __create_pass_dict(self, count):
        if self.__num_words > count:
            print("Source too small. Cannot pull "
                  + self.__num_words + " items.")
            return
        freq_count = 0

        for key in self.word_dict:
            if freq_count < self.__num_words:
                word = key  # self.wordDict[key]
                # maxWord = max(self.wordDict, key=self.wordDict.get)
                unicode_word = unicode(word)

                try:

                    self.cmu_dict[unicode_word]
                    self.__word_lst.append(word)
                    self.__freq_lst.append(self.word_dict[word])
                    # del self.wordDict[word]
                    freq_count += 1

                except:
                    pass
                    # del self.wordDict[word]
            else:
                return

    # outputs a list to a file. List entries are
    # separated by spaces
    # Param1: ???
    def __print_lst(self, w):
        txt = open(self.__out_file, 'w')
        for word in w:
            txt.write(word)
            txt.write(' ')


if __name__ == "__main__":
    fw = FrequentWords()
    in_file = './corpusFiles/editorial_words.txt'
    out_file = './corpusFiles/FEWtst.txt'

    fw.generate_most_freq(in_file, out_file, 10)
    fw.view_most()
