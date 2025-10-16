from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import sys

from app.controller.auth_controller import auth_router
from app.controller.lead_controller import router as lead_router
from app.controller.seo_controller import router as seo_router
from app.controller.plan_controller import router as plan_router
from app.controller.content_controller import router as content_router
from app.db.database import engine, Base
from app.core.config import settings, LOG_LEVEL

# Configure Loguru logging
logger.remove()
logger.add(sys.stdout, level=LOG_LEVEL, format="{time} - {level} - {message}")

app = FastAPI(
    title="Boom_network Backend",
    debug=settings.DEBUG
)

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    logger.info("🚀 Starting ISP Backend API...")
    Base.metadata.create_all(bind=engine)
    logger.info("✅ Database tables created successfully.")

# Register routers
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(lead_router, prefix="/leads", tags=["Leads"])
app.include_router(seo_router, prefix="/seo", tags=["SEO"])
app.include_router(content_router, prefix="/contents", tags=["Contents"])
app.include_router(plan_router, prefix="/plans", tags=["Plans"])
