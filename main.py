from fastapi import Fastapi
from routers import routes

app = Fastapi()

app.include_router(routes.router)