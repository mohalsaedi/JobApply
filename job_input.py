"""
job_input.py
------------
Collects the job-specific details (job title, company name, employer
email, job description) interactively from the console, so you don't
need to edit any code to apply to a new job — just run the program and
paste the details in.

Kept in its own file so the input/UX logic never mixes with the
generation or sending logic.
"""

from models import JobTarget


def _read_multiline(prompt: str) -> str:
    """
    Reads a multi-line block of pasted text.
    Type the details (or paste a full job description), then finish
    by typing END on its own line and pressing Enter.
    """
    print(prompt)
    print("(Paste the text, then type END on its own line to finish. "
          "Leave blank + END to skip.)")
    lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)
    return "\n".join(lines).strip()


def collect_job_target() -> JobTarget:
    """Prompts the user for job details and returns a JobTarget."""
    print("\n=== Enter job details ===")

    job_title = input("Job title: ").strip()
    company_name = input("Company name: ").strip()
    employer_email = input("Employer email address: ").strip()
    job_description = _read_multiline("\nJob description")

    email_subject = input(
        "\nEmail subject line: "
    ).strip()

    return JobTarget(
        job_title=job_title,
        company_name=company_name,
        employer_email=employer_email,
        job_description=job_description,
        email_subject=email_subject,
    )