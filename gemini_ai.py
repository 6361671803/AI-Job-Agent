import os
import re
from dotenv import load_dotenv

try:
    import google.genai as genai
    GENAI_PACKAGE = "genai"
except ImportError:
    try:
        import google.generativeai as genai
        GENAI_PACKAGE = "generativeai"
    except ImportError:
        genai = None
        GENAI_PACKAGE = None

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
model_name = os.getenv("GENAI_MODEL", "models/gemini-2.5-flash")
gemini_enabled = os.getenv("GEMINI_ENABLED", "true").lower() in ("1", "true", "yes")


def _fallback_analysis(resume_text):
    text = resume_text.lower()
    sections = {
        "skills": ["python", "java", "sql", "aws", "docker", "react", "node", "excel", "html", "css"],
        "experience": ["experience", "worked", "developed", "managed", "led", "implemented", "engineer"],
        "education": ["bachelor", "master", "phd", "university", "college", "degree", "diploma"],
    }

    found_skills = [skill for skill in sections["skills"] if skill in text]
    experience = any(keyword in text for keyword in sections["experience"])
    education = any(keyword in text for keyword in sections["education"])

    lines = [
        "AI resume analysis is running in fallback mode.",
        "This summary is based on resume text patterns rather than external Gemini AI.",
        "",
        "- Identified strengths:",
    ]

    if found_skills:
        lines.append(f"  • Skills detected: {', '.join(found_skills[:8])}")
    else:
        lines.append("  • No major technical skills detected from the resume text.")

    if experience:
        lines.append("  • Resume appears to include professional experience details.")
    else:
        lines.append("  • Experience details are not clearly described; add a stronger experience section.")

    if education:
        lines.append("  • Education is mentioned, so the resume likely includes academic background.")
    else:
        lines.append("  • Education section was not clearly detected; include university or degree details.")

    lines.append("")
    lines.append("- Suggested improvements:")
    lines.append("  • Add a clear summary or objective at the top.")
    lines.append("  • List quantified achievements and project outcomes.")
    lines.append("  • Match more job-specific keywords from the roles you want.")
    return "\n".join(lines)


def _is_quota_error(exc):
    message = str(exc).lower()
    return (
        "429" in message
        or "quota" in message
        or "rate limit" in message
        or "too many requests" in message
    )


def analyze_resume(resume_text):
    if not gemini_enabled or not api_key or genai is None:
        message = _fallback_analysis(resume_text)
        if not gemini_enabled:
            message = (
                "AI analysis is running in local fallback mode because Gemini is disabled. "
                "Set GEMINI_ENABLED=true to enable external AI analysis if you have quota available.\n\n"
                + message
            )
        elif not api_key:
            message = (
                "AI analysis is running in local fallback mode. "
                "Set GOOGLE_API_KEY in your .env file to enable Gemini analysis.\n\n" + message
            )
        elif genai is None:
            message = (
                "AI analysis is running in local fallback mode because no supported Gemini client is installed. "
                "Install the Google Generative AI SDK and restart the app.\n\n" + message
            )
        return message

    prompt = f"""
    Analyze this resume and provide:

    1. Skills
    2. Experience
    3. Education
    4. Suggested Job Roles
    5. Strengths
    6. Improvement Suggestions

    Resume:
    {resume_text}
    """

    try:
        if GENAI_PACKAGE == "genai":
            client = genai.client.Client(api_key=api_key)
            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )
            return getattr(response, "text", str(response))

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        return response.text

    except Exception as exc:
        fallback = _fallback_analysis(resume_text)
        if _is_quota_error(exc):
            return (
                "Gemini quota or rate limit exceeded. Using local fallback analysis instead. "
                "Please wait for quota reset, upgrade your Google Cloud project, or set GEMINI_ENABLED=false to avoid Gemini calls.\n\n"
                f"{fallback}"
            )
        return (
            f"AI Analysis Error: {exc}\n\n"
            "Fallback analysis is shown below:\n\n"
            f"{fallback}"
        )
