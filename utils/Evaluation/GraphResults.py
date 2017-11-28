from ResultsEval import Evaluation
import matplotlib.pyplot as plt
import numpy as np
class GraphResults:
    """
    The physical results of Evaluation being displayed visually in graphs
    """
    def __init__(self):
        self.RE = Evaluation()

    def graph_commonness(self,size):
        """
        Graphs the total amount of each phone or bigram in a bar graph
        Param:
            size: 1 for phone, 2 for bigram
        Warning:
            Bigram is a mess because of all the options
        """
        percentage = self.RE.percentage_wrong(1)
        if(size == 1):
            normalize = self.RE.make_normalization_phone_dict()
            percentage = self.RE.percentage_wrong(1)
        elif(size == 2):
            normalize = self.RE.make_normalize_bigrams_dict(0)
            percentage = self.RE.percentage_wrong(2)

        y_axis = []
        labels = []

        for tup in percentage:
            labels.append(tup[0])
            y_axis.append(normalize[tup[0]])

        y_pos = np.arange(len(y_axis))
        plt.xticks(y_pos,labels)
        plt.bar(y_pos,y_axis,align='center',alpha=0.5)
        plt.show()

    def graph_missed(self,size):
        """
        Creates a double bar graph of the ratio of a phones missed rate
        vs the amount of times it appears
        Param:
            size: 1 for phone
        """

        percentage = self.RE.percentage_wrong(1)
        if(size == 1):
            normalize = self.RE.make_normalization_phone_dict() #overall count of phones
            percentage = self.RE.percentage_wrong(1)
            missed = self.RE.count_all() #count of missed phones

        y_axis = []
        missed_axis = []
        labels = [] #phones to be displayed
        for tup in percentage:
            labels.append(tup[0])
            y_axis.append(normalize[tup[0]])
            #needs the try catch block in the situation
            #that all of the phones have not been missed/seen
            try:
                missed_axis.append(missed[tup[0]])
            except:
                missed_axis.append(0)

        y_pos = np.arange(len(y_axis))
        plt.xticks(y_pos,labels)
        plt.bar(y_pos,y_axis,align='center',alpha=0.5)
        plt.bar(y_pos,missed_axis,align='center',alpha=0.5,color = 'red')
        plt.show()


    def percentage_missed_phones(self,grasp):
        """
        Creates a scatter plot of the percentage missed of each phone,
        normalized by the amount of occurances per phone
        Param:
            Grasp: a number between 0 and 1 to show the amount of outliers
            of the graph
        """

        percentage = self.RE.percentage_wrong(1)
        normalize = self.RE.make_normalization_phone_dict()
        x_axis =[]
        y_axis = []
        labels = []

        for tup in percentage:
            x_axis.append(tup[1])
            labels.append(tup[0])
            y_axis.append(normalize[tup[0]])
        max_count = max(y_axis)
        fig,ax = plt.subplots()
        ax.scatter(x_axis,y_axis)
        for i in range(len(x_axis)):
            ax.annotate(labels[i],(x_axis[i],y_axis[i]))
        plt.axis([0,grasp,0,max_count+30])
        plt.ylabel('Occurance of the phone')
        plt.xlabel('Percentage Wrong')
        #plt.plot([1,2,3,4],[1,4,9,16],'ro')
        plt.show()

    def percentage_missed_bigrams(self,grasp):
        """
        Creates a scatter plot of the percentage missed of each phone,
        normalized by the amount of occurances per bigram
        Param:
            Grasp: a number between 0 and 1 to show the amount of outliers
            of the graph
        """
        percentage = self.RE.percentage_wrong(2)
        normalize = self.RE.make_normalize_bigrams_dict(0)
        x_axis =[]
        y_axis = []
        labels = []

        for tup in percentage:
            x_axis.append(tup[1])
            labels.append(tup[0])
            y_axis.append(normalize[tup[0]])
        max_count = max(y_axis)
        fig,ax = plt.subplots()
        ax.scatter(x_axis,y_axis)
        for i in range(len(x_axis)):
            ax.annotate(labels[i],(x_axis[i],y_axis[i]))
        plt.axis([0,grasp,0,max_count+30])
        plt.ylabel('Occurance of the phone')
        plt.xlabel('Percentage Wrong')
        #plt.plot([1,2,3,4],[1,4,9,16],'ro')
        plt.show()

if __name__ == "__main__":
    G = GraphResults()
    G.percentage_missed_phones(0.3)
    G.percentage_missed_bigrams(0.3)
    G.graph_missed(1)
