from ModelUpdate import updateModel
from RequestProcess import getRecommendation

def main():
    print("program start!")

    # if not UP file, not do
    updateModel()

    # if not RR file, not do
    getRecommendation()
    

if __name__ == "__main__":
    main()