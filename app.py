
from flask import Flask, render_template, request
import os
import re
from PyPDF2 import PdfReader
from werkzeug.utils import secure_filename

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create uploads folder
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Load model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Clean text
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z ]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text

# Extract PDF text
def extract_text(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text

# Skill database
skills_db = [
    "python", "java", "c", "c++", "sql",
    "machine learning", "data analysis", "deep learning",
    "flask", "django", "react", "html", "css", "javascript",
    "autocad", "cad",
    "communication", "teamwork", "problem solving"
]

@app.route("/", methods=["GET", "POST"])
def index():
    score = None
    missing_skills = []

    if request.method == "POST":
        file = request.files["resume"]
        job_desc = request.form["job_desc"]

        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            resume_text = extract_text(filepath)

            # Clean text
            resume_clean = clean_text(resume_text)
            job_clean = clean_text(job_desc)

            # Sentence-BERT similarity
            resume_embedding = model.encode([resume_clean])
            job_embedding = model.encode([job_clean])

            similarity = cosine_similarity(resume_embedding, job_embedding)[0][0]
            score = round(similarity * 100, 2)

            # Skill matching
            resume_words = set(resume_clean.split())
            job_words = set(job_clean.split())

            for skill in skills_db:
                skill_tokens = skill.split()

                # skill present in job
                if all(token in job_words for token in skill_tokens):

                    # skill missing in resume
                    if not all(token in resume_words for token in skill_tokens):
                        missing_skills.append(skill)

            # If no missing skills
            if not missing_skills:
                missing_skills = ["No major skill gaps found ✅"]

    return render_template("index.html", score=score, missing_skills=missing_skills)

if __name__ == "__main__":
    app.run(debug=True)