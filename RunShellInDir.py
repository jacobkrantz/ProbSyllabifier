#include phon1ax.pcd
#include tsylb2
from subprocess import Popen, PIPE, STDOUT
import subprocess 
import shlex
#'./tsylb2 -n phon1ax.pcd'


def main():
    print("here")
    #could be subprocess.check_output(args, *, stdin = None, stderr = None, shell = False, universal_newlines = False)
    ''' 
    subprocess.call('./tsylb2 -n phon1ax.pcd', shell = True) 
    The lines above are the ones that work inside of the 
    directory within NIST
    
    #cannot open the phon1ax file in order to see syllabify
    p = Popen(["./tsylb2 -n phon1ax.pcd"] ,shell = True,stdin = PIPE, stdout = PIPE, stderr = PIPE)
    stdout_data = p.communicate(input = 'D IH')[0]
    print(stdout_data)
    '''
    #this opens the file and sets the Pipes
    p = subprocess.Popen("cd ~/Desktop/NIST/sylb/tsylb2-1.1/ && ./tsylb2 -n phon1ax.pcd", shell = True,stdin = PIPE,stdout = PIPE,stderr = PIPE, bufsize = 1) 

    data = p.communicate(input = "p r eh z ih d ah n t \n")[0]
    #data is the output of the machine
    print(data)
    stringData = str(data)
    cropData = stringData[342:458]
    print(cropData)
    '''
    f = open("data.txt",'w')
    f.write(str(data))
    f.close()
    '''
    
        
    #going to need to extract the data

main()
