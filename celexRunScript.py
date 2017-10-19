from celex import Celex
'''
- Allows for a quick run of a desired size pulled from any evolution file.
- Automatically loads the best chromosome from the evolution to test.
- Useful for running large-scale tests of a chromosome that appears
to be performing well.
- For small tests to ensure system functionality, run the unit tests (see README.md)
- is thread-safe.

Set parameters here:
'''
evoFileLocation = "./GeneticAlgorithm/EvolutionLogs/Archive/1/evo309.log"
trainingSize = 500
testingSize = 25
'''---------------------------------------'''


with open(evoFileLocation,'r') as evo:
    bestEvoRaw = evo.readline().split()
    transcriptionScheme = []
    for category in bestEvoRaw:
        transcriptionScheme.append(map(lambda x: x, category))

c = Celex()
c.loadSets(trainingSize,testingSize)
GUID = c.trainHMM(transcriptionScheme)
percentSame = c.testHMM(transcriptionScheme, GUID)
