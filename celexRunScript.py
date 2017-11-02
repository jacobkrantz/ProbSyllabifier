from celex import Celex
'''
- Allows for a quick run of a desired size pulled from any evolution file.
- Automatically loads the best chromosome from the evolution to test.
- Useful for running large-scale tests of a chromosome that appears
to be performing well.
- For small tests to ensure system functionality, run the unit tests
    (see README.md)
- is thread-safe.

Set parameters here:
'''
evo_file_location = "./GeneticAlgorithm/EvolutionLogs/Archive/1/evo309.log"
training_size = 500
testing_size = 25
'''---------------------------------------'''


with open(evo_file_location, 'r') as evo:
    best_evo_raw = evo.readline().split()
    transcription_scheme = []
    for category in best_evo_raw:
        transcription_scheme.append(map(lambda x: x, category))

c = Celex()
c.load_sets(training_size, testing_size)
guid = c.train_hmm(transcription_scheme)
percentSame = c.test_hmm(transcription_scheme, guid)
