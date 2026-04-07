from flask import Flask, render_template, request
import os
import re
from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Clean text
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z ]', '', text)
    return text

# Extract text from PDF
def extract_text(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

@app.route("/", methods=["GET", "POST"])
def index():
    score = None
    missing_skills = None

    if request.method == "POST":
        file = request.files["resume"]
        job_desc = request.form["job_desc"]

        if file:
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)

            resume_text = extract_text(filepath)

            # Preprocess
            resume_clean = clean_text(resume_text)
            job_clean = clean_text(job_desc)

            # TF-IDF
            vectorizer = TfidfVectorizer(stop_words='english')
            vectors = vectorizer.fit_transform([resume_clean, job_clean])

            # Similarity
            similarity = cosine_similarity(vectors[0], vectors[1])[0][0]
            score = round(similarity * 100, 2)

            # Skill gap
            resume_words = set(resume_clean.split())
            job_words = set(job_clean.split())
            missing_skills = list(job_words - resume_words)[:10]

    return render_template("index.html", score=score, missing_skills=missing_skills)

if __name__ == "__main__":
    app.run(debug=True)