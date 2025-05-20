#COLUMN 4: DESCRIPTION OF THE VULNERABILITY (IN-CONTEXT)
import pandas as pd
import os


#IMPORTING CSV FILE
chunkSize = 1000


folderPath = input('Enter Folder Name: ')


fileNum = 1
folderLength = 0
for filename in os.listdir(folderPath):
    file_length = 0
    for df in pd.read_csv(folderPath + '/' + filename, chunksize=chunkSize):
        dfLength = 0
        for index, row in df.iterrows():
            dfLength = dfLength + 1
        file_length = file_length + dfLength
            
    print(str(fileNum) + ') ' + filename + ' Length: ' + str(file_length))
    folderLength = folderLength + file_length

    fileNum = fileNum + 1

print(folderPath + 'Total Length: ' + str(folderLength))
            

