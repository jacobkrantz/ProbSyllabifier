# ProbSyllabifier
Probabilistic syllabifier of written language using a categorization-based first order Hidden Markov Model and the Genetic Algorithm.  
#### Goal  
Create an automatic, probabilistic syllabifier that can achieve the highest possible accuracy of syllabification when tested against words not previously seen.  
Words are represented as a sequence of sounds using the phonetic alphabet DISC, a digital version of IPA. Data source: Celex.  
Also trains and tests against NIST with Arpabet. Word sets for NIST are generated using the Brown Corpus with custom tokenization.  
#### Background  
This is a research project sponsored by Gonzaga University Department of Computer Science. Director of research is Dr. Paul De Palma. Presentation of this work was done at the Spokane Intercollegiate Research Conference (SIRC) in Spokane, WA, earning the Top Oral Presentation award. Also presented at Gonzaga's Research Showcase Poster Session. A paper detailing the work done in this project will be published in the companion proceedings at the [GECCO](http://gecco-2018.sigevo.org/) conference in Kyoto, Japan in July 2018.  

---
## Syllabification
### Getting Started
To work with this syllabification software in Celex, you need a have a copy of the dataset.  
`wordforms.db` contains part of the [Celex linguistics dataset](http://celex.mpi.nl/) refactored to integrate more easily into this python project.  
To work with the NIST source, you need to have [NIST syllabification Software](https://www.nist.gov/file/65961) installed.  
Other data sources are possible but not implemented, such as Miriam Webster.  
This project further has certain dependencies. For now, you must install these using the `requirements.txt` file. For `pypy`:   
`>>> pypy -m pip install -r requirements.txt`  
For `Python 2 or 3`:  
`>>> pip install -r requirements.txt`  
If these attempts fail, try running commands with `sudo`.

### Running the Syllabifier  
A typical run of the syllabifier will involve training the HMM, running the syllabifier, and obtaining an output accuracy. To run the syllabifier, call:  
`$ python run.py`  
At the main menu, enter option 1 to choose the training and testing size for the upcoming run.  
When the main menu returns, enter option 3 to run the syllabifier under the conditions previously set.  
This will run the syllabifier on randomized words and print an output of its accuracy.  
If `"write_results_to_db": true` in `config.json`, you can query the results directly in `wordforms.db` using SQL commands.  
Note: Do not run the NIST aspect of the project. It is the old system which has been completely replaced by the CELEX system.

### Parameters
All of the parameters and configurations are grabbed from the [config.json](./config.json) file. For example, the categorization scheme that is used for the syllabifier is specified under celex_transcription_file. If this is changed, then the scheme being ran will change with it. If someone would like to change aspects of the project do not try digging through the rest of the project intially; attempt to use the extensive amount of tools already written and change the parameters inside of the configuration files. To learn about parameters and configurations, take a look at [Config.md](./Config.md).

### Computing For Optimization  
Our Hidden Markov Model utilizes a dynamic, categorical tagset. To generate this tagset, the HMM needs to be given a scheme of how to convert the observations (DISC sounds) into their corresponding category. To do this autonomously, we start with random categories. Using a Genetic Algorithm, we are able to compute the optimal categorization (given enough time). To start optimizing from the beginning, run:  
`$ python optimize.py `  
If you wish to continue optimizing a previous run, use the command below but replace i with the evolution number to continue from. This evolution must have a log file in the `GeneticAlgorithm/EvolutionLogs/` folder. However, be sure to store the evolutions in another location for overwriting purposes.  
`$ python optimize.py  i `

If you love the scheme that you've been using but from some of the evaluation tools below that one or two phones is acting up, then `PhoneOptimization.py` is a fantastic tool to use. This tool will take the scheme and given phones you would like to optimize. Then run through every different permutation of the one or two phones being in the other categories. It will then output a percentage of each of the schemes. If a scheme (currently just using the .log format for the genetic evolution but this will have another categorization file type supported soon), has a phone or two not having the percentage that you would like, then run this file. To choose the file you'd like to run this on, go to `config.json`-> `phone_optimize`, then change `transcription_file` to the file you would like to run. It's currently looking for files inside of the `GeneticAlgorithm/Evolution` folder. So, put your file inside of there to run it. Finally, to actually run this go to option 4 of the run.py file.

### Evaluation
Inside of the utils folder there are two tools known as `graphingResults.py` and `evaluation.py`. The graphing results file is configured to show all of the missed phones and bigrams in a multitude of ways. The evaluation file has ways of understanding the data in a significant amount of ways. From understanding the most common phone, to grasping the most commonly missed backend of a bigram; there are quite a few tools set up in there. However, BE POSITIVE that the `workingresults` is turned to true in the configuration file, in order to actually check the results you're looking at. These will have a GUI shortly to make it runable with having to change any of the main function.
Note: `The workingresults` will break the syllabifier(by locking the celex database) if it's attempted to be ran in the `GeneticAlgorithm` or `PhoneOptimize` parts of the project. The database doesn't support writing to the database concurrently.  

## Celex Code Example
#### Process for measuring syllabification accuracy  
`Celex.py` is the interface for ProbSyllabifier working with Celex.  
Both `run.py` and `optimize.py` utilize this interface.
Working with it directly can be done as follows:
```python
from celex import Celex

c = Celex()
c.load_sets(10000, 1500) # training_size, testing_size

# train the Hidden Markov Model using the Simple-HOHMM library.
# pass in a transcriptionScheme that contains all phone categories (see test/test_celex.py)
# or default to specification in config.json.
ps_model = c.train_hmm()

# accuracy is the percentage of whole words syllabified correctly.
# test_results is a detailed look at the test run: list<tuple(generated_result, celex_result, isSame)>
# Pass in the trained model to test the syllabifier.
accuracy, test_results = c.test_hmm(ps_model)
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
`test_syllab_parser.py` ensures the observation and hidden state sequences are correctly synthesized from the word inputs.  

## Contributors
Suggestions, issues, and pull requests are welcomed!  
See [Getting Started](#getting-started)  
Further contact: `jkrantz@zagmail.gonzaga.edu`  
See current [Contributors](/graphs/contributors)


## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) for details  
