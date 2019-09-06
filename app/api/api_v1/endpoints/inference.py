from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR

from app.api.utils.db import get_db
from db_models.dbfile import DBFile

router = APIRouter()


async def _process_image(content: bytes,  db: Session, save_file: bool = True):
    if save_file:
        await _save_file(content, db)


async def _save_file(content, db : Session):
    newfile = DBFile(data=content)
    db.add(newfile)
    db.commit()


@router.post("/upload")
async def upload_file(*, db: Session = Depends(get_db), file: UploadFile = File(...)):
    print(file.content_type)
    ctype = file.content_type

    try:
        if ctype == "image/jpeg":
            await _process_image(await file.read(), db)
        # elif ctype is "audio/wav":
        #     save_image(process_audio(await file.read()))
        else:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Only wav and jpeg supported")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to process file")
