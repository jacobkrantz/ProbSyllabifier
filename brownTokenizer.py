# Tokenization process:
# -all words converted lowercase
# -rid of all digits and orthographic text except for hyphens and 
#   apostrophes. Contractions and hyphenated words are maintained
# -hand corrections to find patterns we want to keep/remove

from nltk.corpus import brown
import re
import sys


# only gathers editorial content with -e flag
def getWords():
    getEditorials = False

    if(len(sys.argv) == 2):
        if(sys.argv[1] == "-e"):
            getEditorials = True
        else:
            print("Unknown command")
    
    raw = brown.words()
    editorials = brown.words(categories='editorial')

    if(getEditorials):
        name = 'e'
        selection = editorials
        fileName = 'editorial_words.txt'
    else:
        name = 'r'
        selection = raw
        fileName = 'raw_words.txt'

    fileName = './corpusFiles/' + fileName
    mid = open(fileName,'w')
    for item in selection:
        mid.write(item)
        mid.write(' ')

    mid.close
    return fileName


# tokenizes each word within raw file
def tokenizeWords(fileName):
    Words = open(fileName).read()

    pat = "[^(a-zA-Z\\'\-\s)]|(-)(-)|(\()|(\))"
    patObj = re.compile(pat)

    strOut = patObj.sub("",Words)
    strOut = strOut.lower()

    return strOut


# converts tokenized grouping into a list
def makeLst(strg):
    wordLst   = []
    uniqueLst = []

    strg = strg.split()

    wordLst = list(strg)    # creates list of all tokenized words
    for i in wordLst:
        if (i == "''"):
            wordLst.remove(i)
        if (i == "-"):
            wordLst.remove(i)
        if (i == "'"):
            wordLst.remove(i)

    # creates unordered lst of unique words
    uniqueLst = list(set(strg))

    print("number of tokenized words in corpus:")
    print(len(wordLst))
    print("Number of unique words in corpus:")
    print(len(uniqueLst))

    return wordLst, uniqueLst


# writes list contents to a specified file
def printWords(wordLst,outFile):
    final = open(outFile,'w')
    for word in wordLst:
        final.write(word)
        final.write(' ')


def main():
    fileName = getWords()

    strg = tokenizeWords(fileName)

    wordLst, uniqueLst = makeLst(strg)

    printWords(wordLst,fileName)
    #printWords(uniqueLst,'unique_words.txt')

main()
