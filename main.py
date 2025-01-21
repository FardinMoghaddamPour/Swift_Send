import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from utils.email_utils import (
    attach_file,
    is_valid_email
)
from utils.config import get_config


class EmailSender:

    def __init__(self):

        self.__smtp_server = get_config('SMTP_SERVER')
        self.__smtp_port = get_config('SMTP_PORT', default=587, cast=int)
        self.__smtp_user = get_config('SMTP_USER')
        self.__smtp_password = get_config('SMTP_PASSWORD')
        self.__server = None

    def __connect(self):
        try:
            print(f"Attempting to connect to {self.__smtp_server} on port {self.__smtp_port}...")
            self.__server = smtplib.SMTP(self.__smtp_server, self.__smtp_port)
            self.__server.starttls()
            self.__server.login(self.__smtp_user, self.__smtp_password)
            print("Connected to SMTP server")
            return True
        except smtplib.SMTPException as e:
            print(f"Failed to connect to SMTP server: {e}")
            return False

    def send_email(self, to_emails, cc_emails, subject, body, is_html=False, attachments=None):
        if not all(is_valid_email(email) for email in to_emails + (cc_emails or [])):
            print("Invalid email address found.")
            return

        if not self.__connect():
            return

        message = MIMEMultipart()
        message['From'] = self.__smtp_user
        message['To'] = ", ".join(to_emails)
        message['CC'] = ", ".join(cc_emails) if cc_emails else ""
        message['Subject'] = subject

        message.attach(MIMEText(body, 'html' if is_html else 'plain', 'utf-8'))

        if attachments:
            for filepath in attachments:
                attaching_message = attach_file(message, filepath)
                print(f"Attachment message: {attaching_message}")

        try:
            self.__server.send_message(message)
            print("Email sent successfully")
        except smtplib.SMTPException as e:
            print(f"Failed to send email: {e}")
        finally:
            self.__server.quit()


email_sender = EmailSender()
html_body = """

""" # HTML content here
email_sender.send_email(
    to_emails=[
        # to Receivers here
    ],
    cc_emails=[
        # cc Receivers here
    ],
    subject="Subject here",
    body=html_body,
    is_html=True
)
