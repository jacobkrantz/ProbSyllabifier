
from config import settings as config


class Utils:

    def load_scheme(self, lang):
        """
        Imports a phone transcription scheme
        Args:
            lang (int):  1 if using NIST, else CELEX.
        Returns:
            list<list<char>> transcription_scheme where the inner list is
                a category containing phones
        """
        if lang == 1:
            in_file = "NistTranscriptionFile"
        else:
            in_file = "CelexTranscriptionFile"

        with open(config[in_file], 'r') as file:
            transcription_scheme = []
            for line in file:
                category = line.split(' ')
                category[len(category) - 1] = category[len(category) - 1].strip('\r\n')
                transcription_scheme.append(category)

        return transcription_scheme

    def parse_celex_training_word(self, word, trans_scheme):
        """
        parses a syllabified word into two lists for the HMM.
        Args:
            word (string)
        Returns:
            list<string> observation list
            list<string> state list
        Raises:
            ValueError when the word parameter is not
                a legal syllabification.
        """
        word = list(word.encode('utf-8'))
        word_len = len(word)
        obs = []
        states = []
        previous = self.get_category(word[0], 2, trans_scheme)
        is_boundary = False

        for i in range(1, word_len):
            if(word[i] == '-'):
                is_boundary = True
                continue

            if(is_boundary):
                if(word[i] == '-'):
                    raise ValueError("broke syllabification rule.")
                center = "1"
            else:
                center = "0"

            char = self.get_category(word[i], 2, trans_scheme)
            obs.append(previous + char)
            states.append(previous + center + char)
            previous = char
            is_boundary = False

        return obs, states

    def parse_celex_testing_word(self, word, trans_scheme):
        word = list(word.encode('utf-8'))
        word_len = len(word)
        obs = []
        states = []
        previous = ''

        for i in range(1, word_len):

            previous = word[i-1]
            if(is_boundary):
                if(word[i] == '-'):
                    raise ValueError("broke syllabification rule.")
                center = "1"
            else:
                center = "0"

            char = self.get_category(word[i], 2, trans_scheme)
            obs.append(previous + char)
            states.append(previous + center + char)
            previous = char
            is_boundary = False

        return obs, states

    def get_category(self, phone, lang, transcription_scheme):
        """
        Looks up the category that a phone belongs to.
        Essentially a transformation mapping function.
        Args:
            phone (character)
            lang (int):  1 if using NIST, else CELEX.
            transcription_scheme (list): categories for phones
        Returns:
            character: unique name of category that the phone belongs to. If no
                category exists for the given phone, returns the phone.
        """
        for category in transcription_scheme:
            if phone in category:
                # return an ascii character starting at 'a'
                return chr(transcription_scheme.index(category) + 97)

        return phone

    # ---------------- #
    #     Private      #
    # ---------------- #

    def parse_celex_as_single():
        """
        parses a syllabified word into two lists for the HMM.
        Args:
            word (string)
        Returns:
            list<string> observation list
            list<string> states list
        Raises:
            ValueError when the word parameter is not
                a legal syllabification.
        """
        word = list(word.encode('utf-8'))
        obs = []
        states = []
        previous = ''
        for i, char in enumerate(word):
            if(char == '-'):
                if(previous in ['-', ''] or i == len(word) - 1):
                    raise ValueError("not a legal syllabification: " + word)
                states.append(previous + '1')
            else:
                char = self.get_category(char, 2, trans_scheme)
                obs.append(char)
                if(previous not in ['', '-']):
                    states.append(previous + '0')
            previous = char
        else: # no break:)
            states.append(previous + '0')

        return obs, states
