# AI-Job-Agent
##video:https://youtube.com/shorts/l4n3hg3lDPI?feature=share
## Overview

AI Career Assistant is an intelligent web application that helps job seekers analyze their resumes, identify skill gaps, calculate ATS scores, and receive personalized job recommendations.

The system uses resume parsing, skill extraction, AI-powered analysis, and job matching techniques to provide users with career insights and suitable job opportunities.

---

## Features

### 📄 Resume Upload & Parsing

* Upload resumes in PDF format.
* Extracts text automatically from the uploaded resume.

### 🧠 AI Resume Analysis

* Uses Generative AI to analyze the resume.
* Generates detailed insights about the candidate's profile.

### 🛠 Skill Extraction

* Detects technical and professional skills from the resume.
* Displays extracted skills in an interactive dashboard.

### 📊 ATS Score Calculation

* Calculates an Applicant Tracking System (ATS) score.
* Helps users understand how ATS-friendly their resume is.

### 🎯 Skill Gap Analysis

* Identifies missing skills required for recommended jobs.
* Helps users improve their employability.

### 💼 Job Recommendation System

* Matches resume skills against job requirements.
* Provides ranked job recommendations with match percentages.

### 🌐 Live Job Search Integration

* Fetches real-time job opportunities using Job Search APIs.
* Displays company name, location, and application links.

### 🎨 Interactive Dashboard

* Modern and responsive user interface.
* Displays:

  * Resume details
  * ATS score
  * Skill analysis
  * Missing skills
  * AI insights
  * Recommended jobs

---

## System Workflow

Resume Upload
↓
Resume Parsing
↓
Skill Extraction
↓
ATS Score Analysis
↓
Skill Gap Detection
↓
AI Resume Analysis
↓
Job Recommendation Engine
↓
Live Job Search API
↓
Interactive Dashboard

---

## Technology Stack

### Frontend

* HTML5
* CSS3
* Jinja2 Templates

### Backend

* Python
* Flask

### Libraries

* pdfplumber
* pandas
* requests
* google-generativeai
* reportlab

### APIs

* Gemini AI
* RapidAPI Job Search API

---

## Project Structure

```text
AI JOB AGENT
│
├── app.py
├── resume_parser.py
├── skills.py
├── job_matcher.py
├── ats_analyzer.py
├── skill_gap.py
├── gemini_ai.py
├── job_api.py
├── jobs.csv
│
├── templates
│   ├── index.html
│   └── results.html
│
├── uploads
│
├── requirements.txt
└── README.md
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/AI-Job-Agent.git

cd AI-Job-Agent
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Application

```bash
python app.py
```

### Open Browser

```text
http://127.0.0.1:5000
```

---

## Example Output

### Resume Analysis

* Skills Detected
* ATS Score
* Missing Skills
* AI Insights

### Job Recommendations

| Job Title         | Match Score |
| ----------------- | ----------- |
| Python Developer  | 95%         |
| Backend Developer | 88%         |
| Data Analyst      | 76%         |

---

## Future Enhancements

* Resume Ranking System
* AI Interview Preparation
* Resume Builder
* Multi-Resume Comparison
* LinkedIn Profile Analysis
* Job Alert Notifications
* Cloud Deployment

---

## Academic Relevance

This project demonstrates concepts from:

* Artificial Intelligence
* Natural Language Processing
* Information Retrieval
* Web Development
* Data Processing
* Recommendation Systems

It is suitable as a Final Year Engineering Project and showcases practical applications of AI in career guidance and recruitment.

---

## Author
mohammed fahad
Developed as an AI-powered Career Assistance and Job Recommendation System using Flask, Python, Gemini AI, and Job Search APIs.

⭐ If you find this project useful, consider giving it a star on GitHub.
