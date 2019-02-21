import os
import re
import sys
import time

from ModelUpdate import updateModel
from RequestProcess import getRecommendation

def main():
    print("\nProgram Start! \"Ctrl + C\" to leave!\n")
    dir = "input/"
    patternUU = re.compile("UP\d+.csv")
    patternRR = re.compile("RR\d+.csv")
    while 1:
        for filepath in os.listdir(dir):
            if patternUU.match(filepath):
                updateModel()
                
        for filepath in os.listdir(dir):
            if patternRR.match(filepath):
                getRecommendation()
                
        time.sleep(0.1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram End!")
        sys.exit(0)