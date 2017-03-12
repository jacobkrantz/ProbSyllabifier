from freqLst import FrequentWords as FW
from NISTSyllab import NISTSyllab
from ProbSyllabifier import ProbSyllabifier
from HMM import HMM
import sys

'''
fileName:       run.py
Authors:        Jacob Krantz
Date Modified:  3/11/17

- main file to train and run the Probabilsitic Syllabifier
- Syllabifies a file using NIST
- trians HMM
- runs syllabifier
'''

class color:
    BOLD = '\033[1m'
    END = '\033[0m'


def runNIST():
    inFile = "./corpusFiles/freqWords.txt"
    outFile = "./HMMFiles/SyllabDict.txt"
    nistSyllab = NISTSyllab()

    print ("current input file: " + inFile)
    print ("current output file: " + outFile)

    user_in = raw_input("Press enter to continue, or 'c' to change: ")
    if(user_in == 'c'):
        inFile = raw_input("choose input file: ")
        outFIle = raw_input("choose output file: ")

    generateWords()

    try:
        nistSyllab.syllabifyFile(inFile,outFile)
    except IOError as err:
        print err

def generateWords():
    fw = FW()
    numWords = int(raw_input("Enter number of words to syllabify: "))
    numTestWords = int(raw_input("Enter number of words to test on: "))

    # pulling from entire corpus or editorials
    fwIn = "./corpusFiles/editorial_words.txt"
    fwOut = "./corpusFiles/freqWords.txt"
    testingOut = "./corpusFiles/testSet.txt"

    fw.generateMostFreq(fwIn, fwOut, numWords)
    fw.generateTesting(testingOut, numTestWords)



def trainHMM():
    hmm = HMM()

    hmm.buildMatrixA() # "./HMMFiles/MatrixA.txt"
    hmm.buildMatrixB() # "./HMMFiles/MatrixB.txt"
    hmm.makeViterbiFiles()
    print("Items in training set: " + str(hmm.getTrainingSize()))


def runS():
    ps = ProbSyllabifier()
    obs = " "

    while(obs != ''):

        obs = raw_input("Enter filename or phoneme: ")
        syl = ""
        if("." in obs):
            ps.syllabifyFile(obs)
        elif(obs != ''):
            syl = ps.syllabify(obs.lower())
            print("Syllabification: " + syl)

def help():
    print "Running the Syllabifier:"
    print "     To syllabify a phoneme, enter phones separated by a space."
    print "     To return to the main menu, hit enter with no input."
    print "     *File syllabification is currently under development."

def main():
    choice = ""

    print "----------------------------------------"
    print "Welcome to the Probabilistic Syllabifier"
    print "----------------------------------------"

    while(choice != 5):
        print("\n" + color.BOLD + "Main Menu" + color.END)
        print "Choose an option:"
        print "1. Build sets with NIST"
        print "2. Train the HMM"
        print "3. Run the Syllabifier"
        print "4. Help"
        choice = input("5. Quit\n")

        if(choice == 1):
            runNIST()
        elif(choice == 2):
            trainHMM()
        elif(choice == 3):
            runS()
        elif(choice == 4):
            help()




main()
