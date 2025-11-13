from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import sys

from app.controller.auth_controller import auth_router
from app.controller.lead_controller import router as lead_router
from app.controller.seo_controller import router as seo_router
from app.controller.plan_controller import router as plan_router
from app.controller.content_controller import router as content_router
from app.controller.admin_controller import router as admin_router
from app.db.database import engine, Base
from app.core.config import settings, LOG_LEVEL

# ---------------------------------------------------------------------------
# Safe Loguru Setup
# ---------------------------------------------------------------------------
logger.remove()

valid_levels = ["TRACE", "DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR", "CRITICAL"]
if LOG_LEVEL not in valid_levels:
    print(f"⚠️ Invalid LOG_LEVEL '{LOG_LEVEL}', defaulting to INFO")
    LOG_LEVEL = "INFO"

logger.add(sys.stdout, level=LOG_LEVEL, format="{time} - {level} - {message}")

# ---------------------------------------------------------------------------
# FastAPI App Setup
# ---------------------------------------------------------------------------
app = FastAPI(
    title="Boom_network Backend",
    debug=settings.DEBUG
)

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://boomnetwork.in",
    "https://www.boomnetwork.in"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Startup Events
# ---------------------------------------------------------------------------
@app.on_event("startup")
def startup_event():
    logger.info("🚀 Starting ISP Backend API...")
    Base.metadata.create_all(bind=engine)
    logger.info("✅ Database tables created successfully.")

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(lead_router, prefix="/leads", tags=["Leads"])
app.include_router(seo_router, prefix="/seo", tags=["SEO"])
app.include_router(content_router, prefix="/contents", tags=["Contents"])
app.include_router(plan_router, prefix="/plans", tags=["Plans"])
app.include_router(admin_router, prefix="/admin", tags=["Admin"]) 
