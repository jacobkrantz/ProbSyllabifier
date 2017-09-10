from random import randint
import copy
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

    def __init__(self, config):
        self.config = config
        self.newPopulation = []

    # performs as specified in above header
    def crossover(self, population):
        #print population[0].getGenes()
        self.newPopulation = []
        self.selection(population)
        return population

    #selects the population to continue on living
    def selection(self,population):
        amount = len(population)/2
        temporaryPopulation = len(population)
        spot1 = 0
        spot2 = 0

        for i in range(temporaryPopulation/2):
            spot1 = randint(0,amount)
            spot2 = randint(0,amount)
            #making sure it's not the same chromosome being used
            while(spot1 == spot2):
                spot1 = randint(0,amount)

            #setting up the parents chromosomes
            mother = population[spot1]
            father = population[spot2]

            #remove the chromosomes from the first population set
            population.remove(mother)
            population.remove(father)

            #add the parents to the new Population set
            self.newPopulation.append(mother)
            self.newPopulation.append(father)

            self.matePair(mother,father)


    #Pre: Given the mother and father chromosomes
    #Post: Returns a child chromosome
    def matePair(self,mother,father):
        #the chromosome with a higher fitness has a slightly higher
        #chance of being selected; reenforcing the good genes
        if(mother.getFitness() <= father.getFitness()):
            percentage = father.getFitness()/float(mother.getFitness()+1)

        elif(mother.getFitness() >= father.getFitness()):
            percentage = mother.getFitness()/(float(father.getFitness())+1)

        print "percentage",percentage
        motherRange = percentage
        fatherRange = percentage

        child1 = copy.deepcopy(father)
        print father.getGenes()
        print father.getCategory('F')
        #exchanging the phones into their new, mated categories
        for phone in self.config["GeneList"]:
            randNum = randint(0,1)

            #father
            if(randNum == 0):
                pass

            #mother
            elif(randNum == 1):
                category = mother.getCategory(phone)
                child1.insertIntoCategory(category,phone)
                
        print child1.getGenes()
