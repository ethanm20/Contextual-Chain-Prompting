import os
import pandas as pd

import re



EVAL_CSV_PATH = 'Evaluation-CRCA/'
CHUNK_SIZE = 1000



if __name__ == '__main__':
    grandStatsDict = {
            'F1_Clarity_C5_Total': 0,
            'F2_Relevance_C5_Total': 0,
            'F3_Completeness_C5_Total': 0,
            'F4_Actionability_C5_Total': 0,
            'Num_Rows': 0,
            'Num_CSVs': 0
    }

    for filename in os.listdir(EVAL_CSV_PATH):
        errorVal = False
        csvStatsDict = {
            'F1_Clarity_C5_Total': 0,
            'F2_Relevance_C5_Total': 0,
            'F3_Completeness_C5_Total': 0,
            'F4_Actionability_C5_Total': 0,
            'Num_Rows': 0
            
        }




        #CSV File
        csvPath = EVAL_CSV_PATH + '/' + filename

        for df in pd.read_csv(csvPath, chunksize=CHUNK_SIZE):
            #print(csvPath)
            for index, row in df.iterrows():
                errorVal = False

                #Clarity
                try:
                    clarity = row['F1_Clarity_C5']

                    if (type(clarity) == int):
                        clarity_c5 = clarity
                    else:
                        clarity_str = re.sub(r'\s+', '', clarity)
                        if (clarity_str[0].isnumeric()):
                            clarity_str = clarity_str[0]
                            clarity_c5 = int(clarity_str)
                        else:
                            #If First char is not a number

                            #Remove any number lists to avoid confusion
                            clarity_str = clarity_str.replace("1.", "")
                            clarity_str = clarity_str.replace("2.", "")
                            clarity_str = clarity_str.replace("3.", "")
                            clarity_str = clarity_str.replace("4.", "")
                            clarity_str = clarity_str.replace("5.", "")

                            #Remove any reference of 0 to 5
                            clarity_str = clarity_str.replace("0 and 5", "")
                            clarity_str = clarity_str.replace("0 to 5", "")
                            clarity_str = clarity_str.replace("out of 5", "")

                            #Now get the first number (this will be the rating)
                            clarity_str = re.search(r'\d+', clarity_str).group()
                            clarity_c5 = int(clarity_str)
                            #print("RAN " + str(clarity_c5))
                            #print(clarity)
                except Exception as e:
                    print("Error is: ", e)
                    cwe = filename.replace(".csv", "")
                    print(f"ERROR ({cwe}): Clarity")
                    errorVal = True
                    continue
                

                #Relevance
                
                
                try:
                    relevance = row['F2_Relevance_C5']

                    if (type(relevance) == int):
                        relevance_c5 = relevance
                    else:
                        #relevance_str = re.sub(r'\s+', '', relevance)
                        #relevance_str = relevance_str[0]
                        #relevance_c5 = int(relevance_str)

                        relevance_str = re.sub(r'\s+', '', relevance)
                        if (relevance_str[0].isnumeric()):
                            relevance_str = relevance_str[0]
                            relevance_c5 = int(relevance_str)
                        else:
                            #If First char is not a number

                            #Remove any number lists to avoid confusion
                            relevance_str = relevance_str.replace("1.", "")
                            relevance_str = relevance_str.replace("2.", "")
                            relevance_str = relevance_str.replace("3.", "")
                            relevance_str = relevance_str.replace("4.", "")
                            relevance_str = relevance_str.replace("5.", "")

                            #Remove any reference of 0 to 5
                            relevance_str = relevance_str.replace("0 and 5", "")
                            relevance_str = relevance_str.replace("0 to 5", "")
                            relevance_str = relevance_str.replace("out of 5", "")

                            #Now get the first number (this will be the rating)
                            relevance_str = re.search(r'\d+', relevance_str).group()
                            relevance_c5 = int(relevance_str)
                            #print("RAN " + str(relevance_c5))
                            #print(relevance)
                except:
                    cwe = filename.replace(".csv", "")
                    print(f"ERROR ({cwe}): Relevance")
                    print(relevance)
                    errorVal = True
                    continue

                #Completeness
                
                try:
                    completeness = row['F3_Completeness_C5']

                    if (type(completeness) == int):
                        completeness_c5 = completeness
                    else:
                        #completeness_str = re.sub(r'\s+', '', completeness)
                        #completeness_str = completeness_str[0]
                        #completeness_c5 = int(completeness_str)

                        completeness_str = re.sub(r'\s+', '', completeness)
                        if (completeness_str[0].isnumeric()):
                            completeness_str = completeness_str[0]
                            completeness_c5 = int(completeness_str)
                        else:
                            #If First char is not a number

                            #Remove any number lists to avoid confusion
                            completeness_str = completeness_str.replace("1.", "")
                            completeness_str = completeness_str.replace("2.", "")
                            completeness_str = completeness_str.replace("3.", "")
                            completeness_str = completeness_str.replace("4.", "")
                            completeness_str = completeness_str.replace("5.", "")

                            #Remove any reference of 0 to 5
                            completeness_str = completeness_str.replace("0 and 5", "")
                            completeness_str = completeness_str.replace("0 to 5", "")
                            completeness_str = completeness_str.replace("out of 5", "")

                            #Now get the first number (this will be the rating)
                            #print('Bef')
                            #print(completeness)
                            #print('Bef2')
                            #print(completeness_str)
                            completeness_str = re.search(r'\d+', completeness_str).group()
                            completeness_c5 = int(completeness_str)
                            #print("RAN " + str(completeness_c5))
                            #print(completeness)
                except Exception as e:
                    print('ERROR1: ', e)
                    cwe = filename.replace(".csv", "")
                    print(f"ERROR ({cwe}): Completeness")
                    #print(completeness)
                    errorVal = True
                    continue

                #Actionability
                
                try:
                    actionability = row['F4_Actionability_C5']

                    if (type(actionability) == int):
                        actionability_c5 = actionability
                    else:
                        #actionability_str = re.sub(r'\s+', '', actionability)
                        #actionability_str = actionability_str[0]
                        #actionability_c5 = int(actionability_str)

                        actionability_str = re.sub(r'\s+', '', actionability)
                        if (actionability_str[0].isnumeric()):
                            actionability_str = actionability_str[0]
                            actionability_c5 = int(actionability_str)
                        else:
                            #If First char is not a number

                            #Remove any number lists to avoid confusion
                            actionability_str = actionability_str.replace("1.", "")
                            actionability_str = actionability_str.replace("2.", "")
                            actionability_str = actionability_str.replace("3.", "")
                            actionability_str = actionability_str.replace("4.", "")
                            actionability_str = actionability_str.replace("5.", "")

                            #Remove any reference of 0 to 5
                            actionability_str = actionability_str.replace("0 and 5", "")
                            actionability_str = actionability_str.replace("0 to 5", "")
                            actionability_str = actionability_str.replace("out of 5", "")

                            #Now get the first number (this will be the rating)
                            actionability_str = re.search(r'\d+', actionability_str).group()
                            actionability_c5 = int(actionability_str)
                            #print("RAN " + str(actionability_c5))
                            #print(actionability)
                except:
                    cwe = filename.replace(".csv", "")
                    print(f"ERROR ({cwe}): Actionability")
                    #print(actionability)
                    errorVal = True
                    continue

                #Num Rows
                if (errorVal == False):
                    #Num Rows
                    csvStatsDict['Num_Rows'] = csvStatsDict['Num_Rows'] + 1

                    #Clarity
                    csvStatsDict['F1_Clarity_C5_Total'] = csvStatsDict['F1_Clarity_C5_Total'] + clarity_c5

                    #Relevance
                    csvStatsDict['F2_Relevance_C5_Total'] = csvStatsDict['F2_Relevance_C5_Total'] + relevance_c5

                    #Completeness
                    csvStatsDict['F3_Completeness_C5_Total'] = csvStatsDict['F3_Completeness_C5_Total'] + completeness_c5

                    #Actionability
                    csvStatsDict['F4_Actionability_C5_Total'] = csvStatsDict['F4_Actionability_C5_Total'] + actionability_c5

        if (csvStatsDict['Num_Rows'] == 0):
            print(filename.replace('.csv', '') + ': ERROR')
            continue

        
        #Totals
        grandStatsDict['F1_Clarity_C5_Total'] = grandStatsDict['F1_Clarity_C5_Total'] + csvStatsDict['F1_Clarity_C5_Total']
        grandStatsDict['F2_Relevance_C5_Total'] = grandStatsDict['F2_Relevance_C5_Total'] + csvStatsDict['F2_Relevance_C5_Total']
        grandStatsDict['F3_Completeness_C5_Total'] = grandStatsDict['F3_Completeness_C5_Total'] + csvStatsDict['F3_Completeness_C5_Total']
        grandStatsDict['F4_Actionability_C5_Total'] = grandStatsDict['F4_Actionability_C5_Total'] + csvStatsDict['F4_Actionability_C5_Total']

        grandStatsDict['Num_Rows'] = grandStatsDict['Num_Rows'] + csvStatsDict['Num_Rows']
        grandStatsDict['Num_CSVs'] = grandStatsDict['Num_CSVs'] + 1

        #AVERAGES
        c5ClarityAvg = csvStatsDict['F1_Clarity_C5_Total'] / csvStatsDict['Num_Rows']
        c5RelevanceAvg = csvStatsDict['F2_Relevance_C5_Total'] / csvStatsDict['Num_Rows']
        c5CompletenessAvg = csvStatsDict['F3_Completeness_C5_Total'] / csvStatsDict['Num_Rows']
        c5ActionabilityAvg = csvStatsDict['F4_Actionability_C5_Total'] / csvStatsDict['Num_Rows']

        count = csvStatsDict['Num_Rows']
                
        print(f"{filename.replace('.csv', '')} ({str(count)}): C5 - Cla: {round(c5ClarityAvg,1)} Rel: {round(c5RelevanceAvg,1)} Com: {round(c5CompletenessAvg,1)} Act: {round(c5ActionabilityAvg,1)} ")

    #Grand Total

    c5ClarityAvg = grandStatsDict['F1_Clarity_C5_Total'] / grandStatsDict['Num_Rows']
    c5RelevanceAvg = grandStatsDict['F2_Relevance_C5_Total'] / grandStatsDict['Num_Rows']
    c5CompletenessAvg = grandStatsDict['F3_Completeness_C5_Total'] / grandStatsDict['Num_Rows']
    c5ActionabilityAvg = grandStatsDict['F4_Actionability_C5_Total'] / grandStatsDict['Num_Rows']
            

    print("-------------------------------------------------------------------------------------------------")
    print(f"GRAND TOTAL ({str(grandStatsDict['Num_Rows'])})")
    print(f"- C5 - Cla: {round(c5ClarityAvg,1)} Rel: {round(c5RelevanceAvg,1)} Com: {round(c5CompletenessAvg,1)} Act: {round(c5ActionabilityAvg,1)} ")