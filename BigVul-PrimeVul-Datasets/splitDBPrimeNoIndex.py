from openai import OpenAI
import pandas as pd
import json
import tiktoken
import os
import duckdb
import math

TOKEN_COST = 0.01 / 1000
EST_COMPLETION_TOKENS = 200
GPT_MODEL = 'gpt-4-turbo-2024-04-09'


num_rows = 0
total_prompt_tokens = 0


#IMPORTING CSV FILE
chunkSize = 1000
csvPath = 'bigvul/MSR_data_cleaned.csv'

def make_cwe_dict(primeVulData):
    cweDict = {}

    df = pd.DataFrame.from_dict(primeVulData)
    print(df)

    # ITERATING THROUGH EACH FILE CHANGE
    i = 0
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

    return cweDict

# Iterating through the JSONL 
def get_primevul_data():
    primeVulData = []

    primevul_dfs = [ 
        duckdb.query('''
        SELECT *
        FROM read_json('dbPrimeVulJSONL/primevul_test_paired.jsonl', auto_detect=True, sample_size=1000000)                  
        ''').to_df(),
        duckdb.query('''
        SELECT *
        FROM read_json('dbPrimeVulJSONL/primevul_train_paired.jsonl', auto_detect=True, sample_size=1000000)                  
        ''').to_df(),
        duckdb.query('''
        SELECT *
        FROM read_json('dbPrimeVulJSONL/primevul_valid_paired.jsonl', auto_detect=True, sample_size=1000000)                  
        ''').to_df()
    ]
    prev_func = ""
    prev_commit_id = ""

    for df in primevul_dfs:
        for index, row in df.iterrows():
            if (int(index) % 2 == 0):
                # Even Index
                prev_func = row['func']
                prev_commit_id = row['commit_id']
            else:
                # Odd Index
                if ( math.isnan(row['big_vul_idx']) ): 
                    primeVulData.append({
                        'CWE ID': row['cwe'],
                        'project': row['project'],
                        'commit_id_before_fix': prev_commit_id,
                        'commit_id_after_fix': row['commit_id'],
                        'target': row['target'],
                        'primevul_idx': row['idx'],
                        'hash': row['hash'],
                        'size': row['size'],
                        'message': row['message'],
                        'dataset': row['dataset'],
                        'primevul_func_before_fix': prev_func,
                        'primevul_func_after_fix': row['func'],
                        'big_vul_idx': row['big_vul_idx']
                    })

    return primeVulData

primeVul = get_primevul_data()
print('DONE PRIMEVUL')
print(str(len(primeVul)))
cweDict = make_cwe_dict(primeVul)





# Printing CSVs
for cweid in cweDict:
    cweDict[cweid].to_csv('dbSplitPrimeNoIndex4/' + cweid + '.csv')

        
        




