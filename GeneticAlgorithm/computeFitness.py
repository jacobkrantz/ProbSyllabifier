import multiprocessing
import Queue
import time

from activePool import ActivePool
from celex import Celex
from config import GAConfig


class ComputeFitness:
    """ Computes the fitness of chromosomes in a population concurrently """

    def __init__(self):
        self.celex = Celex()

    def compute(self, population):
        """
        Compute the fitness of all chromosomes in the population.
        Updates the fitness value of all chromosomes.
        Chromosome fitness calculation is done in separate processes.
        """
        sizes = (GAConfig["training_size_hmm"], GAConfig["testing_size_hmm"])
        self.celex.load_sets(sizes[0], sizes[1])

        pool = ActivePool()
        s = multiprocessing.Semaphore(GAConfig["max_thread_count"])
        results_queue = multiprocessing.Queue(len(population) + 1)
        jobs = [
            multiprocessing.Process(
                target = self._compute_single_fitness,
                name = str(i),
                args = (
                    i,
                    s,
                    pool,
                    results_queue,
                    population[i].get_genes()
                )
            )
            for i in range(len(population))
        ]
        [j.start() for j in jobs]

        # pull results from queue before joining threads to avoid pipe deadlock.
        # https://tinyurl.com/yda2aa6k
        pulled_results = 0
        while(pulled_results < len(population)):
            try:
                while(not results_queue.empty()):
                    result = results_queue.get()
                    index = result[0]
                    fitness = result[1]
                    results_list = result[2]
                    population[index].set_fitness(fitness)
                    population[index].set_results(results_list)
                    pulled_results += 1

            except Queue.Empty:
                pass
            time.sleep(1)

        [j.join() for j in jobs]
        return population

    def _compute_single_fitness(self, i, s, pool, results_queue, genes):
        """
        Calculates and puts updated fitness on the results_queue.
        Args:
            i (int): process and population index
            s (multiprocessing.Semaphore)
            pool (ActivePool): manager of the pool and locks
            results_queue (multiprocessing.Queue): communication
                        between processes.
            genes (list<list<char>>): genes of a Chromosome
        """
        process_name = multiprocessing.current_process().name
        with s:
            pool.make_active(process_name)
            ps_model = self.celex.train_hmm(genes)
            fitness, all_results = self.celex.test_hmm(ps_model)
            ps_model = None
            results_queue.put((i, fitness, all_results))
            pool.make_inactive(process_name)
