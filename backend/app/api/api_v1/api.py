from fastapi import APIRouter

from app.api.api_v1.endpoints import kit, geo, dataset, login, users
api_router = APIRouter()

#api_router.include_router(kit.router, prefix="/kit", tags=["kits"])
#api_router.include_router(geo.router, prefix="/geo", tags=["geo"])
api_router.include_router(dataset.router, prefix="/dataset", tags=["dataset"])

api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])