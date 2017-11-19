import sys
from sqlQueryService import SQLQueryService

class Evaluation:
    def __init__(self):
        self.word_list = [] #lists of all the wrong words
        self.correct_list = [] #lists of all the correct syllabifactions
        self.wrong_list = [] #lists of the all the incorrectly syllabifactions

        self.resultsList = []
        self.SQLQuery = SQLQueryService()
        self.__parse_list__(self.SQLQuery.get_incorrect_results())
        self.extra_list, self.short_list = self.__wrong_bigram__()
        print(self.__get_front_extra__(0))



    def __parse_list__(self,results):
        """
        sets word_list, correct_list and wrong_list to
        the three first pieces of the query
        """

        for index,entry in enumerate(results):
            self.word_list.append(entry[0])
            self.correct_list.append(entry[1])
            self.wrong_list.append(entry[2])

    def __wrong_bigram__(self):

        """
        returns a list full of the excessive bigrams
        returns a list full of the inexcessive bigrams
        """
        extra_list = []
        short_list = []
        for index in range(len(self.correct_list)):
            correct_item = self.correct_list[index]
            wrong_item = self.wrong_list[index]
            wroIn = 0 # index of the incorrect item
            corIn = 0 # index of the correct item
            length = min(len(correct_item), len(wrong_item))

            for index in range(length):
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

    def __get_front_extra__(self,index):
        """
        Args:
            index(int): location in the list
        returns the front phone of the bigram in the extra_list
        """
        return self.extra_list[index][0]

    def __get_back_extra__(self,index):
        """
        Args:
            index(int): location in the list
        returns the back phone of the bigram in the extra_list
        """
        return self.extra_list[index][1]

    def __get_front_short__(self,index):
        """
        Args:
            index(int): location in the list
        returns the front phone of the bigram in the short_list
        """
        return self.short_list[index][0]

    def __get_back_short__(self,index):
        """
        Args:
            index(int): location in the list
        returns the back phone of the bigram in the short_list
        """
        return self.short_list[index][0]

if __name__ == "__main__":
    k = Evaluation()
