"""
applicant_data.py
------------------
EDIT THIS FILE with your own information. Keeping your personal data
in its own file (separate from the program logic) means updating your
resume details never requires touching the generator or sender code.

NOTE: This file contains personal/contact information and resume content.
It is recommended to add this file to .gitignore and commit only a
template (e.g. applicant_data.example.py) so your real details are not
pushed to a public repository.
"""

from models import (
    ContactInfo, Education, Experience, Qualifications, Project, Certificate,
)

contact = ContactInfo(
    full_name="Your Full Name",
    email="your.email@example.com",
    phone="+1 555 000 0000",
    location="City, Country",
    linkedin="https://linkedin.com/in/your-profile", # Add your LinkedIn
    github="https://github.com/your-username",  # add your GitHub URL here
    website="https://your-portfolio-site.example.com/"
)

education = [
    Education(
        degree="B.Sc. in Your Degree",
        institution="Your University",
        graduation_year="20XX",
        details="GPA X.XX/4.0, Honors/Distinction (if applicable)",
    ),
]

experience = [
    Experience(
        title="Your Job Title",
        company="Company Name",
        duration="Month Year – Month Year",
        responsibilities=[
            "Describe a key responsibility or achievement.",
            "Describe another responsibility using strong action verbs.",
            "Mention relevant technologies or frameworks used.",
            "Mention any process, database, or system you worked with.",
            "Mention any security, performance, or quality improvements made.",
        ],
    ),
]

projects = [
    Project(
        name="Project Name – Short Description",
        description=[
            "Describe what the project does and the technologies used.",
            "Describe a key technical feature (e.g. authentication, APIs).",
            "Describe scale or impact (e.g. data processed, users served).",
        ],
    ),
    Project(
        name="Another Project Name",
        description=[
            "Describe the core functionality of the project.",
            "Mention techniques or algorithms applied.",
            "Mention any interface or deployment aspect.",
        ],
    ),
]

certificates = [
    Certificate(title="Certificate Title", issuer="Issuing Organization", date="Month Year"),
    Certificate(title="Certificate Title", issuer="Issuing Organization", date="Month Year"),
    Certificate(title="Certificate Title", issuer="Issuing Organization", date="Month Year"),
    Certificate(title="Certificate Title", issuer="Issuing Organization", date="Month Year"),
]

honors = [
    "Honor or award description, Institution (Year)",
    "Another honor or recognition",
    "Any additional achievement worth listing",
]

languages = ["Language (Proficiency)", "Language (Proficiency)"]

core_skills = [
    "Backend Development: e.g. Python (FastAPI), PHP (Laravel), JavaScript (Node.js, Express.js)",
    "Front-End Development: e.g. HTML5, CSS3, Tailwind, React.js, React Native",
    "Databases: e.g. PostgreSQL, MySQL, MongoDB",
    "Deployment: e.g. Heroku, Netlify",
    "Concepts & Principles: e.g. REST API Design, CI/CD, OOP, MVC, Data Structures & Algorithms",
]

qualifications = Qualifications(
    contact=contact,
    education=education,
    experience=experience,
    core_skills=core_skills,
    resume_path="Your Name CV.pdf",
    projects=projects,
    certificates=certificates,
    languages=languages,
    honors=honors,
)
