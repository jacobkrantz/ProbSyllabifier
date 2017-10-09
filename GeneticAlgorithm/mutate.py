from Chromosome import Chromosome
from config import GAConfig as config
from random import randint
import numpy as np

'''
fileName:       GeneticAlgorithm.py
Authors:        Jacob Krantz, Maxwell Dulin
Date Modified:  10/8/17

Genetic Algorithm mutations.
    - automatically determine a mutation factor
    based on stagnation of the population.
    - mutate the population based on a given
    mutation factor.
'''

# keeps the population from getting stagnant by moving around genes
# in the chromosome pseudo-randomly
def mutate(population):
    mutationFactor = calculateMutationFactor(population)

    for i in range(1,len(population)):
        chrom = population[i]
        #we need to rebuild the chromosome because it's a list of sets
        newChromosome = Chromosome(config["NumCategories"])
        curIter = 0

        #per gene mutate
        for category in chrom.getGenes():
            for gene in category:
                percentage = mutationFactor * 100
                randNum = randint(0,99)
                #corresponds to the mutation factor
                if(randNum >= 0 and randNum <= percentage):
                    randomCategory = randint(0, config["NumCategories"] - 1)
                    #makes sure it cannnot be inserted back into the same category
                    while(curIter == randomCategory):
                        randomCategory = randint(0, config["NumCategories"] - 1)
                    newChromosome.insertIntoCategory(randomCategory, gene)
                else:
                    newChromosome.insertIntoCategory(curIter, gene)
            curIter = curIter + 1

    return population

# calcuates a standard deviation of the top 8 chromosomes fitness.
# Rreturns a variable mutation factor, higher when low deviation, lower
# when high deviation.
def calculateMutationFactor(population):
    stdev = np.std(np.array(list(map(lambda x: x.getFitness(), population[:8]))))
    desiredDev = float(config["DesiredDeviation"])
    mutationFactor = float(config["BaseMutationFactor"])
    if stdev <= desiredDev:
        mutationFactor -= (stdev - desiredDev) / (desiredDev * 10)
    elif stdev > (2 * desiredDev):
        mutationFactor *= 0.75

    print "Standard Deviation: ", str(stdev)
    print "Mutation Factor: ", str(mutationFactor)
    return mutationFactor
