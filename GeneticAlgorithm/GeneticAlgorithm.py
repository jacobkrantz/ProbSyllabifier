from __future__ import print_function

import multiprocessing
import os
import shutil
from random import randint

import mutate
from Chromosome import Chromosome
from Mating import Mating
from activePool import ActivePool
from celex import Celex
from config import GAConfig as config

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
    def display_parameters(self):
        ips = config["InitialPopulationSize"]
        ps = config["PopulationSize"]
        nomp = config["NumMatingPairs"]
        mf = config["BaseMutationFactor"]
        ne = config["NumEvolutions"]
        noc = config["NumCategories"]
        nog = len(config["GeneList"])

        display_string = """
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

        print(display_string)

    # initializes the population to hold chromosomes that are
    # generated from random gene-category selections.
    # Computes each chromosomes fitness.
    def initialize_population(self):
        for i in range(config["InitialPopulationSize"]):
            new_chromosome = Chromosome(config["NumCategories"])
            for gene in config["GeneList"]:
                random_category = randint(0, config["NumCategories"] - 1)
                new_chromosome.insert_into_category(random_category, gene)

            self.population.append(new_chromosome)
        self._compute_fitness()
        self._sort()

    # pulls an existing population from an evolution log file.
    def import_population(self, resume_from):
        location = config["LogFileLocation"]
        file_name = location + "evo" + str(resume_from) + ".log"

        with open(file_name, 'r') as in_file:
            for line in in_file:
                if len(line) < len(config["GeneList"]):
                    self.population[-1].set_fitness(float(line))
                    continue

                genes = line.split('\t')
                new_chromosome = Chromosome(config["NumCategories"])
                for i in range(len(genes) - 1):
                    for gene in genes[i]:
                        new_chromosome.insert_into_category(i, gene)
                self.population.append(new_chromosome)

        self._display_population(resume_from)

    # Move current logs to the archive.
    # Each run is kept under unique folder.
    # Creates directories when necessary.
    def archive_logs(self):
        source = config["LogFileLocation"]
        destination = source + "Archive/"

        if not os.path.exists(source):
            os.makedirs(source)
        if not os.path.exists(destination):
            os.makedirs(destination)

        if len(os.listdir(source)) > 1:
            specific_folder = destination + str(
                len(os.listdir(destination))) + '/'
            os.makedirs(specific_folder)
            for f in os.listdir(source):
                if ".log" in f:
                    shutil.move(source + f, specific_folder)

    # 1 evolution: mate the population, mutates them, computes their accuracy,
    # sort by accuracy, and save the best to the file.
    # Repeat evolutions as specified in config.json.
    def evolve(self, evolution_count=0):
        while evolution_count < config["NumEvolutions"]:
            self.population = self.mating.crossover(self.population)
            self.population = mutate.mutate(self.population)
            self._compute_fitness()
            self._sort()
            self._save_all_chromosomes(evolution_count)
            self._display_population(evolution_count)
            evolution_count += 1

    # ---------------- #
    #    "Private"     #
    # ---------------- #

    # compute the fitness of all chromosomes in the population.
    def _compute_fitness(self):
        sizes = (config["TrainingSizeHMM"], config["TestingSizeHMM"])
        self.celex.load_sets(sizes[0], sizes[1])

        pool = ActivePool()
        s = multiprocessing.Semaphore(config["MaxThreadCount"])
        results_queue = multiprocessing.Queue()
        jobs = [
            multiprocessing.Process(target=self._compute_single_fitness,
                                    name=str(i),
                                    args=(i, sizes, s, pool, results_queue))
            for i in range(len(self.population))
        ]
        for j in jobs:
            j.start()

        for j in jobs:
            j.join()

        for result in [results_queue.get() for j in jobs]:
            self.population[result[0]].set_fitness(result[1])

    # sets Chromosome.fitness equal to syllabification accuracy.
    # hmmSizes = (trainingSize, testingSize)
    def _compute_single_fitness(self, i, hmm_sizes, s, pool, results_queue):
        process_name = multiprocessing.current_process().name
        with s:
            pool.make_active(process_name)
            genes = self.population[i].get_genes()
            hmmbo = self.celex.train_hmm(genes)
            fitness = self.celex.test_hmm(hmmbo)
            hmmbo = None
            results_queue.put((i, fitness))
            pool.make_inactive(process_name)

    # sort self.population by fitness (syllabification accuracy)
    # ordering: highest (self.population[0]) -> lowest
    def _sort(self):
        self.population.sort()
        self.population.reverse()

    # outputs all chromosomes to a log file corresponding to a given evolution.
    def _save_all_chromosomes(self, cur_evolution):
        location = config["LogFileLocation"]
        name = "evo" + str(cur_evolution) + ".log"
        file_name = location + name
        map(lambda x: self._save_chromosome_at_index(x, file_name),
            range(len(self.population)))

    # chromosome 'self.population[index]' saved in
    # "GeneticAlgorithm/EvolutionLogs".
    # truncates the file if inserting from index 0.
    # Each 2-line group is a chromosome.
    # Categories are tab-delimited.
    # Genes have no spaces between them.
    def _save_chromosome_at_index(self, index, file_name):
        how_to_open = 'w' if index == 0 else 'a'
        with open(file_name, how_to_open) as out_file:
            for category in self.population[index].get_genes():
                out_file.write(''.join(category) + '\t')
            out_file.write(
                '\n{}\n'.format(self.population[index].get_fitness())
            )

    def _display_population(self, evolution_number=0):
        print("Population after evolution #" + str(evolution_number))
        for i in range(len(self.population)):
            print("chrom{}\t{}".format(i, self.population[i].get_fitness()))
        print()
