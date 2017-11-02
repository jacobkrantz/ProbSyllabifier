"""
11/13/16
this file takes in a text file containing tokenized words.
it outputs a select number of random words to a new textfile named

"""
import random as rand
import sys


def get_words():
    word_lst = []

    if len(sys.argv) == 2:
        file_name = sys.argv[1]
    else:
        file_name = '../corpusFiles/freqEditWords.txt'

    word_file = open(file_name, 'r')

    words = ""
    for line in word_file:
        words = words + ' ' + line
    words = words.split()

    for i in words:
        word_lst.append(i)

    return word_lst


def get_random_lst(word_lst, num_words):
    random_lst = []
    count = 0

    while count < num_words:
        rand_spot = rand.randint(0, len(word_lst) - 1)
        word = word_lst[rand_spot]
        if word not in random_lst:
            random_lst.append(word)
            count += 1

    return random_lst


def print_lst(w, out_file):
    with open(out_file, 'w') as txt:
        for word in w:
            txt.write(word)
            txt.write(' ')


def main():
    # number of random words to be chosen
    num_words = 20

    word_lst = get_words()
    random_lst = get_random_lst(word_lst, num_words)
    print_lst(random_lst, "../corpusFiles/random20.txt")


if __name__ == '__main__':
    main()
