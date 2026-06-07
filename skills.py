skills_db = [
    "Python",
    "Java",
    "C",
    "C++",
    "JavaScript",
    "HTML",
    "CSS",
    "SQL",
    "Flask",
    "Django",
    "React",
    "Node.js",
    "AWS",
    "Docker",
    "Git",
    "MongoDB",
    "MySQL",
    "Machine Learning",
    "Artificial Intelligence",
    "Data Science"
]

def find_skills(text):

    found_skills = []

    for skill in skills_db:

        if skill.lower() in text.lower():
            found_skills.append(skill)

    return found_skills