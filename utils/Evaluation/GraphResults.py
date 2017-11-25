from ResultsEval import Evaluation
import matplotlib.pyplot as plt


class GraphResults:
    def __init__(self):
        self.RE = Evaluation()

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
    G.percentage_missed_bigrams(0.3)


main()
