import csv
import glob
import shutil

# read the oldest file name
filePath = sorted(glob.glob(r"input/UP*"), reverse=False)[0]
fileName = os.path.basename(filePath)

timestamp = time.strftime("%H:%M:%S")
print(timestamp + " Model updating start: " + fileName)

# get the data from currentModel.csv, if it is not exist, the new one will be created
try:
    with open('processed/currentModel.csv', 'r') as f:
        reader = csv.reader(f)
        currentModelList = list(reader)
except FileNotFoundError:
    print("Current Model is not exist. Current Model created !") 
    open('processed/currentModel.csv', 'w+')
    with open('processed/currentModel.csv', 'r') as f:
        reader = csv.reader(f)
        currentModelList = list(reader)

# get the data from UP file        
with open(filePath, 'r') as f:
    reader = csv.reader(f) 
    upList = list(reader)
    

# combined 2 file
with open('processed/currentModel.csv', 'w', newline='') as rowFile:
    rowFileWriter = csv.writer(rowFile)
    combined = []  
    for cm_row in currentModelList:
        combined_row = []
        combined_row.extend(cm_row)  
        
        for up_row in upList:
            if combined_row[0] == up_row[0] and combined_row[1] == up_row[1]:
                combined_row[2] = up_row[2]   
        combined.append(combined_row)
    
    for up_row in upList:
        found = False
        for cm_row in currentModelList:
            if cm_row[0] == up_row[0] and cm_row[1] == up_row[1]:
                found = True
                break
        if found == False:
            combined.append(up_row)
            
    # sort the combined data        
    combined = sorted(combined, reverse=False)
    for cb_row in combined:
        rowFileWriter.writerow(cb_row)


# move the UP file to processed file 
inputPath = "input/" + fileName
processedPath = "processed/" + fileName
shutil.move(inputPath, processedPath)

timestamp = time.strftime("%H:%M:%S")
print(timestamp + " Model updating end: " + fileName)