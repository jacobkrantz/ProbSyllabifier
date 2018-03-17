
import copy
from random import randint

from chromosome import Chromosome
from config import GAConfig as config

'''
fileName:       Mating.py
Authors:        Jacob Krantz, Max Dulin
Date Modified:  9/7/17

Contains the workings for mating together the population.
- retains the top 50% fit chromosomes and removes the rest
- remaining chromosomes are paired
- each pair is mated, generating 2 new chromosomes per pair
- returns the new population, the same size as passed in. Unordered.
'''


class Mating:
    def __init__(self):
        self.newPopulation = []

    def mate(self, population):
        """
        The main function that is called outside of the class
        Args:
            population(list of chromosomes): the full population of the GA
        """

        self.newPopulation = []
        self.newPopulation = self._SUS(population)
        #self._selection_random(population)

        return copy.deepcopy(self.newPopulation)


    #############
    ##Private ###
    #############

    def _SUS(self, population):
        """
        Stochastic Universal Sampling(SUS) method.
        Used to select which parts of the population are selected to live.
        Args:
            population(list of chromosomes): the whole population in the GA.
        Returns:
            Args:

        """
        alter = self._find_chroms(population)
        return self._best_last(population,alter)

    def _best_last(self, population, alter):
        """
        Algorithm for choosing which members of the population mate.
        The current best and the current worse mate. This is continued
        until all members of the population are done.
        Args:
            population(list of chromosomes): all members of the GA's population.
            alter(list of int): which chromosomes shall be kept.
        """

        new_pop = list()
        alter.sort()
        pairs = self._make_pairs(alter)
        for tup in pairs:
            father = copy.deepcopy(population[tup[0]])
            mother = copy.deepcopy(population[tup[1]])
            new_pop.append(father)
            new_pop.append(mother)
            child1,child2 = self._scattered_crossover(mother,father)
            new_pop.append(child1)
            new_pop.append(child2)
        return new_pop

    def _make_pairs(self, alter):
        """
        Creates the mating pairs for the GA
        Args:
            alter(list): the chromosomes index's to be used.
        Returns:
            pairs(list of tuples): each tuple in the list is a mating pair.
        """
        pairs = list()
        for index in range(len(alter)/2):
            pairs.append((alter[index], alter[len(alter)-index-1]))
        return pairs

    def _find_chroms(self, population):
        """
        Grabs the chromosomes that are to be assigned to continue living
        Args:
            population(list of chromosomes): the entire population of the GA.
        Returns:
            range_list(list): an integer array where the values coorespond
                to a spot in the population in the GA.
        """

        cur_num = 0
        total = 0
        fit_list = list()
        fit_list.append(0)
        amount = config["PopulationSize"]
        count = 0
        for chrom in population:
            #should do something to make this more dramatic
            if(count >= len(population)/4):
                increase = chrom.get_fitness() ** 18
                total += increase
                range_val =  cur_num + increase
                cur_num = range_val
                fit_list.append(range_val)
            count+=1

        range_list = [val / (float(total)) for val in fit_list]
        range_list = self._gen_select(range_list)
        return self._fix_spot(range_list)

    def _fix_spot(self, range_list):
        """
        Normalilzes the range_list in order to be understandable by the GA's
        population.
        Args:
            range_list(list): a list of integers
        Returns:
            range_list(list): a list of integers
        """

        for spot in range(len(range_list)):
            range_list[spot] = range_list[spot] + config["PopulationSize"]/4

        for num in range(config["PopulationSize"]/4):
            range_list.append(num)
        return range_list

    def _gen_select(self, range_list):
        """
        Generates the population to be kept and mated.
        Args:
            range_list(list): a list of the areas that the population owns.
        Returns:

        """
        amount = config["PopulationSize"]/4
        interval = int(1/(float(amount))*10000)
        keep_list = list()
        for spot in range(amount):
            location = randint(interval*spot,interval *(spot+1))/float(10000)
            for space in range(len(range_list)):
                if(location >= range_list[space] and location <= range_list[space + 1]):
                    keep_list.append(space)
                    break
        return keep_list

    def _selection_random(self, population):
        """
        Selects the population to continue living
        Args:
            population(list of chromosomes): the full population of the GA
        """

        amount = len(population)
        temporary_population = len(population)
        used_list = []

        # kills the bottom part of the population
        for count in range(amount / 2):
            del population[len(population) - 1]
            self.newPopulation.append(copy.deepcopy(population[count]))
        amount = len(population)
        used_list = []

        for i in range(config["NumMatingPairs"]):
            #currently random
            spot1 = randint(0, amount - 1)
            while spot1 in used_list:
                spot1 = randint(0, amount - 1)

            spot2 = randint(0, amount - 1)
            while spot2 in used_list or spot2 == spot1:
                spot2 = randint(0, amount - 1)

            # setting up the parents chromosomes
            mother = copy.deepcopy(population[spot1])
            father = copy.deepcopy(population[spot2])

            child1, child2 = self._scattered_crossover(mother,father)
            # add two new children to the population
            self.newPopulation.append(child1)
            self.newPopulation.append(child2)
            #self.newPopulation.append(self._mate_pair(mother, father))
            #self.newPopulation.append(self._mate_pair(mother, father))
        return

    def _create_vector(self):
        """
        Creates a random vector of 0's and 1' that is then associated with
        what genes goes into which child from the parents.
        Returns:
            A vector of 0's and 1's.
        """
        vector = list()
        amount = len(config["GeneList"])
        for count in range(amount):
            rand_num = randint(0,1)
            vector.append(rand_num)
        return vector

    def _scattered_crossover(self, mother, father):
        """
        Creates two childern by using the scattered crossover mating algorithm.
        Args:
            mother(Chromosome): the mother chromosome of the children.
            father(Chromosome): the father chromosome of the children.
        Returns:
            child1(Chromosome): the offspring of the parents mating.
            child2(Chromosome): the offapring of the parents mating.
        """

        vector = self._create_vector()
        child1 = Chromosome(config["NumCategories"])
        child1.set_fitness(0)
        child2 = Chromosome(config["NumCategories"])
        child2.set_fitness(0)
        gene_list = config["GeneList"]

        # exchanging the phones into their new, mated categories
        for index in range(len(gene_list)):
            # father
            if vector[index] == 0:
                category = father.get_category(gene_list[index])
                child1.insert_into_category(category,gene_list[index])
                category = mother.get_category(gene_list[index])
                child2.insert_into_category(category,gene_list[index])
            # mother
            elif vector[index] == 1:
                category = father.get_category(gene_list[index])
                child2.insert_into_category(category,gene_list[index])
                category = mother.get_category(gene_list[index])
                child1.insert_into_category(category,gene_list[index])
        return child1,child2

    def _mate_pair(self, mother, father):
        """
        Mates two chromosomes to produce one child
        Args:
            mother(chromosome): the mother of the offspring
            father(chromosome): the father of the offspring
        Returns:
            child(chromosome): the offspring of the mother and father
        """
        father_range = 50
        mother_range = 50
        child1 = copy.deepcopy(father)
        child1.set_fitness(0)

        # exchanging the phones into their new, mated categories
        for phone in config["GeneList"]:
            rand_num = randint(0, 100)
            # father
            if 0 <= rand_num <= father_range:
                pass
            # mother
            elif father_range <= rand_num <= 100:
                category = mother.get_category(phone)
                child1.insert_into_category(category, phone)

        return child1
