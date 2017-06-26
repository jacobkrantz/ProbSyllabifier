from nist import SyllabInfo, CompareNIST
from utils import FrequentWords as FW
from probSyllabifier import HMM, ProbSyllabifier
import sys
from celex import CELEX

'''
fileName:       run.py
Authors:        Jacob Krantz, Max Dulin
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


def buildSets(comparator):
    inFile = "./corpusFiles/brown_words.txt" #/editorial_words.txt
    outFile = "./HMMFiles/SyllabDict.txt"
    freqFile = "./corpusFiles/freqWords.txt"

    inTest = "./corpusFiles/testSet.txt"
    outTest = "./HMMFiles/NISTtest.txt"

    if(comparator == "NIST"):
        nistSyllab = SyllabInfo(comparator)
    #will be for celex database at some point
    else:
        celexSyllab = SyllabInfo(comparator)
    print ("current input file: " + inFile)
    print ("current output file: " + outFile)

    user_in = raw_input("Press enter to continue, or 'c' to change: ")
    if(user_in == 'c'):
        inFile = raw_input("choose input file: ")
        outFIle = raw_input("choose output file: ")

    generateWords(inFile, inTest)

    try:
        if(comparator == "NIST"):
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
def trainHMM(comparator):
    lang = 1 if comparator == "NIST" else 2 # HACK get rid of lang
    hmm = HMM(lang)

    hmm.buildMatrixA() # "./HMMFiles/MatrixA.txt"
    hmm.buildMatrixB() # "./HMMFiles/MatrixB.txt"
    hmm.makeViterbiFiles()
    print("Items in training set: " + str(hmm.getTrainingSize()))

# this currently doesn't work
# runs the probabilistic syllabifier for either a phoneme or file.
def runS(comparator):
    ps = ProbSyllabifier()
    obs = " "

    while(obs != ''):

        obs = raw_input("Enter filename or phoneme: ")

        syl = ""

        if("." in obs):
            #for some reason the output file wasn't here so I created
            #one to be used in order for the function to work
            ps.syllabifyFile(obs,"HMMFiles/outfile.txt",comparator)
        elif(obs != ''):
            syl = ps.syllabify(obs.lower())
            print("Syllabification: " + syl)


# compares the results of ProbS to that of NIST
def testSyllabifier(comparator):

    if(comparator == "NIST"):
        cNIST = CompareNIST()
        ps = ProbSyllabifier()
        testIN = "./corpusFiles/testSet.txt"
        testOUT = "./HMMFiles/probSyllabs.txt"
        ps.syllabifyFile(testIN, testOUT,comparator)

        NISTname = "./HMMFiles/NISTtest.txt"
        probName = "./HMMFiles/probSyllabs.txt"
        cNIST.compare(NISTname, probName)

        viewDif = raw_input("view differences (y): ")
        if(viewDif == 'y'):
            cNIST.viewDifferences()
    else:
        print "Run on Celex. Next version will have this feature"

def help():
    print "Running the Syllabifier:"
    print "     To syllabify a phoneme, enter phones separated by a space."
    print "     To return to the main menu, hit enter with no input."

#gets the type of syllabifaction that the user wants to do
def getComparator():
    comparatorId = 0
    while comparatorId not in [1,2]:
        print("\n" + color.BOLD + "Main Menu" + color.END)
        print "Choose a Comparator:"
        print "1. NIST (with Arpabet)"
        print "2. CELEX (with DISC)"
        try:
            comparatorId = int(input())
        except:
            comparatorId = 0
    return "NIST" if comparatorId == 1 else "CELEX"

#Ensures that alphabets
def isLegalSelection(curComparator, trainedComparator, selection):
    if (selection in [1,4,5,6]) or (curComparator == trainedComparator):
        return True
    print "HMM trained in other Comparator. Try retraining"

def main():
    print "----------------------------------------"
    print "Welcome to the Probabilistic Syllabifier"
    print "----------------------------------------"

    comparator = getComparator()
    trainedComparator = "NIST" # assumes NIST (bad)
    choice = 0
    while(choice != 6):
        print("\n" + color.BOLD + "Main Menu"+ color.END)
        print("Comparator: " +color.YELLOW + comparator + color.END)
        optionSelect = """
Choose an option:
1. Train the HMM
2. Run the Syllabifier
3. Test Results
4. Switch Phonetic Languages
5. Help
6. Quit\n"""

        try:
            choice = int(input(optionSelect))
        except ValueError:
            choice = 0 # loop again
        finally:
            if not isLegalSelection(comparator,trainedComparator,choice):
                choice = 0

        if(choice == 1):
            buildSets(comparator)
            trainHMM(comparator)
            trainedComparator = comparator

        elif(choice == 2):
            runS(comparator)

        elif(choice == 3):
            testSyllabifier(comparator)

        elif(choice == 4):
            comparator = getComparator()

        elif(choice == 5):
            help()

# main()
c = CELEX()
