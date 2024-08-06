import datetime

from sendgrid import SendGridAPIClient

from sendgrid.helpers.mail import Email, Mail, To, PlainTextContent

from provider.db.repositories.users_repository import UsersRepository
from provider.services.config_service import AppConfig


class EmailService:
    def __init__(self, config: AppConfig, users_repository: UsersRepository):
        self.config = config
        self.users_repository = users_repository
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

    def notify(self) -> None:
        users = self.users_repository.find_many(
            {
                "updated_at": {
                    "$lt": datetime.datetime.utcnow() - datetime.timedelta(days=10)
                }
            }
        )
        for user in users:
            self.send_email(user["email"])
