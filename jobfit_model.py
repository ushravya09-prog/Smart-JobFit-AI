from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_job_match(resume_text, job_description):
    """
    Calculate the similarity between a resume and a job description.
    """

    documents = [resume_text, job_description]

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity_score = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2]
    )[0][0]

    match_percentage = round(similarity_score * 100, 2)

    return match_percentage


if __name__ == "__main__":

    resume = """
    Python developer with experience in machine learning,
    pandas, numpy, scikit-learn, and data analysis.
    """

    job_description = """
    Looking for a Machine Learning Engineer with skills in Python,
    machine learning, pandas, numpy, and scikit-learn.
    """

    score = calculate_job_match(resume, job_description)

    print(f"Job Match Score: {score}%")