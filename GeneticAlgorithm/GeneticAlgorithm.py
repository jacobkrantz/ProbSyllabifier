from celex import CELEX
from Chromosome import Chromosome
from Mating import Mating
from random import randint
import copy
'''
fileName:       GeneticAlgorithm.py
Authors:        Jacob Krantz
Date Modified:  9/7/17

Library for all Genetic Algorithm functionality.
This should be the only class referenced outside this module
'''

class GeneticAlgorithm:

    def __init__(self, config):
        # population will hold a list of chromosomes
        self.population = []
        self.config = config
        self.celex = CELEX()
        self.mating = Mating(config)

    # displays all GeneticAlgorithm parameters to the console
    def displayParameters(self):
        ips  = self.config["InitialPopulationSize"]
        ps   = self.config["PopulationSize"]
        nomp = self.config["NumMatingPairs"]
        mf   = self.config["MutationFactor"]
        ne   = self.config["NumEvolutions"]
        noc  = self.config["NumCategories"]
        nog  = len(self.config["GeneList"])

        displayString = """
    Genetic Algorithm Parameters
    ----------------------------
    Initial Population Size  %s
    Population Size          %s
    Number of Mating Pairs   %s
    MutationFactor           %s
    Number of Evolutions     %s
    Number of Categories     %s
    Number of Genes          %s
    """ % (ips, ps, nomp, mf, ne, noc, nog)

        print(displayString)

    # initializes the population to hold chromosomes that are
    # generated from random gene-category selections.
    # Computes each chromosomes fitness.
    def initializePopulation(self):
        for i in range(self.config["InitialPopulationSize"]):
            newChromosome = Chromosome(self.config["NumCategories"])
            for gene in self.config["GeneList"]:
                randomCategory = randint(0, self.config["NumCategories"] - 1)
                newChromosome.insertIntoCategory(randomCategory, gene)
                newChromosome.setFitness(0)
            self.population.append(newChromosome)
        self.__computeFitness()
        self.__sort()

        self.__displayPopulation(0)

    # 1 evolution: mate the population, mutates them, computes their accuracy,
    # sort by accuracy, and save the best to the file.
    # Repeat evolutions as specified in config.json.
    def evolve(self):
        evolutionCount = 0
        while evolutionCount < self.config["NumEvolutions"]:
            self.__displayPopulation(evolutionCount)
            self.population = self.mating.crossover(copy.deepcopy(self.population))
            #self.__mutate()
            self.__displayPopulation(evolutionCount)
            self.__computeFitness()
            self.__sort()
            #self.__saveMostFitChromosome(evolutionCount)
            self.__displayPopulation(evolutionCount)
            evolutionCount += 1

    #----------------#
    #   "Private"    #
    #----------------#

    # compute the fitness of all chromosomes in the population by
    #   running the ProbSyllabifier.
    # sets Chromosome.fitness equal to syllabification accuracy.
    def __computeFitness(self):
        trainSize = self.config["TrainingSizeHMM"]
        testSize = self.config["TestingSizeHMM"]
        for i in range(len(self.population)):
            if(self.population[i].getFitness() == 0):
                genes = self.population[i].getGenes()
                self.celex.trainHMM(trainSize, testSize, genes)
                fitness = self.celex.testHMM(genes)
                self.population[i].setFitness(fitness)

    # sort self.population by fitness (syllabification accurracy)
    # ordering: highest (self.population[0]) -> lowest
    def __sort(self):
        self.population.sort()
        self.population.reverse()

    # keeps the population from getting stagnant by moving around genes
    # in the chromosome pseudo-randomly
    def __mutate(self):
        pass

    # Best chromosome saved in "GeneticAlgorithm/EvolutionLogs".
    # Each line is a category.
    def __saveMostFitChromosome(self, curEvolution):
        bestChromosome = self.population[0]
        location = "GeneticAlgorithm/EvolutionLogs/"
        prefix = "evo" + str(curEvolution) + "-"
        fitness = str(bestChromosome.getFitness())
        fileName = location + prefix + fitness + ".log"

        with open(fileName, 'w') as outFile:
            for category in bestChromosome.getGenes():
                outFile.write(' '.join(category) + '\n')

    def __displayPopulation(self, evolutionNumber):
        print("Population after evolution #" + str(evolutionNumber))
        for i in range(len(self.population)):
            print("chrom" + str(i) + "\t" + str(self.population[i].getFitness()))
        print
