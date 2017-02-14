## module for running the NIST Syllabifier
## assumes tsylb2 file exists in directory '~/NIST/tsylb2-1.1/'

from subprocess import Popen, PIPE, STDOUT
import subprocess 
import shlex
import re


class NIST:

    ## uses NIST to find syllabification of a word in arpabet
    ## ArpString must have no stress
    ## returns list of syllabifications
    def syllabify(self, ArpString):
        syllabs = []

        try:

            ArpString = ArpString.lower()
            data      = self.__runNIST(ArpString)
            syllabs   = self.__parseNISTData(data, ArpString)

        except:

            print("Arpabet String Input Error.")

        return syllabs



    ## ------------------------------
    ##            PRIVATE
    ## ------------------------------



    ## takes in a phonetic pronounciation and runs them through NIST
    ## returns the proper syllabification(s) in a list  
    def __runNIST(self,ArpString):
        sylbLst = []

        p = subprocess.Popen("cd ~/NIST/tsylb2-1.1/ && ./tsylb2 -n phon1ax.pcd", shell = True,stdin = PIPE,stdout = PIPE,stderr = PIPE, bufsize = 1) 

        data = p.communicate(input = ArpString + "\n")[0] # data = output
        
        return data


    ## takes in the raw output of NIST 
    ## parses for pronounciations and returns all in a list
    def __parseNISTData(self, data, ArpString):
        pattern   = '\/.*?\/'
        pattern2 = '[^0-9]'
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
            newString = ""
            for i in range(len(tmp)):
                if(tmp[i] !='0' and tmp[i] != '1' and tmp[i] != '2' and tmp[i] !="'"):
                    newString += tmp[i]   
            returnLst.append(newString)

        return returnLst

