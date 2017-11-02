import matplotlib.pyplot as plt
import numpy as np

'''
- Standard deviation is calculated from the fitness values
    within a single evolution. Evolutions are not compared to
    one another in calculating the standard deviation.
- The value of 'deviationScope' refers to the top n fitness values that
    will be considered in the standard deviation.
- graphs
'''

deviation_scope = 8
evolution_std_dev_list = []

try:
    logNumber = 0
    while True:
        path = "../GeneticAlgorithm/EvolutionLogs/"
        file_name = "evo" + str(logNumber) + ".log"
        with open(path + file_name, 'r') as in_file:
            fitness_lst = []
            for count, line in enumerate(in_file, start=1):
                if count % 2 == 0:
                    fitness_lst.append(float(line.strip('\n')))

            temp_fitness_array = np.array(fitness_lst[:deviation_scope])
            evolution_std_dev_list.append(
                float("%.1f" % np.std(temp_fitness_array))
            )
        logNumber += 1

except IOError:
    pass
finally:
    plt.plot(evolution_std_dev_list)
    plt.xlabel('Evolution Number')
    plt.ylabel('Standard Deviation')
    plt.grid()
    plt.show()
