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
        #spot on the line
        self.spot = 0
        self.countLines = 0
        self.initialList = []
        self.bigramLst = []
        #the string line from the file inputted
        self.line = ''

    ##brings in the contents of the file
    ##Puts them into initialList, a class variable
    def __bringInFile(self,inputFile):

        with open(inputFile) as f:
            for line in f:
                self.initialList.append(line)
                self.countLines+=1

    #Creates the list of bigrams
    def makeBiagramList(self):

        self.__bringInFile("./HMMFiles/SyllabDict.txt")
        #self.__makeParseWord(1)
        for i in range(self.countLines):
            self.__makeParseWord(i)
    #Parses a word into bigrams and whether there was a boundary between them.
    #In the format (firstPhone,secondPhone,boundary)
    #if there is a boundary, the value is a 1. If there is no boundary the value is 0.
    def __makeParseWord(self, index):
        boundary = False
        phoneLst = []
        line = self.initialList[index]

        #takes out the beginning word in the dictionary
        while(line[0] != ' '):
            line = line[1:]
        self.line = line[1:]

        oldPhone = self.__findNextPhone()
        while(self.spot < len(line)):
            #get the phone
            phone = self.__findNextPhone()
            #knowing that the word has ended
            value = self.__boundaryFound(phone,oldPhone)

            if(phone == '\0' and self.spot == 0):
                break
            else:
                self.bigramLst.append([oldPhone,phone,value])
            oldPhone = phone



    #takes in a line that has been cropped out
    #returns true if a boundary is found between the two phone
    #and false otherwise
    def __boundaryFound(self,phone,oldPhone):
        setString = ''
        for i in range (2,len(self.line)):
            if(self.line[self.spot-i] != oldPhone[0]):
                setString = self.line[self.spot-i]+setString
            else:
                break
        if('[' in setString):
            return 1;
        else:
            return 0;


    #Takes in a line that has been cropped down
    #to find the next phone in the line and the number in the line.
    #returns the next phone in the line
    def __findNextPhone(self):
        phone = ""
        while(self.spot < len(self.line)):
            if(self.line[self.spot].isalpha()):
                phone += self.line[self.spot]
                if(self.line[self.spot+1].isalpha() == False):
                    self.spot+=1
                    return phone

            self.spot +=1

        #resets the value of spot to be used later.
        self.spot = 0
        #used to end the loop in makeParseWord
        return '\0'
