from __future__ import print_function

from datetime import datetime
from itertools import permutations
import logging as log
import multiprocessing
import os
import shutil
import zipfile

from celex import Celex
from chromosome import Chromosome
from computeFitness import ComputeFitness
from config import settings,GAConfig
from evaluation import Evaluation
import mutate

class PhoneOptimize:
    def __init__(self):
        self.compute_fitness = ComputeFitness()
        self.phone_list = settings["phone_optimize"]["phone_list"]
        self.file_name = settings["phone_optimize"]["transcription_file"]
        self.population = []
        self.opt_phone = ""
        self.celex = Celex()
        self.eval = Evaluation()

    def run_genetic(self,scheme,spot):
        """
        Runs the whole optimization.
        This
        1. Gets the best scheme from the population.
        2. Finds the most needed phone to be optimized.
        3. Creates the population set.
        4. Inserts the phone into the correct category.
        5. Computes the accuracy of each scheme.
        6. Returns the best scheme.
        """

        self.population = []
        self.population.append(scheme[spot])
        self.phone_list = [self.eval.set_data(self.population[0])]
        #Gets the phone that will be evaluated.
        log.info("The phone " + self.phone_list[0] + " was choosen for the scheme in slot " + str(spot)+ ".")

        self._create_population_set()
        self._insert_phones()
        self.population = self.compute_fitness.compute(self.population)
        self._sort()

        ## replaces the worst scheme with the best scheme.
        scheme[-1] = self.population[0]
        return scheme

    def make_population(self):
        """
        Runs the process of creating a population with the specified phones changed
        For individual runs of the evaluator without the Genetic Algorithm
        """
        self.pick_scheme()
        self._create_population_set()
        self._insert_phones()
        self.population = self.compute_fitness.compute(self.population)

    def view_population(self):
        """Displays the chromosome with its phones, in each category"""
        for chrom in self.population:
            chrom.print_chrom()

    ##########
    #Private#
    #########

    def _check_file_type(self):
        """
        _checks the population file type. Either a syllabifier .txt file or a GA evo file
        Returns:
            1 for a syllabifier file, 2 for a GA file
        """
        location = GAConfig["log_file_location"]
        self.file_name

        exten = self.file_name[-4:]
        if exten == ".txt": #syllabifier scheme
            return 1
        elif exten == ".log": #genetic Algorithm scheme
            return 2
        else:
            assert(False)

    def _import_population_log(self):
        """
        Pulls an existing population from an evolution log file.
        """
        location = GAConfig["log_file_location"]
        file_name = location + self.file_name

        with open(file_name, 'r') as in_file:
            for line in in_file:
                genes = line.split('\t')
                new_chromosome = Chromosome(GAConfig["num_categories"])
                for i in range(len(genes) - 1):
                    for gene in genes[i]:
                        new_chromosome.insert_into_category(i, gene)
                self.population.append(new_chromosome)
                return

    def _pick_scheme(self):
        """
        Runs the correct population import scheme
        """
        scheme = self._check_file_type()
        if(scheme == 2):
            self._import_population_log()
        else:
            self._import_population_txt()

    def _import_population_txt(self):
        """
        Imports a phonetic categorization scheme that relates to the syllablifier
        """
        location = GAConfig["log_file_location"]
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



    def _display_population(self):
        """ Displays the population"""
        print("Chrom#   Percent Accuracy")
        print("_________________________")
        for i in range(len(self.population)):
            print("chrom{}     {}".format(i, self.population[i].get_fitness()))
        print()

    def _create_population_set(self):
        """
        Creates the base set of chromosomes to be modified with each phone given
        """
        for num in range(GAConfig["num_categories"]**len(self.phone_list)):
            new_chromosome = self._chrom_copy(self.population[0])
            self.population.append(new_chromosome)

    def _insert_phones(self):
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
            for spot in range(GAConfig["num_categories"]):
                spot_lst.append([spot])
        elif(len(self.phone_list) == 2):
            for spot in range(GAConfig["num_categories"]):
                for spot2 in range(GAConfig["num_categories"]):
                    spot_lst.append([spot,spot2])
        return spot_lst

    def _import_phones(self):
        """
        Pulls in the genes (phones) used for the particular language.
        Returns:
            List(strings): Each string represents a phone
        """
        gene_list = []
        phones_file = GAConfig["gene_file"]
        with open(phones_file, 'r') as in_file:
            for line in in_file:
                line = line.replace("\n","")
                gene_list.append(line)
        return gene_list

    def _chrom_copy(self, chrom):
        """
        Copies the value of the chromosome into a new chromosome
        Returns:
            A non references identical chromosome
        """
        new_chromosome = Chromosome(GAConfig["num_categories"])
        gene_list = self._import_phones()
        for phone in gene_list:
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
