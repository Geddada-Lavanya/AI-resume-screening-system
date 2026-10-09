
import os
import re
import unicodedata
from uuid import uuid4

from flask import Flask, render_template, request
from PyPDF2 import PdfReader
from werkzeug.utils import secure_filename
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10 MB

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# 1. Load one fixed pretrained model
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)
model.eval()


# 2. Skills catalog organized by real-world domains.
# Keys are canonical skill names; values are alternative spellings.
SKILLS_BY_DOMAIN = {
    "Programming Languages": [
        "Python", "Java", "C", "C++", "C#", "JavaScript",
        "TypeScript", "Go", "Golang", "Rust", "Kotlin", "Swift",
        "PHP", "Ruby", "R", "Scala", "Perl", "Dart", "Objective-C",
        "MATLAB", "Julia", "Bash", "PowerShell", "SQL", "PL/SQL",
        "T-SQL", "Fortran", "COBOL", "Assembly"
    ],

    "Web Development": [
        "HTML", "CSS", "Sass", "Bootstrap", "Tailwind CSS",
        "React", "Angular", "Vue.js", "Next.js", "Nuxt.js",
        "Node.js", "Express.js", "Django", "Flask", "FastAPI",
        "Spring Boot", "ASP.NET", ".NET", "Laravel", "Ruby on Rails",
        "REST API", "GraphQL", "WebSockets", "jQuery",
        "Responsive Web Design", "Web Accessibility",
        "Progressive Web Apps", "Web Performance Optimization"
    ],

    "Mobile Development": [
        "Android Development", "iOS Development", "Flutter",
        "React Native", "Xamarin", "Jetpack Compose",
        "SwiftUI", "Android Studio", "Mobile App Development"
    ],

    "Data Analysis and BI": [
        "Data Analysis", "Data Analytics", "Microsoft Excel",
        "Power BI", "Tableau", "Looker", "Looker Studio",
        "Qlik Sense", "DAX", "Power Query", "Pivot Tables",
        "Data Visualization", "Business Intelligence",
        "Statistical Analysis", "Exploratory Data Analysis",
        "Data Cleaning", "Data Wrangling", "Reporting",
        "KPI Reporting", "A/B Testing", "Hypothesis Testing"
    ],

    "Databases and Data Engineering": [
        "MySQL", "PostgreSQL", "SQLite", "Oracle Database",
        "Microsoft SQL Server", "MongoDB", "Redis", "Cassandra",
        "DynamoDB", "Elasticsearch", "Neo4j", "Snowflake",
        "Databricks", "Apache Spark", "PySpark", "Hadoop",
        "Apache Kafka", "Apache Airflow", "dbt", "ETL",
        "ELT", "Data Warehousing", "Data Modeling",
        "Data Pipelines", "Data Lake", "Data Lakehouse",
        "Azure Data Factory", "Azure Data Lake Storage",
        "Azure Synapse Analytics", "Amazon Redshift",
        "Amazon S3", "Google BigQuery", "Fivetran",
        "Informatica", "Talend", "SSIS", "Data Governance"
    ],

    "Artificial Intelligence and Machine Learning": [
        "Artificial Intelligence", "Machine Learning",
        "Deep Learning", "Natural Language Processing",
        "Computer Vision", "Reinforcement Learning",
        "Supervised Learning", "Unsupervised Learning",
        "Feature Engineering", "Model Training",
        "Model Evaluation", "Model Deployment",
        "Scikit-learn", "TensorFlow", "Keras", "PyTorch",
        "XGBoost", "LightGBM", "CatBoost", "OpenCV",
        "NumPy", "Pandas", "SciPy", "Matplotlib", "Seaborn",
        "Time Series Forecasting", "Recommendation Systems",
        "Anomaly Detection", "Classification", "Regression",
        "Clustering", "Information Retrieval", "OCR",
        "Speech Recognition", "Sentiment Analysis",
        "Named Entity Recognition", "Text Classification",
        "Object Detection", "Image Segmentation",
        "Model Interpretability", "MLOps", "MLflow",
        "Kubeflow", "ONNX"
    ],

    "Generative AI and LLMs": [
        "Generative AI", "Large Language Models",
        "Transformers", "Hugging Face", "LangChain",
        "LlamaIndex", "Retrieval-Augmented Generation",
        "Prompt Engineering", "Vector Databases",
        "FAISS", "ChromaDB", "Pinecone", "Weaviate",
        "Embeddings", "Semantic Search", "RAG Evaluation",
        "AI Agents", "Agentic AI", "Fine-Tuning",
        "LoRA", "QLoRA", "OpenAI API", "Gemini API",
        "Amazon Bedrock", "Azure OpenAI Service",
        "Responsible AI", "Guardrails", "Multimodal AI"
    ],

    "Cloud Computing": [
        "Amazon Web Services", "AWS", "Microsoft Azure",
        "Google Cloud Platform", "GCP", "EC2", "AWS Lambda",
        "Amazon S3", "Amazon RDS", "Amazon DynamoDB",
        "Amazon SageMaker", "Amazon Bedrock",
        "AWS IAM", "Amazon VPC", "Azure Virtual Machines",
        "Azure Functions", "Azure Blob Storage",
        "Azure Databricks", "Azure Machine Learning",
        "Azure DevOps", "Google Cloud Run",
        "Google Cloud Storage", "Cloud Architecture",
        "Serverless Computing", "Cloud Security",
        "Cloud Migration", "Infrastructure as Code",
        "Terraform", "AWS CloudFormation"
    ],

    "DevOps and Software Engineering": [
        "Git", "GitHub", "GitLab", "Bitbucket",
        "Docker", "Kubernetes", "Jenkins", "GitHub Actions",
        "GitLab CI/CD", "CI/CD", "Linux", "Unix",
        "Bash Scripting", "Ansible", "Puppet", "Chef",
        "Prometheus", "Grafana", "ELK Stack",
        "Software Development Life Cycle", "Agile",
        "Scrum", "Kanban", "Microservices",
        "System Design", "Design Patterns",
        "Object-Oriented Programming", "Data Structures",
        "Algorithms", "Unit Testing", "Integration Testing",
        "Test-Driven Development", "Code Review"
    ],

    "Cybersecurity": [
        "Cybersecurity", "Information Security",
        "Network Security", "Application Security",
        "Penetration Testing", "Ethical Hacking",
        "Vulnerability Assessment", "SIEM",
        "Incident Response", "Digital Forensics",
        "Identity and Access Management", "IAM",
        "OAuth 2.0", "OpenID Connect", "SAML",
        "Zero Trust Security", "Cryptography",
        "Encryption", "Firewalls", "OWASP Top 10",
        "Burp Suite", "Wireshark", "Nmap",
        "Security Auditing", "Risk Assessment",
        "SOC Operations", "Compliance"
    ],

    "Networking and IT Support": [
        "Computer Networks", "TCP/IP", "DNS", "DHCP",
        "HTTP", "HTTPS", "VPN", "LAN", "WAN",
        "Routing", "Switching", "Cisco Networking",
        "Network Troubleshooting", "Load Balancing",
        "Proxy Servers", "Active Directory",
        "Windows Server", "IT Support", "System Administration",
        "Help Desk", "Technical Support", "ITIL"
    ],

    "Testing and Quality Assurance": [
        "Software Testing", "Manual Testing", "Automation Testing",
        "Selenium", "Playwright", "Cypress", "Appium",
        "Postman", "REST Assured", "JUnit", "PyTest",
        "TestNG", "JMeter", "Load Testing", "Performance Testing",
        "API Testing", "Regression Testing", "Bug Tracking",
        "Jira", "Quality Assurance"
    ],

    "Enterprise and Business Platforms": [
        "Salesforce", "Salesforce Apex", "Lightning Web Components",
        "ServiceNow", "ServiceNow CSA", "ServiceNow CAD",
        "SAP", "SAP ABAP", "SAP HANA", "Workday",
        "Microsoft Dynamics 365", "SharePoint",
        "Power Automate", "Power Apps", "UiPath",
        "Robotic Process Automation", "Business Analysis",
        "Requirements Gathering", "Process Mapping"
    ],

    "Design and Product": [
        "Figma", "Adobe XD", "Adobe Photoshop",
        "Adobe Illustrator", "UI Design", "UX Design",
        "Wireframing", "Prototyping", "Usability Testing",
        "Design Thinking", "Product Management",
        "Product Analytics", "Roadmapping"
    ],

    "Project and Communication Skills": [
        "Communication", "Teamwork", "Leadership",
        "Problem Solving", "Critical Thinking",
        "Time Management", "Adaptability", "Collaboration",
        "Stakeholder Management", "Presentation Skills",
        "Documentation", "Decision Making", "Mentoring",
        "Conflict Resolution", "Analytical Thinking"
    ],

    "Finance and Operations": [
        "Financial Analysis", "Financial Modeling",
        "Accounting", "Bookkeeping", "Auditing",
        "Budgeting", "Forecasting", "Risk Management",
        "Investment Analysis", "Accounts Payable",
        "Accounts Receivable", "Supply Chain Management",
        "Inventory Management", "Demand Forecasting",
        "Procurement", "Logistics", "Operations Research"
    ],

    "Marketing and Sales": [
        "Digital Marketing", "SEO", "SEM", "Google Analytics",
        "Content Marketing", "Email Marketing", "Social Media Marketing",
        "Market Research", "CRM", "Lead Generation",
        "Salesforce CRM", "Sales Strategy", "Customer Success",
        "Customer Relationship Management", "Brand Management"
    ],

    "Scientific and Engineering Tools": [
        "AutoCAD", "CAD", "SolidWorks", "CATIA",
        "ANSYS", "MATLAB Simulink", "Revit", "GIS",
        "Geographic Information Systems", "ArcGIS",
        "LabVIEW", "Embedded Systems", "Arduino",
        "Raspberry Pi", "Internet of Things", "IoT",
        "PLC Programming", "Robotics", "Control Systems"
    ],

    "Research and Education": [
        "Research Methodology", "Technical Writing",
        "Literature Review", "Academic Writing",
        "Curriculum Development", "Instructional Design",
        "Learning Management Systems", "Data Collection",
        "Experimental Design", "Scientific Computing"
    ]
}


# 3. Optional aliases for common variations.
# Add aliases carefully to avoid false matches.
SKILL_ALIASES = {
    "JavaScript": ["ECMAScript"],
    "TypeScript": ["TS"],
    "C++": ["CPP"],
    "C#": ["C sharp"],
    "Node.js": ["Node JS"],
    "React": ["React.js"],
    "Vue.js": ["Vue JS"],
    "Next.js": ["Next JS"],
    "Express.js": ["Express JS", "Express"],
    "Scikit-learn": ["Scikit learn", "sklearn"],
    "PySpark": ["Python Spark"],
    "PostgreSQL": ["Postgres"],
    "Microsoft SQL Server": ["MS SQL Server", "MSSQL"],
    "Amazon Web Services": ["AWS Cloud"],
    "Google Cloud Platform": ["Google Cloud"],
    "Large Language Models": ["Large Language Model"],
    "Natural Language Processing": ["NLP"],
    "Computer Vision": ["CV"],
    "Retrieval-Augmented Generation": ["Retrieval Augmented Generation"],
    "CI/CD": ["Continuous Integration", "Continuous Delivery"],
    "Object-Oriented Programming": ["OOP", "Object Oriented Programming"],
    "Robotic Process Automation": ["RPA"],
    "Internet of Things": ["IoT"],
    "Geographic Information Systems": ["GIS"],
    "Business Intelligence": ["BI"],
    "Exploratory Data Analysis": ["EDA"]
}


# 4. Build a flat catalog of canonical skill names.
ALL_SKILLS = sorted({
    skill
    for domain_skills in SKILLS_BY_DOMAIN.values()
    for skill in domain_skills
})


# 5. Normalize whitespace and Unicode without destroying meaning.
def normalize_text(text):
    text = unicodedata.normalize("NFKC", text or "")
    text = text.replace("\x00", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# Skill matching uses lowercase text but preserves symbols like +, # and .
def normalize_for_skills(text):
    return normalize_text(text).casefold()


def extract_text(pdf_path):
    reader = PdfReader(pdf_path)
    pages = []

    for page in reader.pages:
        page_text = page.extract_text() or ""
        pages.append(page_text)

    return normalize_text(" ".join(pages))


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def skill_variations(skill):
    variations = [skill]
    variations.extend(SKILL_ALIASES.get(skill, []))
    return variations


def contains_skill(text, skill):
    """
    Match a complete skill phrase or its known aliases.
    Avoid matching 'java' inside 'javascript'.
    """
    for variation in skill_variations(skill):
        pattern = (
            r"(?<!\w)"
            + re.escape(variation.casefold())
            + r"(?!\w)"
        )

        if re.search(pattern, text, flags=re.IGNORECASE):
            return True

    return False


def find_missing_skills(resume_text, job_text):
    resume_normalized = normalize_for_skills(resume_text)
    job_normalized = normalize_for_skills(job_text)

    required_skills = [
        skill for skill in ALL_SKILLS
        if contains_skill(job_normalized, skill)
    ]

    present_skills = [
        skill for skill in required_skills
        if contains_skill(resume_normalized, skill)
    ]

    missing_skills = [
        skill for skill in required_skills
        if skill not in present_skills
    ]

    return required_skills, present_skills, missing_skills


def calculate_similarity(resume_text, job_text):
    """
    Use the same model and consistent preprocessing each time.
    Do not remove punctuation or digits before generating embeddings.
    """
    resume_text = normalize_text(resume_text)
    job_text = normalize_text(job_text)

    if not resume_text or not job_text:
        raise ValueError("Resume text and job description cannot be empty.")

    resume_embedding = model.encode(
        [resume_text],
        normalize_embeddings=True,
        convert_to_numpy=True,
        show_progress_bar=False
    )

    job_embedding = model.encode(
        [job_text],
        normalize_embeddings=True,
        convert_to_numpy=True,
        show_progress_bar=False
    )

    similarity = float(
        cosine_similarity(resume_embedding, job_embedding)[0, 0]
    )

    # Keep the raw cosine value for interpretation.
    # The percentage is a display format, not a hiring probability.
    score = round(similarity * 100, 2)

    return score, similarity


@app.route("/", methods=["GET", "POST"])
def index():
    score = None
    missing_skills = []
    required_skills = []
    present_skills = []
    error = None

    if request.method == "POST":
        file = request.files.get("resume")
        job_desc = request.form.get("job_desc", "")

        if not file or not file.filename:
            error = "Please upload a PDF resume."
        elif not allowed_file(file.filename):
            error = "Only PDF files are allowed."
        elif not normalize_text(job_desc):
            error = "Please enter a job description."
        else:
            safe_name = secure_filename(file.filename)

            # Unique name avoids overwriting files with the same name.
            filename = f"{uuid4().hex}_{safe_name}"
            filepath = os.path.join(
                app.config["UPLOAD_FOLDER"], filename
            )

            try:
                file.save(filepath)

                resume_text = extract_text(filepath)

                if not resume_text:
                    raise ValueError(
                        "No readable text found. "
                        "The PDF may be scanned or image-only."
                    )

                score, raw_similarity = calculate_similarity(
                    resume_text, job_desc
                )

                required_skills, present_skills, missing_skills = (
                    find_missing_skills(resume_text, job_desc)
                )

                if not required_skills:
                    missing_skills = [
                        "No skills from the current catalog "
                        "were detected in the job description."
                    ]
                elif not missing_skills:
                    missing_skills = [
                        "No missing skills detected in the current catalog."
                    ]

            except Exception as exc:
                error = str(exc)

            finally:
                # Remove the uploaded file after processing.
                if os.path.exists(filepath):
                    os.remove(filepath)

    return render_template(
        "index.html",
        score=score,
        required_skills=required_skills,
        present_skills=present_skills,
        missing_skills=missing_skills,
        error=error
    )


@app.errorhandler(413)
def file_too_large(error):
    return "File too large. Maximum upload size is 10 MB.", 413


if __name__ == "__main__":
    # Debug mode should be enabled only during local development.
    app.run(debug=True)