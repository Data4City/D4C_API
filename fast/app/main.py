from fastapi import FastAPI
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from app.api.api_v1.api import api_router
from app.core.config import ALLOWED_HOSTS, API_V1_STR, PROJECT_NAME
from app.core.errors import http_422_error_handler, http_error_handler
from app.db.session import Session, engine
app = FastAPI(title=PROJECT_NAME)

if not ALLOWED_HOSTS:
    ALLOWED_HOSTS = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(HTTPException, http_error_handler)
app.add_exception_handler(HTTP_422_UNPROCESSABLE_ENTITY, http_422_error_handler)

app.include_router(api_router, prefix=API_V1_STR)

from sqlalchemy_utils import create_database, database_exists

if not database_exists(engine.url):
    print("NIGGA")
    from app.db.base import Base

    create_database(engine.url)
    Base.metadata.create_all(bind=engine)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = Session()
    response = await call_next(request)
    request.state.db.close()
    return response


if __name__ == "__main__":
    import uvicorn
    from app.db.base import Base

    Base.metadata.create_all(bind=engine)
    uvicorn.run(app, host="0.0.0.0", port=8000)
