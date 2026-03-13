from fastapi import FastAPI
from app.routes import health, license

app = FastAPI()

app.include_router(health.router)
app.include_router(license.router)