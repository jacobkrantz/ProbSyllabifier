from celex import CELEX
from nist import NIST
import sys

'''
fileName:       run.py
Authors:        Jacob Krantz, Max Dulin
Date Modified:  3/14/17

- main file to run entire program
- Syllabifies a file using NIST
- capable of running full suite of tools with NIST
- CELEX soon to be operational
'''
class color:
    YELLOW = '\033[93m'
    BOLD = '\033[1m'
    END = '\033[0m'

# this currently doesn't work
# runs the probabilistic syllabifier for either a phoneme or file.
def runS(NIST, CELEX, comparator):
    obs = " "

    while(obs != ''):
        obs = raw_input("Enter filename or phoneme: ")
        syl = ""
        if("." in obs):
            #for some reason the output file wasn't here so I created
            #one to be used in order for the function to work
            if comparator == "NIST":
                NIST.syllabifyFile(obs,"HMMFiles/outfile.txt",comparator)
            else:
                CELEX.syllabifyFile(obs,"HMMFiles/outfile.txt",comparator)
        elif(obs != ''):
            if comparator == "NIST":
                syl = NIST.syllabify(obs.lower())
            else:
                syl = CELEX.syllabify(obs.lower())
            print("Syllabification: " + syl)

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
    nist = NIST()
    celex = CELEX()
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
            nist.trainHMM() if comparator == "NIST" else celex.trainHMM()

        elif(choice == 2):
            runS(nist, celex, comparator)

        elif(choice == 3):
            nist.testHMM() if comparator == "NIST" else celex.testHMM()

        elif(choice == 4):
            comparator = getComparator()

        elif(choice == 5):
            help()

main()
