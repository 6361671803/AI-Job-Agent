
from flask import Flask, render_template, request, send_file
from resume_parser import extract_text
from skills import find_skills
from job_matcher import match_jobs
from job_api import fetch_jobs
from third_party_job_api import fetch_adzuna_jobs
from gemini_ai import analyze_resume
from ats_analyzer import calculate_ats_score
from skills_gap import find_missing_skills
from country_detector import detect_country_from_resume, detect_languages_from_resume
import os
from dotenv import load_dotenv
from pdf_generator import generate_pdf

# Load environment variables from a .env file (if present)
load_dotenv()

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

COUNTRY_SEARCH_KEYWORDS = {
    "United States": ["united states", "usa", "america", "u.s.", "us"],
    "Canada": ["canada", "canadian"],
    "United Kingdom": ["united kingdom", "uk", "great britain", "gb", "england"],
    "India": ["india", "indian"],
    "Australia": ["australia", "australian"],
    "Germany": ["germany", "german", "deutschland"]
}


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        file = request.files["resume"]

        if not file:
            return "No file uploaded"

        os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            file.filename
        )

        file.save(filepath)

        # Extract Resume Text
        resume_text = extract_text(filepath)

        # Detect country from resume content
        detected_country, country_confidence = detect_country_from_resume(resume_text)
        detected_languages = detect_languages_from_resume(resume_text)

        # Use detected country, but allow override from form
        preferred_country = request.form.get("preferred_country", "Any") or "Any"
        if preferred_country == "Any":
            preferred_country = detected_country

        # Extract Skills
        skills = find_skills(resume_text)

        # Match Jobs
        job_results, no_country_matches = match_jobs(
            skills,
            preferred_country
        )
        country_note = None
        if no_country_matches:
            job_results, _ = match_jobs(skills, "Any")
            country_note = (
                f"No local jobs were found for {preferred_country}. "
                "Showing all job matches instead."
            )

        # Live jobs from API (use first detected skill as a simple keyword)
        live_jobs = None
        live_country_note = None
        live_enabled = os.getenv("LIVE_JOBS_ENABLED", "true").lower() in ("1", "true", "yes")
        if live_enabled:
            try:
                if len(skills) > 0:
                    live_jobs = fetch_jobs(skills[0], preferred_country)
                    # If API returned listings and user asked for a country, try to filter by location.
                    if live_jobs and live_jobs.get("data") and preferred_country.lower() != "any":
                        original = list(live_jobs.get("data") or [])
                        filtered = []
                        country_tokens = COUNTRY_SEARCH_KEYWORDS.get(
                            preferred_country,
                            [preferred_country.lower()]
                        )

                        for job in original:
                            location_text = " ".join([
                                str(job.get("job_city", "")),
                                str(job.get("job_country", "")),
                                str(job.get("job_state", "")),
                                str(job.get("job_region", "")),
                                str(job.get("job_title", "")),
                                str(job.get("employer_name", "")),
                                str(job.get("job_description", ""))
                            ]).lower()

                            if any(token in location_text for token in country_tokens):
                                filtered.append(job)

                        # If strict metadata filtering yields no results, try a looser keyword match.
                        if not filtered:
                            loose = []
                            for job in original:
                                combined = " ".join([
                                    str(job.get("job_title", "")),
                                    str(job.get("employer_name", "")),
                                    str(job.get("job_city", "")),
                                    str(job.get("job_country", "")),
                                    str(job.get("job_description", ""))
                                ]).lower()
                                if any(token in combined for token in country_tokens):
                                    loose.append(job)

                            if loose:
                                filtered = loose

                        # If still empty, keep original results but note that API didn't provide country-specific matches
                        if filtered:
                            live_jobs["data"] = filtered
                        else:
                            live_country_note = (
                                f"No country-specific live jobs were found for {preferred_country}. "
                                "Showing general live listings instead."
                            )
                            live_jobs["data"] = original
                else:
                    live_jobs = None
            except Exception as e:
                live_jobs = None
                print("Live jobs API error:", e)
        else:
            # live jobs disabled by env flag
            live_jobs = None

        # If live API provided no country-specific results, try Adzuna as a third-party source
        third_party_jobs = None
        third_party_note = None
        try:
            need_third_party = False
            if live_jobs is None:
                need_third_party = True
            elif live_jobs and not live_jobs.get("data"):
                need_third_party = True
            elif live_country_note:
                # API had general results but none matched country strictly — still try third-party for better local coverage
                need_third_party = True

            if need_third_party and len(skills) > 0:
                keyword = skills[0]
                try:
                    third_party_jobs = fetch_adzuna_jobs(keyword, preferred_country)
                    if third_party_jobs and third_party_jobs.get("data"):
                        third_party_note = f"Third-party results from Adzuna for {preferred_country}."
                except Exception as e:
                    third_party_jobs = None
                    third_party_note = f"Adzuna fetch error: {e}"
        except Exception:
            third_party_jobs = None
            third_party_note = None

        # ATS Score
        ats_score = calculate_ats_score(
            resume_text,
            skills
        )

        # Missing Skills
        missing_skills = find_missing_skills(
            skills,
            job_results
        )

        total_skills = len(skills)
        total_jobs = len(job_results)
        top_job = job_results[0]["title"] if job_results else "No Match"

        strengths = []
        weaknesses = []

        if len(skills) >= 5:
            strengths.append("Good technical skill set")
        else:
            weaknesses.append("Add more technical skills")

        if "project" in resume_text.lower():
            strengths.append("Projects section found")
        else:
            weaknesses.append("Projects section missing")

        if "experience" in resume_text.lower():
            strengths.append("Experience section found")
        else:
            weaknesses.append("Experience section missing")

        if "education" in resume_text.lower():
            strengths.append("Education section found")
        else:
            weaknesses.append("Education section missing")

        # AI Analysis
        try:
            ai_analysis = analyze_resume(
                resume_text
            )
        except Exception as e:
            ai_analysis = (
                f"AI Analysis Error: {str(e)}"
            )

        print("\n===== RESUME TEXT =====\n")
        print(resume_text)

        print("\n===== SKILLS FOUND =====\n")
        print(skills)

        print("\n===== JOB MATCHES =====\n")

        for job in job_results:
            print(
                job["title"],
                "-",
                str(job["score"]) + "%"
            )

        return render_template(
            "results.html",
            filename=file.filename,
            skills=skills,
            analysis=ai_analysis,
            ats_score=ats_score,
            missing_skills=missing_skills,
            jobs=job_results,
            total_skills=total_skills,
            total_jobs=total_jobs,
            top_job=top_job,
            strengths=strengths,
            weaknesses=weaknesses,
            live_jobs=live_jobs,
            preferred_country=preferred_country,
            detected_country=detected_country,
            detected_languages=detected_languages,
            country_confidence=round(country_confidence),
            country_note=country_note,
            live_country_note=live_country_note,
            third_party_jobs=third_party_jobs,
            third_party_note=third_party_note
        )

    return render_template("index.html")


@app.route("/download-report", methods=["POST"])
def download_report():
    # Receive report fields from form and generate PDF
    filename = request.form.get("filename", "")
    ats_score = request.form.get("ats_score", "")
    preferred_country = request.form.get("preferred_country", "Any")
    skills_raw = request.form.get("skills", "")
    missing_raw = request.form.get("missing_skills", "")
    analysis = request.form.get("analysis", "")

    skills = skills_raw.split("||") if skills_raw else []
    missing_skills = missing_raw.split("||") if missing_raw else []

    pdf_file = generate_pdf(
        filename,
        ats_score,
        skills,
        missing_skills,
        analysis,
        preferred_country
    )

    return send_file(pdf_file, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)

