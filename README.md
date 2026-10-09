# AI Resume Screening System

A web-based NLP application that compares resumes with job descriptions using Sentence-BERT semantic similarity. It generates a match score and identifies missing skills to help users improve their resumes for job applications.

## Features

* Upload resumes in PDF format.
* Extract resume text using PyPDF2.
* Use Sentence-BERT embeddings to compare resumes with job descriptions.
* Generate a semantic similarity score from 0–100%.
* Identify required, present, and missing skills.
* Support a broad range of skills across multiple professional domains.
* Use skill aliases to recognize common alternative names for technologies and concepts.
* Display results through a responsive Flask-based web interface.
* Validate PDF uploads and handle errors.

## Tech Stack

* **Programming Language:** Python
* **Backend:** Flask
* **NLP Model:** Sentence-Transformers (`all-MiniLM-L6-v2`)
* **Similarity Calculation:** Scikit-learn cosine similarity
* **PDF Processing:** PyPDF2
* **Frontend:** HTML, CSS, JavaScript
* **Deep Learning Backend:** PyTorch, used by Sentence-Transformers

## Project Structure

```text
resume_matcher/
├── app.py
├── requirements.txt
├── .gitignore
├── templates/
│   └── index.html
└── uploads/          # Local uploads; excluded from Git
```

The `uploads/` directory is used locally to process uploaded resumes. Uploaded resumes should not be committed to the repository.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Geddada-Lavanya/AI-resume-screening-system.git
cd AI-resume-screening-system
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python app.py
```

Open the following URL in your browser:

http://127.0.0.1:5000/

The Sentence-Transformers model may need to download the first time the application runs.

## How It Works

1. The user uploads a resume in PDF format and enters a job description.
2. PyPDF2 extracts text from the uploaded resume.
3. The application normalizes the text before processing.
4. Sentence-BERT converts the resume and job description into numerical embeddings.
5. Cosine similarity calculates how semantically similar the two texts are.
6. The application identifies skills required by the job description using a predefined skill catalog and skill aliases.
7. The application compares the required skills with the resume and displays the present and missing skills.
8. The results are displayed on the web interface.

## Match Score Interpretation

The score represents semantic similarity between the resume and job description. It is not a guaranteed ATS score or a direct measure of a candidate's suitability.

The following ranges are illustrative:

* **0–20%:** Low semantic similarity
* **20–40%:** Limited semantic similarity
* **40–60%:** Moderate semantic similarity
* **60–80%:** High semantic similarity
* **80–100%:** Very high semantic similarity

Actual results depend on the wording, content, and relevance of the resume and job description.

## Skill Gap Analysis

The application uses a predefined catalog of skills organized by professional domain. It checks for required skills in the job description and identifies which of those skills are not detected in the resume.

For example:

**Required skills:** Python, Flask, SQL, teamwork

**Skills detected in resume:** Python, SQL

**Missing skills:** Flask, teamwork

Skill detection is based on text matching and known aliases, so it may not recognize every skill expressed in an unusual way. A skill reported as missing may still be present implicitly in the resume.

## Use Cases

* Students preparing for campus placements.
* Job seekers comparing their resumes with job descriptions.
* Identifying skill gaps before applying for a role.
* Improving resume alignment with job requirements.

## Future Improvements

* Highlight matched skills in resumes.
* Generate personalized resume improvement suggestions using generative AI.
* Support DOCX resumes.
* Add downloadable screening reports.
* Deploy the application to a cloud platform.
* Improve skill detection using advanced NLP techniques.

## Limitations

* Currently supports PDF resume uploads.
* Image-only or scanned PDFs may require OCR to extract text.
* Similarity scores should be treated as guidance, not hiring decisions.
* Skill detection depends on the predefined skill catalog and matching rules.

## Author

**Lavanya Geddada**

GitHub: https://github.com/Geddada-Lavanya
