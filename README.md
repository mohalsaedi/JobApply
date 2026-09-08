# Job Application Agent

A small, modular Python project that:
1. Takes your qualifications (education, experience, core skills) and contact info.
2. Sends them to **Gemma 3 27B** to draft a professional job application email tailored to a specific role.
3. Sends that email to the employer with your **resume file attached**.

## Project structure

```
job_application_agent/
├── models.py           # Data classes: ContactInfo, Education, Experience, Qualifications, JobTarget
├── config.py            # Loads API keys / SMTP settings from environment variables
├── applicant_data.py    # <-- YOUR personal info goes here (edit this)
├── email_generator.py   # Calls Gemma 3 27B to draft the email
├── email_sender.py       # Sends the email via SMTP with the resume attached
├── main.py               # Ties everything together — run this
├── requirements.txt
├── README.md
```

Each concern lives in its own file, so:
- Updating your resume/skills → edit `applicant_data.py` only.
- Changing the AI prompt or model → edit `email_generator.py` only.
- Switching email providers → edit `email_sender.py` / `.env` only.

## Setup

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure secrets**
   ```bash
   cp .env.example .env
   ```
   Then edit `.env` and fill in:
   - `OPENROUTER_API_KEY` — from https://openrouter.ai/keys
   - `SMTP_USERNAME` / `SMTP_PASSWORD` — your email account. For Gmail, generate an "App Password" at https://myaccount.google.com/apppasswords (do not use your normal password).

3. **Add your resume file**
   Place your resume (e.g. `resume.pdf`) in this folder, and make sure `applicant_data.py`'s `resume_path` points to it.

4. **Fill in your info**
   Edit `applicant_data.py` with your real name, contact details, education, experience, and skills.

5. **Set the target job**
   Open `main.py` and edit the `JobTarget(...)` block with the actual job title, company name, employer email, and (optionally) the job description text — this helps Gemma 3 27B tailor the email.

6. SMTP Config
 - Open Gmail
 - Manage Your Google Account
 - Search Icon, Type in Search bar App Passwords 
 - Create App Name (Needed in SMTP_APPNMAE) 
 - Copy The Generated App Password and Paste it at .env file (SMTP Password)

## Run it

```bash
python main.py
```

The script will:
1. Print the AI-generated subject line and email body for your review.
2. Ask for confirmation (`y`/`n`) before sending.
3. Send the email with your resume attached once confirmed.

## Notes

- The model used is `Gemma 3 27B` (Gemma 3 27B) — fast and cost-efficient for this kind of text generation.
- Nothing is sent to the employer without your explicit confirmation at the prompt.
- If you plan to apply to many jobs, you can adapt `main.py` to loop over a list of `JobTarget` entries instead of a single one.
