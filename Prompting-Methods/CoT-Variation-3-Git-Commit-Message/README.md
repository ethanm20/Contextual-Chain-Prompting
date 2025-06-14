# **CoT Variation 3:** CoT method where **Git Commit Message** is given as a Ground Truth.

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

## 🧠 Prompts

| Column Name | Prompt |
|-------------|--------|
| C1 Description of Functionality (In-Context) | Please provide a clear and comprehensive description of the functionality of the code. In the outputted description please ensure that:<br>1. The description is limited to one paragraph and between 90-100 words.<br>Code:<br>$primevul_func_before_fix |
| C2 Description of Functionality (Generic) | Please provide a clear and comprehensive description of the functionality of the code that was given to you in the first prompt. In the outputted description please ensure that:<br>1. The description is limited to one paragraph and between 90-100 words.<br>2. Do not include any variable/function/expression names in the description. |
| C3 Explanation of Vulnerability (In-Context) | Please explain the vulnerability in the Vulnerable Code (with Git Commit Message below) and then explain how the vulnerability was fixed in the changed code. To explain the cause of the vulnerability, get the context from the changed code on how the vulnerability was fixed. In your response please ensure that:<br>1. The response is limited to one paragraph and between 90-100 words.<br>2. The response should include variable/function/expression names from the code.<br>Code before Change/Fix (Vulnerable Code):<br>The code provided in the first prompt.<br>Code after Change/Fix (Fixed Code):<br>$primevul_func_after_fix<br>Git Commit Message for Code Change:<br>$git_commit_message |
| C4 Explanation of Vulnerability (Generic) | Please explain the vulnerability in the Vulnerable Code (with Git Commit Message below) and then explain how the vulnerability was fixed in the changed code. To explain the cause of the vulnerability, get the context from the changed code on how the vulnerability was fixed. In your response please ensure that:<br>1. The response is limited to one paragraph and between 90-100 words.<br>2. Do not include any variable/function/expression names in the description.<br>Git Commit Message for Code Change:<br>$git_commit_message |
| C5 Explanation of How Vulnerability Fixed (In-Context) | Please explain how the vulnerability was fixed. In your response please ensure that:<br>1. The response is limited to one paragraph and between 90-100 words.<br>2. The response should include variable/fuction/expression names from the code. |
| C6 Explanation of How Vulnerability Fixed (Generic) | Please explain how the vulnerability was fixed. In your response please ensure that:<br>1. The response is limited to one paragraph and between 90-100 words.<br>2. Do not include any variable/function/expression names in the description. |


## 📊 Results - CoT Variation 3

### IFA

| Metric   | Top 5 | Top 10 |
|----------|--------|---------|
| Hits     | 542    | 581     |
| IFA Avg  | 1.33   | 1.79    |

### CRCA


| Score Type | Cla (Clarity) | Rel (Relevance) | Com (Completeness) | Act (Actionability) |
|------------|----------------|------------------|----------------------|----------------------|
| C3         | 4.5            | 4.7              | 4.1                  | 4.2                  |
| C5         | 4.5            | 4.7              | 4.1                  | 4.4                  |
