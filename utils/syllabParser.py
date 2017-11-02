"""
fileName:       SyllabParser.py
Authors:        Max Dulin, Jacob Krantz
Date Modified:  3/15/17

-Functions:
    makePhonemeLst

- Parses the SyllabDict.txt into a list of tuples.
- Default input file:
    - ./HMMFiles/SyllabDict.txt

"""


class SyllabParser:
    def __init__(self):
        # spot on the line
        self.spot = 0
        # where the lines are stored in the beginning
        self.initial_list = []
        # the list where the list of bigram lists per word is stored
        self.bigram_lst = []
        # the string line from the file inputted
        self.line = ''

    # Creates a list of phonemes. Phonemes consist of bigrams of the
    # form: [['d', 'aa', 0], ['aa', 'l', 1], ['l', 'er', 0]]
    # filename param defaults to ./HMMFiles./SyllabDict.txt
    def make_nist_phoneme_lst(self, file_name="./HMMFiles/SyllabDict.txt"):
        with open(file_name) as f:
            for line in f:
                self.initial_list.append(line)

        for i in range(len(self.initial_list)):
            self.__make_parse_word(i)

        bigs = self.bigram_lst
        self.__init__()
        return bigs

    # Creates a list of phonemes. Phonemes consist of bigrams of the
    # form: [['d', 'aa', 0], ['aa', 'l', 1], ['l', 'er', 0]]
    def parse_celex_training_set(self, training_set):
        training_set = map(lambda x: x.encode('utf-8'), training_set)
        return map(lambda word: self._parse_celex_word(word), training_set)

    # ------------------------------
    #            PRIVATE
    # ------------------------------

    # assumptions: a boundary cannot start or end a word
    #   a boundary cannot follow a boundary
    def _parse_celex_word(self, word):
        word = word.split()[0]
        word = '<' + word + '>'
        phoneme_bigram_list = []
        was_boundary = False
        if word[0] == '-' or word[-1] == '-':
            raise SyntaxError("CELEX word '" + word + "' broke syllab rule.")
        for i in range(1, len(word)):
            if not was_boundary:
                if word[i] == '-':
                    was_boundary = True
                    phoneme_bigram_list.append([word[i - 1], word[i + 1], 1])
                else:
                    phoneme_bigram_list.append([word[i - 1], word[i], 0])
                    was_boundary = False
            else:
                was_boundary = False
                if word[i] == '-':
                    raise SyntaxError(
                        "CELEX word '" + word + "' broke syllab rule."
                    )
        return phoneme_bigram_list

    # Parses a word into bigrams and whether there was a boundary between them.
    # In the format (firstPhone,secondPhone,boundary)
    # if there is a boundary, the value is a 1. If there is no boundary
    # the value is 0.
    def __make_parse_word(self, index):
        # List to hold each bigram in a word
        phone_lst = []
        line = self.initial_list[index]

        # takes out the beginning word in the dictionary
        while line[0] != ' ':
            line = line[1:]
        self.line = line[1:]

        # stores the first phone into old_phone
        old_phone = self.__find_next_phone()
        while self.spot < len(line):
            # get the phone
            phone = self.__find_next_phone()
            # knowing that the word has ended
            value = self.__boundary_found(phone, old_phone)

            # ends the while loop to end the function if true
            if phone == '\0' and self.spot == 0:
                self.bigram_lst.append(phone_lst)
                break
            else:
                phone_lst.append([old_phone, phone, value])
            old_phone = phone

    # takes in a line that has been cropped out
    # returns 1 if a boundary is found between the two phone
    # and 0 otherwise
    def __boundary_found(self, phone, old_phone):
        set_string = ''
        for i in range(2, len(self.line)):
            if self.line[self.spot - i] != old_phone[0]:
                set_string = self.line[self.spot - i] + set_string
            else:
                break
        # checks to see if there is a left bracket inside of it.
        return 1 if '[' in set_string else 0

    # Takes in a line that has been cropped down
    # to find the next phone in the line and the number in the line.
    # returns the next phone in the line
    def __find_next_phone(self):
        phone = ""
        while self.spot < len(self.line):
            if self.line[self.spot].isalpha():
                phone += self.line[self.spot]
                if not self.line[self.spot + 1].isalpha():
                    self.spot += 1
                    return phone

            self.spot += 1

        self.spot = 0
        return '\0'  # end the loop in makeParseWord
