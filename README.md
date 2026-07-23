# 🚀 Smart JobFit AI

**Smart JobFit AI** is an advanced AI-powered Resume Matcher and ATS Optimizer. It uses **hybrid Natural Language Processing (NLP)**—combining **SBERT (Sentence-Transformers)** for semantic context understanding and **TF-IDF N-gram vectorization** for keyword alignment—to calculate a precise **Job Match Score**, extract matching/missing skills dynamically, and provide actionable AI optimization tips.

![Smart JobFit AI Interface](images/home.png)

---

## ✨ Features

- **Hybrid Semantic Match Score**: Combines SBERT dense embeddings (60%) with lexical TF-IDF N-gram matching (40%) to evaluate true relevance beyond basic word matching.
- **Dynamic NLP Skill Extraction**: Auto-detects technical skills, frameworks, cloud tools, and domain acronyms without relying on rigid hardcoded lists.
- **Actionable AI Recommendations**: Generates tailored advice to help job seekers optimize missing keywords and resume sections.
- **RESTful API Endpoint**: Exposes a `/api/analyze` POST endpoint for programmatic integrations.
- **In-Memory File Processing**: High-concurrency safe PDF parsing with no temporary disk file race conditions.
- **Modern Glassmorphic UI**: Fast, responsive, dark-mode dashboard built with CSS3, HTML5, and FontAwesome icons.
- **Dockerized & Test-Covered**: Includes `Dockerfile` and comprehensive unit test suite via `pytest`.

---

## 🛠️ Technology Stack

- **Core Engine**: Python 3.10+, Flask
- **Machine Learning & NLP**: Scikit-Learn, PyPDF2, SBERT (`sentence-transformers/all-MiniLM-L6-v2`), NLTK / Regex NLP
- **Testing & DevOps**: Pytest, Docker
- **Frontend**: HTML5, CSS3 Glassmorphism, FontAwesome, Google Fonts (Plus Jakarta Sans)

---

## 📁 Project Structure

```
Smart-JobFit-AI/
│
├── app.py                  # Flask web server & REST API endpoints
├── jobfit_model.py         # Hybrid SBERT + TF-IDF engine & skill extraction
├── resume_parser.py        # PDF text extractor and string normalizer
├── requirements.txt        # Python package dependencies
├── Dockerfile              # Docker container setup
├── .dockerignore           # Excluded files for container builds
├── README.md               # Documentation
│
├── templates/
│   └── index.html          # Modern glassmorphism web dashboard
│
└── tests/
    └── test_app.py         # Pytest unit testing suite
```

---

## 🚀 Getting Started

### 1. Local Setup

```bash
# Clone the repository
git clone https://github.com/ushravya09-prog/Smart-JobFit-AI.git
cd Smart-JobFit-AI

# Install dependencies
pip install -r requirements.txt

# Run the Flask application
python app.py
```
Open your browser and navigate to `http://localhost:5000`.

---

### 2. Running Unit Tests

Run `pytest` to execute automated test cases covering text parsing, hybrid matching, skill extraction, and Flask routes:

```bash
pytest tests/
```

---

### 3. Running with Docker 🐳

```bash
# Build the Docker image
docker build -t smart-jobfit-ai .

# Run the container
docker run -p 5000:5000 smart-jobfit-ai
```

---

## 🌐 REST API Usage

You can programmatically analyze resumes by making a POST request to `/api/analyze`:

```bash
curl -X POST http://localhost:5000/api/analyze \
  -F "resume=@path/to/resume.pdf" \
  -F "job_description=Looking for Python developer with Flask and Docker experience."
```

### Sample Response:

```json
{
  "scores": {
    "overall_score": 82.5,
    "semantic_score": 85.0,
    "keyword_score": 78.8
  },
  "matching_skills": ["python", "flask", "docker"],
  "missing_skills": ["kubernetes", "aws"],
  "recommendations": [
    "🌟 **Excellent Match**: Your resume strongly aligns with this job description!"
  ]
}
```

---

## 👤 Author

**Shravya U**  
*Artificial Intelligence & Machine Learning Student*