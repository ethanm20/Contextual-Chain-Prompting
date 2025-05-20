from openai import OpenAI
import pandas as pd
import json
import tiktoken
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

# IMPORTANT!
# TODO: STATIC CONSTANTS THAT SHOULD BE CHECKED EACH TIME BEFORE RUNNING

#----------------------------------------------------------------
# START STATIC CONSTANTS
INPUT_CSV_FOLDER = '../../dbSplitPrime'

# The specific CWE ID we are going to run the model on
#cweID = "CWE-89"

# The folder the outputted CSV will be saved in (this folder must exist, if not manually make the folder before running this code)
OUTPUT_CSV_PATH = 'outputBulk/'

# Token Costings
TOKEN_COST = 0.01 / 1000


# GPT Model
GPT_MODEL = "gpt-4o-mini"

PROMPTS_FILE = 'prompts.json'


# END STATIC CONSTANTS
#-----------------------------------------------------------


#Message History Global Variable
messagesHistory = []

#CSV FILE CHUNK SIZE
CHUNK_SIZE = 1000


#----------------------------------------------------------------

def calculate_tokens(prompt):
    encoding = tiktoken.encoding_for_model('gpt-4-turbo-2024-04-09')
    num_tokens = len(encoding.encode(prompt))
    return num_tokens

# HANDLING CALL TO API
def get_completion(prompt, i):
    global messagesHistory

    messagesHistory.append({"role": "user", "content": prompt})
    num_tokens = calculate_tokens(str(messagesHistory))

    print(messagesHistory)

    print('NUM TOKENS: ' + str(num_tokens))

    if (num_tokens < 20000):
        time.sleep(2)
    elif (num_tokens < 80000):
        time.sleep(61)
    
    response = client.chat.completions.create(model=GPT_MODEL,
    messages=messagesHistory,
    temperature=0)

    messagesHistory.append({'role': response.choices[0].message.role, 'content': response.choices[0].message.content})

    print(messagesHistory)
    print('After')
    

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

def handle_conditional_prompts(prompt, prompts, filename):
    #global cweID
    cweID = filename.replace(".csv", "")

    conditionalNeeded = True
    # Check if P4 returned with Correct CWE-ID
    p4_response = get_prompt_response('P4', prompts).split(',')
    if (cweID in p4_response):
        conditionalNeeded = False

    return conditionalNeeded


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






def calculateBulkCost(df):
    total_completion_tokens = 0
    total_prompt_tokens = 0
    total_num_rows = 0
    
    for index, row in df.iterrows():
        prompts = Prompts(row).getPrompts()

        promptStats = []

        for prompt in prompts:
            encoding = tiktoken.encoding_for_model('gpt-4-turbo-2024-04-09')
            num_tokens = len(encoding.encode(prompt['prompt']))
            num_tokens = 1
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

    return {
        'num_rows': total_num_rows,
        'prompt_tokens': total_prompt_tokens,
        'completion_tokens': total_completion_tokens,
        'cost': round((total_prompt_tokens + total_completion_tokens) * TOKEN_COST, 3)
    }

def export_csv(df, filename):
    df.to_csv(OUTPUT_CSV_PATH + filename)

def append_columns_to_df(index, df, prompts):
    i = 1
    for promptObj in prompts:
        df.loc[index, promptObj['column_name']] = messagesHistory[i]['content']
        i = i + 2

    #TODO: RUN CONDITIONAL HERE
    #if (len(get_prompt_response('P6', prompts)) == 0):
        #There was no reprompting

        #In Context
        #df.loc[index, 'C3_Explanation_of_Vulnerability_In_Context'] = get_prompt_response('P2', prompts)

        #Generic 
        #df.loc[index, 'C4_Explanation_of_Vulnerability_Generic'] = get_prompt_response('P3', prompts)
    #else: 
        #Reprompting

        #In Context
        #df.loc[index, 'C3_Explanation_of_Vulnerability_In_Context'] = get_prompt_response('P8', prompts)

        #Generic 
        #df.loc[index, 'C4_Explanation_of_Vulnerability_Generic'] = get_prompt_response('P9', prompts)


    return df


def iterate_csv(csvPath, filename):
    global messagesHistory
    
    # ITERATING THROUGH EACH FILE CHANGE
    for df in pd.read_csv(csvPath, chunksize=CHUNK_SIZE):
        
        promptsTotalStats = calculateBulkCost(df)

        response = f"""
        Would you like to make bulk multi-prompts CoT call to GPT API (Y/N)? 
        Filename (CWE): {str(filename)}
        Total Number of Rows: {str(promptsTotalStats['num_rows'])}
        Prompt Tokens: {str(promptsTotalStats['prompt_tokens'])}
        Completion Tokens: {str(promptsTotalStats['completion_tokens'])}
        Total Cost: US${str(promptsTotalStats['cost'])} 
        """

        response = 'Y'

        if (response == 'Y'):
            for index, row in df.iterrows():
                prompts = Prompts(row).getPrompts()
                
                messagesHistory = []
                i = 1

                for prompt in prompts:
                    print('---------------------------------')
                    # If Prompt is Conditional Only Execute if Necessary
                    if (prompt['conditional'] == True):
                        if (handle_conditional_prompts(prompt, prompts, filename) == True):
                            try:
                                get_completion(prompt['prompt'], i)
                                i = i + 2
                            except Exception as error:
                                print('ERROR: SAVING CSV')
                                print(error)
                                export_csv(df, filename)
                                messagesHistory.append({"role":"user", "content": ""})
                                messagesHistory.append({"role":"assistant", "content": ""}) 
                                #i = i + 2
                        else:
                            #Save "" into CSV
                            messagesHistory.append({"role":"user", "content": ""})
                            messagesHistory.append({"role":"assistant", "content": ""})
                            #i = i + 2
                    else:
                        try:
                            get_completion(prompt['prompt'], i)
                            i = i + 2
                        except Exception as error:
                            print('ERROR: SAVING CSV')
                            print(error)
                            export_csv(df, filename)
                            messagesHistory.append({"role":"user", "content": ""})
                            messagesHistory.append({"role":"assistant", "content": ""}) 
                            #i = i + 2

                    print('Message History')
                    print(messagesHistory)
                    print('---------------------------------')
                    
                
                df = append_columns_to_df(index, df, prompts)  

            export_csv(df, filename)

if __name__ == '__main__':
    folderPath = INPUT_CSV_FOLDER

    for filename in os.listdir(folderPath ):
        #CSV File
        #filename = input("Enter Filename: ")
        filePath = folderPath + '/' + filename
            
        iterate_csv(filePath, filename)

            

