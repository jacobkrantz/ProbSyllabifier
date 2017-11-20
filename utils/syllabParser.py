class SyllabParser:
    """
    Utility for parsing input strings into ngram lists. Used for creating
        training models within the Hidden Markov Model (`hmm.py`).
    """

    def __init__(self):
        self.spot = 0 # spot on the line
        self.bigram_lst = [] # the list where the list of bigram lists per word is stored
        self.line = '' # the string line from the file inputted

    # Creates a list of phonemes. Phonemes consist of bigrams of the
    # form: [['d', 'aa', 0], ['aa', 'l', 1], ['l', 'er', 0]]
    # filename param defaults to ./HMMFiles./SyllabDict.txt
    def make_nist_phoneme_lst(self, file_name="./HMMFiles/SyllabDict.txt"):
        initial_list = [] # where the lines are stored in the beginning
        with open(file_name) as f:
            for line in f:
                initial_list.append(line)

        for i, line in enumerate(initial_list):
            self.__make_parse_word(i, line)

        return self.bigram_lst

    def parse_celex_set_as_bigrams(self, training_set):
        """
        Args:
            training_set (list<string>)
        Returns:
            list<list<phone>> all training entries broken into bigrams.
        """
        training_set = map(lambda x: x.encode('utf-8'), training_set)
        return map(lambda word: self._parse_celex_word_as_bigram(word), training_set)

    def parse_celex_set_as_trigrams(self, training_set):
        training_set = map(lambda x: x.encode('utf-8'), training_set)
        return map(lambda word: self._parse_celex_word_as_trigram(word), training_set)

    # ------------------------------
    #            PRIVATE
    # ------------------------------

    def _parse_celex_word_as_bigram(self, word):
        """
        Creates a list of phone bigrams.
        Args:
            word (string)
        Returns:
            list<[phone,phone,boundary]>
                example: [['<', 'aa', 0], ['aa', 'l', 1], ['l', '>', 0]]
        """
        word = '<' + word.split()[0] + '>'
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

    def _parse_celex_word_as_trigram(self, word):
        """
        Creates a list of phone trigrams.
        <sQ-pI> becomes:
            [('<', 's', 'Q', 0, 0),
             ('s', 'Q', 'p', 0, 1),
             ('Q', 'p', 'I', 1, 0),
             ('p', 'I', '>', 0, 0)]
        Args:
            word (string): syllabified CELEX DISC
        Returns:
            list of trigrams in 5-tuples
        """
        word = '<' + word.split()[0] + '>'
        phoneme_trigram_list = []
        word_chars = []
        boundaries = []
        for i, character in enumerate(word):
            if(character == '-'):
                boundaries.append(1)
            else:
                word_chars.append(character)
                if(len(word_chars) > len(boundaries)):
                    boundaries.append(0)

        for i in range(2, len(word_chars)):
            trigram = (
                word_chars[i-2],
                word_chars[i-1],
                word_chars[i],
                boundaries[i-1],
                boundaries[i]
            )
            phoneme_trigram_list.append(trigram)

        return phoneme_trigram_list


    # Parses a word into bigrams and whether there was a boundary between them.
    # In the format (firstPhone,secondPhone,boundary)
    # if there is a boundary, the value is a 1. If there is no boundary
    # the value is 0.
    def __make_parse_word(self, index, line):
        # List to hold each bigram in a word
        phone_lst = []

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
