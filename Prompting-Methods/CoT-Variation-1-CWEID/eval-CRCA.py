import os
import pandas as pd

import re


EVAL_CSV_PATH = 'Evaluation-CRCA/'
CHUNK_SIZE = 1000



if __name__ == '__main__':
    grandStatsDict = {
            'C3_Clarity_Total': 0,
            'C5_Clarity_Total': 0,
            'C3_Relevance_Total': 0,
            'C5_Relevance_Total': 0,
            'C3_Completeness_Total': 0,
            'C5_Completeness_Total': 0,
            'C3_Actionability_Total': 0,
            'C5_Actionability_Total': 0,
            'Num_Rows': 0,
            'Num_CSVs': 0
    }

    for filename in os.listdir(EVAL_CSV_PATH):
        errorVal = False
        csvStatsDict = {
            'C3_Clarity_Total': 0,
            'C5_Clarity_Total': 0,
            'C3_Relevance_Total': 0,
            'C5_Relevance_Total': 0,
            'C3_Completeness_Total': 0,
            'C5_Completeness_Total': 0,
            'C3_Actionability_Total': 0,
            'C5_Actionability_Total': 0,
            'Num_Rows': 0
            
        }




        #CSV File
        csvPath = EVAL_CSV_PATH + '/' + filename

        for df in pd.read_csv(csvPath, chunksize=CHUNK_SIZE):
            for index, row in df.iterrows():
                errorVal = False

                #Clarity
                clarity = row['G1_Clarity_C3_C5']
                try:
                    clarity = re.sub(r'\s+', '', clarity)

                    clarity_c3_str = clarity.split(',')[0].replace(" ", "")
                    clarity_c3 = int(clarity_c3_str)

                    clarity_c5_str = clarity.split(',')[1].replace(" ", "")
                    clarity_c5_str = clarity_c5_str[0]
                    clarity_c5 = int(clarity_c5_str)

                    
                except:
                    cwe = filename.replace(".csv", "")
                    print(f"ERROR ({cwe}): Clarity")
                    errorVal = True
                    continue

                #csvStatsDict['C3_Clarity_Total'] = csvStatsDict['C3_Clarity_Total'] + clarity_c3
                #csvStatsDict['C5_Clarity_Total'] = csvStatsDict['C5_Clarity_Total'] + clarity_c5
                

                #Relevance
                relevance = row['G2_Relevance_C3_C5']
                #print("Relevance: " + relevance)
                
                try:
                    #print(relevance)
                    #relevance = re.sub(r'\s+', '', relevance)
                    #relevance_c3 = int(relevance.split(',')[0])
                    #relevance_c5 = int(relevance.split(',')[1])
                    #print(relevance_c3)
                    #print(relevance_c5)

                    relevance = re.sub(r'\s+', '', relevance)

                    relevance_c3_str = relevance.split(',')[0].replace(" ", "")
                    relevance_c3 = int(relevance_c3_str)

                    relevance_c5_str = relevance.split(',')[1].replace(" ", "")
                    relevance_c5_str = relevance_c5_str[0]
                    relevance_c5 = int(relevance_c5_str)

                except Exception as e:
                    print("Error is: ", e)
                    cwe = filename.replace(".csv", "")
                    print(f"ERROR ({cwe}): Relevance")
                    #print(relevance)
                    errorVal = True
                    continue

                #csvStatsDict['C3_Relevance_Total'] = csvStatsDict['C3_Relevance_Total'] + relevance_c3
                #csvStatsDict['C5_Relevance_Total'] = csvStatsDict['C5_Relevance_Total'] + relevance_c5

                #Completeness
                completeness = row['G3_Completeness_C3_C5']
                try:
                    #completeness = re.sub(r'\s+', '', completeness)
                    #completeness_c3 = int(completeness.split(',')[0].replace(" ", ""))
                    #completeness_c5 = int(completeness.split(',')[1].replace(" ", ""))

                    completeness = re.sub(r'\s+', '', completeness)

                    completeness_c3_str = completeness.split(',')[0].replace(" ", "")
                    completeness_c3 = int(completeness_c3_str)

                    completeness_c5_str = completeness.split(',')[1].replace(" ", "")
                    completeness_c5_str = completeness_c5_str[0]
                    completeness_c5 = int(completeness_c5_str)
                except:
                    cwe = filename.replace(".csv", "")
                    print(f"ERROR ({cwe}): Completeness")
                    #print(completeness)
                    errorVal = True
                    continue

                #csvStatsDict['C3_Completeness_Total'] = csvStatsDict['C3_Completeness_Total'] + completeness_c3
                #csvStatsDict['C5_Completeness_Total'] = csvStatsDict['C5_Completeness_Total'] + completeness_c5

                #Actionability
                actionability = row['G4_Actionability_C3_C5']
                try:
                    #actionability = re.sub(r'\s+', '', actionability)
                    #actionability_c3 = int(actionability.split(',')[0].replace(" ", ""))
                    #actionability_c5 = int(actionability.split(',')[1].replace(" ", ""))

                    actionability = re.sub(r'\s+', '', actionability)

                    actionability_c3_str = actionability.split(',')[0].replace(" ", "")
                    actionability_c3 = int(actionability_c3_str)

                    actionability_c5_str = actionability.split(',')[1].replace(" ", "")
                    actionability_c5_str = actionability_c5_str[0]
                    actionability_c5 = int(actionability_c5_str)
                except:
                    cwe = filename.replace(".csv", "")
                    print(f"ERROR ({cwe}): Actionability")
                    #print(actionability)
                    errorVal = True
                    continue
                #csvStatsDict['C3_Actionability_Total'] = csvStatsDict['C3_Actionability_Total'] + actionability_c3
                #csvStatsDict['C5_Actionability_Total'] = csvStatsDict['C5_Actionability_Total'] + actionability_c5

                #Num Rows
                if (errorVal == False):
                    #Num Rows
                    csvStatsDict['Num_Rows'] = csvStatsDict['Num_Rows'] + 1

                    #Clarity
                    csvStatsDict['C3_Clarity_Total'] = csvStatsDict['C3_Clarity_Total'] + clarity_c3
                    csvStatsDict['C5_Clarity_Total'] = csvStatsDict['C5_Clarity_Total'] + clarity_c5

                    #Relevance
                    csvStatsDict['C3_Relevance_Total'] = csvStatsDict['C3_Relevance_Total'] + relevance_c3
                    csvStatsDict['C5_Relevance_Total'] = csvStatsDict['C5_Relevance_Total'] + relevance_c5

                    #Completeness
                    csvStatsDict['C3_Completeness_Total'] = csvStatsDict['C3_Completeness_Total'] + completeness_c3
                    csvStatsDict['C5_Completeness_Total'] = csvStatsDict['C5_Completeness_Total'] + completeness_c5

                    #Actionability
                    csvStatsDict['C3_Actionability_Total'] = csvStatsDict['C3_Actionability_Total'] + actionability_c3
                    csvStatsDict['C5_Actionability_Total'] = csvStatsDict['C5_Actionability_Total'] + actionability_c5

        if (csvStatsDict['Num_Rows'] == 0):
            print(filename.replace('.csv', '') + ': ERROR')
            continue

        grandStatsDict['Num_Rows'] = grandStatsDict['Num_Rows'] + csvStatsDict['Num_Rows']
        #Totals
        grandStatsDict['C3_Clarity_Total'] = grandStatsDict['C3_Clarity_Total'] + csvStatsDict['C3_Clarity_Total']
        grandStatsDict['C5_Clarity_Total'] = grandStatsDict['C5_Clarity_Total'] + csvStatsDict['C5_Clarity_Total']
        grandStatsDict['C3_Relevance_Total'] = grandStatsDict['C3_Relevance_Total'] + csvStatsDict['C3_Relevance_Total']
        grandStatsDict['C5_Relevance_Total'] = grandStatsDict['C5_Relevance_Total'] + csvStatsDict['C5_Relevance_Total']
        grandStatsDict['C3_Completeness_Total'] = grandStatsDict['C3_Completeness_Total'] + csvStatsDict['C3_Completeness_Total']
        grandStatsDict['C5_Completeness_Total'] = grandStatsDict['C5_Completeness_Total'] + csvStatsDict['C5_Completeness_Total']
        grandStatsDict['C3_Actionability_Total'] = grandStatsDict['C3_Actionability_Total'] + csvStatsDict['C3_Actionability_Total']
        grandStatsDict['C5_Actionability_Total'] = grandStatsDict['C5_Actionability_Total'] + csvStatsDict['C5_Actionability_Total']
        grandStatsDict['Num_CSVs'] = grandStatsDict['Num_CSVs'] + 1

        #C3 & C5
        
        c3ClarityAvg = csvStatsDict['C3_Clarity_Total'] / csvStatsDict['Num_Rows']
        c3RelevanceAvg = csvStatsDict['C3_Relevance_Total'] / csvStatsDict['Num_Rows']
        c3CompletenessAvg = csvStatsDict['C3_Completeness_Total'] / csvStatsDict['Num_Rows']
        c3ActionabilityAvg = csvStatsDict['C3_Actionability_Total'] / csvStatsDict['Num_Rows']
        c5ClarityAvg = csvStatsDict['C5_Clarity_Total'] / csvStatsDict['Num_Rows']
        c5RelevanceAvg = csvStatsDict['C5_Relevance_Total'] / csvStatsDict['Num_Rows']
        c5CompletenessAvg = csvStatsDict['C5_Completeness_Total'] / csvStatsDict['Num_Rows']
        c5ActionabilityAvg = csvStatsDict['C5_Actionability_Total'] / csvStatsDict['Num_Rows']

        count = csvStatsDict['Num_Rows']

        #C3
        #print(f"{filename.replace('.csv', '')} | Cla: {round(c3ClarityAvg,1)} | Rel: {round(c3RelevanceAvg,1)} | Com: {round(c3CompletenessAvg,1)} | Act: {round(c3ActionabilityAvg,1)} | {str(count)} ")

        #C5
        print(f"{filename.replace('.csv', '')} | Cla: {round(c5ClarityAvg,1)} | Rel: {round(c5RelevanceAvg,1)} | Com: {round(c5CompletenessAvg,1)} | Act: {round(c5ActionabilityAvg,1)} | {str(count)} ")

          
                
        #print(f"{filename.replace('.csv', '')} ({str(count)}): C3 - Cla: {round(c3ClarityAvg,1)} Rel: {round(c3RelevanceAvg,1)} Com: {round(c3CompletenessAvg,1)} Act: {round(c3ActionabilityAvg,1)} | C5 - Cla: {round(c5ClarityAvg,1)} Rel: {round(c5RelevanceAvg,1)} Com: {round(c5CompletenessAvg,1)} Act: {round(c5ActionabilityAvg,1)} ")

    #Grand Total
    c3ClarityAvg = grandStatsDict['C3_Clarity_Total'] / grandStatsDict['Num_Rows']
    c3RelevanceAvg = grandStatsDict['C3_Relevance_Total'] / grandStatsDict['Num_Rows']
    c3CompletenessAvg = grandStatsDict['C3_Completeness_Total'] / grandStatsDict['Num_Rows']
    c3ActionabilityAvg = grandStatsDict['C3_Actionability_Total'] / grandStatsDict['Num_Rows']

    c5ClarityAvg = grandStatsDict['C5_Clarity_Total'] / grandStatsDict['Num_Rows']
    c5RelevanceAvg = grandStatsDict['C5_Relevance_Total'] / grandStatsDict['Num_Rows']
    c5CompletenessAvg = grandStatsDict['C5_Completeness_Total'] / grandStatsDict['Num_Rows']
    c5ActionabilityAvg = grandStatsDict['C5_Actionability_Total'] / grandStatsDict['Num_Rows']
            

    print("-------------------------------------------------------------------------------------------------")
    print(f"GRAND TOTAL ({str(grandStatsDict['Num_Rows'])})")
    print(f"- C3 - Cla: {round(c3ClarityAvg, 1)} Rel: {round(c3RelevanceAvg, 1)} Com: {round(c3CompletenessAvg, 1)} Act: {round(c3ActionabilityAvg, 1)}") 
    print(f"- C5 - Cla: {round(c5ClarityAvg,1)} Rel: {round(c5RelevanceAvg,1)} Com: {round(c5CompletenessAvg,1)} Act: {round(c5ActionabilityAvg,1)} ")