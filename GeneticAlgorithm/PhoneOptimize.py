from __future__ import print_function
from itertools import permutations
from datetime import datetime
import multiprocessing
import os
import shutil
from random import randint
import zipfile
import logging as log
import mutate
from Chromosome import Chromosome
from Mating import Mating
from activePool import ActivePool
from celex import Celex
from config import settings,GAConfig
from computeFitness import ComputeFitness
from evaluation import Evaluation

class PhoneOptimize:
    def __init__(self):
        self.compute_fitness = ComputeFitness()
        self.phone_list = settings["PhoneOptimize"]["phone_list"]
        self.file_name = settings["PhoneOptimize"]["transcription_file"]
        self.population = []
        self.opt_phone = ""
        self.celex = Celex()
        self.Eval = Evaluation()

    def run_genetic(self,scheme,spot):
        """
        Runs the whole optimization
        """
        self.population.append(scheme[spot])
        self.phone_list = [self.Eval.set_data(self.population[0])]
        log.info("The phone " + self.phone_list[0] + " was choosen for the scheme in slot " + str(spot)+ ".")

        self.create_population_set()
        self.insert_phones()
        self.population = self.compute_fitness.compute(self.population)
        self._sort()
        scheme[spot] = self.population[0]
        return scheme

    def check_file_type(self):
        """
        Checks the population file type. Either a syllabifier .txt file or a GA evo file
        Returns:
            1 for a syllabifier file, 2 for a GA file
        """
        location = GAConfig["LogFileLocation"]
        self.file_name

        exten = self.file_name[-4:]
        if exten == ".txt": #syllabifier scheme
            return 1
        elif exten == ".log": #genetic Algorithm scheme
            return 2
        else:
            assert(False)

    def import_population_log(self):
        """
        Pulls an existing population from an evolution log file.
        """
        location = GAConfig["LogFileLocation"]
        file_name = location + self.file_name

        with open(file_name, 'r') as in_file:
            for line in in_file:
                genes = line.split('\t')
                new_chromosome = Chromosome(GAConfig["NumCategories"])
                for i in range(len(genes) - 1):
                    for gene in genes[i]:
                        new_chromosome.insert_into_category(i, gene)
                self.population.append(new_chromosome)
                return

    def pick_scheme(self):
        """
        Runs the correct population import scheme
        """
        scheme = self.check_file_type()
        if(scheme == 2):
            self.import_population_log()
        else:
            self.import_population_txt()

    def import_population_txt(self):
        """
        Imports a phonetic categorization scheme that relates to the syllablifier
        """
        location = GAConfig["LogFileLocation"]
        file_name = location + self.file_name
        chrom_list = []
        categories = 0
        with open(file_name, 'r') as in_file:
            for line in in_file:
                category_list = []
                for char in line:
                    if(char != ' ' and char != '\n' and  char !='\t'):
                        category_list.append(char)
                chrom_list.append(category_list)
        chrom_list = chrom_list[:-1]

        chrom = Chromosome(len(chrom_list))
        spot = 0

        for category in (chrom_list):
            for phone in category:
                chrom.insert_into_category(spot,phone)
            spot+=1
        self.population.append(chrom)
        return

    def make_population(self):
        """
        Runs the process of creating a population with the specified phones changed
        """

        self.pick_scheme()

        #self.view_population()
        self.create_population_set()
        self.insert_phones()
        self.population = self.compute_fitness.compute(self.population)

    def _display_population(self):
        """ Displays the population"""
        print("Chrom#   Percent Accuracy")
        print("_________________________")
        for i in range(len(self.population)):
            print("chrom{}     {}".format(i, self.population[i].get_fitness()))
        print()

    def strip_phones(self, phone_strip):
        """
        Deletes a phone from the chromosome
        Returns:
            The phone that has been deleted
        """
        chrom = self.population[0]
        chrom.remove_gene(phone_strip)
        return phone_strip

    def create_population_set(self):
        """
        Creates the base set of chromosomes to be modified with each phone given
        """
        for num in range(GAConfig["NumCategories"]**len(self.phone_list)):
            new_chromosome = self.chrom_copy(self.population[0])
            self.population.append(new_chromosome)

    def insert_phones(self):
        """
        Inserts the delted phones into the population"
        Args:
            phone_list: The list of phones that are to be added to the population
        """
        permutations = self._create_list()
        pop_spot = 1 #beacause the first spot in population has the original

        for attempt in permutations:

            for spot in range(len(attempt)):
                self.population[pop_spot].insert_into_category(attempt[spot],self.phone_list[spot])
            pop_spot+=1
        self.population.pop(0)

    def _create_list(self):
        """
        Creates a list of all the possible permutations for a given a chromosomes set
        Args:
            phone_list: the phones that are going to be added in
        Returns:
            A list with all the different permutations
        """
        spot_lst = []
        if len(self.phone_list) == 0:
            return
        elif len(self.phone_list) == 1:
            for spot in range(GAConfig["NumCategories"]):
                spot_lst.append([spot])
        elif(len(self.phone_list) == 2):
            for spot in range(GAConfig["NumCategories"]):
                for spot2 in range(GAConfig["NumCategories"]):
                    spot_lst.append([spot,spot2])
        return spot_lst


    def view_population(self):
        """Displays the chromosome with its phones, in each category"""
        for chrom in self.population:
            chrom.print_chrom()

    def chrom_copy(self, chrom):
        """
        Copies the value of the chromosome into a new chromosome
        Returns:
            A non references identical chromosome
        """
        new_chromosome = Chromosome(GAConfig["NumCategories"])

        for phone in GAConfig["GeneList"]:
            spot = chrom.get_category(phone)
            if(spot != None):
                new_chromosome.insert_into_category(spot,phone)
        return new_chromosome

    def output_into_file(self, schema):
        """
        Outputs the population to a file
        """
        pass

    def _sort(self):
        """
        Sort self.population by fitness (syllabification accuracy)
        Ordering: highest (self.population[0]) -> lowest
        """
        self.population.sort()
        self.population.reverse()
