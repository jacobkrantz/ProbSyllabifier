import sys
from sqlQueryService import SQLQueryService
import operator
from collections import Counter
class Evaluation:
    """
    In order to optimize the categorization scheme a way to
    understand the data is needed. This class is the framework
    to get why some phones are in the wrong category
    """
    def __init__(self):
        self.word_list = [] #lists of all the wrong words
        self.correct_list = [] #lists of all the correct syllabifactions
        self.wrong_list = [] #lists of the all the incorrectly syllabifactions
        #need to make a function to count all of the phone here, so it's proportional
        self.resultsList = []
        self.SQLQuery = SQLQueryService()
        self._parse_list(self.SQLQuery.get_incorrect_results())
        self.extra_list, self.short_list = self._wrong_bigram()

    def _parse_list(self,results):
        """
        Sets word_list, correct_list and wrong_list to
        the three first pieces of the query
        Args:
            results: the full query from the the working_results table
        """

        for index,entry in enumerate(results):
            self.word_list.append(entry[0])
            self.correct_list.append(entry[1])
            self.wrong_list.append(entry[2])


    def _wrong_bigram(self):

        """
        Sets the extra_list and the short_list to get the evaluation ready
        Returns:
            a list full of the excessive bigrams
        Returns:
            a list full of the inexcessive bigrams
        """

        #need to take out the repeats in here for the percentage to work!
        extra_list = []
        short_list = []
        for index in range(len(self.correct_list)):
            correct_item = self.correct_list[index]
            wrong_item = self.wrong_list[index]
            wroIn = 0 # index of the incorrect item
            corIn = 0 # index of the correct item
            length = min(len(correct_item), len(wrong_item))

            for i in range(length):
                if(length <= corIn or length <= wroIn):
                    break
                if(correct_item[corIn] != wrong_item[wroIn]):

                    #might want to add an inverse idea to this
                    if(correct_item[corIn] == '-'):
                        short_list.append(wrong_item[wroIn-1]+wrong_item[wroIn])
                        corIn+=1
                    elif(wrong_item[wroIn] == '-'):
                        extra_list.append(wrong_item[wroIn-1]+wrong_item[wroIn+1])
                        wroIn+=1
                wroIn+=1
                corIn+=1

        return extra_list,short_list

    def _get_extra(self,index, front_or_back):
        """
        Args:
            index(int): location in the list
            front_or_back(int): the front of the bigram[0] or the back of the bigram[1]
        Returns the front phone of the bigram in the short_list
        """
        return self.extra_list[index][front_or_back]

    def _get_short(self,index,front_or_back):
        """
        Args:
            index(int): location in the list
            front_or_back(int): the front of the bigram[0] or the back of the bigram[1]
        Returns:
            the front phone of the bigram in the short_list
        """
        return self.short_list[index][front_or_back]


    def count_bigrams(self,dict_type,front_back):
        """
        Args:
            dict_type: 0 or 1, use the extra_list(0) or the short_list(1)
            front_back: 0 for the front of the phone, 1 for the back of the phone
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
                count_freq_front[front] +=1
            else:
                count_freq_front[front] = 1
        return count_freq_front

    def print_dict(self,dictionary):
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
        dict1 = self.count_bigrams(0,0)
        dict2 = self.count_bigrams(0,1)
        dict3 = self.count_bigrams(1,0)
        dict4 = self.count_bigrams(1,1)
        count_freq = {}

        for key in dict1:
            if(key in count_freq):
                count_freq[key] +=dict1[key]
            else:
                count_freq[key] = dict1[key]

        for key in dict2:
            if(key in count_freq):
                count_freq[key] +=dict2[key]
            else:
                count_freq[key] = dict2[key]

        for key in dict3:
            if(key in count_freq):
                count_freq[key] +=dict3[key]
            else:
                count_freq[key] = dict3[key]

        for key in dict4:
            if(key in count_freq):
                count_freq[key] +=dict4[key]
            else:
                count_freq[key] = dict4[key]
        return count_freq

    def make_normalization_phone_dict(self):
        """
        Gets a count of the total number of times a phone could have been syllabified
        Returns:
            A dictionary full of the amount of times each phone occured
        """
        normalize = {}
        all_phones = self.SQLQuery.get_all_results()
        for group in all_phones:
            for index,phone in enumerate(group[0]):
                if(index == 0 or index == (len(group[0])-1)):
                    inc = 1
                else:
                    inc = 2

                if(phone in normalize):
                    normalize[phone] += inc
                elif(phone != '-'):
                    normalize[phone] = inc
        #self.print_dict(normalize)
        return normalize

    def common_missed_bigrams(self,order):
        """
        Creates a dictionary to count the amount of bigrams that were missed
        Param:
             order: if order is one, then return an ordered list. Otherwise, return a dict
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

        if(order ==1):
            return sorted(missed_dict.items(),reverse = True,key=operator.itemgetter(1))
        else:
            return missed_dict

    def make_normalize_bigrams_dict(self,order):
        """
        Creates a dictionary that has all of the bigrams
        Param:
            order: 1 for an order list, anything else for the unordered list
        Returns:
            An orded list or a dictionary
        """
        normalize = {}
        all_phones = self.SQLQuery.get_all_results()
        inc = 1
        for group in all_phones:
            word = group[0].replace("-","")
            print word
            for index in range(len(word)-1):
                bigram = word[index]+ word[index+1]
                print bigram
                #need to filter out all of the - in here
                if(bigram in normalize):
                    normalize[bigram] += inc
                else:
                    normalize[bigram] = inc
        if(order==1):
            return sorted(normalize.items(),reverse = True,key=operator.itemgetter(1))
        else:
            return normalize

    def percentage_wrong(self,length):
        """
        Gets the reader an understanding of what phones were missed the most or least often
        Param:
            length: 1 for phone, 2 for bigram, 3 for trigram
        Returns:
            A dictionary full of words with their cooresponding missed rate.
            from the front and back of a bigram

        """
        percentage_dict = {}
        if(length == 1):
            wrong_dict = k.count_all()
            all_dict = self.make_normalization_phone_dict()
        elif(length ==2):
            wrong_dict = self.common_missed_bigrams(0)
            all_dict = self.make_normalize_bigrams_dict(0)
        else:
            return -1
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

if __name__ == "__main__":
    k = Evaluation()
    #t = k.count_bigrams(1,1)
    #k.print_dict(k.count_all())
    #k.print_dict(k.make_normalization_dict())
    #k.print_dict(t)
