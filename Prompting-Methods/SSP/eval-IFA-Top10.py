import os
import pandas as pd

import re



#EVAL_CSV_PATH = 'outputEvalIFA/'
EVAL_CSV_PATH = 'Evaluation-IFA/'
CHUNK_SIZE = 1000



if __name__ == '__main__':
    grand_top_10_total = 0
    grand_ifa_total = 0
    grand_num_rows = 0

    for filename in os.listdir(EVAL_CSV_PATH):
        errorVal = False
        csvStatsDict = {
            'Got_Top_10_CWE_Total': 0,
            'IFA_Total': 0,
            'Valid_Rows': 0,
            'Num_Rows': 0,
            'Num_CSVs': 0
        }

        #CSV File
        csvPath = EVAL_CSV_PATH + '/' + filename
        for df in pd.read_csv(csvPath, chunksize=CHUNK_SIZE):
            for index, row in df.iterrows():
                if (row['T2_Correctly_Found_CWE'] == 'D'):
                    print("DISQUALIFIED")
                    continue

                #Num Rows
                csvStatsDict['Num_Rows'] = csvStatsDict['Num_Rows'] + 1

                #Increment Top 10
                if (row['T2_Correctly_Found_CWE'] == 'Y'):
                    csvStatsDict['Got_Top_10_CWE_Total'] = csvStatsDict['Got_Top_10_CWE_Total'] + 1
                    csvStatsDict['IFA_Total'] = csvStatsDict['IFA_Total'] + int(row['T3_IFA'])



        if (csvStatsDict['Num_Rows'] == 0):
            print(filename.replace('.csv', '') + ': ERROR - ZERO ROWS')
            continue
        
        cweID = filename.replace('.csv', '')

        ifaAvg = -1

        if (csvStatsDict['Got_Top_10_CWE_Total'] > 0):
            #Printing for this CSV
            print(f"{cweID} | Top 10: {str(csvStatsDict['Got_Top_10_CWE_Total'])} | IFA Avg: {str(round(csvStatsDict['IFA_Total'] / csvStatsDict['Got_Top_10_CWE_Total'], 1))} | Num Rows: {csvStatsDict['Num_Rows']}")
        else:
            print(f"{cweID} | Top 10: {str(csvStatsDict['Got_Top_10_CWE_Total'])} | IFA Avg: N/A | Num Rows: {csvStatsDict['Num_Rows']}")

        #Add to Grand Totals
        grand_top_10_total = grand_top_10_total + csvStatsDict['Got_Top_10_CWE_Total']
        grand_ifa_total = grand_ifa_total + csvStatsDict['IFA_Total']
        grand_num_rows = grand_num_rows + csvStatsDict['Num_Rows']

    print(f'GRAND TOTALS | Top 10: {str(grand_top_10_total)} | IFA Avg: {str(round(grand_ifa_total/grand_top_10_total, 2))} | Num Rows: {str(grand_num_rows)}')