from celex import Celex
from nist import NIST
import sys
import json

'''
fileName:       run.py
Authors:        Jacob Krantz, Max Dulin
Date Modified:  9/17

- main file to run machine
- Syllabifies a file using NIST or Celex
'''
class color:
    YELLOW = '\033[93m'
    BOLD = '\033[1m'
    END = '\033[0m'

# runs the probabilistic syllabifier for either a phoneme or file.
def runS(NIST, Celex, comparator):
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
                Celex.syllabifyFile(obs,"HMMFiles/outfile.txt",comparator)
        elif(obs != ''):
            if comparator == "NIST":
                syl = NIST.syllabify(obs.lower())
            else:
                syl = Celex.syllabify(obs.lower(), GUID)
            print("Syllabification: " + syl)

def help():
    print "Running the Syllabifier:"
    print "     To syllabify a phoneme, enter phones separated by a space."
    print "     To return to the main menu, hit enter with no input."

#gets the type of syllabifaction that the user wants to do
def getComparator(config):
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

    comparator = "NIST" if comparatorId == 1 else "CELEX"
    config["comparator"] = comparator
    with open('config.json','w') as outfile:
        json.dump(config, outfile, sort_keys = True, indent = 4)
    return comparator

#Ensures correct comparator
def isLegalSelection(curComparator, trainedComparator, selection):
    if (selection in [1,4,5,6]) or (curComparator == trainedComparator):
        return True
    print "HMM trained in other Comparator. Try retraining"

def loadConfiguration():
    with open('config.json') as json_data_file:
        data = json.load(json_data_file)
    return data

def main():
    nist = NIST()
    celex = Celex()
    config = loadConfiguration()
    print "----------------------------------------"
    print "Welcome to the Probabilistic Syllabifier"
    print "----------------------------------------"

    comparator = config["comparator"]
    trainedComparator = config["comparator"]
    hmmGUID = "" # used for CELEX file management
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
            if comparator == "NIST":
                nist.trainHMM()
            else:
                hmmGUID = celex.InputTrainHMM()
            trainedComparator = comparator

        elif(choice == 2):
            runS(nist, celex, comparator, hmmGUID)

        elif(choice == 3):
            if comparator == "NIST":
                nist.testHMM()
            else:
                celex.testHMM([], hmmGUID)

        elif(choice == 4):
            comparator = getComparator(config)

        elif(choice == 5):
            help()

main()
