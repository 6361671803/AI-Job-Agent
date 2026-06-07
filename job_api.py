import os
import requests


def fetch_jobs(keyword="Python Developer", country="Any"):
    """Fetch jobs from RapidAPI JSearch. Requires env var RAPIDAPI_KEY.

    Args:
        keyword: Job search keyword (usually a skill)
        country: Country to filter jobs by (e.g., "United States", "Canada")

    Returns the parsed JSON response.
    """
    api_key = os.getenv("RAPIDAPI_KEY")
    if not api_key:
        raise RuntimeError(
            "RAPIDAPI_KEY not set. Set the RAPIDAPI_KEY environment variable to use the live jobs API."
        )

    url = "https://jsearch.p.rapidapi.com/search"

    # Enhance query with country if specified
    query = keyword
    if country and country.lower() != "any":
        query = f"{keyword} jobs in {country}"

    querystring = {
        "query": query,
        "page": "1",
        "num_pages": "1"
    }

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }

    response = requests.get(
        url,
        headers=headers,
        params=querystring
    )

    response.raise_for_status()
    return response.json()
