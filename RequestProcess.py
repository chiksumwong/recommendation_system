import os
import csv
import glob
import time
import shutil

from surprise import SVD
from surprise import Dataset, Reader
from surprise import accuracy
from surprise.model_selection import train_test_split
from collections import defaultdict

# print the result from predictions
def get_items_recommendation(inputID, predictions, maxOutputItems=10):
    # First map the predictions to each user.
    top_n = defaultdict(list)
    for userID, itemID, true_r, est, _ in predictions:
        top_n[userID].append((itemID, est))

    # Then sort the predictions for each user and retrieve the k highest ones.
    for userID, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[userID] = user_ratings[:maxOutputItems]
        
    # Print the recommended items for each user
    for userID, user_ratings in top_n.items():
        if inputID == userID:
            outputRR = ','.join(str(e[0]) for e in user_ratings)
    return outputRR

# create the output file
def output_RR(inputID, outputRR):
    timestamp = time.strftime("%Y%m%d%H%M%S")
    fileName = "output/RR" + timestamp + "out.csv"

    with open(fileName, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([inputID, outputRR])


# remove the file from input folder to processed folder
def move_file(fileName):
    inputPath = "input/" + fileName
    processedPath = "processed/" + fileName
    shutil.move(inputPath, processedPath)


# get recommendation
def getRecommendation():

    try:
        # get the oldest "RR" file path and name
        filePath = sorted(glob.glob(r"input/RR*"), reverse=False)[0]
        fileName = os.path.basename(filePath)

        # start process the request
        timestamp = time.strftime("%H:%M:%S")
        print(timestamp + " Request processing start: " + fileName)

        # get the userID from "RR" file
        with open(filePath, 'r') as f:
            rows = csv.reader(f)
            row = next(rows)
            inputID = row[0]

    except FileNotFoundError:
        print("RR file is not exist.") 

        
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
        outputRR = get_items_recommendation(inputID, predictions, maxOutputItems=10)
        
        # output result
        output_RR(inputID, outputRR)
        
        # move file
        move_file(fileName)
    except FileNotFoundError:
        print("Current Model is not exist. Please put the UP file to input folder !") 

    timestamp = time.strftime("%H:%M:%S")
    print(timestamp + " Request processing end: " + fileName)