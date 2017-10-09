import numpy as np
import matplotlib.pyplot as plt

'''
- Standard deviation is calculated from the fitness values
    within a single evolution. Evolutions are not compared to
    one another in calculating the stardard deviation.
- The value of 'deviationScope' refers to the top n fitness values that
    will be considered in the standard deviation.
- graphs
'''

deviationScope = 8
evolutionStdDevList = []

try:
    logNumber = 0
    while True:
        path = "GeneticAlgorithm/EvolutionLogs/Archive/0/"
        fileName = "evo" + str(logNumber) + ".log"
        with open(path + fileName, 'r') as inFile:
            fitnessLst = []
            for count, line in enumerate(inFile, start=1):
                if(count % 2 == 0):
                    fitnessLst.append(float(line.strip('\n')))

            tempFitnessArray = np.array(fitnessLst[:deviationScope])
            evolutionStdDevList.append(float("%.1f" % np.std(tempFitnessArray)))
        logNumber += 1

except IOError:
    pass
finally:
    plt.plot(evolutionStdDevList)
    plt.xlabel('Evolution Number')
    plt.ylabel('Standard Deviation')
    plt.grid()
    plt.show()
