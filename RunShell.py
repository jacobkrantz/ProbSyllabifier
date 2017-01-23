import subprocess
import shlex

def main():
    subprocess.call(shlex.split('./tsylb2 -n phon1ax.pcd'))

main()
