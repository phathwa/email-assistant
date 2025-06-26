# app/notifications.py

from django.conf import settings
from django.core.mail import send_mail

def send_reply_notification(sender: str, intent: str, tone: str, summary: str, full_reply: str):
    """Sends an email notification when a new reply is generated."""
    subject = "✅ New Email Reply Generated"
    message = f"""
    A user has successfully generated an email reply.

    --- User Input ---
    Sender: {sender}
    Intent: {intent}
    Tone: {tone}
    Summary: {summary}

    --- AI Generated Response ---
    {full_reply}
    """
    try:
        send_mail(
            subject,
            message,
            'noreply@emailassistant.com',  # From address
            [settings.ADMIN_EMAIL],       # To address (from settings.py)
            fail_silently=False,
        )
        print("Reply notification email sent successfully.")
    except Exception as e:
        # Log email sending errors if necessary, but don't crash the app
        print(f"Error sending reply notification email: {e}")


def send_compose_notification(recipient: str, purpose: str, tone: str, full_reply: str):
    """Sends an email notification when a new email is composed."""
    subject = "✅ New Email Composed"
    message = f"""
    A user has successfully composed a new email.

    --- User Input ---
    Recipient: {recipient}
    Purpose: {purpose}
    Tone: {tone}

    --- AI Generated Response ---
    {full_reply}
    """
    try:
        send_mail(
            subject,
            message,
            'noreply@emailassistant.com',  # From address
            [settings.ADMIN_EMAIL],       # To address (from settings.py)
            fail_silently=False,
        )
        print("Compose notification email sent successfully.")
    except Exception as e:
        # Log email sending errors if necessary, but don't crash the app
        print(f"Error sending compose notification email: {e}")
