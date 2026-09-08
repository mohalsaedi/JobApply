"""
models.py
---------
Plain data classes describing the applicant's information.
Keeping these separate from logic makes it trivial to update your
personal data without touching any of the generation/sending code.
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class ContactInfo:
    full_name: str
    email: str
    phone: str
    location: str = ""
    linkedin: str = ""
    github: str = ""
    website: str = ""


@dataclass
class Education:
    degree: str
    institution: str
    graduation_year: str
    details: str = ""  # e.g. GPA, honors, relevant coursework


@dataclass
class Experience:
    title: str
    company: str
    duration: str
    responsibilities: List[str] = field(default_factory=list)


@dataclass
class Project:
    name: str
    description: List[str] = field(default_factory=list)


@dataclass
class Certificate:
    title: str
    issuer: str
    date: str = ""


@dataclass
class Qualifications:
    contact: ContactInfo
    education: List[Education]
    experience: List[Experience]
    core_skills: List[str]
    resume_path: str  # path to the resume file to attach (PDF/DOCX)
    projects: List[Project] = field(default_factory=list)
    certificates: List[Certificate] = field(default_factory=list)
    languages: List[str] = field(default_factory=list)
    honors: List[str] = field(default_factory=list)


@dataclass
class JobTarget:
    """Information about the specific job/employer being applied to."""
    job_title: str
    company_name: str
    employer_email: str
    job_description: str = ""  # optional posting text, improves email relevance
    email_subject: str = "Job Application"