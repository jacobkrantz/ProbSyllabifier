from activePool import ActivePool
from celex import Celex
from Chromosome import Chromosome
from config import GAConfig as config
from Mating import Mating
from random import randint
import multiprocessing
import mutate
import os
import shutil

'''
fileName:       GeneticAlgorithm.py
Authors:        Jacob Krantz, Maxwell Dulin
Date Modified:  10/8/17

Library for all Genetic Algorithm functionality.
This should be the only class referenced outside this module
'''

class GeneticAlgorithm:

    def __init__(self):
        # population holds a list of chromosomes
        self.population = []
        self.celex = Celex()
        self.mating = Mating()

    # displays all GeneticAlgorithm parameters to the console
    def displayParameters(self):
        ips  = config["InitialPopulationSize"]
        ps   = config["PopulationSize"]
        nomp = config["NumMatingPairs"]
        mf   = config["BaseMutationFactor"]
        ne   = config["NumEvolutions"]
        noc  = config["NumCategories"]
        nog  = len(config["GeneList"])

        displayString = """
    Genetic Algorithm Parameters
    ----------------------------
    Initial Population Size  %s
    Population Size          %s
    Number of Mating Pairs   %s
    BaseMutationFactor       %s
    Number of Evolutions     %s
    Number of Categories     %s
    Number of Genes          %s
    """ % (ips, ps, nomp, mf, ne, noc, nog)

        print(displayString)

    # initializes the population to hold chromosomes that are
    # generated from random gene-category selections.
    # Computes each chromosomes fitness.
    def initializePopulation(self):
        for i in range(config["InitialPopulationSize"]):
            newChromosome = Chromosome(config["NumCategories"])
            for gene in config["GeneList"]:
                randomCategory = randint(0, config["NumCategories"] - 1)
                newChromosome.insertIntoCategory(randomCategory, gene)

            self.population.append(newChromosome)
        self._computeFitness()
        self._sort()

    # pulls an existing population from an evolution log file.
    def importPopulation(self, resumeFrom):
        location = config["LogFileLocation"]
        fileName = location + "evo" + str(resumeFrom) + ".log"

        with open(fileName, 'r') as inFile:
            for line in inFile:
                if(len(line) < len(config["GeneList"])):
                    self.population[-1].setFitness(float(line))
                    continue

                genes = line.split('\t')
                newChromosome = Chromosome(config["NumCategories"])
                for i in range(len(genes) - 1):
                    for gene in genes[i]:
                        newChromosome.insertIntoCategory(i, gene)
                self.population.append(newChromosome)

        self._displayPopulation(resumeFrom)

    # Move current logs to the archive.
    # Each run is kept under unique folder.
    # Creates directories when necessary.
    def archiveLogs(self):
        source = config["LogFileLocation"]
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
        while evolutionCount < config["NumEvolutions"]:
            self.population = self.mating.crossover(self.population)
            self.population = mutate.mutate(self.population)
            self._computeFitness()
            self._sort()
            self._saveAllChromosomes(evolutionCount)
            self._displayPopulation(evolutionCount)
            evolutionCount += 1

    #----------------#
    #   "Private"    #
    #----------------#

    # compute the fitness of all chromosomes in the population.
    def _computeFitness(self):
        sizes = (config["TrainingSizeHMM"], config["TestingSizeHMM"])
        self.celex.loadSets(sizes[0], sizes[1])

        pool = ActivePool()
        s = multiprocessing.Semaphore(config["MaxThreadCount"])
        resultsQueue = multiprocessing.Queue()
        jobs = [
            multiprocessing.Process(target=self._computeSingleFitness, name=str(i), args=(i, sizes, s, pool, resultsQueue))
            for i in range(len(self.population))
        ]
        for j in jobs:
            j.start()

        for j in jobs:
            j.join()

        for result in [resultsQueue.get() for j in jobs]:
            self.population[result[0]].setFitness(result[1])

    # sets Chromosome.fitness equal to syllabification accuracy.
    # hmmSizes = (trainingSize, testingSize)
    def _computeSingleFitness(self, i, hmmSizes, s, pool, resultsQueue):
        processName = multiprocessing.current_process().name
        with s:
            pool.makeActive(processName)
            genes = self.population[i].getGenes()
            HMMBO = self.celex.trainHMM(genes)
            fitness = self.celex.testHMM(HMMBO)
            HMMBO = None
            resultsQueue.put((i, fitness))
            pool.makeInactive(processName)

    # sort self.population by fitness (syllabification accurracy)
    # ordering: highest (self.population[0]) -> lowest
    def _sort(self):
        self.population.sort()
        self.population.reverse()

    # outputs all chromosomes to a log file cooresponding to a given evolution.
    def _saveAllChromosomes(self, curEvolution):
        location = config["LogFileLocation"]
        name = "evo" + str(curEvolution) + ".log"
        fileName = location + name
        map(lambda x: self._saveChromosomeAtIndex(x, fileName), range(len(self.population)))

    # chromosome 'self.population[index]' saved in "GeneticAlgorithm/EvolutionLogs".
    # truncates the file if inserting from index 0.
    # Each 2-line group is a chromosome.
    # Categories are tab-delimited.
    # Genes have no spaces between them.
    def _saveChromosomeAtIndex(self, index, fileName):
        howToOpen = 'w' if index == 0 else 'a'
        with open(fileName, howToOpen) as outFile:
            for category in self.population[index].getGenes():
                outFile.write(''.join(category) + '\t')
            outFile.write('\n' + str(self.population[index].getFitness()) + '\n')

    def _displayPopulation(self, evolutionNumber = 0):
        print("Population after evolution #" + str(evolutionNumber))
        for i in range(len(self.population)):
            print("chrom" + str(i) + "\t" + str(self.population[i].getFitness()))
        print
