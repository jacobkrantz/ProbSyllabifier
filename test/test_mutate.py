from GeneticAlgorithm import mutate, Chromosome
from config import GAConfig as config
import unittest
import sys

class TestMutate(unittest.TestCase):

    def setUp(self):
        self.populationZero = []
        self.populationLow  = []
        self.populationHigh = []
        self.population     = []
        self.genes          = []

        self._setUp_calc_mutate_factor()
        self._setUp_mutate()

    def tearDown(self):
        self.populationZero = None
        self.populationLow  = None
        self.populationHigh = None
        self.population     = None
        self.initMutFactor  = None
        self.genes          = None

    def test_calculate_mutation_factor(self):
        '''
        tests that an approximately correct mutation factor is generated
        for the upcoming round of mutations.
        '''
        mutationFactor = mutate.calculateMutationFactor(self.populationLow)
        # mutation should increase when (dev < desiredDev)
        self.assertGreater(mutationFactor, self.initMutFactor)
        self.assertNotAlmostEqual(mutationFactor, self.initMutFactor)

        mutationFactor = mutate.calculateMutationFactor(self.populationZero)
        # mutation should increase greatly
        self.assertGreater(mutationFactor, self.initMutFactor)
        self.assertNotAlmostEqual(mutationFactor, self.initMutFactor)

        mutationFactor = mutate.calculateMutationFactor(self.populationHigh)
        # mutation should decrease when (2*desiredDev < dev)
        self.assertGreater(self.initMutFactor, mutationFactor)

    def test_mutate(self):
        '''
        tests the entire mutation function because we don't know why genes are
        not being mutated.
        '''
        newPopulation = mutate.mutate(self.population)
        # first chromosome in population should not be mutated
        self.assertEqual(newPopulation[0].getGenes(), self.population[0].getGenes())

        # at least one chromosome should have a mutation performed
        # (this may fail at an incredibly low mutation factor. check config)
        diffExists = False
        for i, chromosome in enumerate(newPopulation):
            if(self.population[i].getGenes() != chromosome.getGenes()):
                diffExists = True
        self.assertTrue(diffExists)

    #--------------------#
    #      private       #
    #--------------------#

    def _setUp_calc_mutate_factor(self):
        '''
        Creates three populations to be used in mutation factor generation
        self.populationZero, self.populationLow, self.populationHigh
        '''
        self.initMutFactor = float(config["BaseMutationFactor"])

        self.populationZero = [] # dev: 0.00
        for fitness in [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]:
            self.populationZero.append(self._makeChromosome(fitness))

        self.populationLow = [] # dev: 0.57735
        for fitness in [87,88,88,88,88,88,88,88,88,89,89,89]:
            self.populationLow.append(self._makeChromosome(fitness))

        self.populationHigh = [] # dev: 5.940998
        for fitness in [75,77,85,86,87,88,89,90,91,92,93,94]:
            self.populationHigh.append(self._makeChromosome(fitness))

    def _setUp_mutate(self):
        '''
        Creates a population (self.population) complete with identical genes and identical fitness.
        We expect to see a population with all members except the first
            to be mutated to some degree (~15% of genes)
        '''
        self.genes = [
            ['b','h','z','m','0','x','Z'],
            ['p','C','T','_','v'],
            ['k'],
            ['d','n'],
            ['$','I','P','2','5','~'],
            ['@','E','i','1','u','7','8','U'],
            ['t','N'],
            ['H','#','r','c','F'],
            ['D','j','Q','3','4','V','9','{'],
            ['S','R','l','6'],
            ['q','s'],
            ['J','w','g','f']
        ]
        self.population = []
        for j in range(config["NumChromsInDeviation"]):
            newChromosome = Chromosome(config["NumCategories"])
            newChromosome.setFitness(88.9)
            for i in range(len(self.genes) - 1):
                for gene in self.genes[i]:
                    newChromosome.insertIntoCategory(i, gene)
            self.population.append(newChromosome)

    # helper function sets a single chromosome
    def _makeChromosome(self, fitness):
        chrom = Chromosome(0)
        chrom.setFitness(fitness)
        return chrom

    # keep for deeper testing purposes. not currently used.
    def _displayPopulation(self, pop):
        for chrom in pop:
            print "chromosome:"
            for category in chrom.getGenes():
                for gene in category:
                    sys.stdout.write(gene)
                sys.stdout.write(' ')
            sys.stdout.write('\n')

if __name__ == '__main__':
    unittest.main()
