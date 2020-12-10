from fastapi import FastAPI, Depends
from starlette.requests import Request
import uvicorn

from app.api.api_v1.routers.users import users_router
from app.api.api_v1.routers.auth import auth_router
from app.api.api_v1.routers.locals import locals_router
from app.api.api_v1.routers.items import items_router
from app.core import config
from app.db.session import SessionLocal
from app.core.auth import get_current_active_user
from app.core.celery_app import celery_app
from app import tasks

API_VERSION = config.API_V1_STR

app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url=f"{API_VERSION}/docs",
    redoc_url=None,
    openapi_url=f"{API_VERSION}/openapi.json",
)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = SessionLocal()
    response = await call_next(request)
    request.state.db.close()
    return response


@app.get(API_VERSION)
async def root():
    return {"message": "Hello World"}


@app.get(f"{API_VERSION}/task")
async def example_task():
    celery_app.send_task("app.tasks.example_task", args=["Heddllo World"])

    return {"message": "success"}


# Routers
app.include_router(
    users_router,
    prefix=API_VERSION,
    tags=["users"],
    dependencies=[Depends(get_current_active_user)],
)
app.include_router(auth_router, prefix="/api", tags=["auth"])

app.include_router(locals_router, prefix=API_VERSION, tags=["locals"])
app.include_router(items_router, prefix=API_VERSION, tags=["items"])


@app.get("/itens/{item_id}")
async def obtem_itens(item_id: int):
    return {"item": item_id}


if __name__ == "__main__":
    uvicorn.run(
        # "main:app", host="0.0.0.0", reload=True, port=8888, root_path="/api"
        "main:app", host="0.0.0.0", reload=True, port=8000
    )
