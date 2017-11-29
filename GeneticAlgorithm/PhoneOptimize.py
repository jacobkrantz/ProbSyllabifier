from __future__ import print_function
from itertools import permutations
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
from config import settings,GAConfig
from GeneticAlgorithm import GeneticAlgorithm

class PhoneOptimize(GeneticAlgorithm):
    def __init__(self):
        self.phone_list = settings["PhoneOptimize"]["phone_list"]
        self.file_name = settings["PhoneOptimize"]["transcription_file"]
        self.population = []
        self.celex = Celex()

    def display_parameters(self):
        """ Displays all configuation parameters to the console. """
        noc = GAConfig["NumCategories"]
        nog = len(GAConfig["GeneList"])


        display_string = """
    Genetic Algorithm Parameters
    ----------------------------
    Number of Categories     %s
    Number of Genes          %s
    """ % (noc, nog)

        print(display_string)

    def import_population(self):
        """
        Pulls an existing population from an evolution log file.
        Args:
            resume_from (int): evolution number to import from.
        """
        location = GAConfig["LogFileLocation"]
        file_name = location + self.file_name

        with open(file_name, 'r') as in_file:
            for line in in_file:
                if len(line) < len(GAConfig["GeneList"]):
                    self.population[-1].set_fitness(float(line))
                    continue

                genes = line.split('\t')
                new_chromosome = Chromosome(GAConfig["NumCategories"])
                for i in range(len(genes) - 1):
                    for gene in genes[i]:
                        new_chromosome.insert_into_category(i, gene)
                self.population.append(new_chromosome)
                return

        self._display_population()

    def make_population(self):
        """
        Runs the process of creating a population with the specified phones changed
        """
        self.import_population()
        #optimize.view_population()
        self.create_population_set()
        self.insert_phones()
        self.compute_fitness()


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
        #print (len(self.population))

    def insert_phones(self):
        """
        Inserts the delted phones into the population"
        Args:
            phone_list: The list of phones that are to be added to the population
        """
        permutations = self._create_list()
        pop_spot = 1 #beacause the first spot in population has the original
        #print(permutations[55])
        #print (self.population[56].print_chrom())

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
