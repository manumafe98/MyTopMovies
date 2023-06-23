from fastapi import Fastapi
from routers import routes
from fastapi.staticfiles import StaticFiles

app = Fastapi()

app.include_router(routes.router)
app.mount("/static", StaticFiles(directory="static"), name="static")
