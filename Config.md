This is the documentation of the Config.json file that controls all of the parameters throughout the whole syllabifier.

## File Setups:
### Environment:
Where the syllabifer is being phyiscally ran at.  
`Local` standard environment settings.  
`AWS` email notifications sent upon evolution run completion.  
### celex_transcription_file:
A category scheme that is done in Celex's DISC form, which contains a single category per line.
### nist_transcription_file:
A category scheme that is done with Arpabet.
### comparator:
What the syllabifier is comparing and getting the words broken down into a group of phones from:  
`CELEX` or `NIST`  
### hmm_order:
State and observation history for the Hidden Markov Model.  
`1`: bigram assumption, first order.  
`2`: second order, and so on.  
### log_level:
Standard output log verbosity:  
`debug`: Shows all prints and testing outputs.  
`info`: Shows results and warnings.  
`warning`: Shows issues with what is going in the program, such as word's being skipped.  

### Model parameters:
use_start_tags: insert `<` as a start tag and `>` as an end tag to all words. `true` or `false`  
k_smoothing: Add a smoothing value to all HMM probabilities. Float greater than or equal to `0.0`  

### Database configuration files:
database_context: The database that is being used for the system.  
write_results_to_db: Write to the database or not in the program. `true` or `false`  
language: Which language to use the syllabifier with. Currently supports `English`.  
default_alphabet: The phonetic alphabet in usage, which is in database. (Currently only using `DISC`)  
path: Where the database is stored at locally.  
protected_tables: A list of tables that cannot be wrote over.   

## Accuracy Testing  
cross_validation: k-fold cross-validation used for testing publishable syllabification accuracy.  
	k_value: number of partitions to make in the validation set.  
	n_value: number of words to be included in the validation set.  

## Genetic Algorithm

max_thread_count: The maximum amount of instances allowed for the syllabifer at a time.  
initial_population_size: The initial amount of categorization schemes(chromosomes) to start a optimization with.   
population_size: The maintained size of the population of chromosomes.  
num_mating_pairs: The number of mating chromosomes per evolution.  
num_chroms_not_to_mutate: The amount of chromosomes not affected by mutate.  
base_mutation_factor: The base percentage of chromosomes mutated, which is changed by the deviation.  
desired_deviation: The wanted standard deviation for the percentage's of the chromosomes.  
num_chroms_in_deviation: number of top chromosome fitness values to be included in the deviation calculation.  
num_evolutions: The amount of generations to run the genetic algorithm for.  
num_categories: The amount of categories in the phonetic categorization scheme.  
category_restriction: Do categories have a minimum occupancy? True or False.  
category_restriction_count: If category_restriction is on, what's the minimum amount per category allowed.
training_size_hmm: The amount of words to train the HMM on.  
testing_size_hmm: The amount of words to test the accuracy of the scheme on.  
gene_list: The list of phonetic characters in the language being used.  
log_file_location: The location to store the output of the genetic algorithm.  

## phone_optimize  

phone_list: The phone/s(1 or 2) that are going to be ran through the testing state.  
transcription_file: The categorization file that is being optimized.  
evo_frequency: Evolution frequency in which `PhoneOptimize` will automatically be called in `GeneticAlgorithm`.   
evo_at_least: Current evolution must be at east this value in order to run `PhoneOptimize`.  

## Email  

from_address: Sender address for end-of-run email notification.  
to_address: Recipients of end-of-run email notification.  
password:  
smtp_server:  
smtp_port:  		
