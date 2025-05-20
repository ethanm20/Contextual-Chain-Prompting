from openai import OpenAI
import pandas as pd
import json
import tiktoken
import time
import os
import string


#----------------------------------------------------------------
# START STATIC CONSTANTS
INPUT_CSV_FOLDER = 'Output/'

IFA_FOLDER = 'Evaluation-IFA/'
CRCA_FOLDER = 'Evaluation-CRCA/'
OUTPUT_CSV_PATH = 'Evaluation-IFA-CRCA-Merged-New/'

CHUNK_SIZE = 1000

#---------------------------------------------------------------


def export_csv(df, filename):
    df.to_csv(OUTPUT_CSV_PATH + filename)

def append_columns_to_df(dfOutput, index):

    #IFA
    for dfIFA in pd.read_csv(IFA_FOLDER + filename, chunksize=CHUNK_SIZE):
        dfOutput.loc[index, "T1_Top_10_CWE_IDs"] = dfIFA.loc[index, "T1_Top_10_CWE_IDs"]
        dfOutput.loc[index, "T2_Correctly_Found_CWE"] = dfIFA.loc[index, "T2_Correctly_Found_CWE"]
        dfOutput.loc[index, "T3_IFA"] = dfIFA.loc[index, "T3_IFA"]

    #CRCA
    for dfCRCA in  pd.read_csv(CRCA_FOLDER + filename, chunksize=CHUNK_SIZE):
        dfOutput.loc[index, "G1_Clarity_C3_C5"] = dfCRCA.loc[index, "G1_Clarity_C3_C5"]
        dfOutput.loc[index, "G2_Relevance_C3_C5"] = dfCRCA.loc[index, "G2_Relevance_C3_C5"]
        dfOutput.loc[index, "G3_Completeness_C3_C5"] = dfCRCA.loc[index, "G3_Completeness_C3_C5"]
        dfOutput.loc[index, "G4_Actionability_C3_C5"] = dfCRCA.loc[index, "G4_Actionability_C3_C5"]

    return dfOutput


def iterate_csv(filename):
    global messagesHistory
    
    # ITERATING THROUGH EACH FILE CHANGE
    for dfOutput in pd.read_csv(INPUT_CSV_FOLDER + filename, chunksize=CHUNK_SIZE):
        for index, row in dfOutput.iterrows():

            dfOutput = append_columns_to_df(dfOutput, index)  

        export_csv(dfOutput, filename)

if __name__ == '__main__':
    i = 0
    for filename in os.listdir(INPUT_CSV_FOLDER):
        if ((filename not in os.listdir(OUTPUT_CSV_PATH) and (filename != 'NoCWEID.csv'))):
            print("Iterator: " + str(i))
            
            print("CSV: " + INPUT_CSV_FOLDER + filename)
            iterate_csv(filename)
            i = i + 1