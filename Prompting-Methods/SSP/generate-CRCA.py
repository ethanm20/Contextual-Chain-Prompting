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
INPUT_CSV_FOLDER = 'Output1/'

# The specific CWE ID we are going to run the model on
#cweID = "CWE-89"

# The folder the outputted CSV will be saved in (this folder must exist, if not manually make the folder before running this code)
OUTPUT_CSV_PATH = 'Evaluation-CRCA2/'

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

def api_call(C5_description, func_before, metric_num):
    global client

    prompt = ""
    if (metric_num == 1):
        #Clarity
        prompt = f"Give a rating between 0 and 5 (inclusive) on the Clarity of the Explanation and Repair Description (i.e., how clear and understandable the description is) \n Please simply return a single number as the rating and do not return anything else. \n Explanation and Repair Description: {C5_description}"
    elif (metric_num == 2):
        #Relevance
        prompt = f"Give a rating between 0 and 5 (inclusive) on the Relevance of the Explanation and Repair Description (i.e., how relevant the genrated text is to the specific context of the code snippet) \n Please simply return a single number as the rating and do not return anything else. \n Explanation and Repair Description: {C5_description} \n Code Before Repair: {func_before}"
    elif (metric_num == 3):
        #Completeness
        prompt = f"Give a rating between 0 and 5 (inclusive) on the Completeness of the Explanation and Repair Description (i.e., whether the text covers all relevant aspects of the vulnerability without leaving out important details) \n Please simply return a single number as the rating and do not return anything else. \n Explanation and Repair Description: {C5_description} \n Code Before Repair: {func_before}"
    elif (metric_num == 4):
        #Actionability
        prompt = f"Give a rating between 0 and 5 (inclusive) on the Actionability of the Explanation and Repair Description (i.e., whether the text provides enough information to act on the vulnerability) \n Please simply return a single number as the rating and do not return anything else. \n Explanation and Repair Description: {C5_description} "

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

def append_columns_to_df(df, response, metric_num, index):
    columnName = ""
    if (metric_num == 1):
        #Clarity (C5)
        columnName = "F1_Clarity_C5"
    elif (metric_num == 2):
        #Relevance (C5)
        columnName = "F2_Relevance_C5"
    elif (metric_num == 3):
        #Completeness (C5)
        columnName = "F3_Completeness_C5"
    elif (metric_num == 4):
        #Actionability (C5)
        columnName = "F4_Actionability_C5"

    df.loc[index, columnName] = response

    return df

def check_index_not_in_existing_csv(index, filename):
    #OutputBulk
    try:
        #The Existing CSVs
        df = pd.read_csv(OUTPUT_CSV_PATH + filename)
        existing_max_index = len(df) - 1

        if (index > existing_max_index):
            return True
        
        return False
    except:
        #CSV was Not Made Yet
        return True
    
def copy_row_from_existing_csv(index, df):
    #Existing CSV
    df_existing = pd.read_csv(OUTPUT_CSV_PATH + filename)
    existing_row = df_existing.loc[index]

    #df = df.append(existing_row, ignore_index = True)
    df = pd.concat([df, existing_row], ignore_index = True)

    return df



def iterate_csv(csvPath, filename):
    global messagesHistory
    
    # ITERATING THROUGH EACH FILE CHANGE
    for df in pd.read_csv(csvPath, chunksize=CHUNK_SIZE):
        for index, row in df.iterrows():
            if (check_index_not_in_existing_csv(index, filename)):
                #Index is at the end of CSV
                for metric_num in range(1, 5):
                    response = api_call(row['primevul_func_before_fix'], row['primevul_func_after_fix'], metric_num)
                    df = append_columns_to_df(df, response, metric_num, index)  
            else:
                df = copy_row_from_existing_csv(index, df)

        export_csv(df, filename)

if __name__ == '__main__':
    folderPath = INPUT_CSV_FOLDER

    for filename in os.listdir(folderPath ):
        if filename not in os.listdir(OUTPUT_CSV_PATH):
            #CSV File
            #filename = input("Enter Filename: ")
            filePath = folderPath + '/' + filename
            
            print("CSV: " + filePath)
            iterate_csv(filePath, filename)

            

