#COLUMN 4: DESCRIPTION OF THE VULNERABILITY (IN-CONTEXT)
from openai import OpenAI
import pandas as pd
import json
import tiktoken
#from apikey import get_api_key
import time
import os
import string

CONFIG_FILE = "config.json"

def get_api_key():
    api_key = ""
    with open(CONFIG_FILE) as f:
            data = json.load(f)
            api_key = data['API_Key']
    return api_key

client = OpenAI(api_key=get_api_key())  

TOKEN_COST = 0.50 / 1000000
GPT_MODEL = 'gpt-3.5-turbo-0125'
GPT_MODEL1 = 'gpt-4o-mini'
COMPLETION_TOKENS = 100

TOKEN_COST_INPUT = 0.50 / 1000000
TOKEN_COST_OUTPUT = 1.50 / 1000000

messagesHistory = []

INPUT_CSV_PATH = '../../dbSplitPrime/'
OUTPUT_CSV_PATH = 'outputBulk5/'

PROMPTS_FILE = 'promptsBulk.json'


#IMPORTING CSV FILE
chunkSize = 1000

# GETTING the CWE to be searched for
#cweID = input('Enter CWE-ID: ')

cweID = ""

#csvPath = '../../dbSplitPrime/' + cweID + '.csv'

def calculate_tokens(prompt):
    encoding = tiktoken.encoding_for_model('gpt-3.5-turbo-0125')
    num_tokens = len(encoding.encode(prompt))
    return num_tokens

# HANDLING CALL TO API
def get_completion(prompt):
    messagesHistory.append({"role": "user", "content": prompt})
    num_tokens = calculate_tokens(str(messagesHistory))

    print('NUM TOKENS: ' + str(num_tokens))

    model = "gpt-4o-mini"


    try:
        response = client.chat.completions.create(model="gpt-4o-mini",
        messages=messagesHistory,
        temperature=0)
        messagesHistory.append({'role': response.choices[0].message.role, 'content': response.choices[0].message.content})
    except:
        print("API, WAITING 70 SECONDS")
        time.sleep(80)
        response = client.chat.completions.create(model="gpt-4o-mini",
        messages=messagesHistory,
        temperature=0)
        messagesHistory.append({'role': response.choices[0].message.role, 'content': response.choices[0].message.content})
        time.sleep(80)
    

    return response.choices[0].message.content

# Gets the Returned Response by Column Prefix
def get_prompt_response(columnPrefix, prompts):
    response = ''
    i = 0
    for promptObj in prompts:
        if (promptObj['column_prefix'] == columnPrefix):
            if ( ((i * 2) + 1) < len(messagesHistory) ):
                response = messagesHistory[(i * 2) + 1]['content']
        i = i + 1
    return response

def handle_conditional_prompts(prompt, prompts):
    return True
    global cweID

    conditionalNeeded = True
    # Check if P4 returned with Correct CWE-ID
    p4_response = get_prompt_response('P4', prompts).split(',')
    print("P4")
    print(p4_response)
    if (cweID in p4_response):
        print("CONDITIONAL ACTIVATED")
        conditionalNeeded = False

    return conditionalNeeded
        


def calculateBulkCost(df):
    total_completion_tokens = 0
    total_prompt_tokens = 0
    total_num_rows = 0
    
    for index, row in df.iterrows():
        prompts = Prompts(row).getPrompts()

        promptStats = []

        for prompt in prompts:
            encoding = tiktoken.encoding_for_model(GPT_MODEL)
            num_tokens = len(encoding.encode(prompt['prompt']))
            promptStats.append({
                'prompt': prompt['prompt'],
                'prompt_tokens': num_tokens,
                'response_length': prompt['response_length']
            })

        for i in range(len(promptStats)):
            promptSplit = promptStats[:i]
            for prompt in promptSplit:
                total_prompt_tokens = total_prompt_tokens + prompt['prompt_tokens']
                total_prompt_tokens = total_prompt_tokens + prompt['response_length']
            total_completion_tokens = total_completion_tokens + promptStats[i]['response_length']

        total_num_rows = total_num_rows + 1

        total_cost = (total_prompt_tokens * TOKEN_COST_INPUT) + (total_completion_tokens * TOKEN_COST_OUTPUT)

    return {
        'num_rows': total_num_rows,
        'prompt_tokens': total_prompt_tokens,
        'completion_tokens': total_completion_tokens,
        'cost': round(total_cost, 3)
    }

class Prompts: 
    def __init__(self, row):
        with open(PROMPTS_FILE) as f:
            data = json.load(f)
            promptsData = data['prompts']
            for i in range(len(promptsData)):
                prompt = promptsData[i]
                text = promptsData[i]['prompt']
                
                t = string.Template(text)
                text = t.substitute(primevul_func_before_fix = row['primevul_func_before_fix'], primevul_func_after_fix = row['primevul_func_after_fix'], CWE_ID = row['CWE ID'], git_commit_message = row['commit_message'], cve_summary = row['Summary'])

                promptsData[i]['prompt'] = text

            self.prompts = promptsData

    def getPrompts(self):
        return self.prompts

def export_csv(df):
    df.to_csv('outputBulk5/' + cweID + '.csv')

def append_columns_to_df(index, df, prompts):
    i = 1
    #print(messagesHistory)
    #print("Length Prompts: " + str(len(prompts)))
    #print("Length Msg Hist: " + str(len(messagesHistory)))
    for promptObj in prompts:
        #print(i)
        if (i < len(messagesHistory)):
            df.loc[index, promptObj['column_name']] = messagesHistory[i]['content']
        i = i + 2


    return df


# ITERATING THROUGH EACH FILE CHANGE

for filename in os.listdir(INPUT_CSV_PATH):
    if ((filename not in os.listdir(OUTPUT_CSV_PATH)) and (filename != 'NoCWEID.csv')):
        csvPath = INPUT_CSV_PATH + filename
        cweID = filename.replace('.csv', '')
        print(cweID)
        for df in pd.read_csv(csvPath, chunksize=chunkSize):
            for index, row in df.iterrows():
                prompts = Prompts(row).getPrompts()

                messagesHistory = []

                print('ROW NUM: ' + str(index))

                for prompt in prompts:
                    #print('---------------------------------')
                    # If Prompt is Conditional Only Execute if Necessary
                    if (prompt['conditional'] == True):
                        if (handle_conditional_prompts(prompt, prompts) == True):
                            print('EXECUTING CONDITIONAL GPT CALL')
                            get_completion(prompt['prompt'])
                        else:
                            #Save "" into CSV
                            messagesHistory.append({"role": "user", "content": " "})
                            messagesHistory.append({"role": "assistant", "content": ""})
                    else:
                        try:
                            get_completion(prompt['prompt'])
                        except:
                            print('ERROR: SAVING CSV')
                            #Fallback to save data if fatal error
                            export_csv(df)

                    #print(messagesHistory)
                    #print('---------------------------------')
                
                #time.sleep(5)
                df = append_columns_to_df(index, df, prompts)
                

            export_csv(df)
            

