'''
fileName:       Chromosome.py
Authors:        Jacob Krantz,Max Dulin
Date Modified:  9/7/17

Contains
- definitions and properties of a chromosome
- methods for modifying the chromosome

*Chromosomes are phone transcription schemes
'''

class Chromosome:

    def __init__(self, numCategories):
        self.genes = self.initGenes(numCategories)
        self.fitness = float(0.00)

    # for sorting a collection of chromosomes. Pythonic beauty.
    def __lt__(self, other):
        return self.fitness < other.fitness

    # categories are implemented as sets
    def initGenes(self, numCategories):
        genes = []
        for i in range(numCategories):
            genes.append(set())
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
        self.genes[categoryNumber].add(gene)

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

    #prints the genes out in a nicer manner
    def printChrom(self):
        count = 0
        for category in self.genes:
            print "Category ",count,": ",
            for gene in category:
                print gene,
            count = count + 1
            print
