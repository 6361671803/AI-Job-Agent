import re

COUNTRY_KEYWORDS = {
    "United States": [
        "usa", "united states", "u.s.", "us", "america", "american",
        "california", "new york", "texas", "florida", "chicago",
        "los angeles", "san francisco", "seattle", "austin",
        "new jersey", "massachusetts", "pennsylvania"
    ],
    "Canada": [
        "canada", "canadian", "toronto", "vancouver", "calgary",
        "montreal", "ottawa", "manitoba", "british columbia",
        "ontario", "quebec", "alberta"
    ],
    "United Kingdom": [
        "uk", "united kingdom", "england", "london", "manchester",
        "birmingham", "bristol", "scotland", "wales", "northern ireland",
        "british", "gb", "great britain"
    ],
    "India": [
        "india", "indian", "delhi", "mumbai", "bangalore", "hyderabad",
        "pune", "chennai", "kolkata", "gurgaon", "noida"
    ],
    "Australia": [
        "australia", "australian", "sydney", "melbourne", "brisbane",
        "perth", "adelaide", "auckland", "new zealand"
    ],
    "Germany": [
        "germany", "german", "berlin", "munich", "hamburg", "frankfurt",
        "cologne", "dusseldorf", "deutschland"
    ],
}

PHONE_PATTERNS = {
    "United States": r"\+?1[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}",
    "Canada": r"\+?1[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}",
    "United Kingdom": r"\+?44[-.\s]?\d{4}[-.\s]?\d{6}|\+?44\s?\d{3,5}\s?\d{6,8}",
    "India": r"\+?91[-.\s]?\d{10}",
    "Australia": r"\+?61[-.\s]?\d{2}[-.\s]?\d{4}[-.\s]?\d{4}",
    "Germany": r"\+?49[-.\s]?\d{3,4}[-.\s]?\d{3,10}",
}

UNIVERSITY_PATTERNS = {
    "United States": [
        "harvard", "stanford", "mit", "yale", "columbia", "princeton",
        "berkeley", "cornell", "penn", "caltech", "nyu", "duke",
        "northwestern", "carnegie mellon", "michigan", "illinois",
        "ucla", "usc", "georgia tech"
    ],
    "United Kingdom": [
        "oxford", "cambridge", "london school of economics", "imperial college",
        "university of london", "edinburgh", "manchester", "kings college"
    ],
    "India": [
        "iit", "delhi university", "mumbai university", "bangalore institute",
        "anna university", "delhi institute of technology"
    ],
    "Canada": [
        "mcgill", "university of toronto", "ubc", "mcmaster", "ryerson"
    ],
    "Australia": [
        "melbourne", "sydney", "unsw", "anu", "monash", "macquarie"
    ],
    "Germany": [
        "technische universitat", "humboldt", "heidelberg", "munich technical"
    ]
}

LANGUAGE_KEYWORDS = {
    "India": [
        "hindi", "tamil", "telugu", "bengali", "punjabi", "gujarati",
        "marathi", "malayalam", "kannada", "urdu"
    ],
    "Germany": [
        "german"
    ],
    "United Kingdom": [
        "welsh", "scottish gaelic", "irish gaelic", "gaelic"
    ],
    "Canada": [
        "french"
    ],
    "Australia": [
        "maori"
    ]
}


def _matches_keyword(keyword, text_lower):
    escaped = re.escape(keyword)
    if len(keyword) <= 3 and keyword.isalpha():
        pattern = rf"\b{escaped}\b"
    else:
        pattern = escaped
    return re.search(pattern, text_lower, re.IGNORECASE) is not None


def detect_country_from_resume(resume_text):
    """
    Detect country from resume by analyzing:
    - Geographic keywords (city/state mentions)
    - Phone number formats
    - University/institution names
    - Work location mentions

    Returns tuple: (detected_country, confidence_score)
    """
    if not resume_text:
        return "Any", 0

    text_lower = resume_text.lower()
    country_scores = {country: 0 for country in COUNTRY_KEYWORDS}

    # Check for country keywords
    for country, keywords in COUNTRY_KEYWORDS.items():
        for keyword in keywords:
            if _matches_keyword(keyword, text_lower):
                country_scores[country] += 1

    # Check for phone patterns
    for country, pattern in PHONE_PATTERNS.items():
        if re.search(pattern, resume_text, re.IGNORECASE):
            country_scores[country] += 2

    # Check for universities
    for country, universities in UNIVERSITY_PATTERNS.items():
        for university in universities:
            if _matches_keyword(university, text_lower):
                country_scores[country] += 3

    # Check for languages other than English
    for country, languages in LANGUAGE_KEYWORDS.items():
        for language in languages:
            if _matches_keyword(language, text_lower):
                country_scores[country] += 3

    # Find the country with highest score
    best_country, score = max(country_scores.items(), key=lambda x: x[1])

    # If score is 0 or very low, return "Any" (no clear detection)
    if score == 0:
        return "Any", 0

    # Confidence: normalize score (rough estimate)
    # Avoid overconfident low counts
    confidence = min(100, int((score / 6) * 100))
    confidence = max(confidence, 30)

    return best_country, confidence


def detect_languages_from_resume(resume_text):
    """Detect language keywords from resume text."""
    if not resume_text:
        return []

    text_lower = resume_text.lower()
    found = []
    for country, languages in LANGUAGE_KEYWORDS.items():
        for language in languages:
            if _matches_keyword(language, text_lower):
                found.append(language.capitalize())
                break

    return sorted(set(found))
