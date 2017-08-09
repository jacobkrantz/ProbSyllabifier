# ProbSyllabifier
Probabilistic syllabifier of English language using HMM.
Trains and tests against the CELEX dataset using DISC, a phonetic transcription similar to IPA.
Also trains and tests against NIST with Arpabet. Word sets for NIST are generated using the Brown Corpus with custom tokenization.

---
### Syllabification

#### Programs:

*NIST.py*  
Interfaces directly with the NIST Syllabifier.  
*SyllabInfo.py*  
Syllabifies an entire file of words and outputs resulting dictionary to a new file.  
*SyllabParser.py*  
Takes in the syllabDict.txt and outputs a list containing each word with a bigram that was a phone given the previous phone, along with whether there was a syllable boundary.  
*HMM.py*  
Used to build a Hidden Markov Model: trains A and B matrices.  
*utils.py*  
Tools currently associated with training and using HMM matrices.  
*run.py*  
This is the main file to run on:
Run this file to use the Syllabifier. Used for building the sets for the syllabifier, training the matrices, running the syllabifier and testing the syllabifier. T


### Tokenization

*brownTokenizer.py*  
tokenizes a corpus  
*freqLst.py*  
generates a file containing the 1000 most frequent words given a tokenized corpus  
*randomWords.py*  
follows FreqLst.py. generates a random subset of words given a tokenized grouping of words


#### HMM Files:
*MatrixA.txt*  
Holds the information from Matrix A  
*MatrixB.txt*  
Holds the information from Matrix B  
*syllabDict.txt*  
Houses the dictionary created in NISTSyllab.py.
*phoneCategoriesArp.txt*
Holds the categories for the Arpabet phones
*phoneCategoriesIPA.txt*
Holds the temporary categories for the IPA phones


#### Corpus Files:

*brown_words.txt*  
All tokenized words in the Brown corpus  
*editorial_words.txt*  
every untokenized word in the Editorials category of the Brown corpus  
*freqEditWords.txt*  
1000 most frequently used words in the Editorials category of the brown corpus  
*freq_words.txt*  
1000 most frequently used words in the brown corpus  
*randomWords.txt*  
random selection of 20 words from freq_words.txt  

#### Observations and Future Ideas
What if we built a support vector machine from this?
We could test if the word is so many phones then it should have 1,2,3... syllables in it.
some of the problems
