# ProbSyllabifier
Probabilistic syllabifier of English language using HMM.
Word sets generated using Brown Corpus with custom tokenization
 
---
###Tokenization

####Program Order:

*brownTokenizer.py*  
tokenizes a corpus  
*freqLst.py*  
generates a file containing the 1000 most frequent words given a tokenized corpus  
*randomWords.py*  
generates a random subset of words given a tokenized grouping of words  

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

---

