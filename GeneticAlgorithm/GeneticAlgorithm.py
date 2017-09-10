from celex import CELEX
from Chromosome import Chromosome
from Mating import Mate
from random import randint
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

    # displays all GeneticAlgorithm parameters to the console
    def displayParameters(self):
        ips = self.config["InitialPopulationSize"]
        ps  = self.config["PopulationSize"]
        mf  = self.config["MutationFactor"]
        ne  = self.config["NumEvolutions"]
        noc = self.config["NumCategories"]
        nog = len(self.config["GeneList"])

        displayString = """
    Genetic Algorithm Parameters
    ----------------------------
    Initial Population Size  %s
    Population Size          %s
    MutationFactor           %s
    Number of Evolutions     %s
    Number of Categories     %s
    Number of Genes          %s
    """ % (ips, ps, mf, ne, noc, nog)

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

            self.population.append(newChromosome)
        self.computeFitness()

    def evolve(self):
        pass

    #----------------#
    #   "Private"    #
    #----------------#

    # compute the fitness of all chromosomes in the population by
    #   running the ProbSyllabifier.
    # sets Chromosome.fitness equal to syllabification accuracy.
    def computeFitness(self):
        trainSize = self.config["TrainingSizeHMM"]
        testSize = self.config["TestingSizeHMM"]
        for i in range(len(self.population)):
            genes = self.population[i].getGenes()
            self.celex.trainHMM(trainSize, testSize, genes)
            fitness = self.celex.testHMM(genes)
            self.population[i].setFitness(fitness)

    # sort self.population by fitness (syllabification accurracy)
    # ordering: highest (self.population[0]) -> lowest
    def sort(self):
        self.population.sort().reverse()

    # keeps the population from getting stagnant by moving around genes
    # in the chromosome pseudo-randomly
    def mutate(self):
        pass

    # best chromosome should be saves to an aptly named file
    # after each evolution.
    def saveMostFitChromosome(self):
        pass
