import os
import csv
import glob
import time
import shutil
import sys
from datetime import datetime

from surprise import SVD
from surprise import Dataset, Reader
from surprise import accuracy
from surprise.model_selection import train_test_split
from collections import defaultdict

"""
Print the result from predictions function 
"""
def get_items_recommendation(inputID, predictions, maxOutputItems=10):
    # map the predictions to each user.
    top_n = defaultdict(list)
    for userID, itemID, true_r, est, _ in predictions:
        top_n[userID].append((itemID, est))
    # sort the predictions for each user and related items(defult max is 10).
    for userID, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[userID] = user_ratings[:maxOutputItems]    
    # get the recommended items by userID(inputID)
    for userID, user_ratings in top_n.items():
        if inputID == userID:
            outputResult = ','.join(str(e[0]) for e in user_ratings)
    return outputResult

"""
Create the output file function 
"""
def output_RR(fileNameBase, inputID, outputRR):
    filePath = "output/" + fileNameBase + "out.csv"
    with open(filePath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([inputID, outputRR])

"""
Remove the file from input folder to processed folder function 
"""
def move_file(fileName):
    inputPath = "input/" + fileName
    processedPath = "processed/" + fileName
    shutil.move(inputPath, processedPath)

"""
Get recommendation function 
"""
def getRecommendation():
    try:
        # get the oldest "RR" file path and name
        filePath = sorted(glob.glob(r"input/RR*"), reverse=False)[0]
        fileName = os.path.basename(filePath)
        fileNameBase = os.path.splitext(fileName)[0]

        # start process the request
        timestamp = datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]
        print(timestamp + " Request processing start: " + fileName)

        # get the userID from "RR" file
        with open(filePath, 'r') as f:
            rows = csv.reader(f)
            row = next(rows)
            inputID = row[0]

    except FileNotFoundError:
        print("Request process file is not exist.") 
        
    try:
        file_path = os.path.expanduser('processed/currentModel.csv')
        reader = Reader(line_format='user item rating', sep=',')
        data = Dataset.load_from_file(file_path, reader=reader)
        trainset = data.build_full_trainset()
        # chose the algo
        algo = SVD()
        # train the model
        algo.fit(trainset)
        # get predict
        testset = trainset.build_anti_testset()
        predictions = algo.test(testset)
        
        try:
            outputRR = get_items_recommendation(inputID, predictions, maxOutputItems=10)

            # output result
            output_RR(fileNameBase, inputID, outputRR)
        
            # move file
            move_file(fileName)

            # end process the request
            timestamp = datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]
            print(timestamp + " Request processing end: " + fileName)

        except UnboundLocalError:
            print("It is not the recommendation for userID " + inputID + " ! Please add related user preference file then get request again.")
            # end process the request
            timestamp = datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]
            print(timestamp + " Request processing end: " + fileName)
            move_file(fileName)

    except FileNotFoundError:
        print("Current Model is not exist. Please put the UP file to input folder !") 
        sys.exit(0)