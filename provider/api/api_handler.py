from typing import AsyncGenerator
from contextlib import asynccontextmanager
from provider.api.admin_router import AdminRouter
from provider.api.users_router import UsersRouter
from provider.auth.auth_router import AuthRouter
from provider.notifications.email_service import EmailService
from provider.notifications.scheduler_service import SchedulerService
from provider.services.logger_service import LoggerService
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


class APIHandler:
    def __init__(
        self,
        users_router: UsersRouter,
        admin_router: AdminRouter,
        auth_router: AuthRouter,
        scheduler_service: SchedulerService,
        logger_service: LoggerService,
        email_service: EmailService,
    ):
        self.users_router = users_router
        self.admin_router = admin_router
        self.auth_router = auth_router
        self.scheduler_service = scheduler_service
        self.logger_service = logger_service
        self.email_service = email_service
        self.app = FastAPI(
            title="Dynamic-IP-Provider-Service",
            lifespan=asynccontextmanager(self.lifespan),
        )
        self.include_routers()
        self.logger_service.info()

    def include_routers(self) -> None:
        self.app.include_router(self.users_router.get_router())
        self.app.include_router(self.admin_router.get_router())
        self.app.include_router(self.auth_router.get_routers())
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["http://localhost:3000"],
            allow_credentials=True,
            allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
            allow_headers=[
                "Content-Type",
                "Set-Cookie",
                "Access-Control-Allow-Headers",
                "Access-Control-Allow-Origin",
                "Authorization",
            ],
        )

    def lifespan(self, app: FastAPI) -> AsyncGenerator:
        self.scheduler_service.add_job(self.email_service.notify)
        self.scheduler_service.start()
        yield
        self.scheduler_service.stop()
