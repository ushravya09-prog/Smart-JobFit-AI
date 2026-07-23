from io import BytesIO
from flask import Flask, render_template, request, jsonify
from resume_parser import extract_text_from_pdf
from jobfit_model import calculate_job_match, extract_skills, generate_recommendations

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max upload limit


@app.route("/", methods=["GET", "POST"])
def index():
    scores = None
    matching_skills = []
    missing_skills = []
    recommendations = []
    error_message = None

    if request.method == "POST":
        try:
            if "resume" not in request.files or not request.files["resume"].filename:
                error_message = "Please upload a valid PDF resume."
                return render_template("index.html", error_message=error_message)

            resume_file = request.files["resume"]
            job_description = request.form.get("job_description", "").strip()

            if not job_description:
                error_message = "Please enter a job description."
                return render_template("index.html", error_message=error_message)

            # Read PDF in-memory cleanly (avoids single-file collision)
            pdf_bytes = BytesIO(resume_file.read())
            resume_text = extract_text_from_pdf(pdf_bytes)

            if not resume_text or len(resume_text.strip()) == 0:
                error_message = "Could not extract text from the uploaded PDF. Please make sure it is not scanned/image-only."
                return render_template("index.html", error_message=error_message)

            # Calculate hybrid match scores
            scores = calculate_job_match(resume_text, job_description)

            # Extract skills dynamically
            resume_skills = extract_skills(resume_text)
            job_skills = extract_skills(job_description)

            # Compute skill overlap
            matching_skills = sorted(list(set(resume_skills) & set(job_skills)))
            missing_skills = sorted(list(set(job_skills) - set(resume_skills)))

            # Generate actionable recommendations
            recommendations = generate_recommendations(
                matching_skills,
                missing_skills,
                scores["overall_score"]
            )

        except Exception as e:
            error_message = f"An error occurred while processing: {str(e)}"

    return render_template(
        "index.html",
        scores=scores,
        matching_skills=matching_skills,
        missing_skills=missing_skills,
        recommendations=recommendations,
        error_message=error_message
    )


@app.route("/api/analyze", methods=["POST"])
def api_analyze():
    """REST API endpoint for programmatic resume analysis."""
    if "resume" not in request.files or "job_description" not in request.form:
        return jsonify({"error": "Missing resume file or job_description parameter"}), 400

    try:
        resume_file = request.files["resume"]
        job_description = request.form["job_description"]

        pdf_bytes = BytesIO(resume_file.read())
        resume_text = extract_text_from_pdf(pdf_bytes)

        scores = calculate_job_match(resume_text, job_description)
        resume_skills = extract_skills(resume_text)
        job_skills = extract_skills(job_description)

        matching_skills = sorted(list(set(resume_skills) & set(job_skills)))
        missing_skills = sorted(list(set(job_skills) - set(resume_skills)))
        recommendations = generate_recommendations(
            matching_skills, missing_skills, scores["overall_score"]
        )

        return jsonify({
            "scores": scores,
            "matching_skills": matching_skills,
            "missing_skills": missing_skills,
            "recommendations": recommendations
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)