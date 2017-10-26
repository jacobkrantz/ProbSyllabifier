from GeneticAlgorithm import mutate, Chromosome
from config import GAConfig as config
import unittest

class TestMutate(unittest.TestCase):

    def setUp(self):
        self.initMutFactor = float(config["BaseMutationFactor"])
        lowDevFitnessLst =  [87,88,88,88,88,88,88,88,88,89,89,89] # dev: 0.57735
        highDevFitnessLst = [83,84,85,86,87,88,89,90,91,92,93,94] # dev: 3.60555

        self.populationLow = []
        for fitness in lowDevFitnessLst:
            self.populationLow.append(self.makeChromosome(fitness))

        self.populationHigh = []
        for fitness in highDevFitnessLst:
            self.populationHigh.append(self.makeChromosome(fitness))

    def tearDown(self):
        self.populationLow = None
        self.populationHigh = None
        self.initMutFactor = None

    def test_calculate_mutation_factor(self):
        mutationFactor = mutate.calculateMutationFactor(self.populationLow)
        # mutation should increase when (dev < desiredDev)
        self.assertGreater(mutationFactor, self.initMutFactor)
        self.assertNotAlmostEqual(mutationFactor, self.initMutFactor)

        mutationFactor = mutate.calculateMutationFactor(self.populationHigh)
        # mutation should stay the same when (desiredDev < dev < 2*desiredDev)
        self.assertEqual(mutationFactor, self.initMutFactor)

    # helper function sets a single chromosome
    def makeChromosome(self, fitness):
        chrom = Chromosome(0)
        chrom.setFitness(fitness)
        return chrom

if __name__ == '__main__':
    unittest.main()
