from fastapi import APIRouter

from app.api.api_v1.endpoints import kit, geo, inference, login, users
api_router = APIRouter()

api_router.include_router(kit.router, prefix="/kit", tags=["kits"])
api_router.include_router(geo.router, prefix="/geo", tags=["geo"])
api_router.include_router(inference.router, prefix="/inference", tags=["inference"])

api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])