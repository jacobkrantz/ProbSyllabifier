

class Chromosome:
    """
    Chromosomes contain phone transcription schemes.
    Contains
        - definitions and properties of a chromosome
        - methods for modifying the chromosome
    """

    def __init__(self, num_categories):
        self.genes = self.init_genes(num_categories)
        self.fitness = float(0.00)
        self.results = list()

    def __lt__(self, other):
        """for sorting a collection of chromosomes. Pythonic beauty."""
        return self.fitness < other.fitness

    def init_genes(self, num_categories):
        """
        Initializes the genes to be a list of n empty sets.
        Args:
            num_categories (int): number of categories the genes will contain.
        """
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

    def set_results(self, results):
        """
        self.results: list<(p_syl_result, c_syl_result, same)>
            p_syl_result: syllabified word by probSyllabifier
            c_syl_result: syllabified word by CELEX
            same: 1 if p_syl_result == c_syl_result else 0
        """
        self.results = results

    def get_results(self):
        return self.results

    def insert_into_category(self, category_number, gene):
        """
        Inserts a gene into a specified category.
        Removes gene from the previous location it was in.
        Args:
            category_number (int): which category to insert into
            gene (char): gene to be moved into category category_number
        """
        self.remove_gene(gene)
        self.genes[category_number].add(gene)

    # ---------------- #
    #    "Private"     #
    # ---------------- #

    def remove_gene(self, gene):
        """
        Removes a gene from the population.
        Args:
            gene (char): gene to be removed
        Returns:
            True if gene found and removed. False otherwise.
        """
        for i in range(len(self.genes)):
            if gene in self.genes[i]:
                self.genes[i].remove(gene)
                return True
        return False

    def get_category(self, gene):
        """
        Finds the category that a phone exists in.
        Args:
            gene (char): gene to be found
        """
        for i in range(len(self.genes)):
            if gene in self.genes[i]:
                return i

    def print_chrom(self):
        """prints the genes out in a nicer manner"""
        count = 0
        for category in self.genes:
            print "Category ", count, ": ",
            for gene in category:
                print gene,
            count = count + 1
            print
