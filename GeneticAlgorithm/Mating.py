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
        return copy.deepcopy(self.newPopulation)

    #selects the population to continue on living
    def selection(self,population):
        amount = len(population)/2
        print(len(population)),"Len of pop"
        print amount, "Value of amount"
        temporaryPopulation = len(population)

        for i in range(self.config["NumMatingPairs"]):

            spot1 = randint(0,amount-1)
            spot2 = randint(0,amount-1)
            #making sure it's not the same chromosome being used
            while(spot1 == spot2):
                spot2 = randint(0,amount-1)

            #setting up the parents chromosomes
            mother = copy.deepcopy(population[spot1])
            father = copy.deepcopy(population[spot2])

            #add the parents to the new Population set
            self.newPopulation.append(mother)
            self.newPopulation.append(father)

            #remove the chromosomes from the first population set
            if(spot1 > spot2):
                del population[spot1]
                del population[spot2]

            else:
                del population[spot2]
                del population[spot1]

            #add two new children to the population
            #print self.newPopulation[-1].getGenes()
            self.newPopulation.append(self.matePair(mother,father))
            self.newPopulation.append(self.matePair(mother,father))

            amount = amount - 2
        return


    #Pre: Given the mother and father chromosomes
    #Post: Returns a child chromosome
    def matePair(self,mother,father):
        #print "Father Fit",father.getFitness()
        #print "mother fit",mother.getFitness()
        #the chromosome with a higher fitness has a slightly higher
        #chance of being selected; reenforcing the good genes


        #possibly need to get the count of the evolution
        if(mother.getFitness() == 0 or father.getFitness() == 0):
            if(mother.getFitness() == 0):
                fatherRange = 70
                motherRange = 30
            else:
                fatherRange = 30
                motherRange = 70

        else:
            whole = father.getFitness() + mother.getFitness()
            #percentage = father.getFitness()/float(mother.getFitness())
            fatherRange = father.getFitness()/float(whole) * 100
            motherRange = mother.getFitness()/float(whole) * 100

        fatherRange = 50
        motherRange = 50
        #print "Fatherrange",fatherRange
        #print "motherRange",motherRange
        #print motherRange + fatherRange
        child1 = copy.deepcopy(father)
        child1.setFitness(0)
        #print father.getGenes()
        #print mother.getGenes()
        #print father.getCategory('F')
        #exchanging the phones into their new, mated categories
        for phone in self.config["GeneList"]:

            randNum = randint(0,100)
            #print phone,randNum
            #father
            if(randNum >= 0 and randNum <= fatherRange):
                pass
            #mother
            elif(randNum >= fatherRange and randNum <= 100):
                category = mother.getCategory(phone)
                child1.insertIntoCategory(category,phone)

        #print child1.getGenes()
        return child1
