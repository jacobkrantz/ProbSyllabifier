from __future__ import print_function

from datetime import datetime
import multiprocessing
import os
import shutil
from random import randint
import zipfile

import mutate
from Chromosome import Chromosome
from Mating import Mating
from activePool import ActivePool
from celex import Celex
from config import GAConfig as config
from GeneticAlgorithm import GeneticAlgorithm

class PhoneOptimize:
    def __init__(self):
        self.population = []
        self.celex = Celex()

    def display_parameters(self):
        """ Displays all configuation parameters to the console. """
        noc = config["NumCategories"]
        nog = len(config["GeneList"])

        display_string = """
    Genetic Algorithm Parameters
    ----------------------------
    Number of Categories     %s
    Number of Genes          %s
    """ % (ips, ps, nomp, mf, ne, noc, nog)

        print(display_string)

    def initialize_population(self):
        """
        Initializes the population to hold chromosomes that are
        Generated from random gene-category selections.
        Computes each chromosomes fitness.
        """


        self._compute_fitness()
        self._sort()

    def import_population(self, resume_from):
        """
        Pulls an existing population from an evolution log file.
        Args:
            resume_from (int): evolution number to import from.
        """
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
                return

        self._display_population(resume_from)

    def _compute_fitness(self):
        """
        Compute the fitness of all chromosomes in the population.
        Updates the fitness value of all chromosomes.
        Chromosome fitness calculation is done in separate processes.

        """
        sizes = (config["TrainingSizeHMM"], config["TestingSizeHMM"])
        self.celex.load_sets(sizes[0], sizes[1])

        pool = ActivePool()
        s = multiprocessing.Semaphore(config["MaxThreadCount"])
        results_queue = multiprocessing.Queue()
        jobs = [
            multiprocessing.Process(target=self._compute_single_fitness,
                                    name=str(i),
                                    args=(i, s, pool, results_queue))
            for i in range(len(self.population))
        ]
        for j in jobs:
            j.start()

        for j in jobs:
            j.join()

        for result in [results_queue.get() for j in jobs]:
            self.population[result[0]].set_fitness(result[1])

    def _compute_single_fitness(self, i, s, pool, results_queue):
        """
        Calculates and puts updated fitness on the results_queue.
        Args:
            i (int): process and population index
            s (multiprocessing.Semaphore)
            pool (ActivePool): manager of the pool and locks
            results_queue (multiprocessing.Queue): communication
                        between processes.
        """
        process_name = multiprocessing.current_process().name
        with s:
            pool.make_active(process_name)
            genes = self.population[i].get_genes()
            hmmbo = self.celex.train_hmm(genes)
            fitness = self.celex.test_hmm(hmmbo)
            hmmbo = None
            results_queue.put((i, fitness))
            pool.make_inactive(process_name)

    def _display_population(self, evolution_number=0):
        """ Displays the population and the current evolution number. """
        print("Population after evolution #" + str(evolution_number))
        for i in range(len(self.population)):
            print("chrom{}\t{}".format(i, self.population[i].get_fitness()))
        print()

    def strip_phones(self,phone_strip):
        """
        Deletes a phone from the chromosome
        Returns:
            The phone that has been deleted
        """
        chrom = self.population[0]
        chrom.remove_gene(phone_strip)
        return phone_strip

    def create_population_set(self,phone_list):
        """
        Creates the base set of chromosomes to be modified with each phone given
        """

        for num in range(config["NumCategories"]**len(phone_list)):
            new_chromosome = self.chrom_copy(self.population[0])
            self.population.append(new_chromosome)
        self.view_population()
        print (len(self.population))

    def _insert_phones(self,phone_list):
        spot_lst = []
        for spot in range(config["NumCategories"]**len(phone_list)):
            pass


    def view_population(self):
        """Displays the chromosome with its phones, in each category"""
        for chrom in self.population:
            chrom.print_chrom()

    def chrom_copy(self,chrom):
        """
        Copies the value of the chromosome into a new chromosome
        Returns:
            A non references identical chromosome
        """
        new_chromosome = Chromosome(config["NumCategories"])

        for phone in config["GeneList"]:
            spot = chrom.get_category(phone)
            if(spot != None):
                new_chromosome.insert_into_category(spot,phone)
        return new_chromosome
