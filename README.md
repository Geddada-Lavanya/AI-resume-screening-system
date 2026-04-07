# 🚀 AI-resume-screening-system

A web-based NLP application that compares resumes with job descriptions and provides a match score along with skill gap analysis.

---

## 📌 Features

- 📄 Upload resume in PDF format
- 🧠 Uses NLP (Sentence-BERT) for semantic similarity
- 📊 Generates match score (0–100%)
- 🔍 Identifies missing skills from job description
- 🌐 Simple and clean Flask-based UI

---

## 🛠️ Tech Stack

- Python
- Flask
- Sentence-Transformers (BERT-based model)
- Scikit-learn
- PyPDF2

---

## 📂 Project Structure

resume_matcher/
│── app.py
│── templates/
│ └── index.html
│── uploads/


---

---

## ⚙️ Installation

1. Clone the repository:

git clone https://github.com/Geddada-Lavanya/AI-resume-screening-system.git

cd resume-matcher


2. Install dependencies:
  pip install flask sentence-transformers scikit-learn PyPDF2

---

## ▶️ Run the App


python app.py


Open in browser:

http://127.0.0.1:5000/


---

## 🧠 How It Works

1. Resume is uploaded (PDF)
2. Text is extracted using PyPDF2
3. Text is cleaned and preprocessed
4. Sentence-BERT converts text into embeddings
5. Cosine similarity is used to calculate match score
6. Skill gap is identified using keyword matching

---

## 📊 Match Score Interpretation

- 0–20% → Low match
- 20–40% → Basic match
- 40–60% → Moderate match
- 60–80% → Good match
- 80–100% → Strong match

---

## 🔍 Example Output
Match Score: 62.4%

Missing Skills:

python
flask
teamwork


---

## 🚀 Future Improvements

- Highlight matched skills
- Add resume suggestions using AI
- Deploy on cloud (Render / Railway)
- Add support for DOCX files

---

## 🎯 Use Case

- Students preparing for placements
- Resume optimization before applying
- Quick ATS-style resume screening

---

## 📌 Author

Lavanya
