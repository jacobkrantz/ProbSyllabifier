import sys

from GeneticAlgorithm import GeneticAlgorithm
from config import GAConfig, settings
from utils import EmailClient

"""
fileName:       optimize.py
Authors:        Jacob Krantz, Max Dulin
Date Modified:  9/10/17

- Optimizes the phone category transcriptions using a
    genetic algorithm.
- Commandline argument:
    integer representing an evolution number to continue from.
    optional.
    ex. 'python optimize.py 50'
"""


# evolutionNumber represents the evolution log file to continue from
def optimize():
    ga = GeneticAlgorithm()
    ga.display_parameters()

    assert(GAConfig["PopulationSize"]/4 == GAConfig["NumMatingPairs"])
    evolution_number = 0
    if len(sys.argv) > 1:
        evolution_number = int(sys.argv[1])
        ga.import_population(evolution_number)
        evolution_number += 1
    else:
        ga.archive_logs()
        ga.initialize_population()

    evolutions_to_run = GAConfig["NumEvolutions"]
    ga.evolve(evolutions_to_run, evolution_number)

    if(settings["environment"] == "AWS"):
        email_client = EmailClient()
        zip_file_name = ga.send_evolutions_to_zip()
        for to_address in settings["email"]["to_addresses"]:
            email_client.notify_run_complete(to_address, zip_file_name)


optimize()
