from GeneticAlgorithm import GeneticAlgorithm
import json

'''
fileName:       optimize.py
Authors:        Jacob Krantz, Max Dulin
Date Modified:  9/7/17

- Optimizes the phone category transcriptions using a
    genetic algorithm.
'''

# loads all GeneticAlgorithm paramters as JSON (a dictionary)
def loadConfiguration():
    with open('config.json') as json_data_file:
        data = json.load(json_data_file)
    return data["GeneticAlgorithm"]


def optimize():
    config = loadConfiguration()
    ga = GeneticAlgorithm(config)

    ga.displayParameters()
    ga.initializePopulation()
    ga.evolve()

optimize()
