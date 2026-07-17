from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from PyPDF2 import PdfReader


def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text


def calculate_job_match(resume_text, job_description):
    documents = [resume_text, job_description]

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity_score = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2]
    )[0][0]

    return round(similarity_score * 100, 2)


if __name__ == "__main__":

    print("===== Smart JobFit AI =====")

    pdf_path = input("\nEnter your resume PDF filename: ")

    resume_text = extract_text_from_pdf(pdf_path)

    job_description = input(
        "\nEnter the job description and required skills:\n"
    )

    score = calculate_job_match(resume_text, job_description)

    print("\n==============================")
    print(f"Job Match Score: {score}%")
    print("==============================")