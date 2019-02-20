import os
import re
from ModelUpdate import updateModel
from RequestProcess import getRecommendation

def main():
    dir = "input/"
    patternUU = re.compile("UP\d+.csv")
    patternRR = re.compile("RR\d+.csv")
    while (True):
        for filepath in os.listdir(dir):
            if patternUU.match(filepath):
                updateModel()
                break
            if patternRR.match(filepath):
                getRecommendation()
                break

if __name__ == "__main__":
    main()