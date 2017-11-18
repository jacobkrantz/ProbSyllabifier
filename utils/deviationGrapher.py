import matplotlib.pyplot as plt

'''
- Standard deviation is calculated from the fitness values
    within a single evolution. Evolutions are not compared to
    one another in calculating the standard deviation.
- The value of 'deviationScope' refers to the top n fitness values that
    will be considered in the standard deviation.
- graphs
'''

def stddev(lst):
    mean = float(sum(lst)) / len(lst)
    return sqrt(float(reduce(lambda x,y: x+y, map(lambda x: (x-mean) **2, lst))) / len(lst))


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

            evolution_std_dev_list.append(
                float("%.1f" % stddev(fitness_lst[:deviation_scope]))
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
