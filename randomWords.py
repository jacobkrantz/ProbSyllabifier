'''
11/13/16
this file takes in a text file containing tokenized words.
it outputs a select number of random words to a new textfile named

'''
import random as rand
import sys

def getWords():
    wordLst = []

    if(len(sys.argv) == 2):
        fileName = sys.argv[1]
    else:
        fileName = 'freqEditWords.txt'

    wordFile = open(fileName,'r') 

    words = ""
    for line in wordFile:
        words = words + ' ' + line
    words = words.split()

    for i in words:
        wordLst.append(i)

    return wordLst

def getRandomLst(wordLst,numWords):
    randomLst = []
    count = 0

    while(count < numWords):
        randSpot = rand.randint(0,len(wordLst)-1)
        word = wordLst[randSpot]
        if(word not in randomLst):
            randomLst.append(word)
            count += 1 

    return randomLst

def printLst(w,outFile):
    txt = open(outFile,'w')
    for word in w:
        txt.write(word)
        txt.write(' ')

def main():
    #number of random words to be chosen
    numWords = 20

    wordLst = getWords()
    randomLst = getRandomLst(wordLst,numWords)
    printLst(randomLst,"random20.txt")

main()
