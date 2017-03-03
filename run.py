from NISTSyllab import NISTSyllab
from ProbSyllabifier import ProbSyllabifier
from HMM import HMM
import sys

'''
fileName:       run.py
Authors:        Jacob Krantz
Date Modified:  2/28/17

- main file to train and run the Probabilsitic Syllabifier
- Syllabifies a file using NIST
- trians HMM
- runs syllabifier
'''

class color:
    BOLD = '\033[1m'
    END = '\033[0m'


def runNIST():
    inFile = "./corpusFiles/freqEditWords.txt"
    outFile = "./HMMFiles/SyllabDict.txt"
    nistSyllab = NISTSyllab()

    print ("current input file: " + inFile)
    print ("current output file: " + outFile)

    user_in = raw_input("Press enter to continue, or 'c' to change: ")
    if(user_in == 'c'):
        inFile = raw_input("choose input file: ")
        outFIle = raw_input("choose output file: ")

    try:
        nistSyllab.syllabifyFile(inFile,outFile)
    except IOError as err:
        print err


def trainHMM():
    hmm = HMM()

    hmm.buildMatrixA() # "./HMMFiles/MatrixA.txt"
    hmm.buildMatrixB() # "./HMMFiles/MatrixB.txt"
    hmm.makeViterbiFiles()


def runS():
    ps = ProbSyllabifier()
    obs = raw_input("Enter filename or phoneme: ")
    syl = ""

    if("." in obs):
        ps.syllabifyFile(obs)
    else:
        syl = ps.syllabify(obs)
        print("Syllabification: " + syl)


def main():
    choice = ""

    print "----------------------------------------"
    print "Welcome to the Probabilistic Syllabifier"
    print "----------------------------------------"

    while(choice != 4):
        print("\n" + color.BOLD + "Main Menu" + color.END)
        print "Choose an option:"
        print "1. Syllabify with NIST"
        print "2. Train the HMM"
        print "3. Run the Syllabifier"
        choice = input("4. Quit\n")

        if(choice == 1):
            runNIST()
        elif(choice == 2):
            trainHMM()
        elif(choice == 3):
            runS()

main()
