"""
email_generator.py
-------------------
Builds a prompt from the applicant's qualifications + the target job,
sends it to the configured model via OpenRouter, and returns a
ready-to-send professional email body.

NOTE: This version adds support for "cold outreach" emails — i.e. emails
where there is NO announced/posted job opening and the applicant is
proactively offering their skills to a company. To use this, add a new
field to JobTarget in models.py:

    class JobTarget:
        ...
        is_cold_outreach: bool = False

Set is_cold_outreach=True whenever the user is not responding to an
actual job posting.
"""
 
import re

from openai import OpenAI, APIStatusError
from config import Config
from models import Qualifications, JobTarget


class EmailGenerator:

    # Company names that count as "not really provided" — if job.company_name
    # matches one of these (case-insensitive), we treat it as missing rather
    # than passing it to the model as a real name.
    _PLACEHOLDER_COMPANY_NAMES = {
        "company", "your company", "the company", "شركة", "n/a", "na", "",
    }

    def __init__(self):
        Config.validate()
        # OpenRouter exposes an OpenAI-compatible API, so we use the
        # openai SDK but point it at OpenRouter's base URL.
        self.client = OpenAI(
            api_key=Config.OPENROUTER_API_KEY,
            base_url=Config.OPENROUTER_BASE_URL,
        )

    @staticmethod
    def _resolve_company_name(company_name: str):
        """
        Returns the cleaned company name, or None if it looks like a
        placeholder (e.g. "Company", "your company", blank, etc.) rather
        than a real name.
        """
        if not company_name:
            return None
        cleaned = company_name.strip()
        if cleaned.lower() in EmailGenerator._PLACEHOLDER_COMPANY_NAMES:
            return None
        return cleaned

    @staticmethod
    def _build_prompt(qualifications: Qualifications, job: JobTarget) -> str:
        # Whether this is a speculative / cold-outreach email (no posted
        # opening) as opposed to a reply to an announced job opening.
        # Falls back to False if the field doesn't exist yet on JobTarget,
        # so this stays backwards-compatible until models.py is updated.
        is_cold_outreach = getattr(job, "is_cold_outreach", False)

        edu_lines = "\n".join(
            f"- {e.degree}, {e.institution} ({e.graduation_year})"
            + (f" — {e.details}" if e.details else "")
            for e in qualifications.education
        )

        exp_lines = "\n".join(
            f"- {e.title} at {e.company} ({e.duration}):\n  "
            + "\n  ".join(f"* {r}" for r in e.responsibilities)
            for e in qualifications.experience
        )

        skills_line = ", ".join(qualifications.core_skills)

        if job.job_description:
            if is_cold_outreach:
                job_desc_block = (
                    "\nBackground context about the company/role area "
                    "(there is NO posted job opening — this is just "
                    "context the applicant is using to target the "
                    f"email):\n{job.job_description}\n"
                )
            else:
                job_desc_block = (
                    f"\nJob description provided by employer:\n"
                    f"{job.job_description}\n"
                )
        else:
            job_desc_block = ""

        if job.email_subject:
            subject_instruction = (
                "- Do NOT include a subject line — the subject has already "
                "been decided separately. Start directly with the greeting."
            )
        elif is_cold_outreach:
            subject_instruction = (
                "- A clear subject line on the first line, formatted as: "
                "Subject: <subject text>\n"
                "- Then a blank line, then the email body.\n"
                "- The subject line must NOT imply there is a job opening "
                'or that the applicant is "applying" to a posted role '
                '(avoid words like "Application for..." or "Regarding '
                'your job posting..."). Instead it should signal proactive '
                'interest, e.g. reference the exact job title/role area '
                'and the applicant\'s name, such as "<Job Title> — '
                '<Applicant Name>" or "Exploring opportunities in '
                '<role area> — <Applicant Name>".'
            )
        else:
            subject_instruction = (
                "- A clear subject line on the first line, formatted as: "
                "Subject: <subject text>\n"
                "- Then a blank line, then the email body."
            )

        # --- Company name handling -------------------------------------
        # Only pass a real company name to the model if one was actually
        # given. If it's missing/placeholder, tell the model explicitly
        # NOT to guess one from the email address, domain, signature, or
        # any other clue in the job description — it must stay generic.
        resolved_company = EmailGenerator._resolve_company_name(job.company_name)

        if resolved_company:
            company_line = f"Company: {resolved_company}"
            company_instruction = (
                f'- Mention the company name "{resolved_company}" by name '
                "only ONCE in the whole body (e.g. in the opening line). "
                'After that, refer to it naturally as "your team", "your '
                'organization", "the role", etc. — do not repeat the '
                "company name again later in the email."
            )
        else:
            company_line = "Company: (not provided — do not guess or invent one)"
            company_instruction = (
                "- No company name was provided. Do NOT guess, infer, or "
                "invent one from the email address, domain, signature, or "
                "any other text in the job description below — even if it "
                'seems obvious. Refer to the employer only as "your '
                'organization" or "your team" throughout the email.'
            )
        # -----------------------------------------------------------------

        # --- Framing: applying to a posted job vs. cold outreach --------
        if is_cold_outreach:
            intent_instruction = f"""You are helping a job seeker write a professional, concise
COLD OUTREACH email — proactively offering their skills to a company that
has NOT posted or announced any specific job opening. The applicant is
reaching out speculatively, hoping the company might have (or create) a
fit for someone with their background.

Critical: do NOT phrase this as an "application" to an existing role, and
do NOT say things like "I am writing to apply for the position" or "in
response to your posting" — there is no posting. Instead, the email should
read as a proactive, respectful introduction: the applicant is expressing
interest in contributing their skills to the company and asking whether
there might be relevant opportunities, now or in the near future."""
            opening_instruction = (
                "- Open with one short, warm sentence introducing the "
                "applicant and stating interest in opportunities related "
                f'to "{job.job_title}" work at the company — phrased as '
                "proactive interest, NOT as applying to an announced "
                'opening (avoid "I am writing to apply for..." or similar).'
            )
            closing_instruction = (
                "- Close with one confident, friendly sentence mentioning "
                "the attached resume and inviting the reader to reach out "
                "if there's a potential fit, now or down the line."
            )
        else:
            intent_instruction = """You are helping a job applicant write a professional, concise
job application email to send to a prospective employer, in response to
an announced/posted job opening."""
            opening_instruction = (
                "- Open with one short, warm sentence stating the exact "
                "job title above."
            )
            closing_instruction = (
                "- Close with one confident, friendly sentence mentioning "
                "the attached resume."
            )
        # -----------------------------------------------------------------
    
        return f"""{intent_instruction}

Applicant contact info:
- Name: {qualifications.contact.full_name}
- Email: {qualifications.contact.email}
- Phone: {qualifications.contact.phone}
- Website: {qualifications.contact.website}
- Location: {qualifications.contact.location}

Education:
{edu_lines}

Experience:
{exp_lines}

Core skills: {skills_line}

IMPORTANT — exact job title / role area to use: "{job.job_title}"
Use this exact wording every time you refer to the role. Even if the
text below mentions other possible or alternate titles for this role
area, ignore those — use ONLY the exact title given above, word-for-word,
and never substitute a different title.

{company_line}
{job_desc_block}
Write a complete email that is SIMPLE, CLEAN, and ATTRACTIVE:
{subject_instruction}
- Address it professionally (use "Hiring Manager" if no name is given).
{company_instruction}
{opening_instruction}
- In the middle, pick ONLY the 2-3 most relevant skills/experiences for
  this specific role/area — do not list everything, be selective.
- Keep paragraphs short (2-3 sentences max each). No long blocks of text.
- Keep the total body under 130 words.
- Simple, natural language — no corporate buzzwords or clichés
  (avoid phrases like "dynamic professional", "results-driven", "synergy").
{closing_instruction}
- Do not use placeholder brackets like [Company Name] — use the actual
  details given above.
- Do NOT invent or assume any fact about the applicant that is not
  explicitly present in the Education/Experience/Core skills data above.
  In particular, never describe the applicant's current status (e.g.
  "final-year student", "recent graduate", "currently studying",
  "undergraduate", etc.) unless that exact status is explicitly stated
  in the data. If the data only lists a degree with an institution and
  graduation year, treat that as a completed qualification and refer to
  it neutrally (e.g. "I hold a degree in X from Y") — do not guess
  whether the applicant is still enrolled, about to graduate, or already
  graduated. When in doubt, omit the status claim entirely rather than
  risk stating something false.
- Plain text only — no Markdown formatting of any kind (no **bold**,
  *italics*, backticks, or bullet symbols like - or *). This email will
  be sent as plain text, so any Markdown characters would show up
  literally instead of being styled.
- Sign off using the applicant's name and contact details, each on its
  own line, with no formatting symbols around them.
"""

    def generate(self, qualifications: Qualifications, job: JobTarget) -> dict:
        """
        Returns a dict: {"subject": str, "body": str}
        """
        prompt = self._build_prompt(qualifications, job)

        extra_headers = {}
        if Config.OPENROUTER_SITE_URL:
            extra_headers["HTTP-Referer"] = Config.OPENROUTER_SITE_URL
        if Config.OPENROUTER_APP_NAME:
            extra_headers["X-Title"] = Config.OPENROUTER_APP_NAME

        try:
            response = self.client.chat.completions.create(
                model=Config.OPENROUTER_MODEL,
                max_tokens=Config.OPENROUTER_MAX_TOKENS,
                messages=[{"role": "user", "content": prompt}],
                extra_headers=extra_headers or None,
            )
        except APIStatusError as e:
            if e.status_code == 402:
                raise RuntimeError(
                    "OpenRouter rejected the request: insufficient credits "
                    "for the requested max_tokens. Either add credits at "
                    "https://openrouter.ai/settings/credits, or lower "
                    "OPENROUTER_MAX_TOKENS in your .env file (currently "
                    f"{Config.OPENROUTER_MAX_TOKENS})."
                ) from e
            raise

        text = response.choices[0].message.content.strip()

        if job.email_subject:
            # User specified their own subject line — use it verbatim
            # (still cleaned of stray Markdown) and treat the whole
            # response as the body.
            return {
                "subject": self._strip_markdown(job.email_subject),
                "body": self._strip_markdown(text),
            }

        return self._split_subject_and_body(text)

    @staticmethod
    def _strip_markdown(text: str) -> str:
        """
        Safety net: removes common Markdown symbols in case the model
        adds them despite instructions, since this email is sent as
        plain text and Markdown would show up as literal characters.
        """
        # Bold / italics: **text** or *text* or __text__ or _text_
        text = re.sub(r"(\*\*|__)(.*?)\1", r"\2", text)
        text = re.sub(r"(\*|_)(.*?)\1", r"\2", text)
        # Inline code backticks
        text = text.replace("`", "")
        # Leading bullet markers ("- " or "* " at start of a line)
        text = re.sub(r"(?m)^[\*\-]\s+", "", text)
        return text

    @staticmethod
    def _split_subject_and_body(text: str) -> dict:
        lines = text.splitlines()
        subject = "Job Application"
        body_start = 0

        for i, line in enumerate(lines):
            if line.strip().lower().startswith("subject:"):
                subject = line.split(":", 1)[1].strip()
                body_start = i + 1
                break

        body = "\n".join(lines[body_start:]).strip()
        return {
            "subject": EmailGenerator._strip_markdown(subject),
            "body": EmailGenerator._strip_markdown(body),
        }
