import logging
from fastapi import Depends, FastAPI
from fastapi.openapi.utils import get_openapi
from starlette_prometheus import metrics, PrometheusMiddleware
from .dependencies import get_query_token, get_token_header
from .config import settings
from .routers import items, users
from .logging import logging as log

log.setup_logging(default_path="./app/log_config.yaml")
logger = logging.getLogger(__name__)

#app = FastAPI(dependencies=[Depends(get_query_token)])
app = FastAPI()

## Prometheus metrics
app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics/", metrics)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="FAST API",
        version="1.0.0",
        description="REST APIs using FastAPI, SQLAlchemy, Alembic & Prometheus.",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

app.include_router(users.router)
app.include_router(items.router)


@app.get("/main")
async def root():
    logger.info('Root endpoint')
    return {"message": "Hello Bigger Applications!"}
