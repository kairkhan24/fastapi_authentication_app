from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.rest.router import router as auth_router
from src.config import settings


def get_application() -> FastAPI:
    application = FastAPI(
        title=settings.PROJECT_NAME,
        debug=settings.DEBUG,
    )
    application.include_router(auth_router, prefix='/api')

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return application


app = get_application()
