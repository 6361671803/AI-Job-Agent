def find_missing_skills(resume_skills, jobs):

    all_job_skills = set()

    for job in jobs:

        title = job["title"]

        if title == "Python Developer":
            all_job_skills.update(
                ["Python", "Flask", "SQL", "Git"]
            )

        elif title == "Backend Developer":
            all_job_skills.update(
                ["Python", "Django", "SQL", "Docker"]
            )

        elif title == "AWS Engineer":
            all_job_skills.update(
                ["AWS", "Docker", "Python"]
            )

    missing = []

    for skill in all_job_skills:

        if skill not in resume_skills:
            missing.append(skill)

    return missing