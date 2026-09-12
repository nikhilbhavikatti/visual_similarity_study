# Visual Similarity Study


A Streamlit-based user study for investigating how people visually judge the similarity of one-dimensional kernel-support distributions.


The study presents three 1D kernel-support distributions for each question:


- **Option A**
- **Reference distribution Q**
- **Option B**


Participants select the option that appears more similar to the reference distribution Q based only on their visual impression.


Unlike the Wasserstein Similarity Study, this study does not show whether an answer is correct or incorrect. It also does not show Wasserstein distances or any other mathematical similarity measure during the study.


## Live application


Open the deployed Streamlit application here:


> **[https://visual-similarity-study.streamlit.app/](https://visual-similarity-study.streamlit.app/)**


## Project structure


```text
visual_similarity_study/
├── app.py
├── requirements.txt
├── .streamlit/
│   └── config.toml
├── images/
│   ├── example/
│   │   └── wasserstein_example.png
│   ├── Q1/
│   │   ├── a.png
│   │   ├── b.png
│   │   └── t.png
│   ├── Q2/
│   │   ├── a.png
│   │   ├── b.png
│   │   └── t.png
│   └── ...
│       └── Q20/
│           ├── a.png
│           ├── b.png
│           └── t.png
├── create_wasserstein_example.py
├── study2_analysis.py
└── study2/
    ├── participant_01.csv
    ├── participant_02.csv
    └── ...
```


## Question-image convention


Each question uses three image files:


| File | Meaning |
|---|---|
| `images/Qi/a.png` | Option A distribution |
| `images/Qi/t.png` | Reference distribution Q |
| `images/Qi/b.png` | Option B distribution |


For example, Question 1 requires:


```text
images/Q1/a.png
images/Q1/t.png
images/Q1/b.png
```


Question 20 requires:


```text
images/Q20/a.png
images/Q20/t.png
images/Q20/b.png
```


The application generates the image paths automatically:


```python
NUM_QUESTIONS = 20

QUESTIONS = [
    {
        "target_image": f"images/Q{i}/t.png",
        "option_a_image": f"images/Q{i}/a.png",
        "option_b_image": f"images/Q{i}/b.png",
    }
    for i in range(1, NUM_QUESTIONS + 1)
]
```


## Local installation


### 1. Install dependencies


```bash
pip install -r requirements.txt
```


### 2. Start the application


```bash
streamlit run app.py
```


Streamlit will print a local address, usually:


```text
http://localhost:8501
```


Open that link in a web browser.


## Requirements


The application uses the following main Python packages:


```text
streamlit
pandas
openpyxl
matplotlib
numpy
```


A typical `requirements.txt` is:


```text
streamlit>=1.35.0
pandas>=2.0.0
openpyxl>=3.1.0
matplotlib>=3.7.0
numpy>=1.24.0
```


If you only run the Streamlit application and do not run the analysis scripts, some packages may not be necessary. Keeping all listed packages makes the complete repository reproducible.


## Creating the instructional example plot


The repository includes a script that generates the example figure used in the introductory slide:


```bash
python create_wasserstein_example.py
```


It creates:


```text
images/example/wasserstein_example.png
```


The generated figure contains:


- Option A as a compact kernel-support distribution.
- Reference Q as a compact distribution in a similar location.
- Option B as a wider distribution at a different location.
- Small vertical jitter to make overlapping supports easier to see.


Although the same example image may also be used in the Wasserstein Similarity Study, this Visual Similarity Study does not show Wasserstein-distance values to participants.


## Analysis of downloaded results


Use `study2_analysis.py` to analyze downloaded participant-result CSV files.


Expected analysis directory structure:


```text
Result_analysis/
├── study2_analysis.py
├── answer_key.csv
└── study2/
    ├── participant_01.csv
    ├── participant_02.csv
    ├── participant_03.csv
    └── participant_04.csv
```


Each downloaded participant CSV must contain:


```csv
Question,Your Answer
Q1,Option A
Q2,Option B
Q3,Option A
```


The answer key must contain:


```csv
Question,Correct Answer
Q1,Option B
Q2,Option A
Q3,Option B
```


The answer key is used only for post-study analysis. It is not exposed to participants during the study.


The analysis script supports any number of participant CSV files. It generates:


```text
study_analysis/
├── all_responses_merged.csv
├── question_summary.csv
├── response_matrix.csv
├── response_matrix.xlsx
├── pairwise_agreement.csv
├── participant_accuracy.png
├── question_accuracy.png
├── option_selection_by_question.png
├── response_heatmap.png
└── pairwise_agreement_heatmap.png
```


Run the analysis with:


```bash
python study2_analysis.py
```


### Analysis outputs


| Output | Description |
|---|---|
| `all_responses_merged.csv` | All participant responses merged with the answer key for analysis |
| `question_summary.csv` | Per-question counts for selected A, selected B, answer-key matches, and majority choice |
| `response_matrix.csv` | Matrix of participant A/B selections for every question |
| `response_matrix.xlsx` | Formatted response matrix with answer-key matches highlighted in light green |
| `pairwise_agreement.csv` | Percentage agreement between every pair of participants |
| `participant_accuracy.png` | Agreement with the answer key for each participant |
| `question_accuracy.png` | Agreement with the answer key for each question |
| `option_selection_by_question.png` | Grouped bar chart of Selected A, Selected B, and majority response by question |
| `response_heatmap.png` | Participant response matrix with answer-key matches highlighted in light green |
| `pairwise_agreement_heatmap.png` | Heatmap showing pairwise agreement between participants |


## Deployment with Streamlit Community Cloud


To create a shareable application link:


1. Push this repository to GitHub.
2. Go to [Streamlit Community Cloud](https://share.streamlit.io/).
3. Sign in with GitHub.
4. Select **Create app**.
5. Choose this repository and the desired branch, usually `main`.
6. Set the main file path to:


   ```text
   app.py
   ```


7. Click **Deploy**.
8. Copy and share the generated `streamlit.app` link.


A `requirements.txt` file should be placed in the repository root, or beside the Streamlit entry file, so Streamlit Community Cloud can install the required dependencies.


## Theme configuration


The application is configured for light mode. Create:


```text
.streamlit/config.toml
```


with:


```toml
[theme]
base = "light"
```


## Reproducibility notes


- Keep all question images under version control.
- Use stable question identifiers such as Q1 to Q20.
- Keep the same image filenames and folder structure across study runs.
- Record the Git commit hash used during data collection.
- Give each downloaded participant CSV a unique filename before analysis.