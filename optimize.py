from GeneticAlgorithm import GeneticAlgorithm
import json
import sys
from random import randint
from config import GAConfig as config

'''
fileName:       optimize.py
Authors:        Jacob Krantz, Max Dulin
Date Modified:  9/10/17

- Optimizes the phone category transcriptions using a
    genetic algorithm.
- Commandline argument:
    integer representing an evolution number to continue from.
    optional.
    ex. 'python optimize.py 50'
'''

# evolutionNumber represents the evolution log file to continue from
def optimize():
    ga = GeneticAlgorithm()
    ga.display_parameters()

    assert(config["PopulationSize"]/4 == config["NumMatingPairs"])
    evolutionNumber = 0
    if len(sys.argv) > 1:
        evolutionNumber = int(sys.argv[1])
        ga.import_population(evolutionNumber)
        evolutionNumber += 1
    else:
        ga.archive_logs()
        ga.initialize_population()

    ga.evolve(evolutionNumber)

optimize()
