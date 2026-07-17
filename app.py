from flask import Flask, render_template, request
from resume_parser import extract_text_from_pdf
from jobfit_model import calculate_job_match, extract_skills

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():

    score = None
    matching_skills = []
    missing_skills = []

    if request.method == "POST":

        resume_file = request.files["resume"]
        job_description = request.form["job_description"]

        # Save uploaded resume temporarily
        resume_path = "uploaded_resume.pdf"
        resume_file.save(resume_path)

        # Extract text from resume
        resume_text = extract_text_from_pdf(resume_path)

        # Calculate match score
        score = calculate_job_match(resume_text, job_description)

        # Extract skills
        resume_skills = extract_skills(resume_text)
        job_skills = extract_skills(job_description)

        # Find matching and missing skills
        matching_skills = list(set(resume_skills) & set(job_skills))
        missing_skills = list(set(job_skills) - set(resume_skills))

    return render_template(
        "index.html",
        score=score,
        matching_skills=matching_skills,
        missing_skills=missing_skills
    )


if __name__ == "__main__":
    app.run(debug=True)