from __future__ import print_function

from datetime import datetime
import multiprocessing
import os
import shutil
from random import randint
import zipfile

import mutate
from Chromosome import Chromosome
from Mating import Mating
from activePool import ActivePool
from celex import Celex
from config import GAConfig as config


class GeneticAlgorithm:
    """ Library for all Genetic Algorithm functionality """

    def __init__(self):
        # population holds a list of chromosomes
        self.population = []
        self.celex = Celex()
        self.mating = Mating()

    def display_parameters(self):
        """ Displays all GeneticAlgorithm parameters to the console. """
        ips = config["InitialPopulationSize"]
        ps = config["PopulationSize"]
        nomp = config["NumMatingPairs"]
        mf = config["BaseMutationFactor"]
        ne = config["NumEvolutions"]
        noc = config["NumCategories"]
        nog = len(config["GeneList"])

        display_string = """
    Genetic Algorithm Parameters
    ----------------------------
    Initial Population Size  %s
    Population Size          %s
    Number of Mating Pairs   %s
    BaseMutationFactor       %s
    Number of Evolutions     %s
    Number of Categories     %s
    Number of Genes          %s
    """ % (ips, ps, nomp, mf, ne, noc, nog)

        print(display_string)

    def initialize_population(self):
        """
        Initializes the population to hold chromosomes that are
        Generated from random gene-category selections.
        Computes each chromosomes fitness.
        """
        for i in range(config["InitialPopulationSize"]):
            new_chromosome = Chromosome(config["NumCategories"])
            for gene in config["GeneList"]:
                random_category = randint(0, config["NumCategories"] - 1)
                new_chromosome.insert_into_category(random_category, gene)

            self.population.append(new_chromosome)
        self._compute_fitness()
        self._sort()

    def import_population(self, resume_from):
        """
        Pulls an existing population from an evolution log file.
        Args:
            resume_from (int): evolution number to import from.
        """
        location = config["LogFileLocation"]
        file_name = location + "evo" + str(resume_from) + ".log"

        with open(file_name, 'r') as in_file:
            for line in in_file:
                if len(line) < len(config["GeneList"]):
                    self.population[-1].set_fitness(float(line))
                    continue

                genes = line.split('\t')
                new_chromosome = Chromosome(config["NumCategories"])
                for i in range(len(genes) - 1):
                    for gene in genes[i]:
                        new_chromosome.insert_into_category(i, gene)
                self.population.append(new_chromosome)

        self._display_population(resume_from)

    def archive_logs(self):
        """
        Move current logs to the archive.
        Each run is kept under unique folder.
        Creates directories when necessary.
        """
        source = config["LogFileLocation"]
        destination = source + "Archive/"

        if not os.path.exists(source):
            os.makedirs(source)
        if not os.path.exists(destination):
            os.makedirs(destination)

        if len(os.listdir(source)) > 1:
            specific_folder = destination + str(
                len(os.listdir(destination))) + '/'
            os.makedirs(specific_folder)
            for f in os.listdir(source):
                if((".log" in f) or (".zip" in f)):
                    shutil.move(source + f, specific_folder)

    def send_evolutions_to_zip(self):
        """
        Compresses the .log files in `GeneticAlgorithm/EvolutionLogs`
        Does not include archived runs.
        throws:
            IOError when no log files exist in the source directory
        Returns:
            string: fileName for the compressed files
        """
        source = config["LogFileLocation"]
        for f in os.listdir(source):
            if ".log" in f:
                break
        else:
            raise IOError("no .log files exist")

        now = str(datetime.now()).split(' ')
        now[1] = now[1].split('.')[0]
        fileName = source + "evolutionLogs_" + now[0] + '_' + now[1] + ".zip"
        myzip = zipfile.ZipFile(fileName, 'w', zipfile.ZIP_DEFLATED)
        try:
            for f in os.listdir(source):
                if ".log" in f:
                    myzip.write(source + f)
        finally:
            myzip.close()

        return os.getcwd() + '/' + fileName

    def evolve(self, evolutions_to_run, evolution_count=0):
        """
        Mate the population, mutate, and compare fitness.
        Sort by fitness and save the evolution to a log file.
        Args:
            evolutions_to_run (int)
            evolution_count (int): if resuming a run, this is the evolution
                    number to continue from.
        """
        for i in range(evolutions_to_run):
            self.population = self.mating.crossover(self.population)
            self.population = mutate.mutate(self.population)
            self._compute_fitness()
            self._sort()
            self._save_all_chromosomes(evolution_count)
            self._display_population(evolution_count)
            evolution_count += 1

    # ---------------- #
    #    "Private"     #
    # ---------------- #

    def _compute_fitness(self):
        """
        Compute the fitness of all chromosomes in the population.
        Updates the fitness value of all chromosomes.
        Chromosome fitness calculation is done in separate processes.

        """
        sizes = (config["TrainingSizeHMM"], config["TestingSizeHMM"])
        self.celex.load_sets(sizes[0], sizes[1])

        pool = ActivePool()
        s = multiprocessing.Semaphore(config["MaxThreadCount"])
        results_queue = multiprocessing.Queue()
        jobs = [
            multiprocessing.Process(target=self._compute_single_fitness,
                                    name=str(i),
                                    args=(i, s, pool, results_queue))
            for i in range(len(self.population))
        ]
        for j in jobs:
            j.start()

        for j in jobs:
            j.join()

        for result in [results_queue.get() for j in jobs]:
            self.population[result[0]].set_fitness(result[1])

    def _compute_single_fitness(self, i, s, pool, results_queue):
        """
        Calculates and puts updated fitness on the results_queue.
        Args:
            i (int): process and population index
            s (multiprocessing.Semaphore)
            pool (ActivePool): manager of the pool and locks
            results_queue (multiprocessing.Queue): communication
                        between processes.
        """
        process_name = multiprocessing.current_process().name
        with s:
            pool.make_active(process_name)
            genes = self.population[i].get_genes()
            hmmbo = self.celex.train_hmm(genes)
            fitness = self.celex.test_hmm(hmmbo)
            hmmbo = None
            results_queue.put((i, fitness))
            pool.make_inactive(process_name)

    def _sort(self):
        """
        Sort self.population by fitness (syllabification accuracy)
        Ordering: highest (self.population[0]) -> lowest
        """
        self.population.sort()
        self.population.reverse()

    def _save_all_chromosomes(self, cur_evolution):
        """
        Outputs all chromosomes to a log file.
        Args:
            cur_evolution (int): which evolution for naming the log file.
        """
        location = config["LogFileLocation"]
        name = "evo" + str(cur_evolution) + ".log"
        file_name = location + name
        map(lambda x: self._save_chromosome_at_index(x, file_name),
            range(len(self.population)))

    def _save_chromosome_at_index(self, index, file_name):
        """
        Outputs a single chromosome to a log file.
        Truncates the file if inserting from index 0.
        Log file structure:
            Each 2-line group is a chromosome.
            Categories are tab-delimited.
            Genes have no spaces between them.
        Args:
            index (int): index of the chromosome in the population to be saved.
            file_name (string): nave of evolution log to save chromosome to.
        """
        how_to_open = 'w' if index == 0 else 'a'
        with open(file_name, how_to_open) as out_file:
            for category in self.population[index].get_genes():
                out_file.write(''.join(category) + '\t')
            out_file.write(
                '\n{}\n'.format(self.population[index].get_fitness())
            )

    def _display_population(self, evolution_number=0):
        """ Displays the population and the current evolution number. """
        print("Population after evolution #" + str(evolution_number))
        for i in range(len(self.population)):
            print("chrom{}\t{}".format(i, self.population[i].get_fitness()))
        print()
