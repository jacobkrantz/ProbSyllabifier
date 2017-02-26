# ProbSyllabifier
Probabilistic syllabifier of English language using HMM.
Word sets generated using Brown Corpus with custom tokenization

---
###Syllabification

####Programs:

*NIST.py*  
Interfaces directly with the NIST Syllabifier.  
*NISTSyllab.py*  
Syllabifies an entire file of words and outputs resulting dictionary to a new file.  
*SyllabParser.py*  
Takes in the syllabDict.txt and outputs a list containing each word with a bigram that was a phone given the previous phone, along with whether there was a syllable boundary.  
*HMM.py*  
Used to build a Hidden Markov Model: trains A and B matrices.  
*utils.py*  
Tools currently associated with training and using HMM matrices.  
*run.py*  
Run this file to use the Syllabifier. Used for running NIST, training HMM, and using the HMM.

####HMM Files:
*MatrixA.txt*  
Holds the information from Matrix A  
*MatrixB.txt*  
Holds the information from Matrix B  
*syllabDict.txt*  
Houses the dictionary created in NISTSyllab.py.  

---
###Tokenization

####Program Order:

*brownTokenizer.py*  
tokenizes a corpus  
*freqLst.py*  
generates a file containing the 1000 most frequent words given a tokenized corpus  
*randomWords.py*  
follows FreqLst.py. generates a random subset of words given a tokenized grouping of words  

####Corpus Files:

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


*Note: attempt0 stores our first attempt at doing this with the HMM's*
