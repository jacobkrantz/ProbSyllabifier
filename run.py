from SyllabInfo import SyllabInfo
from freqLst import FrequentWords as FW
from HMM import HMM
from ProbSyllabifier import ProbSyllabifier
from testing import CompareNIST
from testing import CompareCELEX
import sys

'''
fileName:       run.py
Authors:        Jacob Krantz
Date Modified:  3/14/17

- main file to train and run the Probabilsitic Syllabifier
- Syllabifies a file using NIST
- trians HMM
- runs syllabifier
'''

class color:
    YELLOW = '\033[93m'
    BOLD = '\033[1m'
    END = '\033[0m'


def runDatabase(lang):
    inFile = "./corpusFiles/brown_words.txt" #/editorial_words.txt
    outFile = "./HMMFiles/SyllabDict.txt"
    freqFile = "./corpusFiles/freqWords.txt"

    inTest = "./corpusFiles/testSet.txt"
    outTest = "./HMMFiles/NISTtest.txt"

    if(lang ==1):
        nistSyllab = SyllabInfo(lang)
    #will be for celex database at some point
    else:
        celexSyllab = SyllabInfo(lang)
    print ("current input file: " + inFile)
    print ("current output file: " + outFile)

    user_in = raw_input("Press enter to continue, or 'c' to change: ")
    if(user_in == 'c'):
        inFile = raw_input("choose input file: ")
        outFIle = raw_input("choose output file: ")

    generateWords(inFile, inTest)

    try:
        if(lang == 1):
            nistSyllab.syllabifyFile(freqFile,outFile)
            nistSyllab.syllabifyFile(inTest,outTest)
        else:
            celexSyllab.syllabifyFile(freqFile,outFile)
            celexSyllab.syllabifyFile(inTest, outTest)
    except IOError as err:
        print err


# builds word set files to be used in NIST syllabification
def generateWords(fileIn, testFileIn):
    fw = FW()
    numWords = int(raw_input("Enter number of words to syllabify: "))
    numTestWords = int(raw_input("Enter number of words to test on: "))

    # pulling from entire corpus or editorials
    fileIn = "./corpusFiles/brown_words.txt" #/editorial_words.txt
    fwOut = "./corpusFiles/freqWords.txt"

    fw.generateMostFreq(fileIn, fwOut, numWords)
    fw.generateTesting(fileIn, testFileIn, numTestWords) # testFileIn is outfile


# build A and B matrices. Makes files to be used in the Viterbi
# decoding algorithm.
def trainHMM(lang):
    hmm = HMM(lang)

    hmm.buildMatrixA() # "./HMMFiles/MatrixA.txt"
    hmm.buildMatrixB() # "./HMMFiles/MatrixB.txt"
    hmm.makeViterbiFiles()
    print("Items in training set: " + str(hmm.getTrainingSize()))

# this currently doesn't work
# runs the probabilistic syllabifier for either a phoneme or file.
def runS(lang):
    ps = ProbSyllabifier()
    obs = " "

    while(obs != ''):

        obs = raw_input("Enter filename or phoneme: ")

        syl = ""

        if("." in obs):
            #for some reason the output file wasn't here so I created
            #one to be used in order for the function to work
            ps.syllabifyFile(obs,"HMMFiles/outfile.txt",lang)
        elif(obs != ''):
            syl = ps.syllabify(obs.lower())
            print("Syllabification: " + syl)


# compares the results of ProbS to that of NIST
def testSyllabifier(lang):



    if(lang == 1):
        cNIST = CompareNIST()
        ps = ProbSyllabifier()
        testIN = "./corpusFiles/testSet.txt"
        testOUT = "./HMMFiles/probSyllabs.txt"
        ps.syllabifyFile(testIN, testOUT,lang)

        NISTname = "./HMMFiles/NISTtest.txt"
        probName = "./HMMFiles/probSyllabs.txt"
        cNIST.compare(NISTname, probName)

        viewDif = raw_input("view differences (y): ")
        if(viewDif == 'y'):
            cNIST.viewDifferences()
    else:
        cCelex = CompareCELEX()
        print "Run on Celex. Next version will have this feature"

def help():
    print "Running the Syllabifier:"
    print "     To syllabify a phoneme, enter phones separated by a space."
    print "     To return to the main menu, hit enter with no input."

#gets the type of syllabifaction that the user wants to do
def getState():
    state = 0
    while state != 1 and state != 2:
        print("\n" + color.BOLD + "Main Menu" + color.END)
        print "Choose an option:"
        print "1. Arpabet"
        print "2. IPA"
        state = input("")
    return state

#Ensures that IPA is not being mixed with arpabet and vice versa
def getCheck(state1,state2,state3,state4,curState,choice):
    return True
    #checks the train hmm option
    if(curState == state2 and choice == 2):
        if(curState == state1):
            return True
        else:
            print "Please enter the information in either Arpabet or IPA."
            return False

    #checks the run syllabifer option
    if(curState == state2 and curState == state1 and curState == state3 and choice == 3):
        return True

    #checks the test results option
    if(curState == state1 and curState == state2 and curState == state4 and choice == 4):
        return True

    print "Please enter the information in either Arpabet or IPA."
    return False

def main():
    choice = ""
    state1= state2= state3=state4 = 0
    print "----------------------------------------"
    print "Welcome to the Probabilistic Syllabifier"
    print "----------------------------------------"

    state = getState()
    while(choice != 7):
        if(state == 1):
            displayState = "Arpabet"
        else:
            displayState = "IPA"

        print("\n" + color.BOLD + "Main Menu"+ color.END)
        print("Mode: " +color.YELLOW + displayState+ color.END)
        print "Choose an option:"
        print "1. Build sets"
        print "2. Train the HMM"
        print "3. Run the Syllabifier"
        print "4. Test Results"
        print "5. Help"
        print "6. Switch Phonetic Languages"

        try:
            choice = input("7. Quit\n")
        except:
            choice = 8 # just loop again

        if(choice == 1):
            state1 = state
            runDatabase(state)

        elif(choice == 2):
            state2 = state
            if(getCheck(state1,state2,state3,state4,state,choice)):
                trainHMM(state)

        elif(choice == 3):
            state3 = state
            if(getCheck(state1,state2,state3,state4,state,choice)):
                runS(state)

        elif(choice == 4):
            state4 = state
            if(getCheck(state1,state2,state3,state4,state,choice)):
                testSyllabifier(state)


        elif(choice == 5):
            help()
        elif(choice == 6):
            state = getState()

main()
