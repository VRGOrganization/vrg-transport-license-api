from fastapi import FastAPI
from app.routes import health, license_route

app = FastAPI(root_path="/api/v1")

app.include_router(health.router)
app.include_router(license_route.router)