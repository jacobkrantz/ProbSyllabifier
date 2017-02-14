from NISTSyllab import NISTSyllab
from HMM import HMM

'''
fileName:       run.py
Authors:        Jacob Krantz
Date Modified:  2/14/17

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
    nistSyllab.syllabifyFile(inFile,outFile)


def trainHMM():
    hmm = HMM()
    outFileA = "./HMM/MatrixA.txt"
    outFileB = "./HMM/MatrixB.txt"

    print("current output files: " + outFileA + " " + outFileB)
    hmm.buildMatrixA(outFileA)
    hmm.buildMatrixB(outFileB)

def runS():
    print "not yet complete"
    return


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
