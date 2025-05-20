## 🧠 Prompting Methods

* **CoT Generic:** Plain CoT method without any Ground Truths.
* **CoT Variation 1:** CoT method where **CWE ID** is provided as a Ground Truth.
* **CoT Variation 2:** CoT method where **CWE ID and CVE Summary** are given as Ground Truths.
* **CoT Variation 3:** CoT method where **Git Commit Message** is given as a Ground Truth.
* **SSP:** Single Short Prompt Baseline 


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

