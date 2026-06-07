import os
import requests

# Map common country display names to Adzuna country codes
ADZUNA_COUNTRY_CODES = {
    "United States": "us",
    "United Kingdom": "gb",
    "Canada": "ca",
    "Australia": "au",
    "India": "in",
    "Germany": "de",
    "Any": "us"
}


def fetch_adzuna_jobs(keyword="Python Developer", country="Any", results_per_page=10):
    """Fetch jobs from Adzuna API.

    Requires ADZUNA_APP_ID and ADZUNA_APP_KEY in environment.

    Returns parsed JSON list of job dicts or raises RuntimeError.
    """
    app_id = os.getenv("ADZUNA_APP_ID")
    app_key = os.getenv("ADZUNA_APP_KEY")
    if not app_id or not app_key:
        raise RuntimeError("ADZUNA_APP_ID or ADZUNA_APP_KEY not set in environment.")

    country_code = ADZUNA_COUNTRY_CODES.get(country, "us")
    url = f"https://api.adzuna.com/v1/api/jobs/{country_code}/search/1"

    params = {
        "app_id": app_id,
        "app_key": app_key,
        "what": keyword,
        "results_per_page": results_per_page,
        "content-type": "application/json"
    }

    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    # Normalize to list of jobs with expected fields similar to our live API
    jobs = []
    for item in data.get("results", []):
        jobs.append({
            "job_title": item.get("title"),
            "employer_name": item.get("company", {}).get("display_name"),
            "job_city": item.get("location" , {}).get("area", [None])[-1] if item.get("location") else None,
            "job_country": country,
            "job_description": item.get("description"),
            "job_apply_link": item.get("redirect_url")
        })

    return {"data": jobs}
