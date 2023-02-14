from fastapi import FastAPI

from app.core.store import store
from app.common.router import router as common_router
from app.iris.router import router as iris_router

app = FastAPI()

app.include_router(
    common_router,
    prefix="",
    tags=["Core"])
app.include_router(
    iris_router,
    prefix="/iris",
    tags=["Iris model"])

@app.on_event("startup")
async def app_startup():
    # spin up http sessions to be used for application
    store.start()

@app.on_event("shutdown")
async def app_shutdown():
    # clear up resources on shutdown
    await store.shutdown()
