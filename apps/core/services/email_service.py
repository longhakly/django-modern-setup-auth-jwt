import smtplib
from email.mime.text import MIMEText

import retrying
from django.conf import settings

from apps.auth_user.services import UserService


class EmailService:
    def __init__(self):
        self.email_host_user = getattr(settings, "EMAIL_HOST_USER", None)
        self.email_host_password = getattr(settings, "EMAIL_HOST_PASSWORD", None)
        self.email_port = getattr(settings, "EMAIL_PORT", 587)
        self.email_host = getattr(settings, "EMAIL_HOST", "smtp.gmail.com")

    def send_email(self, body, subject, recipients, body_type="plain"):
        session = smtplib.SMTP(self.email_host, self.email_port)
        session.starttls()
        session.login(self.email_host_user, self.email_host_password)
        sender = self.email_host_user
        msg = MIMEText(body, body_type)

        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = ", ".join(recipients)

        session.sendmail(sender, recipients, msg.as_string())

    @retrying.retry(wait_fixed=5000, stop_max_attempt_number=3)
    def send_verify_email(self, user):
        __user_service = UserService()
        uid = __user_service.generate_uidb64(user)
        token = __user_service.generate_token(user)
        verify_url = f"{settings.WEB_BASE_URL}/auth/verify/{uid}/{token}"

        body = f"""
        Dear {user.email},<br><br>
        Please verify your account by clicking the link below:<br>
        <a href="{verify_url}">{verify_url}</a><br><br>
        If you did not request this, please ignore this email.<br><br>
        Regards,<br>
        Your Team
        """
        subject = "Verify Your Account"
        recipients = [user.email]

        try:
            self.send_email(body, subject, recipients, "html")
            print(f"Email sent to {user.email}")
        except Exception as e:
            print(f"Failed to send email to {user.email}: {e}")
            raise e

    @retrying.retry(wait_fixed=5000, stop_max_attempt_number=3)
    def send_reset_email(self, user):
        __user_service = UserService()
        uid = __user_service.generate_uidb64(user)
        token = __user_service.generate_token(user)
        reset_url = f"{settings.WEB_BASE_URL}/auth/reset-password/{uid}/{token}"

        body = f"""
        Dear {user.email},<br><br>
        We received a request to reset your password.<br><br>
        You can reset your password by clicking the link below:<br><br>
        <a href="{reset_url}">{reset_url}</a><br><br>
        If you did not request a password reset, please ignore this email or contact support.<br><br>
        This link will expire in a limited time for your security.<br><br>
        Best regards,<br>
        Your Support Team
        """

        subject = "Reset Your Password"
        recipients = [user.email]

        try:
            self.send_email(body, subject, recipients, "html")
            print(f"Email sent to {user.email}")
        except Exception as e:
            print(f"Failed to send email to {user.email}: {e}")
            raise e

