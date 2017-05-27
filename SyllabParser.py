import sys

'''
fileName:       SyllabParser.py
Authors:        Max Dulin, Jacob Krantz
Date Modified:  3/15/17

-Functions:
    makePhonemeLst

- Parses the SyllabDict.txt into a list of tuples.
- Default input file:
    - ./HMMFiles/SyllabDict.txt

'''

class SyllabParser:


    def __init__(self):

        self.fileName = "./HMMFiles/SyllabDict.txt"
        #spot on the line
        self.spot = 0
        #the amount of lines in the text file of syllbabifactions inputted
        self.countLines = 0
        #where the lines are stored in the beginning
        self.initialList = []
        #the list where the list of bigram lists per word is stroed
        self.bigramLst = []
        #the string line from the file inputted
        self.line = ''


    # Creates a list of phonemes. Phonemes consist of bigrams of the
    # form: [['d', 'aa', 0], ['aa', 'l', 1], ['l', 'er', 0]]
    # filename param defaults to ./HMMFiles./SyllabDict.txt
    def makePhonemeLst(self, fileName="./HMMFiles/SyllabDict.txt"):

        self.fileName = fileName
        self.__bringInFile()

        for i in range(self.countLines):
            self.__makeParseWord(i)

        bigs = self.bigramLst
        self.__init__()
        return bigs


    ## ------------------------------
    ##            PRIVATE
    ## ------------------------------

    ##brings in the contents of the file
    ##Puts them into initialList, a class variable
    def __bringInFile(self):

        with open(self.fileName) as f:
            for line in f:
                self.initialList.append(line)
                self.countLines+=1


    #Parses a word into bigrams and whether there was a boundary between them.
    #In the format (firstPhone,secondPhone,boundary)
    #if there is a boundary, the value is a 1. If there is no boundary the value is 0.
    def __makeParseWord(self, index):
        #List to hold each bigram in a word
        phoneLst = []
        line = self.initialList[index]

        #takes out the beginning word in the dictionary
        #while(line[0] != ' '):
            #line = line[1:]
        self.line = line[1:]

        #stores the first phone into oldPhone
        oldPhone = self.__findNextPhone()
        while(self.spot < len(line)):
            #get the phone
            phone = self.__findNextPhone()
            #knowing that the word has ended
            value = self.__boundaryFound(phone,oldPhone)

            #ends the while loop to end the function if true
            if(phone == '\0' and self.spot == 0):
                self.bigramLst.append(phoneLst)
                break
            else:
                phoneLst.append([oldPhone,phone,value])
                #self.bigramLst.append([oldPhone,phone,value])
            oldPhone = phone



    #takes in a line that has been cropped out
    #returns true if a boundary is found between the two phone
    #and false otherwise
    def __boundaryFound(self,phone,oldPhone):

        setString = '' #string
        for i in range (2,len(self.line)):
            if(self.line[self.spot-i] != oldPhone[0]):
                setString = self.line[self.spot-i]+setString
            else:
                break
        #checks to see if there is a left bracket inside of it.
        if('[' in setString):
            #if there's a boundary
            return 1;
        else:
            #if there's no boundary
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
