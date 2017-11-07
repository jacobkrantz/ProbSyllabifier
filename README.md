# ProbSyllabifier
Probabilistic syllabifier of written language using a first order Hidden Markov Model and the Genetic Algorithm.  
#### Goal  
Create an automatic, probabilistic syllabifier that can achieve the highest possible accuracy of syllabification when tested against words not previously seen.  
Words are represented as a sequence of sounds using the phonetic alphabet DISC, a digital version of IPA. Data source: Celex.  
Also trains and tests against NIST with Arpabet. Word sets for NIST are generated using the Brown Corpus with custom tokenization.  
#### Background  
This is a research project sponsored by Gonzaga University Department of Computer Science. Director of research is Dr. Paul De Palma. Presentation of this work was done at the Spokane Intercollegiate Research Conference (SIRC) in Spokane, WA, earning the Top Oral Presentation award. Also presented at Gonzaga's Research Showcase Poster Session.

---
## Syllabification
### Getting Started
To work with this syllabification software in Celex, you need a have a copy of the dataset.  
`wordforms.db` contains part of the Celex linguistics dataset refactored to integrate more easily into this python project.  
To work with the NIST source, you need to have [NIST syllabification Software](https://www.nist.gov/file/65961) installed.  
Other data sources are possible but not implemented, such as Miriam Webster.  
### Running the Syllabifier  
A typical run of the syllabifier will involve training the HMM, running the syllabifier, and obtaining an output accuracy. To run the syllabifier, call:  
`$ python run.py`  
At the main menu, enter option 1 to choose the training and testing size for the upcoming run.  
When the main menu returns, enter option 3 to run the syllabifier under the conditions previously set.  
This will run the syllabifier on randomized words and print an output of its accuracy.  
If `"write_results_to_DB": true` in `config.json`, you can query the results directly in `wordforms.db` using SQL commands.  
Note: Do not run the NIST aspect of the project. It is the old system which has been completely replaced by the CELEX system.

### Computing For Optimization  
Our Hidden Markov Model utilizes a dynamic, categorical tagset. To generate this tagset, the HMM needs to be given a scheme of how to convert the observations (DISC sounds) into their corresponding category. To do this autonomously, we start with random categories. Using a Genetic Algorithm, we are able to compute the optimal categorization (given enough time). To start optimizing from the beginning, run:  
`$ python optimize.py `  
If you wish to continue optimizing a previous run, use the command below but replace i with the evolution number to continue from. This evolution must have a log file in the `GeneticAlgorithm/EvolutionLogs/` folder. However, be sure to store the evolutions in another location for overwriting purposes.
`$ python optimize.py  i `  
## Celex Code Example
#### Process for measuring syllabification accuracy  
`Celex.py` is the interface for ProbSyllabifier working with Celex.  
Both `run.py` and `optimize.py` utilize this interface.
Working with it directly can be done as follows:
```python
c = Celex()
c.loadSets(10000, 1500) # testingSize, trainingSize

# train the A and B matrices of the Hidden Markov Model.
# pass in a transcriptionScheme that contains all phone categories (see test/test_celex.py)
# or default to specification in config.json.
HMMBO = c.trainHMM()

# Accuracy is the percentage a whole word was syllabified correctly out of all test words.
# Pass in the provided HMMBO trained data object to test the syllabifier.
Accuracy = c.testHMM(HMMBO)
```

## Tests
Tests should be ran before any pull requests.  
Unit tests are implemented in Python's `unittest` module and accessed through:  
```
$ cd ProbSyllabifier
$ python -m unittest discover -s test
```
#### Test Cases
`test_celex.py` ensures that Celex training and testing work with both a given transcription scheme and without.  
`test_mutate.py` ensures the mutation factor generation is accurate and mutates the proper chromosomes of the population.  
`test_sql_query_service.py` ensures the database queries all act as expected.  
`test_syllab_parser.py` ensures the tuples are extracted correctly from the CELEX training data.  

## Contributors
Suggestions, issues, and pull requests are welcomed!  
See [Getting Started](#getting-started)  
Further contact: `jkrantz@zagmail.gonzaga.edu`  
See current [Contributors](www.github.com/jacobkrantz/ProbSyllabifier/graphs/contributors)


## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) for details  
