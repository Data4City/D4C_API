from fastapi import APIRouter

from app.api.api_v1.endpoints import kit, geo
api_router = APIRouter()

api_router.include_router(kit.router, prefix="/kit", tags=["kits"])
api_router.include_router(geo.router, prefix="/geo", tags=["geo"])


