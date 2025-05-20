# A Contextual-Chain-Prompting Approach for Code Vulnerability Explanation

**Authors:** Helen Paik, Dipankar Chaki, Ethan Marlow

**Description:** Enhancing descriptions of vulnerabilities using Chain of Thought prompting techniques.

**Abstract:** This thesis attempts to improve upon existing vulnerability detection tools in IDEs by
improving the outputted description returned to the user so developers can understand
identified vulnerabilities and take appropriate action to remediate them. Following a
Literature Survey it is evident that vulnerability descriptions returned to developers in
IDE lack utility for developers without a high degree of knowledge in Cyber Security.
In solving this problem, we investigate methods to form an enhanced knowledge base
that returns informative description that are useful for developers.

As a solution to this problem, this thesis proposes a refined Chain of Thought prompting
approach using the BigVul and PrimeVul datasets to produce an Enhanced Knowledgebase for C/C++ functions enabling accurate and useful descriptions based on Clarity,
Relevance, Completeness and Actionability to be returned to developers using the GPT
4o Mini dataset. Additionally, the paper explores whether feeding particular Ground
Truths from the dataset, namely the CWE ID, CVE Summary and Git Commit Message improve the quality and accuracy of the description.

Following evaluation using two distinct methods, this thesis highlights that the refined
Chain of Thought prompting approach proposed results in a significant improvement to
both the utility and accuracy of vulnerability descriptions/explanations. Additionally,
it highlights that feeding the GPT 4o Mini LLM with the CWE ID and CVE Summary
significantly improves the generated descriptions.

**Publication Date:** 31 January 2025

**Link to Paper/Report:** [https://ieee.org/]

## 📚 Structure

* **BigVul-PrimeVul Datasets** Contains the extracted BigVul/PrimeVul datasets (Preliminary Knowledgebase).
* **Prompting Methods** Contains the prompting methods

## 🧠 Prompting Methods

* **CoT Generic:** Plain CoT method without any Ground Truths.
* **CoT Variation 1:** CoT method where **CWE ID** is provided as a Ground Truth.
* **CoT Variation 2:** CoT method where **CWE ID and CVE Summary** are given as Ground Truths.
* **CoT Variation 3:** CoT method where **Git Commit Message** is given as a Ground Truth.
* **SSP:** Single Short Prompt Baseline 


## 📂 Prompting Methods Subfolder Structure

#### Dataset Generation #### 

* **generate-GPT.py**    Generates the data using the GPT-4o-Mini LLM.
* **Output:** CSV files with all input columns with C1-C6 columns generated using the LLM appended. 

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

## 🖥️ Accessing Repository

1. Clone the Git repository by running the below command:

```
git clone https://github.com/ethanm20/CoT-Vulnerability-Descriptions.git
```

2. Open the repository root folder:
```
cd CoT-Vulnerability-Descriptions
```

## 🛠️ Installing Dependencies
The following Python libraries are required:
* Pandas
* OpenAI
* Anthropic 
* Tiktoken

1. Install Pandas
```
pip3 install pandas
```

2. Install OpenAI
```
pip3 install openai
```

3. Install Anthropic
```
pip3 install anthropic
```

4. Install Tiktoken
```
pip3 install tiktoken
```

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

3. Merging GPT Descriptions, IFA & CRCA Evaluations into a single consolidated CSV File per CWE-ID: 
```
python3 merge-IFA-CRCA.py
```

## 📈 Aggregating Results

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



## 📊 CoT Prompting Methods Results


### IFA Results (Top 5 and Top 10)

| Method       | Top 5 Hits | Top 5 IFA Avg | Top 10 Hits | Top 10 IFA Avg |
|--------------|------------|---------------|-------------|----------------|
| CoT-Generic  | 420        | 1.37          | 444         | 1.71           |
| CoT-Var-1    | 724        | 1.23          | 744         | 1.41           |
| CoT-Var-2    | 753        | 1.29          | 801         | 1.67           |
| CoT-Var-3    | 542        | 1.33          | 581         | 1.79           |
| SSP          | 491        | 1.55          | 550         | 2.21           |



### CRCA Evaluation Results (C3 and C5 Scores)

| Method       | C3 - Cla | C3 - Rel | C3 - Com | C3 - Act | C5 - Cla | C5 - Rel | C5 - Com | C5 - Act |
|--------------|----------|----------|----------|----------|----------|----------|----------|----------|
| CoT-Generic  | 4.5      | 4.7      | 4.1      | 4.1      | 4.5      | 4.7      | 4.1      | 4.4      |
| CoT-Var-1    | 4.5      | 4.6      | 4.0      | 4.1      | 4.5      | 4.6      | 4.1      | 4.4      |
| CoT-Var-2    | 4.5      | 4.7      | 4.1      | 4.2      | 4.4      | 4.7      | 4.1      | 4.3      |
| CoT-Var-3    | 4.5      | 4.7      | 4.1      | 4.2      | 4.5      | 4.7      | 4.1      | 4.4      |
| SSP          | –        | –        | –        | –        | 2.7      | 4.7      | 3.6      | 3.3      |





