from __future__ import print_function

from datetime import datetime
import os
from random import randint
import shutil
import zipfile

from chromosome import Chromosome
from computeFitness import ComputeFitness
from config import GAConfig, settings
from mating import Mating
import mutate
from phoneOptimize import PhoneOptimize


class GeneticAlgorithm:
    """ Library for all Genetic Algorithm functionality """

    def __init__(self):
        # population holds a list of chromosomes
        self.population = []
        self.mating = Mating()
        self.computeFitness = ComputeFitness()
        self.phones = []
        self.phone_opt = PhoneOptimize()

    def display_parameters(self):
        """ Displays all GeneticAlgorithm parameters to the console. """
        ips = GAConfig["initial_population_size"]
        ps = GAConfig["population_size"]
        nomp = GAConfig["num_mating_pairs"]
        mf = GAConfig["base_mutation_factor"]
        ne = GAConfig["num_evolutions"]
        noc = GAConfig["num_categories"]
        nog = len(self.phones)

        display_string = """
    Genetic Algorithm Parameters
    ----------------------------
    Initial Population Size  %s
    Population Size          %s
    Number of Mating Pairs   %s
    Base Mutation Factor     %s
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
        for i in range(GAConfig["initial_population_size"]):
            new_chromosome = Chromosome(GAConfig["num_categories"])
            for gene in self.phones:
                random_category = randint(0, GAConfig["num_categories"] - 1)
                new_chromosome.insert_into_category(random_category, gene)
                #need to make sure that the chromosome has all categories fixed here.

            #adds the restrictions to the categories
            if(GAConfig["category_restriction"] == "True"):
                new_chromosome = self.space_chrom(new_chromosome)

            self.population.append(new_chromosome)

        self.population = self.computeFitness.compute(self.population)
        self._sort()

    def space_chrom(self,chrom):
        """
        Spaces the chromosome so that every category has at least one gene
        Args:
            chrom(chromosome): the chromosome to be spaced correctly.
        Returns:
            chrom(chromosome): the spaced out chromosome
        """

        #actual value/number of actegory
        for spot in range(GAConfig["num_categories"]):
            while(True):
                if(chrom.amount_of_genes(spot) < int(GAConfig["category_restriction_count"])):
                    go = True
                    #grabs a category that can be take from.
                    while(go):
                        random_cat= self.get_rand_cat()
                        if(chrom.can_move(random_cat,int(GAConfig["category_restriction_count"]))):
                            go = False
                    genes = chrom.get_genes()
                    remove_gene = genes[random_cat].pop() #just takes the back value
                    chrom.remove_gene(remove_gene)
                    chrom.insert_into_category(spot,remove_gene)
                else:
                    break


        return chrom

    def import_phones(self):
        """
        Pulls in the genes (phones) used for the particular language.
        Sets the class variables phones to have all of the phones
        """
        phones_file = GAConfig["gene_file"]
        with open(phones_file, 'r') as in_file:
            for line in in_file:
                line = line.replace("\n","")
                self.phones.append(line)

    def import_population(self, resume_from):
        """
        Pulls an existing population from an evolution log file.
        Args:
            resume_from (int): evolution number to import from.
        """
        location = GAConfig["log_file_location"]
        file_name = location + "evo" + str(resume_from) + ".log"

        with open(file_name, 'r') as in_file:
            for line in in_file:
                if len(line) < len(self.phones):
                    self.population[-1].set_fitness(float(line))
                    continue

                genes = line.split('\t')
                new_chromosome = Chromosome(GAConfig["num_categories"])
                for i in range(len(genes) - 1):
                    for gene in genes[i]:
                        new_chromosome.insert_into_category(i, gene)
                self.population.append(new_chromosome)

        self.display_population(resume_from)

    def archive_logs(self):
        """
        Move current logs to the archive.
        Each run is kept under unique folder.
        Creates directories when necessary.
        """
        source = GAConfig["log_file_location"]
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
        source = GAConfig["log_file_location"]
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

    def evolve(self, evolutions_to_run, evolution_count = 0):
        """
        Mate the population, mutate, and compare fitness.
        Sort by fitness and save the evolution to a log file.
        Args:
            evolutions_to_run (int)
            evolution_count (int): if resuming a run, this is the evolution
                    number to continue from.
        """


        for i in range(evolutions_to_run):
            self.population = self.mating.mate(self.population)
            self.population = mutate.mutate(self.population)

            self.population = self.computeFitness.compute(self.population)
            self._sort()
            self.population = self.optimize_best(
                self.population,
                evolution_count
            )
            self._sort()
            self._save_all_chromosomes(evolution_count)
            self.display_population(evolution_count)
            evolution_count += 1

    # ---------------- #
    #    "Private"     #
    # ---------------- #

    def optimize_best(self, population, evo_num):
        """
        Optimizes the best chromosome of the population.
        Technique is to move worst gene to its relative best category.
        Runs `PhoneOptimize` if proper evolution.
        Sets each chromosome's results to `None` to save memory.
        Args:
            population (list<Chromosome>)
            evo_num (int): the evolution number currently being ran.
        Returns:
            list<Chromosome>: population
        """
        evo_at_least = settings["phone_optimize"]["evo_at_least"]
        evo_frequency = settings["phone_optimize"]["evo_frequency"]
        if((evo_num >= evo_at_least) and (evo_num % evo_frequency == 0)):
            self.population = self.phone_opt.run_genetic(self.population,0)# call main function in PhoneOptimize once ready.
        map(lambda c: c.set_results(None), population)
        return population

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
        location = GAConfig["log_file_location"]
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

    def display_population(self, evolution_number=0):
        """ Displays the population and the current evolution number. """
        print("Population after evolution #" + str(evolution_number))
        for i in range(len(self.population)):
            print("chrom{}\t{}".format(i, self.population[i].get_fitness()))
        print()


    def get_rand_cat(self):
        """
        Returns a random number between 0 and the number of categories
        """
        return randint(0,GAConfig["num_categories"]-1)

if __name__ == "__main__":
    GA = GeneticAlgorithm()
