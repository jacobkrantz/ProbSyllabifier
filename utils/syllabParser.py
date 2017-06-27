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
        #spot on the line
        self.spot = 0
        #where the lines are stored in the beginning
        self.initialList = []
        #the list where the list of bigram lists per word is stroed
        self.bigramLst = []
        #the string line from the file inputted
        self.line = ''


    # Creates a list of phonemes. Phonemes consist of bigrams of the
    # form: [['d', 'aa', 0], ['aa', 'l', 1], ['l', 'er', 0]]
    # filename param defaults to ./HMMFiles./SyllabDict.txt
    def makeNistPhonemeLst(self, fileName="./HMMFiles/SyllabDict.txt"):
        with open(fileName) as f:
            for line in f:
                self.initialList.append(line)

        for i in range(len(self.initialList)):
            self.__makeParseWord(i)

        bigs = self.bigramLst
        self.__init__()
        return bigs

    # Creates a list of phonemes. Phonemes consist of bigrams of the
    # form: [['d', 'aa', 0], ['aa', 'l', 1], ['l', 'er', 0]]
    def parseCelexTrainingSet(self, trainingSet):
        trainingSet = map(lambda x: x.encode('utf-8'), trainingSet)
        return map(lambda word: self._parseCelexWord(word), trainingSet)

    ## ------------------------------
    ##            PRIVATE
    ## ------------------------------

    # assumtions: a boundary cannot start or end a word
    #   a boundary cannot follow a boundary
    def _parseCelexWord(self, word):
        word = word.split()[0]
        phonemeBigramList = []
        wasBoundary = False
        if word[0] == '-' or word[-1] == '-':
            raise SyntaxError("CELEX word '" + word + "' broke syllab rule.")
        for i in range(1,len(word)):
            if not wasBoundary:
                if word[i] == '-':
                    wasBoundary = True
                    phonemeBigramList.append([word[i-1],word[i+1],1])
                else:
                    phonemeBigramList.append([word[i-1],word[i],0])
                    wasBoundary = False
            else:
                wasBoundary = False
                if word[i] == '-':
                    raise SyntaxError("CELEX word '" + word + "' broke syllab rule.")
        return phonemeBigramList

    #Parses a word into bigrams and whether there was a boundary between them.
    #In the format (firstPhone,secondPhone,boundary)
    #if there is a boundary, the value is a 1. If there is no boundary the value is 0.
    def __makeParseWord(self, index):
        #List to hold each bigram in a word
        phoneLst = []
        line = self.initialList[index]

        #takes out the beginning word in the dictionary
        while(line[0] != ' '):
            line = line[1:]
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
            oldPhone = phone

    #takes in a line that has been cropped out
    #returns 1 if a boundary is found between the two phone
    #and 0 otherwise
    def __boundaryFound(self,phone,oldPhone):
        setString = ''
        for i in range (2,len(self.line)):
            if(self.line[self.spot-i] != oldPhone[0]):
                setString = self.line[self.spot-i]+setString
            else:
                break
        #checks to see if there is a left bracket inside of it.
        return 1 if '[' in setString else 0

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

        self.spot = 0
        return '\0' # end the loop in makeParseWord
