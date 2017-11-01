from Chromosome import Chromosome
from config import GAConfig as config
from random import randint
import numpy as np

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
    mutFactor = calculateMutationFactor(pop)
    return [pop[0]] + list(map(lambda x:mutateChrom(x,mutFactor), pop[1:]))

def calculateMutationFactor(pop):
    """
    Calcuates a standard deviation of the top chromosomes fitness.
    Returns a variable mutation factor; higher when low deviation,
    lower when high deviation.

    Args:
        pop (list of type Chromosome): entire working population.
    Returns:
        float: factor for chromosome mutation.
    """
    stdev = np.std(np.array(list(map(lambda x: x.getFitness(), pop[:config["NumChromsInDeviation"]]))))
    desiredDev = float(config["DesiredDeviation"])
    mutationFactor = float(config["BaseMutationFactor"])

    if stdev <= desiredDev:
        mutationFactor -= (stdev - desiredDev) / float((desiredDev * 10))
    elif stdev > (2 * desiredDev):
        mutationFactor *= 0.75

    return mutationFactor

def mutateChrom(chromosome, mutationFactor):
    '''
    Per-gene: each gene has a percent chance of mutating to a random category.

    Args:
        chromosome (Chromosome): the chomosome to mutate
        mutationFactor (float): the factor used to alter the chromosome
    Returns:
        Chromosome: the provided chromosome with mutations made
    '''
    newChromosome = Chromosome(config["NumCategories"])

    for catIndex, category in enumerate(chromosome.getGenes()):
        for gene in category:
            newCategory = catIndex
            if(float(randint(0,99))/100 <= mutationFactor):
                while(newCategory == catIndex):
                    newCategory = randint(0, config["NumCategories"] - 1)
            newChromosome.insertIntoCategory(newCategory, gene)

    return newChromosome
