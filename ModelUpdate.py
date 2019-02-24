import os
import csv
import glob
import time
import shutil
import pandas as pd
from datetime import datetime

"""
Update current model function 
"""
def updateModel():
    # read the oldest file name
    filePath = sorted(glob.glob(r"input/UP*"), reverse=False)[0]
    fileName = os.path.basename(filePath)

    # get the data from currentModel.csv, if it is not exist, the new one will be created
    try:
        with open('processed/currentModel.csv', 'r') as f:
            reader = csv.reader(f)
            currentModelList = list(reader)
    except FileNotFoundError:
        print("Current Model is not exist!") 
        print("Current Model created!") 
        open('processed/currentModel.csv', 'w+')
        with open('processed/currentModel.csv', 'r') as f:
            reader = csv.reader(f)
            currentModelList = list(reader)

    # get the upList from UP file and remove the null and repeat row
    df = pd.read_csv(filePath, names=['uid','iid','score']) 
    df.drop_duplicates(keep='first', inplace=True)  # dropping all repeat row 
    df = df.dropna()                                # remove all row which contain null
    df['uid'] =  df['uid'].astype('int')
    df['iid'] =  df['iid'].astype('int')
    df = df.astype(str)                            
    df['score'] = df['score'].str.replace('.0', '')
    upList = df.values.tolist()                     # change the data from dataframe to list

    # start updating model
    timestamp = datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]
    print(timestamp + " Model updating start: " + fileName) 

    # combined 2 file
    with open('processed/currentModel.csv', 'w', newline='') as rowFile:
        rowFileWriter = csv.writer(rowFile)
        combined = []  
        # if user change the score, update the score in current model
        for cm_row in currentModelList:
            combined_row = []
            combined_row.extend(cm_row)  
            for up_row in upList:
                if combined_row[0] == up_row[0] and combined_row[1] == up_row[1]:
                    combined_row[2] = up_row[2]
            combined.append(combined_row)
        # add the row to current if the row is not exist in current model
        for up_row in upList:
            found = False
            for cm_row in currentModelList:
                if cm_row[0] == up_row[0] and cm_row[1] == up_row[1]:
                    found = True
                    break
            if found == False:
                combined.append(up_row)
        # sort the combined data and write in current model
        combined = sorted(combined, key=lambda x: x[0], reverse=False)
        for cb_row in combined:
            rowFileWriter.writerow(cb_row)

    # move the UP file to processed file 
    inputPath = "input/" + fileName
    processedPath = "processed/" + fileName
    shutil.move(inputPath, processedPath)

    # end updating model
    timestamp = datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]
    print(timestamp + " Model updating end: " + fileName)