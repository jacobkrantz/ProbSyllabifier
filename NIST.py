## module for running the NIST Syllabifier
## assumes tsylb2 file exists in directory '~/NIST/tsylb2-1.1/'

from subprocess import Popen, PIPE, STDOUT
import subprocess 
import shlex
import re


## uses NIST to find syllabification of a word in arpabet
## ArpString must have no stress
## returns list of syllabifications
def syllabify(ArpString):
    syllabs = []

    try:

        ArpString = ArpString.lower()
        data      = __runNIST(ArpString)
        syllabs   = __parseNISTData(data, ArpString)

    except:

        print("Input Error.")

    return syllabs



## ------------------------------
##            PRIVATE
## ------------------------------



## takes in a phonetic pronounciation and runs them through NIST
## returns the proper syllabification(s) in a list  
def __runNIST(ArpString):
    sylbLst = []

    p = subprocess.Popen("cd ~/NIST/tsylb2-1.1/ && ./tsylb2 -n phon1ax.pcd", shell = True,stdin = PIPE,stdout = PIPE,stderr = PIPE, bufsize = 1) 

    data = p.communicate(input = ArpString + "\n")[0] # data = output
    
    return data


## takes in the raw output of NIST 
## parses for pronounciations and returns all in a list
def __parseNISTData(data, ArpString):
    pattern   = '\/.*?\/'
    error     = 'ERR'
    returnLst = []
    proLst    = []
    data = str(data)

    if(len(re.findall(error, data))):
        print("Error. No syllabification found for: " + ArpString)

    proLst = re.findall(pattern, data)
    proLst = proLst[1:]

    for item in proLst:

        tmp = item.strip('/# ')
        tmp = tmp.strip('#')
        returnLst.append(tmp)

    return returnLst
