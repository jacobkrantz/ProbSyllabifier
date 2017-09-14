from celex import CELEX
from Chromosome import Chromosome
from Mating import Mating
from random import randint
import shutil
import os
import copy
'''
fileName:       GeneticAlgorithm.py
Authors:        Jacob Krantz, Maxwell Dulin
Date Modified:  9/14/17

Library for all Genetic Algorithm functionality.
This should be the only class referenced outside this module
'''

class GeneticAlgorithm:

    def __init__(self, config):
        # population holds a list of chromosomes
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

            self.population.append(newChromosome)
        self.__computeFitness()
        self.__sort()

    # pulls an existing population from an evolution log file.
    def importPopulation(self, resumeFrom):
        location = self.config["LogFileLocation"]
        fileName = location + "evo" + str(resumeFrom) + ".log"

        with open(fileName, 'r') as inFile:
            for line in inFile:
                if(len(line) < len(self.config["GeneList"])):
                    self.population[-1].setFitness(float(line))
                    continue

                genes = line.split('\t')
                newChromosome = Chromosome(self.config["NumCategories"])
                for i in range(len(genes) - 1):
                    for gene in genes[i]:
                        newChromosome.insertIntoCategory(i, gene)
                self.population.append(newChromosome)

        self.__computeFitness()
        self.__displayPopulation(resumeFrom)

    # Move current logs to the archive.
    # Each run is kept under unique folder.
    # Creates directories when necessary.
    def archiveLogs(self):
        source = self.config["LogFileLocation"]
        destination = source + "Archive/"

        if not os.path.exists(source):
            os.makedirs(source)
        if not os.path.exists(destination):
            os.makedirs(destination)

        if len(os.listdir(source)) > 1:
            specificFolder = destination + str(len(os.listdir(destination))) + '/'
            os.makedirs(specificFolder)
            for f in os.listdir(source):
                if ".log" in f:
                    shutil.move(source + f, specificFolder)

    # 1 evolution: mate the population, mutates them, computes their accuracy,
    # sort by accuracy, and save the best to the file.
    # Repeat evolutions as specified in config.json.
    def evolve(self, evolutionCount = 0):
        while evolutionCount < self.config["NumEvolutions"]:
            self.population = self.mating.crossover(self.population)
            self.__mutate()
            self.__computeFitness()
            self.__sort()
            self.__saveAllChromosomes(evolutionCount)
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
        for i in range(1,len(self.population)):
            chrom = self.population[i]
            #we need to rebuild the chromosome because it's a list of sets
            newChromosome = Chromosome(self.config["NumCategories"])
            curIter = 0
            #per gene mutate
            for category in chrom.getGenes():
                for gene in category:
                    percentage = self.config["MutationFactor"] * 100
                    randNum = randint(0,99)
                    #cooresponds to the mutation factor
                    if(randNum >= 0 and randNum <= percentage):
                        randomCategory = randint(0,self.config["NumCategories"]-1)
                        #makes sure it cannnot be inserted back into the same category
                        while(curIter == randomCategory):
                            randomCategory = randint(0,self.config["NumCategories"]-1)
                        newChromosome.insertIntoCategory(randomCategory,gene)
                    else:
                        newChromosome.insertIntoCategory(curIter,gene)
                curIter = curIter + 1
            self.population[i] = newChromosome

            #per chromosomes mutate
            '''
            if(randNum >= 0 and randNum < self.config["MutationFactor"]):
                chrom.printChrom()
                randChrom = randint(0,53)
                phone = self.config["GeneList"][randChrom]
                randomCategory = randint(0,self.config["NumCategories"]-1)
                chrom.insertIntoCategory(randomCategory,phone)
                chrom.printChrom()
            '''

    # outputs all chromosomes to a log file cooresponding to a given evolution.
    def __saveAllChromosomes(self, curEvolution):
        map(lambda x: self.__saveChromosomeAtIndex(x, curEvolution), range(len(self.population)))

    # chromosome 'self.population[index]' saved in "GeneticAlgorithm/EvolutionLogs".
    # truncates the file if inserting from index 0.
    # Each 2-line group is a chromosome.
    # Categories are tab-delimited.
    # Genes have no spaces between them.
    def __saveChromosomeAtIndex(self, index, curEvolution):
        location = self.config["LogFileLocation"]
        name = "evo" + str(curEvolution) + ".log"
        fileName = location + name

        howToOpen = 'w' if index == 0 else 'a'
        with open(fileName, howToOpen) as outFile:
            for category in self.population[index].getGenes():
                outFile.write(''.join(category) + '\t')
            outFile.write('\n' + str(self.population[index].getFitness()) + '\n')

    def __displayPopulation(self, evolutionNumber = 0):
        print("Population after evolution #" + str(evolutionNumber))
        for i in range(len(self.population)):
            print("chrom" + str(i) + "\t" + str(self.population[i].getFitness()))
        print
