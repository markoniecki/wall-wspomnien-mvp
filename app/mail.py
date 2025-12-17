import os
import mimetypes
import smtplib
from email.message import EmailMessage


# def send_pdf_email(to_email: str, subject: str, body: str, pdf_path: str):
#     """
#     SMTP sender. Ustaw w .env:
#       SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, SMTP_FROM
#     """
#     host = os.getenv("SMTP_HOST")
#     port = int(os.getenv("SMTP_PORT", "587"))
#     user = os.getenv("SMTP_USER")
#     password = os.getenv("SMTP_PASS")
#     from_email = os.getenv("SMTP_FROM", user)
#
#     if not all([host, port, user, password, from_email]):
#         raise RuntimeError("Brakuje konfiguracji SMTP w zmiennych środowiskowych.")
#
#     msg = EmailMessage()
#     msg["From"] = from_email
#     msg["To"] = to_email
#     msg["Subject"] = subject
#     msg.set_content(body)
#
#     ctype, encoding = mimetypes.guess_type(pdf_path)
#     if ctype is None:
#         ctype = "application/pdf"
#     maintype, subtype = ctype.split("/", 1)
#
#     with open(pdf_path, "rb") as f:
#         msg.add_attachment(
#             f.read(),
#             maintype=maintype,
#             subtype=subtype,
#             filename=os.path.basename(pdf_path),
#         )
#
#     with smtplib.SMTP(host, port) as smtp:
#         smtp.starttls()
#         smtp.login(user, password)
#         smtp.send_message(msg)
