from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from config.config import AppConfig
from config.containers import init_container
from config.log_config import configure_logging
from api.v1.chats.handlers import router as chats_router


def create_app() -> FastAPI:
    container = init_container()
    config = container.resolve(AppConfig)
    configure_logging(config.log_level, config.debug)

    app = FastAPI(
        title=config.app_title,
        docs_url=config.docs_url,
        redoc_url=config.redoc_url,
        version=config.version,
        debug=config.debug,
        secret_key=config.secret_key,
        config=config,
        container=container,
    )
    app.include_router(chats_router)

    # noinspection PyTypeChecker
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health")
    async def health() -> dict:
        return {"status": "ok"}

    return app
