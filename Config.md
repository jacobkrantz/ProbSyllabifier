This is the documentation of the Config.json file that controls all of the parameters throughout the whole syllabifier.

## File Setups:
### Environment: 
Where the syllabifer is being phyiscally ran at. (Local or AWS)
### CelexTranscriptionFile: 
A category scheme that is done in Celex's DISC form, which contains a single category per line.
### NistTranscriptionFile: 
A category scheme that is done with Arpabet.
### comparator:
What the syllabifier is comparing and getting the words broken down into a group of phones from: 
CELEX or NIST
### NGramValue: 
The amount of layers to look back, which is 2 or 3 currently. 
### logLevel: 
  #### The amount of output to the user:  <br />
  info: Shows as little as possible, just the results.  <br />
  warnings: Shows issues with what is going in the program, such as word's being skipped.  <br />
  debug: Shows all prints and testing outputs.  <br />

### Database configuration files:
databaseContext: The database that is being used for the system.  <br />
write_results_to_DB: Write to the database or not in the program. (True or False) <br />
default_alphabet: The phonetic alphabet in usage, which is in database. (Currently only using DISC)<br />
path: Where the database is stored at locally. <br />
#### protected_tables: A list of tables that cannot be wrote over.<br />
read_permissions: Whether the database can be read by the user. <br />
write_permissions: Whether the database can be written into by the user. <br />

## Accuracy Testing

crossValidation: The most consistent method of testing the syllabifier for its true accuracy level. <br />
	Kvalue:       <br />
	NValue:       <br />

## Genetic Algorithm

MaxThreadCount: The maximum amount of instances allowed for the syllabifer at a time. <br />
InitialPopulationSize: The initial amount of categorization schemes(chromosomes) to start a optimization with. <br /> 
PopulationSize: The maintained size of the population of chromosomes. <br /> 
NumMatingPairs: The number of mating chromosomes per evolution. <br />
NumChomNotToMutate: The amount of chromosomes not affected by mutate. <br />
BaseMutationFactor: The base percentage of chromosomes mutated, which is changed by the deviation.  <br />
DesiredDeviation: The wanted standard deviation for the percentage's of the chromosomes.  <br />
NumChromsInDeviation:  <br />
NumEvolutions: The amount of generations to run the genetic algorithm for.  <br />
NumCategories: The amount of categories in the phonetic categorization scheme.  <br />
TrainingSizeHMM: The amount of words to train the HMM on.  <br />
TestingSizeHMM: The amount of words to test the accuracy of the scheme on.  <br />
GeneList: The list of phonetic characters in the language being used.  <br />
LogFileLocation: The location to store the output of the genetic algorithm.  <br />

## PhoneOptimize 
phone_list: The phone/s(1 or 2) that are going to be ran through the testing state.  <br />
transcription_file: the categorization file that is being optimized.  <br />

email:
from_address: what email address that the email is coming from.  <br />
to_address: what email addresses that the email is being sent to.  <br />

password:  <br />
smtp_server:  <br />
smtp_port:  <br />
	
		
