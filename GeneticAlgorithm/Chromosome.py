"""
fileName:       Chromosome.py
Authors:        Jacob Krantz,Max Dulin
Date Modified:  9/7/17

Contains
- definitions and properties of a chromosome
- methods for modifying the chromosome

*Chromosomes are phone transcription schemes
"""


class Chromosome:
    def __init__(self, num_categories):
        self.genes = self.init_genes(num_categories)
        self.fitness = float(0.00)

    # for sorting a collection of chromosomes. Pythonic beauty.
    def __lt__(self, other):
        return self.fitness < other.fitness

    # categories are implemented as sets
    def init_genes(self, num_categories):
        genes = []
        for i in range(num_categories):
            genes.append(set())
        return genes

    def get_genes(self):
        return self.genes

    def get_fitness(self):
        return float(self.fitness)

    def set_fitness(self, new_fitness):
        self.fitness = float(new_fitness)

    # inserts a gene into a specified category.
    # removes gene from previous category it was in.
    def insert_into_category(self, category_number, gene):
        self.remove_gene(gene)
        self.genes[category_number].add(gene)

    # ---------------- #
    #    "Private"     #
    # ---------------- #

    # removes a gene from the population.
    # returns True if gene is found and removed.
    def remove_gene(self, gene):
        for i in range(len(self.genes)):
            if gene in self.genes[i]:
                self.genes[i].remove(gene)
                return True
        return False

    # gets the location, starting from 0, of the phone in the category scheme
    def get_category(self, phone):
        count = 0
        for category in self.genes:
            if phone in category:
                return count
            else:
                count = count + 1

    # prints the genes out in a nicer manner
    def print_chrom(self):
        count = 0
        for category in self.genes:
            print "Category ", count, ": ",
            for gene in category:
                print gene,
            count = count + 1
            print
