# 🚀 Smart JobFit AI

Smart JobFit AI is a Machine Learning-based web application that compares a user's resume with a job description and calculates a Job Match Score using Natural Language Processing (NLP).

The application extracts text from a PDF resume, compares it with the job description using TF-IDF Vectorization and Cosine Similarity, and displays:
- 📊 Job Match Score
- ✅ Matching Skills
- ❌ Missing Skills

---

## Features

- Upload Resume (PDF)
- Paste Job Description
- Automatic Resume Text Extraction
- Job Match Percentage
- Matching Skills Detection
- Missing Skills Detection
- Clean Flask Web Interface

---

## Technologies Used

- Python
- Flask
- Scikit-learn
- TF-IDF Vectorizer
- Cosine Similarity
- PyPDF2
- HTML
- CSS

---

## Project Structure

```
Smart-JobFit-AI/
│
├── app.py
├── jobfit_model.py
├── resume_parser.py
├── requirements.txt
├── README.md
│
├── templates/
│   └── index.html
│
├── images/
│   └── home.png
```

---

## How It Works

1. Upload your resume in PDF format.
2. Enter a job description.
3. The application extracts text from the resume.
4. TF-IDF converts the resume and job description into numerical vectors.
5. Cosine Similarity calculates how closely they match.
6. Matching and missing skills are displayed along with the Job Match Score.

---

## Screenshot

![Smart JobFit AI](images/home.png)

---

## Future Improvements

- Resume recommendations
- ATS Resume Score
- Keyword Suggestions
- Resume Improvement Tips
- Multiple Resume Comparison
- Download Report as PDF

---

## Author

**Shravya U**

Artificial Intelligence & Machine Learning Student