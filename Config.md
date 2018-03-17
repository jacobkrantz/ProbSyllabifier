This is the documentation of the Config.json file that controls all of the parameters throughout the whole syllabifier.

## File Setups:
### Environment:
Where the syllabifer is being phyiscally ran at.  
`Local` standard environment settings.  
`AWS` email notifications sent upon evolution run completion.  
### CelexTranscriptionFile:
A category scheme that is done in Celex's DISC form, which contains a single category per line.
### NistTranscriptionFile:
A category scheme that is done with Arpabet.
### comparator:
What the syllabifier is comparing and getting the words broken down into a group of phones from:  
`CELEX` or `NIST`  
### NGramValue:
State and observation history for the Hidden Markov Model.  
`2`: bigram assumption, first order.  
`3`: trigram assumption, pseudo-second order.  
### logLevel:
Standard output log verbosity:  
`debug`: Shows all prints and testing outputs.  
`info`: Shows results and warnings.  
`warning`: Shows issues with what is going in the program, such as word's being skipped.  

### Model parameters:
use_start_tags: insert `<` as a start tag and `>` as an end tag to all words. `true` or `false`  
k_smoothing: Add a smoothing value to all HMM probabilities. Float greater than or equal to `0.0`  

### Database configuration files:
databaseContext: The database that is being used for the system.  
write_results_to_DB: Write to the database or not in the program. `true` or `false`  
default_alphabet: The phonetic alphabet in usage, which is in database. (Currently only using `DISC`)  
path: Where the database is stored at locally.  
protected_tables: A list of tables that cannot be wrote over.  
read_permissions: Whether the database can be read by the user.  
write_permissions: Whether the database can be written into by the user.  

## Accuracy Testing  
crossValidation: k-fold cross-validation used for testing publishable syllabification accuracy.  
	Kvalue: number of partitions to make in the validation set.  
	NValue: number of words to be included in the validation set.  

## Genetic Algorithm

MaxThreadCount: The maximum amount of instances allowed for the syllabifer at a time.  
InitialPopulationSize: The initial amount of categorization schemes(chromosomes) to start a optimization with.   
PopulationSize: The maintained size of the population of chromosomes.  
NumMatingPairs: The number of mating chromosomes per evolution.  
NumChomNotToMutate: The amount of chromosomes not affected by mutate.  
BaseMutationFactor: The base percentage of chromosomes mutated, which is changed by the deviation.  
DesiredDeviation: The wanted standard deviation for the percentage's of the chromosomes.  
NumChromsInDeviation: number of top chromosome fitness values to be included in the deviation calculation.  
NumEvolutions: The amount of generations to run the genetic algorithm for.  
NumCategories: The amount of categories in the phonetic categorization scheme.  
CategoryRestriction: Do categories have a minimum occupancy? True or False.  
CategoryRestrictionCount: If CategoryRestriction is on, what's the minimum amount per category allowed.
TrainingSizeHMM: The amount of words to train the HMM on.  
TestingSizeHMM: The amount of words to test the accuracy of the scheme on.  
GeneList: The list of phonetic characters in the language being used.  
LogFileLocation: The location to store the output of the genetic algorithm.  

## PhoneOptimize  

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
