"""
email_sender.py
----------------
Sends the AI-generated email to the employer via SMTP, with the
applicant's resume file attached.

Sends as HTML (with a plain-text fallback for older mail clients) so
the phone number, email, LinkedIn, and website links are clickable
(tel: / mailto: / https: links) in the recipient's inbox.
"""

import os
import re
import html
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from config import Config
from models import ContactInfo


class EmailSender:
    def __init__(self):
        Config.validate()

    def send(self, to_email: str, subject: str, body: str, attachment_path: str,
              contact: ContactInfo = None, from_display_name: str = "") -> None:
        if not os.path.isfile(attachment_path):
            raise FileNotFoundError(f"Resume file not found: {attachment_path}")

        msg = MIMEMultipart("mixed")
        msg["From"] = (
            f"{from_display_name} <{Config.SMTP_USERNAME}>"
            if from_display_name
            else Config.SMTP_USERNAME
        )
        msg["To"] = to_email
        msg["Subject"] = subject

        # Plain text + HTML alternative, so clients that can't render
        # HTML still show a clean plain-text version.
        alt_part = MIMEMultipart("alternative")
        alt_part.attach(MIMEText(body, "plain"))
        alt_part.attach(MIMEText(self._to_html(body, contact), "html"))
        msg.attach(alt_part)

        with open(attachment_path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        encoders.encode_base64(part)
        filename = os.path.basename(attachment_path)
        part.add_header("Content-Disposition", f'attachment; filename="{filename}"')
        msg.attach(part)

        with smtplib.SMTP(Config.SMTP_HOST, Config.SMTP_PORT) as server:
            server.starttls()
            server.login(Config.SMTP_USERNAME, Config.SMTP_PASSWORD)
            server.send_message(msg)

    @staticmethod
    def _to_html(body: str, contact: ContactInfo = None) -> str:
        """
        Converts the plain-text email body into simple HTML, turning
        the phone number into a tel: link, the email into a mailto:
        link, and the LinkedIn/website URLs into clickable links.
        """
        escaped = html.escape(body)

        if contact:
            if contact.phone:
                tel_href = re.sub(r"[^\d+]", "", contact.phone)
                escaped = escaped.replace(
                    html.escape(contact.phone),
                    f'<a href="tel:{tel_href}">{html.escape(contact.phone)}</a>',
                )
            if contact.email:
                escaped = escaped.replace(
                    html.escape(contact.email),
                    f'<a href="mailto:{contact.email}">{html.escape(contact.email)}</a>',
                )
            if contact.linkedin:
                escaped = escaped.replace(
                    html.escape(contact.linkedin),
                    f'<a href="{contact.linkedin}">{html.escape(contact.linkedin)}</a>',
                )
            if contact.website:
                    escaped = escaped.replace(
                    html.escape(contact.website),
                     f'<a href="{contact.website}">{html.escape(contact.website)}</a>',
                            )
            # if getattr(contact, "website", None):
            #     escaped = escaped.replace(
            #         html.escape(contact.website),
            #         f'<a href="{contact.website}">{html.escape(contact.website)}</a>',
            #     )

        html_body = escaped.replace("\n", "<br>\n")

        return f"""\
<html>
  <body style="font-family: Arial, Helvetica, sans-serif; font-size: 14px; color: #222; line-height: 1.6;">
    {html_body}
  </body>
</html>
"""