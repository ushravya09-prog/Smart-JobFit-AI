import io
import pytest
from app import app
from resume_parser import extract_text_from_pdf
from jobfit_model import (
    extract_skills,
    calculate_tfidf_similarity,
    calculate_job_match,
    generate_recommendations
)


def test_extract_skills_taxonomy_and_acronyms():
    sample_text = "Experienced Senior Python Developer with Docker, AWS, Kubernetes, and REST API experience."
    skills = extract_skills(sample_text)

    assert "python" in skills
    assert "docker" in skills
    assert "aws" in skills
    assert "kubernetes" in skills
    assert "rest api" in skills


def test_calculate_job_match_structure():
    resume = "Python developer experienced in Flask, SQL, Docker, and Git."
    jd = "Seeking Python Engineer with Flask and SQL skills."

    match_result = calculate_job_match(resume, jd)

    assert "overall_score" in match_result
    assert "semantic_score" in match_result
    assert "keyword_score" in match_result
    assert 0 <= match_result["overall_score"] <= 100


def test_generate_recommendations():
    matching = ["python", "flask"]
    missing = ["docker", "aws"]
    recs = generate_recommendations(matching, missing, overall_score=65.0)

    assert len(recs) > 0
    assert any("Missing Key Skills" in r for r in recs)


def test_flask_index_get():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"Smart JobFit AI" in response.data


def test_flask_api_analyze_missing_params():
    client = app.test_client()
    response = client.post("/api/analyze", data={})
    assert response.status_code == 400
