from __future__ import print_function

import re
import sys

from nltk.corpus import brown

'''
Tokenization process:
    - all words converted lowercase
    - rid of all digits and orthographic text except for hyphens and
        apostrophes. Contractions and hyphenated words are maintained
    - hand corrections to find patterns we want to keep/remove
'''


# only gathers editorial content with -e flag
def get_words():
    get_editorials = False

    if len(sys.argv) == 2:
        if sys.argv[1] == "-e":
            get_editorials = True
        else:
            print("Unknown command")

    raw = brown.words()
    editorials = brown.words(categories='editorial')

    if get_editorials:
        name = 'e'
        selection = editorials
        file_name = 'editorial_words.txt'
    else:
        name = 'r'
        selection = raw
        file_name = 'brown_words.txt'

    file_name = './corpusFiles/' + file_name
    with open(file_name, 'w') as mid:
        for item in selection:
            mid.write(item)
            mid.write(' ')

    return file_name


# tokenizes each word within raw file
def tokenize_words(file_name):
    words = open(file_name).read()

    pat = "[^(a-zA-Z\\'\-\s)]|(-)(-)|(\()|(\))"
    pat_obj = re.compile(pat)

    str_out = pat_obj.sub("", words)
    str_out = str_out.lower()

    return str_out


# converts tokenized grouping into a list
def make_lst(strg):
    word_lst = []
    unique_lst = []

    strg = strg.split()

    word_lst = list(strg)  # creates list of all tokenized words
    for i in word_lst:
        if i in ("''", "-", "'"):
            word_lst.remove(i)

    # creates unordered lst of unique words
    unique_lst = list(set(strg))

    print("number of tokenized words in corpus:")
    print(len(word_lst))
    print("Number of unique words in corpus:")
    print(len(unique_lst))

    return word_lst, unique_lst


# writes list contents to a specified file
def print_words(word_lst, out_file):
    with open(out_file, 'w') as final:
        for word in word_lst:
            final.write(word)
            final.write(' ')


def main():
    file_name = get_words()

    strg = tokenize_words(file_name)

    word_lst, unique_lst = make_lst(strg)

    print_words(word_lst, file_name)
    # print_words(unique_lst,'unique_words.txt')


if __name__ == '__main__':
    main()
