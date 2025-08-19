"""
app/main.py

FastAPI app wiring:
- Logging, DB, routers, global exception shielding.
- CORS can be adjusted as needed.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import configure_logging
from app.api.routes import auth as auth_routes
from app.api.routes import admins as admins_routes
from app.api.routes import regional_managers as rm_routes
from app.api.routes import branch_managers as bm_routes
from app.api.routes import patients as patients_routes
from app.api.routes import audit as audit_routes

configure_logging()
app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

# CORS (adjust origins in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: restrict
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth_routes.router)
app.include_router(admins_routes.router)
app.include_router(rm_routes.router)
app.include_router(bm_routes.router)
app.include_router(patients_routes.router)
app.include_router(patients_routes.extra_router)
app.include_router(audit_routes.router)

print("✅ main.py loaded up to here")

# uvicorn app.main:app --reload
