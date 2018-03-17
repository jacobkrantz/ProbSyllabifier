
import operator


class Evaluation:
    """
    In order to optimize the categorization scheme a way to
    understand the data is needed. This class is the framework
    to get why some phones are in the wrong category.
    """
    def __init__(self):
        self.correct_list = [] # lists of all the correct syllabifactions
        self.wrong_list = [] # lists of the all the incorrectly syllabifactions
        # need to make a function to count all of the phone here, so it's proportional
        self.resultsList = []
        self.extra_list = []
        self.short_list = []
        self.data = None
        self.all_list = []


    def set_data(self, chrom):
        """
        Puts the data into its rightful places in the algorithm
        Args:
            chrom(Chromosome): a scheme being tested
                which holds the data for the evaluation.
        Returns:
            phone(string): the phone that needs to be optimized.
        """
        self.data = chrom.get_results()
        self.parse_list_gen()
        self.extra_list,self.short_list = self._wrong_bigram()
        return self.get_phone()

    def get_phone(self):
        """
        Calculates which phone needs to be optimized the most in the scheme
        Return:
            phone: the most needs phone to be optimized
        """

        common_dict = self.make_normalization_phone_dict()
        percent = self.percentage_wrong()
        choice_dict = dict()
        for phone in percent:
            choice_dict[phone[0]]= phone[1]/2 * (common_dict[phone[0]])

        return max(choice_dict.iteritems(),key = operator.itemgetter(1))[0]

    def parse_list_gen(self):
        """
        Adds the data to the correct and wrong lists data.
        """

        for value in self.data:
            if(value[2]==0):
                self.correct_list.append(value[0])
                self.wrong_list.append(value[1])
            self.all_list.append(value[1])

    def count_bigrams(self, dict_type, front_back):
        """
        Sets word_list, correct_list and wrong_list to
        the three first pieces of the query
        Args:
            dict_type (int): 0 or 1, use the extra_list(0) or the short_list(1)
            front_back (int): 0 for front of the phone, 1 for back of the phone
        Returns:
            A dictionary full of the counts of incorrectly syllabified phones
        """
        if(dict_type == 0):
            eval_list = self.extra_list
        else:
            eval_list = self.short_list
        count_freq_front = {}
        index = 0

        for index in range(len(eval_list)):
            if(dict_type == 0):
                front = self._get_extra(index,front_back)
            else:
                front = self._get_short(index,front_back)

            if(front in count_freq_front):
                count_freq_front[front] += 1
            else:
                count_freq_front[front] = 1
        return count_freq_front


    def print_dict(self, dictionary):
        """
        Prints the dictionary
        Args:
            dictionary: the dictionary to be printed
        """
        sorted_dict = sorted(dictionary.items(),reverse = True,key = operator.itemgetter(1))
        print "Phone--Count"
        for elt in sorted_dict:
            print elt[0],"----", elt[1]

    def count_all(self):
        """
        Counts up all of the missed phones and syllables.
        Returns:
            A dictionary with the total count of each phone missed
        """
        dict_list = [
            self.count_bigrams(0,0),
            self.count_bigrams(0,1),
            self.count_bigrams(1,0),
            self.count_bigrams(1,1)
        ]
        count_freq = {}

        for dictionary in dict_list:
            for key in dictionary:
                if(key in count_freq):
                    count_freq[key] += dictionary[key]
                else:
                    count_freq[key] = dictionary[key]
        return count_freq

    def make_normalization_phone_dict(self):
        """
        Gets a count of the total number of times a phone could have been syllabified
        Returns:
            A dictionary full of the amount of times each phone occured
        """
        normalize = {}
        all_phones = self.all_list

        for group in all_phones:
            for index,phone in enumerate(group):
                if(index == 0 or index == (len(group[0])-1)):
                    inc = 1
                else:
                    inc = 2

                if(phone in normalize):
                    normalize[phone] += inc
                elif(phone != '-'):
                    normalize[phone] = inc
        return normalize

    def common_missed_bigrams(self, order):
        """
        Creates a dictionary to count the amount of bigrams that were missed
        Args:
             order (int): if order is one, then return an ordered list.
                        Otherwise, return a dict.
        Returns:
            A DESC list or a dictionary
        """
        missed_dict = dict()
        for bigram in self.short_list:
            if(bigram in missed_dict):
                missed_dict[bigram] +=1
            else:
                missed_dict[bigram] = 1

        for bigram in self.extra_list:
            if(bigram in missed_dict):
                missed_dict[bigram] +=1
            else:
                missed_dict[bigram] = 1

        if(order == 1):
            return sorted(missed_dict.items(), reverse=True, key=operator.itemgetter(1))
        else:
            return missed_dict

    def percentage_wrong(self):
        """
        Gets the reader an understanding of what phones were missed the most or least often
        Param:
            length (int): 1 for unigram, 2 for bigram, 3 for trigram
        Returns:
            A list full of words with their cooresponding missed rate.
            from the front and back of a bigram.
        """
        percentage_dict = {}
        wrong_dict = self.count_all()
        all_dict = self.make_normalization_phone_dict()
        #if the key is not in the all_dict, then it's being ignored here.
        for key in all_dict:

            if(key in wrong_dict):
                percentage_dict[key] = float(wrong_dict[key]/float(all_dict[key]))
            else:
                percentage_dict[key] = 0

        lst = sorted(percentage_dict.items(),reverse = True,key=operator.itemgetter(1))
        return lst

    def get_short_bigram_missed(self):
        return self.short_list

    def get_extra_bigram_missed(self):
        return self.extra_list

    # ---------------- #
    #    "Private"     #
    # ---------------- #

    def _wrong_bigram(self):
        """
        Sets the extra_list and the short_list to get the evaluation ready
        Returns:
            a list full of the excessive bigrams
        Returns:
            a list full of the inexcessive bigrams
        """
        # need to take out the repeats in here for the percentage to work
        extra_list = []
        short_list = []
        for index in range(len(self.correct_list)):
            correct_item = self.correct_list[index]
            wrong_item = self.wrong_list[index]
            incorrect_in = 0 # index of the incorrect item
            correct_in = 0 # index of the correct item
            length = min(len(correct_item), len(wrong_item))

            for i in range(length):
                if(length <= correct_in or length <= incorrect_in):
                    break
                if(correct_item[correct_in] != wrong_item[incorrect_in]):

                    #might want to add an inverse idea to this
                    if(correct_item[correct_in] == '-'):
                        short_list.append(
                            wrong_item[incorrect_in-1] + wrong_item[incorrect_in]
                        )
                        correct_in += 1
                    elif(wrong_item[incorrect_in] == '-'):
                        extra_list.append(
                            wrong_item[incorrect_in - 1] + wrong_item[incorrect_in + 1]
                        )
                        incorrect_in += 1
                incorrect_in += 1
                correct_in += 1
        return extra_list,short_list

    def _get_extra(self, index, front_or_back):
        """
        Args:
            index(int): location in the list
            front_or_back(int): the front of the bigram[0] or the back of the bigram[1]
        Returns:
            The front phone of the bigram in the short_list
        """
        return self.extra_list[index][front_or_back]

    def _get_short(self, index, front_or_back):
        """
        Args:
            index(int): location in the list
            front_or_back(int): the front of the bigram[0] or the back of the bigram[1]
        Returns:
            The front phone of the bigram in the short_list
        """
        return self.short_list[index][front_or_back]
