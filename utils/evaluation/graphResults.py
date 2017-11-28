import matplotlib.pyplot as plt
import numpy as np

from evaluation import Evaluation


class GraphResults:
    """ Graphical display of results from the `Evaluation` library. """
    def __init__(self):
        self.RE = Evaluation()

    def graph_commonness(self, size):
        """
        Graphs the total amount of each phone or bigram in a bar graph.
        Bigram is currently a mess because of all the options.
        Args:
            size: 1 for phone, 2 for bigram
        Throws:
            IndexError: size not in [1,2]
        """
        percentage_wrong_dict = self.RE.percentage_wrong(1)
        if(size == 1):
            normalize = self.RE.make_normalization_phone_dict()
        elif(size == 2):
            normalize = self.RE.make_normalize_bigrams_dict(0)
            percentage_wrong_dict = self.RE.percentage_wrong(2)
        else:
            raise IndexError("'size' must be 1 or 2.")

        y_axis = []
        labels = []

        for tup in percentage_wrong_dict:
            labels.append(tup[0])
            y_axis.append(normalize[tup[0]])

        y_pos = np.arange(len(y_axis))
        plt.xticks(y_pos, labels)
        plt.bar(y_pos, y_axis, align='center', alpha=0.5)
        plt.show()

    def graph_missed(self, size):
        """
        Creates a double bar graph of the ratio of a phones missed rate
        vs the amount of times it appears.
        Args:
            size (int): 1 for unigram.
        Throws:
            IndexError: size not 1.
        """
        percentage_wrong_dict = self.RE.percentage_wrong(1)
        if(size == 1):
            normalize = self.RE.make_normalization_phone_dict() #overall count of phones
            missed = self.RE.count_all() #count of missed phones
        else:
            raise IndexError("`size` must be 1.")

        y_axis = []
        missed_axis = []
        labels = [] # phones to be displayed
        for tup in percentage_wrong_dict:
            labels.append(tup[0])
            y_axis.append(normalize[tup[0]])
            try:
                missed_axis.append(missed[tup[0]])
            except:
                # all of the phones have not been missed/seen
                missed_axis.append(0)

        y_pos = np.arange(len(y_axis))
        plt.xticks(y_pos,labels)
        plt.bar(y_pos, y_axis, align='center', alpha=0.5)
        plt.bar(y_pos, missed_axis, align='center', alpha=0.5, color='red')
        plt.show()

    def percentage_missed_phones(self, grasp):
        """
        Creates a scatter plot of the percentage missed of each phone,
        normalized by the amount of occurances per phone
        Args:
            Grasp (float): between 0 and 1 to show the amount of
                        outliers of the graph.
        """
        percentage_wrong_dict = self.RE.percentage_wrong(1)
        normalize = self.RE.make_normalization_phone_dict()
        x_axis =[]
        y_axis = []
        labels = []

        for tup in percentage_wrong_dict:
            x_axis.append(tup[1])
            labels.append(tup[0])
            y_axis.append(normalize[tup[0]])

        max_count = max(y_axis)
        fig, ax = plt.subplots()
        ax.scatter(x_axis,y_axis)
        for i in range(len(x_axis)):
            ax.annotate(labels[i],(x_axis[i],y_axis[i]))

        plt.axis([0, grasp, 0, max_count + 30])
        plt.ylabel('Occurance of the phone')
        plt.xlabel('Percentage Wrong')
        plt.show()

    def percentage_missed_bigrams(self, grasp):
        """
        Creates a scatter plot of the percentage missed of each phone,
        normalized by the amount of occurances per bigram
        Args:
            Grasp (float): between 0 and 1 to show the amount of outliers
                    outliers of the graph.
        """
        percentage_wrong_dict = self.RE.percentage_wrong(2)
        normalize = self.RE.make_normalize_bigrams_dict(0)
        x_axis =[]
        y_axis = []
        labels = []

        for tup in percentage_wrong_dict:
            x_axis.append(tup[1])
            labels.append(tup[0])
            y_axis.append(normalize[tup[0]])

        max_count = max(y_axis)
        fig, ax = plt.subplots()
        ax.scatter(x_axis, y_axis)
        for i in range(len(x_axis)):
            ax.annotate(labels[i], (x_axis[i], y_axis[i]))

        plt.axis([0, grasp, 0, max_count + 30])
        plt.ylabel('Occurance of the phone')
        plt.xlabel('Percentage Wrong')
        plt.show()

if __name__ == "__main__":
    G = GraphResults()
    G.percentage_missed_phones(0.3)
    G.percentage_missed_bigrams(0.3)
    G.graph_missed(1)
