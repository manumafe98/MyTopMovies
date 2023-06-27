from fastapi import FastAPI
from routers import routes
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.include_router(routes.router)
app.mount("/static", StaticFiles(directory="static"), name="static")
