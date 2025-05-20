# **CoT Variation 1:** CoT method where **CWE ID** is provided as a Ground Truth.

## 📂 Prompting Method Structure

#### Dataset Generation #### 

* **generate-GPT.py**    Generates the data using the GPT-4o-Mini LLM.
* **Output:** CSV files with all input columns with C1-C6 columns generated using the LLM appended. 
* **promptsBulk.json** JSON file that contains the prompts used for generating the Descriptions & Explanations

#### CRCA Statistics #### 

* **generate-CRCA.py:**  Generates the Clarity, Relevance, Clarity and Actionability (CRCA) scores.
* **Evaluation-CRCA Folder:** CSV files include columns for Completness, Relevance, Clarity and Actionability (CRCA) scores. 

* **eval-CRCA.py:**      Prints a summary of the CRCA statistics.

#### IFA Statistics #### 

* **generate-IFA.py:**   Generates the IFA scores.
* **Evaluation-IFA** CSV files include columns for IFA scores.

* **eval-IFA-Top5.py**   Prints summary of the IFA Top 5 statistics.
* **eval-IFA-Top10.py**  Prints summary of the IFA Top 10 statistics.

#### Merge CRCA & IFA ####

* **merge-IFA-CRCA.py:** Merges the IFA and CRCA scores into one datasheet.
* **Evaluation-IFA-CRCA-Merged** CSV files include columns for both **IFA** and **CRCA** scores.

## 🔑 Configuring APIs
The project uses the following two LLMs which require API access keys to be configured:
* **GPT 4o Mini:** (For Generating Textual Descriptions)
* **Anthropic Claude 3.5:** (For Generating Evaluations)

Configure the API keys in the **config.json** files:
```
{
    "API_Key": "GPT_API_KEY",
    "Claude_API_Key": "ANTHROPIC_API_KEY"
}
```


## 📝 Generating Textual Description 

### 1. Configure Input/Output Folders
The input folder should be configured as the "dbSplitPrime" folder. The output folder is by default configured as "Output". 
```
INPUT_CSV_FOLDER = '../BigVul-PrimeVul-Datasets/dbSplitPrime'
```
```
OUTPUT_CSV_PATH = 'Output/'
```

### 2. Generate the Descriptions

Execute the following inside the relevant CoT method subfolder:
```
python3 generate-GPT.py
```


## 🧮 Generating Evaluation Columns

Execute the below commands to generate the IFA (Initial False Alarm) score and CRCA (Clarity, Relevance, Completeness, Actionability) scores using the Anthropic Claude 3.5 LLM.




1. Generating IFA Columns:
```
python3 generate-IFA.py
```

2. Generating CRCA Columns:
```
python3 generate-CRCA.py
```

3. Merging Descriptions, IFA & CRCA Columns into a Single CSV File: 
```
python3 merge-IFA-CRCA.py
```

## 📈 Aggregating Statistical Data

The below commands aggregate statistical data for each CWE-ID CSV file for IFA and CRCA respectively, including a Grand Total for the CoT method. 

1. Statistics on CRCA
```
python3 eval-CRCA.py
```

2. Statistics on IFA Top 5
```
python3 eval-IFA-Top5.py
```

3. Statistics on IFA Top 10
```
python3 eval-IFA-Top10.py
```

## 📊 Results - CoT Variation 1 

### IFA 

| Metric     | Top 5 | Top 10 |
|------------|--------|---------|
| Hits       | 724    | 744     |
| IFA Avg    | 1.23   | 1.41    |


### CRCA

| Score Type | Cla (Clarity) | Rel (Relevance) | Com (Completeness) | Act (Actionability) |
|------------|----------------|------------------|----------------------|----------------------|
| C3         | 4.5            | 4.6              | 4.0                  | 4.1                  |
| C5         | 4.5            | 4.6              | 4.1                  | 4.4                  |

