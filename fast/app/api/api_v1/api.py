from fastapi import APIRouter

from app.api.api_v1.endpoints import kit

api_router = APIRouter()

api_router.include_router(kit.router, prefix="/kit", tags=["kits"])


