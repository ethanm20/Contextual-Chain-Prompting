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


MAX_INPUT_CSV_LENGTH = 15

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

def api_call(C3_description, C5_description, func_before, metric_num):
    global client

    prompt = ""
    if (metric_num == 1):
        #Clarity
        prompt = f"Give two ratings between 0 and 5 (inclusive) on the Clarity (i.e. how clear and understandable it is) of both the 'Explanation of Vulnerability Description' (given below) and the 'Repair Description (given below). \n Please only return two numbers for the ratings (comma-separated) and do not return anything else. The first number should be the rating for 'Explanation of Vulnerability Description' and the second number should be the rating for the 'Repair Description'. \n Explanation of Vulnerability Description: {C3_description} \n Repair Description: {C5_description}"
    elif (metric_num == 2):
        #Relevance
        prompt = f"Give two ratings between 0 and 5 (inclusive) on the Relevance (i.e., how relevant the generated text is to the specific context of the code snippet) of both the 'Explanation of Vulnerability Description' (given below) and the 'Repair Description (given below). \n Please only return two numbers for the ratings (comma-separated) and do not return anything else. The first number should be the rating for 'Explanation of Vulnerability Description' and the second number should be the rating for the 'Repair Description'. \n Explanation of Vulnerability Description: {C3_description} \n Repair Description: {C5_description} \n Code Before Repair: {func_before}"

    elif (metric_num == 3):
        # Completeness
        prompt = f"Give two ratings between 0 and 5 (inclusive) on the Completeness (i.e., whether the text covers all relevant aspects of the vulnerability without leaving out important details) of both the 'Explanation of Vulnerability Description' (given below) and the 'Repair Description (given below). \n Please only return two numbers for the ratings (comma-separated) and do not return anything else. The first number should be the rating for 'Explanation of Vulnerability Description' and the second number should be the rating for the 'Repair Description'. \n Explanation of Vulnerability Description: {C3_description} \n Repair Description: {C5_description} \n Code Before Repair: {func_before}"

    elif (metric_num == 4):
        #Actionability
        prompt = f"Give two ratings between 0 and 5 (inclusive) on the Actionability (i.e., whether the text provides enough information to act on the vulnerability) of both the 'Explanation of Vulnerability Description' (given below) and the 'Repair Description (given below). \n Please only return two numbers for the ratings (comma-separated) and do not return anything else. The first number should be the rating for 'Explanation of Vulnerability Description' and the second number should be the rating for the 'Repair Description'. \n Explanation of Vulnerability Description: {C3_description} \n Repair Description: {C5_description}"


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
        #Clarity
        columnName = "G1_Clarity_C3_C5"
    elif (metric_num == 2):
        #Relevance
        columnName = "G2_Relevance_C3_C5"
    elif (metric_num == 3):
        #Completeness
        columnName = "G3_Completeness_C3_C5"
    elif (metric_num == 4):
        #Actionability
        columnName = "G4_Actionability_C3_C5"

    df.loc[index, columnName] = response

    return df


def iterate_csv(csvPath, filename):
    global messagesHistory
    
    # ITERATING THROUGH EACH FILE CHANGE
    for df in pd.read_csv(csvPath, chunksize=CHUNK_SIZE):
        for index, row in df.iterrows():
            for metric_num in range(1, 5):
                response = api_call(row['C3_Explanation_of_Vulnerability_In_Context'], row['C5_Explanation_Vulnerability_Fixed_In_Context'], row['primevul_func_before_fix'], metric_num)
                df = append_columns_to_df(df, response, metric_num, index)  

        export_csv(df, filename)

if __name__ == '__main__':
    folderPath = INPUT_CSV_FOLDER

    for filename in os.listdir(folderPath ):
        if (filename not in os.listdir(OUTPUT_CSV_PATH)) and (filename != "NoCWEID.csv"):
            #CSV File
            #filename = input("Enter Filename: ")
            filePath = folderPath + '/' + filename
            
            print("CSV: " + filePath)
            iterate_csv(filePath, filename)

            

