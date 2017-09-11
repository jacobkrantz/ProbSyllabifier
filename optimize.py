from GeneticAlgorithm import GeneticAlgorithm
import json
import sys

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

# loads all GeneticAlgorithm paramters as JSON (a dictionary)
def loadConfiguration():
    with open('config.json') as json_data_file:
        data = json.load(json_data_file)
    return data["GeneticAlgorithm"]

# evolutionNumber represents the evolution log file to continue from
def optimize():
    config = loadConfiguration()
    ga = GeneticAlgorithm(config)
    ga.displayParameters()

    evolutionNumber = 0
    if len(sys.argv) > 1:
        evolutionNumber = int(sys.argv[1])
        ga.importPopulation(evolutionNumber)
        evolutionNumber += 1
    else:
        ga.archiveLogs()
        ga.initializePopulation()

    ga.evolve(evolutionNumber)

optimize()
