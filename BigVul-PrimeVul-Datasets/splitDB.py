from openai import OpenAI
import pandas as pd
import json
import tiktoken
import os

TOKEN_COST = 0.01 / 1000
EST_COMPLETION_TOKENS = 200
GPT_MODEL = 'gpt-4-turbo-2024-04-09'


num_rows = 0
total_prompt_tokens = 0


#IMPORTING CSV FILE
chunkSize = 1000
csvPath = 'bigvul/VulnFuncs.csv'

cweDict = {}


# ITERATING THROUGH EACH FILE CHANGE
i = 1
for df in pd.read_csv(csvPath, chunksize=chunkSize):
    for index, row in df.iterrows():
        cweID = row['CWE ID']
        row = row.to_frame().T

        if (type(cweID) == str):
            if (cweID in cweDict):
                # CWE Already in Dict
                print(str(i) + 'CWE Exists: ' + cweID)
                cweDict[cweID] = cweDict[cweID]._append(row)
            else:
                # Need to add CWE to dict
                print(str(i) + 'CWE Added to Dict: ' + cweID)
                cweDict[cweID] = row
                
        else:
            # No CWE ID
            print(str(i) + 'No CWE ID')
            if ('NoCWEID' in cweDict):
                cweDict['NoCWEID'] = cweDict['NoCWEID']._append(row) 
            else:
                cweDict['NoCWEID'] = row

        i = i + 1

# Printing CSVs
for cweid in cweDict:
    cweDict[cweid].to_csv('dbSplit6/' + cweid + '.csv')

        
        




