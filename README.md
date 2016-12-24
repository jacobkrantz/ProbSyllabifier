# ProbSyllabifier
Probabilistic syllabifier of English language using HMM.
Word sets generated using Brown Corpus with custom tokenization
 
---
###Tokenization

####Program Order:

```
brownTokenizer.py
```
tokenizes a corpus

```
freqLst.py
```
generates a file containing the 1000 most frequent words given a tokenized corpus

```
randomWords.py
``` 
generates a random subset of words given a tokenized grouping of words

####Corpus Files:
```
raw_words.txt
```
every untokenized word in the Brown corpus

```
brown_words.txt
```
All tokenized words in the Brown corpus
```
unique_words.txt
```
All tokenized, unique words in the Brown corpus
```
freq_words.txt
```
Most frequently used words in the brown corpus

```
randomWords.txt
```
random selection of words from freq_words.txt

---

