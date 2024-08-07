import os

from provider.db.database import Database
from provider.db.repositories.users_repository import UsersRepository
from provider.db.repositories.addresses_repository import AddressesRepository
from provider.services.logger_service import LoggerService
from provider.services.config_service import AppConfig
from provider.notifications.email_service import EmailService
from provider.notifications.scheduler_service import SchedulerService
from provider.core.admin_service import AdminService
from provider.core.users_service import UsersService
from provider.auth.auth_router import AuthRouter
from provider.auth.auth_service import AuthService
from provider.api.users_router import UsersRouter
from provider.api.admin_router import AdminRouter
from provider.api.api_handler import APIHandler
from dependency_injector.containers import DeclarativeContainer
from dependency_injector import providers
from provider.utils.jwt_service import JWTService


class Container(DeclarativeContainer):
    config = providers.Factory(AppConfig, os.environ)
    logger_service = providers.Singleton(LoggerService)
    db = providers.Singleton(Database, config)
    users_repository = providers.Factory(UsersRepository, db)
    addresses_repository = providers.Factory(AddressesRepository, db)
    email_service = providers.Factory(EmailService, config, users_repository)
    scheduler_service = providers.Factory(SchedulerService)
    jwt_service = providers.Factory(JWTService, config)
    auth_service = providers.Factory(AuthService, users_repository, jwt_service)
    admin_service = providers.Factory(
        AdminService, users_repository, addresses_repository
    )
    users_service = providers.Factory(
        UsersService, users_repository, addresses_repository
    )
    auth_router = providers.Factory(AuthRouter, users_service, admin_service)
    admin_router = providers.Factory(AdminRouter, admin_service, auth_service)
    users_router = providers.Factory(UsersRouter, users_service, auth_service)
    api_handler = providers.Singleton(
        APIHandler,
        users_router,
        admin_router,
        auth_router,
        scheduler_service,
        logger_service,
        email_service,
    )
