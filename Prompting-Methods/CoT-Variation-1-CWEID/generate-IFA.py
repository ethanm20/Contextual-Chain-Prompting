from openai import OpenAI
import pandas as pd
import json
import tiktoken
import time
import os
import string

import anthropic

CONFIG_FILE = "config.json"

def get_api_key():
    api_key = ""
    with open(CONFIG_FILE) as f:
            data = json.load(f)
            api_key = data['API_Key']
    return api_key

def get_claude_api_key():
    api_key = ""
    with open(CONFIG_FILE) as f:
            data = json.load(f)
            api_key = data['Claude_API_Key']
    return api_key

client = OpenAI(api_key=get_api_key())  

# IMPORTANT!
# TODO: STATIC CONSTANTS THAT SHOULD BE CHECKED EACH TIME BEFORE RUNNING

#----------------------------------------------------------------
# START STATIC CONSTANTS
#INPUT_CSV_FOLDER = 'outputEvalCombined2/'

INPUT_CSV_FOLDER = 'outputBulk5/'

# The specific CWE ID we are going to run the model on
#cweID = "CWE-89"

# The folder the outputted CSV will be saved in (this folder must exist, if not manually make the folder before running this code)
#OUTPUT_CSV_PATH = 'outputEvalIFA/'

OUTPUT_CSV_PATH = 'outputEvalIFA5/'

# Token Costings
TOKEN_COST = 0.01 / 1000


# GPT Model
GPT_MODEL = "gpt-4o-mini"
CLAUDE_MODEL = "claude-3-5-sonnet-20241022"

PROMPTS_FILE = 'prompts.json'


# END STATIC CONSTANTS
#-----------------------------------------------------------


#Message History Global Variable
messagesHistory = []

#CSV FILE CHUNK SIZE
CHUNK_SIZE = 1000


#----------------------------------------------------------------

client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key = get_claude_api_key()
)

def api_call(C6_description):
    global client

    
    #Top 10 CWE IDs
    prompt = f"""
        Based on the below Explanation and Repair Description, what are the most likely vulnerabilities that were fixed? In your response please ensure that: 
            1. You return the 10 most likely CWE IDs. Do not return anything else.
            2. Each CWE ID is in form 'CWE-123'
            3. The returned CWE IDs are separated by commas
            4. The returned CWE IDs are ordered in descending order by likelihood
            5. If there are no found vulnerabilities please return Null
        
        Explanation and Repair Description:
        {C6_description}
   """
   
    message = None

    try:
        message = client.messages.create(
            model = CLAUDE_MODEL,
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
    except:
        print("ERROR, WAITING 60 SEC")
        time.sleep(130)
        message = client.messages.create(
            model = CLAUDE_MODEL,
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        time.sleep(80)

    return message.content[0].text

def export_csv(df, filename):
    df.to_csv(OUTPUT_CSV_PATH + filename)

def append_columns_to_df(df, response, cweID, c6_description, index):
    if cweID in c6_description:
        #DISQUALIFICATION
        df.loc[index, "T1_Top_10_CWE_IDs"] = "D, D"
        df.loc[index, 'T2_Correctly_Found_CWE'] = "D"
        df.loc[index, 'T3_IFA'] = "-1"
        return df



    df.loc[index, "T1_Top_10_CWE_IDs"] = response

    cweIDList = response.split(',')

    #TOP 10           
    if cweID in cweIDList:
        df.loc[index, 'T2_Correctly_Found_CWE'] = "Y"
    else:
        df.loc[index, 'T2_Correctly_Found_CWE'] = "N"
        df.loc[index, 'T3_IFA'] = "-1"
        return df

    #IFA
    for i in range(len(cweIDList)):
        if cweIDList[i] == cweID:
            df.loc[index, 'T3_IFA'] = i + 1
            return df

    return df




def iterate_csv(csvPath, filename):
    global messagesHistory
    
    # ITERATING THROUGH EACH FILE CHANGE
    for df in pd.read_csv(csvPath, chunksize=CHUNK_SIZE):
        for index, row in df.iterrows():
            response = api_call(row['C6_Explanation_Vulnerability_Fixed_Generic'])

            df = append_columns_to_df(df, response, row['CWE ID'], row['C6_Explanation_Vulnerability_Fixed_Generic'], index)  

        export_csv(df, filename)

if __name__ == '__main__':
    folderPath = INPUT_CSV_FOLDER

    for filename in os.listdir(folderPath ):
        if (filename not in os.listdir(OUTPUT_CSV_PATH)):
            #CSV File
            filePath = folderPath + '/' + filename
            
            print("CSV: " + filePath)
            iterate_csv(filePath, filename)

            

