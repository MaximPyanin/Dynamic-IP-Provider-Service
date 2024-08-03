from sendgrid import SendGridAPIClient

from sendgrid.helpers.mail import Email, Mail, To, PlainTextContent
from provider.services.config_service import AppConfig


class EmailService:
    def __init__(self, config: AppConfig):
        self.config = config
        self.__client = SendGridAPIClient(self.config.SENDGRID_API_KEY)
        self.sender = Email(self.config.SENDER_EMAIL)

    def send_email(self, to_email: str):
        return self.__client.send(
            Mail(
                self.sender,
                To(to_email),
                subject="Lack of activity",
                plain_text_content=PlainTextContent(
                    "Your IP address has not been updated for 30 days, and your account may soon be deleted. Please update your IP address to avoid account deletion."
                ),
            )
        )
