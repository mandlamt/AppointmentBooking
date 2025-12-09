import os
from typing import Optional
from fastapi import Header, HTTPException
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage
from .schemas import AppointmentRead

load_dotenv()

API_KEY = os.getenv("API_KEY")
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT") or 0)
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
EMAIL_FROM = os.getenv("EMAIL_FROM")


def get_api_key_dependency(x_api_key: Optional[str] = Header(None)):
    """Dependency that enforces API key if `API_KEY` is set in env.
    If no API_KEY in env, it allows requests through (useful for local/dev/tests).
    """
    if not API_KEY:
        return None
    if not x_api_key or x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API Key")
    return None


def send_email(subject: str, to: str, body: str):
    if not SMTP_HOST or not EMAIL_FROM:
        return False
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_FROM
    msg["To"] = to
    msg.set_content(body)

    try:
        if SMTP_PORT == 465:
            server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT)
        else:
            server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
            server.starttls()
        if SMTP_USERNAME and SMTP_PASSWORD:
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception:
        return False


def send_notification_if_configured(appointment: AppointmentRead):
    # If SMTP configured, send notification to appointment email
    if not SMTP_HOST or not EMAIL_FROM:
        return
    subject = f"Appointment confirmed: {appointment.start_time}"
    body = f"Hi {appointment.name},\n\nYour appointment is scheduled from {appointment.start_time} to {appointment.end_time}.\n\nThanks."
    send_email(subject, appointment.email, body)
