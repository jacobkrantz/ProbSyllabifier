from math import sqrt
from random import randint

from Chromosome import Chromosome
from config import GAConfig as config

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

    for cat_index, category in enumerate(chromosome.get_genes()):
        for gene in category:
            new_category = cat_index
            if float(randint(0, 99)) / 100 <= mutation_factor:
                while new_category == cat_index:
                    new_category = randint(0, config["NumCategories"] - 1)
            new_chromosome.insert_into_category(new_category, gene)

    return new_chromosome


def stddev(lst):
    """
    Calculate the standard deviation of a list of int or float.

    Args:
        numbers (list<int or float>)
    Returns:
        float: resulting standard dev of list
    """
    mean = float(sum(lst)) / len(lst)
    return sqrt(float(reduce(lambda x,y: x+y, map(lambda x: (x-mean) **2, lst))) / len(lst))
