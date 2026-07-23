import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Global SBERT model cache for lazy loading
_sbert_model = None


def _load_sbert():
    global _sbert_model
    if _sbert_model is None:
        try:
            from sentence_transformers import SentenceTransformer
            # Load lightweight, high-performance sentence transformer
            _sbert_model = SentenceTransformer('all-MiniLM-L6-v2')
        except Exception:
            _sbert_model = False  # Soft fallback if model download fails or package missing
    return _sbert_model if _sbert_model is not False else None


# Broad Taxonomy of Common Technical Skills & Tools for Baseline Matching
COMMON_TECH_TAXONOMY = {
    # Programming Languages
    "python", "javascript", "typescript", "java", "c++", "c#", "go", "rust", "r", "ruby", "php", "swift", "kotlin", "scala", "html", "css", "sql",
    # Frameworks & Libraries
    "react", "angular", "vue", "next.js", "node.js", "express", "django", "flask", "fastapi", "spring boot", "bootstrap", "tailwind",
    # Machine Learning & AI / Data Science
    "machine learning", "deep learning", "artificial intelligence", "nlp", "computer vision", "tensorflow", "pytorch", "keras",
    "scikit-learn", "pandas", "numpy", "scipy", "opencv", "spacy", "nltk", "transformers", "langchain", "llm", "rag", "huggingface",
    "data analysis", "data visualization", "power bi", "tableau", "excel", "matplotlib", "seaborn",
    # Cloud, DevOps & Infrastructure
    "docker", "kubernetes", "aws", "azure", "gcp", "google cloud", "terraform", "ansible", "jenkins", "ci/cd", "git", "github", "gitlab",
    "linux", "bash", "shell", "nginx", "microservices", "rest api", "graphql", "kafka", "rabbitmq",
    # Databases & Big Data
    "postgresql", "mysql", "mongodb", "redis", "elasticsearch", "sqlite", "oracle", "snowflake", "spark", "hadoop", "databricks"
}


def extract_skills(text):
    """
    Dynamically extracts technical skills and domain keywords from text.
    Combines taxonomy matching with dynamic regex pattern detection.
    """
    if not text:
        return []

    text_lower = text.lower()
    found_skills = set()

    # 1. Match against extensive technology taxonomy
    for skill in COMMON_TECH_TAXONOMY:
        # Match as whole word / boundary phrase
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            found_skills.add(skill)

    # 2. Dynamic extraction: Technical acronyms & capitalized terms (e.g. AWS, REST, CI/CD, PyTorch)
    dynamic_acronyms = re.findall(r'\b[A-Z]{2,6}\b', text)
    for ac in dynamic_acronyms:
        if ac.lower() not in {"and", "the", "for", "with", "from", "that", "this", "your", "have"}:
            found_skills.add(ac.lower())

    # 3. Dynamic extraction: CamelCase / mixed tech terms (e.g. TensorFlow, MongoDB, PostgreSQL)
    dynamic_tech_terms = re.findall(r'\b[A-Z][a-z]+(?:[A-Z][a-z]+)+\b', text)
    for term in dynamic_tech_terms:
        found_skills.add(term.lower())

    return sorted(list(found_skills))


def calculate_tfidf_similarity(text1, text2):
    """Calculates TF-IDF N-gram lexical similarity score (0 to 100)."""
    if not text1 or not text2:
        return 0.0

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        sublinear_tf=True
    )
    try:
        tfidf_matrix = vectorizer.fit_transform([text1, text2])
        sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return float(sim * 100)
    except Exception:
        return 0.0


def calculate_semantic_similarity(text1, text2):
    """Calculates SBERT dense embedding semantic similarity score (0 to 100)."""
    model = _load_sbert()
    if model is None:
        # Fallback to TF-IDF if SBERT is unavailable
        return calculate_tfidf_similarity(text1, text2)

    try:
        embeddings = model.encode([text1, text2], convert_to_numpy=True)
        # Cosine similarity between 2 normalized embedding vectors
        sim = float(np.dot(embeddings[0], embeddings[1]) / (np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[1])))
        # Scale to percentage [0, 100]
        return max(0.0, min(100.0, float(sim * 100)))
    except Exception:
        return calculate_tfidf_similarity(text1, text2)


def calculate_job_match(resume_text, job_description):
    """
    Computes a hybrid ATS Job Match Score combining:
    - 60% Semantic Similarity (SBERT context & meaning)
    - 40% Lexical Keyword Similarity (TF-IDF N-grams)
    """
    if not resume_text or not job_description:
        return {
            "overall_score": 0.0,
            "semantic_score": 0.0,
            "keyword_score": 0.0
        }

    semantic_score = calculate_semantic_similarity(resume_text, job_description)
    keyword_score = calculate_tfidf_similarity(resume_text, job_description)

    # Hybrid Weighted ATS Score
    overall_score = (0.60 * semantic_score) + (0.40 * keyword_score)

    return {
        "overall_score": round(overall_score, 1),
        "semantic_score": round(semantic_score, 1),
        "keyword_score": round(keyword_score, 1)
    }


def generate_recommendations(matching_skills, missing_skills, overall_score):
    """
    Generates actionable improvement feedback for the candidate.
    """
    recommendations = []

    if overall_score >= 80:
        recommendations.append("🌟 **Excellent Match**: Your resume strongly aligns with this job description!")
    elif overall_score >= 60:
        recommendations.append("👍 **Good Match**: Your profile is relevant, but adding missing key terms will boost ATS ranking.")
    else:
        recommendations.append("⚠️ **Needs Optimization**: Consider tailoring your resume heavily toward the job requirements.")

    if missing_skills:
        top_missing = ", ".join([f"`{s}`" for s in missing_skills[:5]])
        recommendations.append(f"🎯 **Missing Key Skills**: Incorporate top required skills like {top_missing} into your experience bullet points.")

    if len(matching_skills) < 3:
        recommendations.append("💡 **Skill Visibility**: Highlight technical competencies in a dedicated 'Technical Skills' section.")

    recommendations.append("📝 **Action Verbs**: Ensure your bullet points use strong action verbs (e.g. *Engineered*, *Optimized*, *Architected*).")

    return recommendations


if __name__ == "__main__":
    print("===== Smart JobFit AI Engine Test =====")
    sample_resume = "Python Software Engineer with experience in Flask, SQL, Docker, Machine Learning, and AWS."
    sample_jd = "Looking for a Senior Python Developer with Docker, AWS, Kubernetes, and Machine Learning expertise."

    scores = calculate_job_match(sample_resume, sample_jd)
    resume_skills = extract_skills(sample_resume)
    jd_skills = extract_skills(sample_jd)

    matching = sorted(list(set(resume_skills) & set(jd_skills)))
    missing = sorted(list(set(jd_skills) - set(resume_skills)))

    print(f"Match Scores: {scores}")
    print(f"Matching Skills: {matching}")
    print(f"Missing Skills: {missing}")
    print(f"Recommendations: {generate_recommendations(matching, missing, scores['overall_score'])}")