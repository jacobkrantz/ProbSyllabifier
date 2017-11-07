import copy
from random import randint

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

    # performs as specified in above header
    def crossover(self, population):
        # print population[0].getGenes()
        self.newPopulation = []
        self.selection(population)
        return copy.deepcopy(self.newPopulation)

    # selects the population to continue on living
    def selection(self, population):
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

            spot1 = randint(0, amount - 1)
            while spot1 in used_list:
                spot1 = randint(0, amount - 1)

            spot2 = randint(0, amount - 1)
            while spot2 in used_list or spot2 == spot1:
                spot2 = randint(0, amount - 1)

            # setting up the parents chromosomes
            mother = copy.deepcopy(population[spot1])
            father = copy.deepcopy(population[spot2])

            # add two new children to the population
            # print self.newPopulation[-1].getGenes()
            self.newPopulation.append(self.mate_pair(mother, father))
            self.newPopulation.append(self.mate_pair(mother, father))
        return

    # Pre: Given the mother and father chromosomes
    # Post: Returns a child chromosome
    def mate_pair(self, mother, father):

        # possibly need to get the count of the evolution
        if mother.get_fitness() == 0 or father.get_fitness() == 0:
            if mother.get_fitness() == 0:
                father_range = 70
                mother_range = 30
            else:
                father_range = 30
                mother_range = 70
        else:
            whole = father.get_fitness() + mother.get_fitness()
            father_range = father.get_fitness() / float(whole) * 100
            mother_range = mother.get_fitness() / float(whole) * 100

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

        # print child1.getGenes()
        return child1
