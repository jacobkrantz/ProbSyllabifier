from utils import Utils
import sys

'''
fileName:       SyllabParser.py
Authors:        Max Dulin
Date Modified:  2/23/17

- Parses the SyllabDict.txt into a list of tuples.
- Necessary files:
    - ./HMMFiles/SyllabDict.txt

'''

class SyllabParser:

    def __init__(self):
        self.testInt = 0
        self.bigramLst = []
        self.initialList = []
        self.inFile = ""
    def bringInFile(self,inputFile):

        with open(inputFile) as f:
            for line in f:
                self.initialList.append(line)

        print self.initialList[1]
    def makeParseWord(self, index):
        boundary = False
        phoneLst = []
        line = self.initialList[index]

        #takes out the beginning word in the dictionary
        while(line[0] != ' '):
            line = line[1:]
        line = line[1:]
        for i in range(len(line)):
            if(self.phoneCheck(line,i)):
                print("test")


    def phoneCheck(self, line, index):
        if(line[index-1] != ' '):
            return True
        return False

def main():

    newParser = SyllabParser()
    newParser.bringInFile("./HMMFiles/SyllabDict.txt")
    newParser.makeParseWord(1)
    return 0

main()
