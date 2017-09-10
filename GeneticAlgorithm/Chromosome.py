'''
fileName:       Chromosome.py
Authors:        Jacob Krantz
Date Modified:  9/7/17

Contains
- definitions and properties of a chromosome
- methods for modifying the chromosome

*Chromosomes are phone transcription schemes
'''

class Chromosome:

    # structure of chromosome is still in flux
    def __init__(self, numCategories):
        self.genes = self.initGenes(numCategories)
        self.fitness = float(0.00)

    # for sorting a collection of chromosomes. Pythonic beauty.
    def __lt__(self, other):
        return self.fitness < other.fitness

    def initGenes(self, numCategories):
        genes = []
        for i in range(numCategories):
            genes.append([])
        return genes

    def getGenes(self):
        return self.genes

    def getFitness(self):
        return float(self.fitness)

    def setFitness(self, newFitness):
        self.fitness = float(newFitness)

    # inserts a gene into a specified category.
    # removes gene from previous category it was in.
    def insertIntoCategory(self, categoryNumber, gene):
        self.removeGene(gene)
        self.genes[categoryNumber].append(gene)

    #----------------#
    #   "Private"    #
    #----------------#

    # removes a gene from the population.
    # returns True if gene is found and removed.
    def removeGene(self, gene):
        for i in range(0, len(self.genes)):
                if gene in self.genes[i]:
                    self.genes[i].remove(gene)
                    return True
        return False

    #gets the location, starting from 0, of the phone in the category scheme
    def getCategory(self,phone):
        count = 0
        for category in self.genes:
            if(phone in category):
                return count
            else:
                count = count + 1
