"""
main.py
-------
Orchestrates the full flow:
  1. Load your qualifications (from applicant_data.py)
  2. Ask you to paste in the job title, company name, employer email,
     and job description
  3. Ask Gemma 3 27B to draft a professional application email
  4. Send that email to the employer with your resume attached

Run:
    python main.py
"""

from applicant_data import qualifications
from job_input import collect_job_target
from email_generator import EmailGenerator
from email_sender import EmailSender


def main():
    # --- 1. Get the job/employer details (pasted in at runtime) ---
    job = collect_job_target()

    # --- 2. Generate the email with Gemma 3 27B ---
    print("Generating application email with Gemma 3 27B...")
    generator = EmailGenerator()
    result = generator.generate(qualifications, job)

    print("\n--- Generated Subject ---")
    print(result["subject"])
    print("\n--- Generated Body ---")
    print(result["body"])

    # --- 3. Confirm before sending ---
    confirm = input("\nSend this email to the employer now? (y/n): ").strip().lower()
    if confirm != "y":
        print("Aborted. No email was sent.")
        return

    # --- 4. Send it, with resume attached ---
    sender = EmailSender()
    sender.send(
        to_email=job.employer_email,
        subject=result["subject"],
        body=result["body"],
        attachment_path=qualifications.resume_path,
        contact=qualifications.contact,
        from_display_name=qualifications.contact.full_name,
    )
    print(f"Email sent successfully to {job.employer_email}!")


if __name__ == "__main__":
    main()
