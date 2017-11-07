import sys
import unittest

from GeneticAlgorithm import mutate, Chromosome
from config import GAConfig as config


class TestMutate(unittest.TestCase):
    def setUp(self):
        self.population_zero = []
        self.population_low = []
        self.population_high = []
        self.population = []
        self.genes = []

        self._set_up_calc_mutate_factor()
        self._set_up_mutate()

    def tearDown(self):
        self.population_zero = None
        self.population_low = None
        self.population_high = None
        self.population = None
        self.init_mut_factor = None
        self.genes = None

    def test_calculate_mutation_factor(self):
        """
        tests that an approximately correct mutation factor is
        generated for the upcoming round of mutations.
        """
        mutation_factor = mutate.calculate_mutation_factor(self.population_low)
        # mutation should increase when (dev < desiredDev)
        self.assertGreater(mutation_factor, self.init_mut_factor)
        self.assertNotAlmostEqual(mutation_factor, self.init_mut_factor)

        mutation_factor = mutate.calculate_mutation_factor(
            self.population_zero)
        # mutation should increase greatly
        self.assertGreater(mutation_factor, self.init_mut_factor)
        self.assertNotAlmostEqual(mutation_factor, self.init_mut_factor)

        mutation_factor = mutate.calculate_mutation_factor(
            self.population_high)
        # mutation should decrease when (2*desiredDev < dev)
        self.assertGreater(self.init_mut_factor, mutation_factor)

    def test_mutate(self):
        """
        tests the entire mutation function because we don't know why
        genes are not being mutated.
        """
        new_population = mutate.mutate(self.population)
        # first chromosome in population should not be mutated
        self.assertEqual(new_population[0].get_genes(),
                         self.population[0].get_genes())

        # at least one chromosome should have a mutation performed
        # (this may fail at an incredibly low mutation factor. check config)
        diff_exists = False
        for i, chromosome in enumerate(new_population):
            if self.population[i].get_genes() != chromosome.get_genes():
                diff_exists = True
        self.assertTrue(diff_exists)

    # -------------------- #
    #       private        #
    # -------------------- #

    def _set_up_calc_mutate_factor(self):
        """
        Creates three populations to be used in mutation factor
        generation:
            self.populationZero
            self.populationLow
            self.populationHigh
        """
        self.init_mut_factor = float(config["BaseMutationFactor"])

        self.population_zero = []  # dev: 0.00
        for fitness in [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]:
            self.population_zero.append(self._make_chromosome(fitness))

        self.population_low = []  # dev: 0.57735
        for fitness in [87, 88, 88, 88, 88, 88, 88, 88, 88, 89, 89, 89]:
            self.population_low.append(self._make_chromosome(fitness))

        self.population_high = []  # dev: 5.940998
        for fitness in [75, 77, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94]:
            self.population_high.append(self._make_chromosome(fitness))

    def _set_up_mutate(self):
        """
        Creates a population (self.population) complete with identical
        genes and identical fitness. We expect to see a population
        with all members except the first to be mutated to some degree
        (~15% of genes)
        """
        self.genes = [
            ['b', 'h', 'z', 'm', '0', 'x', 'Z'],
            ['p', 'C', 'T', '_', 'v'],
            ['k'],
            ['d', 'n'],
            ['$', 'I', 'P', '2', '5', '~'],
            ['@', 'E', 'i', '1', 'u', '7', '8', 'U'],
            ['t', 'N'],
            ['H', '#', 'r', 'c', 'F'],
            ['D', 'j', 'Q', '3', '4', 'V', '9', '{'],
            ['S', 'R', 'l', '6'],
            ['q', 's'],
            ['J', 'w', 'g', 'f']
        ]
        self.population = []
        for j in range(config["NumChromsInDeviation"]):
            new_chromosome = Chromosome(config["NumCategories"])
            new_chromosome.set_fitness(88.9)
            for i in range(len(self.genes) - 1):
                for gene in self.genes[i]:
                    new_chromosome.insert_into_category(i, gene)
            self.population.append(new_chromosome)

    # helper function sets a single chromosome
    def _make_chromosome(self, fitness):
        chrom = Chromosome(0)
        chrom.set_fitness(fitness)
        return chrom

    # keep for deeper testing purposes. not currently used.
    def _display_population(self, pop):
        for chrom in pop:
            print "chromosome:"
            for category in chrom.get_genes():
                for gene in category:
                    sys.stdout.write(gene)
                sys.stdout.write(' ')
            sys.stdout.write('\n')


if __name__ == '__main__':
    unittest.main()
