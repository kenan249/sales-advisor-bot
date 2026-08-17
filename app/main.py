from fastapi import FastAPI
from app.shared.config import settings
from app.adapters.inbound.http.health import router as health_router
from app.adapters.inbound.http.whatsapp import router as whatsapp_router

app = FastAPI(title=settings.app_name, version="0.1.0")
app.include_router(health_router)
app.include_router(whatsapp_router, prefix=settings.api_prefix)
