import json
import textwrap
from GeneticAlgorithm import PhoneOptimize
from celex import Celex
from nist import NIST

'''
fileName:       run.py
Authors:        Jacob Krantz, Max Dulin
Date Modified:  9/17

- main file to run machine
- Syllabifies a file using NIST or Celex
'''


class Color:
    YELLOW = '\033[93m'
    BOLD = '\033[1m'
    END = '\033[0m'


# runs the probabilistic syllabifier for either a phoneme or file.
def run_s(nist, celex, comparator, hmmbo=None):
    obs = " "

    while obs != '':
        obs = raw_input("Enter filename or phoneme: ")
        syl = ""
        if "." in obs:
            if comparator == "NIST":
                nist.syllabify_file(obs, "HMMFiles/outfile.txt", comparator)
            else:
                celex.syllabify_file(obs, "HMMFiles/outfile.txt", comparator)
        elif obs != '':
            if comparator == "NIST":
                syl = nist.syllabify(obs.lower())
            else:
                syl = celex.syllabify(hmmbo, obs.lower())
            print("Syllabification: " + syl)

# gets the type of syllabifaction that the user wants to do
def get_comparator(config):
    comparator_id = 0
    while comparator_id not in [1, 2]:
        print("\n" + Color.BOLD + "Main Menu" + Color.END)
        print "Choose a Comparator:"
        print "1. NIST (with Arpabet)"
        print "2. CELEX (with DISC)"
        try:
            comparator_id = int(input())
        except:
            comparator_id = 0

    comparator = "NIST" if comparator_id == 1 else "CELEX"
    config["comparator"] = comparator
    with open('config.json', 'w') as outfile:
        json.dump(config, outfile, sort_keys=True, indent=4)
    return comparator


# Ensures correct comparator
def is_legal_selection(cur_comparator, trained_comparator, selection):
    if (selection in [1, 4, 5, 6]) or (cur_comparator == trained_comparator):
        return True
    print "HMM trained in other Comparator. Try retraining"


def load_configuration():
    with open('config.json') as json_data_file:
        data = json.load(json_data_file)
    return data


def main():
    nist = NIST()
    celex = Celex()
    config = load_configuration()
    print "----------------------------------------"
    print "Welcome to the Probabilistic Syllabifier"
    print "----------------------------------------"

    comparator = config["comparator"]
    trained_comparator = config["comparator"]
    choice = 0
    hmmbo = None
    while choice != 6:
        print("\n" + Color.BOLD + "Main Menu" + Color.END)
        print("Comparator: " + Color.YELLOW + comparator + Color.END)
        option_select = textwrap.dedent(
            """
            Choose an option:
            1. Train the HMM
            2. Run the Syllabifier
            3. Test Results
            4. Phone Optimization
            5. Cross Validate on CELEX
            6. Optimize smoothing on CELEX
            7. Quit\n"""
        )

        try:
            choice = int(input(option_select))
        except ValueError:
            choice = 0  # loop again
        finally:
            if not is_legal_selection(comparator, trained_comparator, choice):
                choice = 0

        if choice == 1:
            if comparator == "NIST":
                nist.train_hmm()
            else:
                hmmbo = celex.input_train_hmm()
            trained_comparator = comparator

        elif choice == 2:
            if(hmmbo == None):
                print("Train the system before testing the system. \nPlease use option 1.")
            else:
                run_s(nist, celex, comparator, hmmbo)

        elif choice == 3:
            if comparator == "NIST":
                nist.test_hmm()
            elif(hmmbo == None):
                print("Train the system before testing the system. \nPlease use option 1.")
            else:
                celex.test_hmm(hmmbo)

        elif choice == 4:
            optimize = PhoneOptimize()
            optimize.make_population()

        elif choice == 5:
            celex.cross_validate()

        elif choice == 6:
            celex.optimize_smoothing()


if __name__ == '__main__':
    main()
