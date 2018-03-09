from math import sqrt
from random import randint
from Chromosome import Chromosome
from config import GAConfig as config
import random as rand
'''
fileName:       mutate.py
Authors:        Jacob Krantz, Maxwell Dulin
Date Modified:  10/31/17

Genetic Algorithm mutations.
    - automatically determine a mutation factor
    based on stagnation of the population.
    - mutate the population based on a given
    mutation factor.
    - mutates all chromosomes except for the top.
'''


def mutate(pop):
    """
    Keeps the population from getting stagnant.
    Mutates the entire population.

    Args:
        pop (list of type Chromosome)
    Returns:
        pop (list of type Chromosome)
    """
    mutate_chrom(pop[0],1)

    mut_factor = calculate_mutation_factor(pop)
    save = config["NumChromsNotToMutate"]
    return pop[:save] + list(map(lambda x: mutate_chrom(x, mut_factor), pop[save:]))


def calculate_mutation_factor(pop):
    """
    Calculates a standard deviation of the top chromosomes fitness.
    Returns a variable mutation factor; higher when low deviation,
    lower when high deviation.

    Args:
        pop (list of type Chromosome): entire working population.
    Returns:
        float: factor for chromosome mutation.
    """
    stdev = stddev(list(map(
        lambda x: x.get_fitness(),
        pop[:config["NumChromsInDeviation"]]
    )))
    desired_dev = float(config["DesiredDeviation"])
    mutation_factor = float(config["BaseMutationFactor"])

    if stdev <= desired_dev:
        mutation_factor -= (stdev - desired_dev) / float((desired_dev * 10))
    elif stdev > (2 * desired_dev):
        mutation_factor *= 0.75

    return mutation_factor


def mutate_chrom(chromosome, mutation_factor):
    """
    Per-gene: each gene has a percent chance of mutating to a random category.

    Args:
        chromosome (Chromosome): the chromosome to mutate
        mutation_factor (float): the factor used to alter the chromosome
    Returns:
        Chromosome: the provided chromosome with mutations made
    """
    new_chromosome = Chromosome(config["NumCategories"])
    count = 0
    for cat_index, category in enumerate(chromosome.get_genes()):
        for gene in category:
            new_category = cat_index
            if float(randint(0, 99)) / 100. <= mutation_factor:
                while new_category == cat_index:
                    new_category = randint(0, config["NumCategories"] - 1)
            new_chromosome.insert_into_category(new_category, gene)
            count+=1

    #implements the category restriction for the chromosome
    if(config["CategoryRestriction"] == "True"):
        return organize(new_chromosome)
    return new_chromosome

def organize(chrom):
    """
    Ensures the constraints of having Category Restriction values
    Args:
        chrom(chromosome): the chromosome being checked
    Returns:
        The categorically correct chromosome

    """
    #actual value/number of actegory
    for spot in range(config["NumCategories"]):
        while(True):
            if(chrom.amount_of_genes(spot) < int(config["CategoryRestrictionCount"])):
                go = True
                #grabs a category that can be take from.
                while(go):
                    random_cat= get_rand_cat()
                    if(chrom.can_move(random_cat,int(config["CategoryRestrictionCount"]))):
                        go = False
                genes = chrom.get_genes()
                #select random gene
                random_gene = rand.randint(0,len(genes[random_cat])-1)
                remove_gene = list(genes[random_cat])[random_gene]
                remove_gene = genes[random_cat].pop() #just takes the back value
                chrom.remove_gene(remove_gene)
                chrom.insert_into_category(spot,remove_gene)
            else:
                break
    return chrom

def get_rand_cat():
    """
    Returns a random category number
    """
    return rand.randint(0,config["NumCategories"]-1)

def stddev(lst):
    """
    Calculate the standard deviation of a list of int or float.

    Args:
        numbers (list<int or float>)
    Returns:
        float: resulting standard dev of list
    """
    if(len(lst) == 0):
        return 0
    mean = float(sum(lst)) / len(lst)
    return sqrt(float(reduce(lambda x,y: x+y, map(lambda x: (x-mean) **2, lst))) / len(lst))
