import os
import requests
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail import EmailMessage

class BrevoEmailBackend(BaseEmailBackend):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_key = os.getenv('EMAILBACKEND_API_PASSWORD')  # Fetch Brevo API key from environment variable
        self.default_from_email = os.getenv('EMAILBACKEND_DEFAULT_FROM')  # Default from email address
    
    def send_messages(self, email_messages):
        if not email_messages:
            return 0

        sent_count = 0

        for message in email_messages:
            response = self.send_email(
                subject=message.subject,
                body=message.body,
                from_email=message.from_email or self.default_from_email,
                to_email=message.to,
                html_content=message.extra_headers.get('X-Brevo-Content-Type', 'text/html')
            )
            if response.status_code == 200:
                sent_count += 1
            else:
                print(f"Failed to send email: {response.status_code} {response.text}")
        
        return sent_count
    
    def send_email(self, subject, body, from_email, to_email, html_content):
        url = "https://api.brevo.com/v3/smtp/email"  # Brevo API endpoint for sending emails
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'api-key': self.api_key
        }
        data = {
            "sender": {"email": from_email},
            "to": [{"email": recipient} for recipient in to_email],
            "subject": subject,
            "htmlContent": body,
            "textContent": body
        }
        response = requests.post(url, json=data, headers=headers)
        return response
